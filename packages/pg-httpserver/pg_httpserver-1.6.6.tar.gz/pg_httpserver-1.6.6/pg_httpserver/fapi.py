import json
import time

from fastapi import FastAPI, applications, status
from contextlib import asynccontextmanager
import asyncio
from pg_objectserialization import loads, dumps
import uvicorn
from starlette.datastructures import MutableHeaders
from pg_common import log_info, log_error, start_coroutines, base64_decode, base64_encode, \
    GLOBAL_DEBUG, fernet_decrypt, fernet_encrypt, Context, SessionUser, is_valid_ip
from pg_environment import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from pg_redis import RedisManager
from .define import ENV_NEEDS_BODY_MIDDLEWARE, ENV_NEEDS_CHECK_SESSION, ENV_CHECK_SESSION_IGNORE_URI, \
    ENV_NEEDS_GAME_CONFIG, ENV_NEEDS_GAME_PROPERTY, ENV_CHECK_SESSION_HEADER_KEY, GameException, GameErrorCode, \
    SESSION_EXPIRED_TIME, GameContext, ENV_NEEDS_CHECK_REQUEST_ID, ENV_CHECK_REQUEST_ID_IGNORE_URI, \
    CONTEXT_KEY, GAME_CONTEXT_KEY, REQUEST_COUNTER_KEY, ENV_NEEDS_IP2REGION_API_KEY
from .manager import GameConfigManager, GamePropertyManager, AutoIdManager, XdbManager
from .models import ReqData, RedisKey
CODE_VERSION = 0

__all__ = [
           "run", "app", "CODE_VERSION", "get_session_user", "get_context", "get_game_context", "get_client_ip"
           ]
__auth__ = "baozilaji@gmail.com"


def get_client_ip_from_xff(_xff):
    if not _xff:
        return None
    _ips = _xff.split(",")
    for _ip in _ips:
        if is_valid_ip(_ip.strip()):
            return _ip
    return None

def get_client_ip(req: Request):
    _headers = req.headers
    if not _headers:
        return None
    _xff = _headers['X-Forwarded-For'] if 'X-Forwarded-For' in _headers else None
    _ip = get_client_ip_from_xff(_xff)
    if _ip:
        return _ip

    _ip = _headers['Proxy-Client-IP'] if 'Proxy-Client-IP' in _headers else None
    if is_valid_ip(_ip):
        return _ip

    _ip = _headers['WL-Proxy-Client-IP'] if 'WL-Proxy-Client-IP' in _headers else None
    if is_valid_ip(_ip):
        return _ip

    return req.client.host


def swagger_ui_html_patch(*args, **kwargs):
    return get_swagger_ui_html(*args, **kwargs,
                               swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
                               swagger_css_url="/static/swagger-ui/swagger-ui.css")

applications.get_swagger_ui_html = swagger_ui_html_patch

@asynccontextmanager
async def life_span(_app: FastAPI):
    from pg_httpserver import httpserver_init
    httpserver_init()
    start_coroutines(reload_config())
    if config.get_conf(ENV_NEEDS_IP2REGION_API_KEY, default=False):
        XdbManager.init()
    log_info("http server startup")
    yield
    global _RUNNING
    _RUNNING = False
    if config.get_conf(ENV_NEEDS_IP2REGION_API_KEY, default=False):
        XdbManager.close()
    log_info("http server shutdown")


app = FastAPI(docs_url=None if config.is_prod() else "/docs", lifespan=life_span)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_RUNNING = True


def reload_code_version():
    global CODE_VERSION
    if not CODE_VERSION:
        with open("VERSION") as _f:
            CODE_VERSION = int(_f.read())
            log_info(f"code version is: {CODE_VERSION}")


async def reload_config():
    while _RUNNING:
        try:
            reload_code_version()
            if config.get_conf(ENV_NEEDS_GAME_CONFIG, False):
                await GameConfigManager.reload()
            if config.get_conf(ENV_NEEDS_GAME_PROPERTY, False):
                await GamePropertyManager.reload()
        except Exception as e:
            log_error(e)
        await asyncio.sleep(60)
    log_info(f"server stopped")


@app.get("/health", description="健康检查接口", response_description="返回代码版本号")
async def health():
    return {
        "status": 0,
        "info": "OK",
        "code_version": CODE_VERSION
    }

class _CustomBodyResponder:
    def __init__(self, _app):
        self.app = _app
        self.initial_message = {}

    async def __call__(self, scope, receive, send) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self):
        message = await self.receive()
        _body: bytes = message.get("body", b"")
        if _body:
            _body = base64_decode(_body)
            _body = loads(_body, p=GLOBAL_DEBUG)
            _container_key = CONTEXT_KEY
            self.scope[_container_key].log['req'] = _body
            _body = json.dumps(_body)
            _body = _body.encode()
            message["body"] = _body
        return message
    async def send_with_msg(self, message):
        if message["type"] == "http.response.start":
            self.initial_message = message
            return

        elif message["type"] == "http.response.body":
            headers = MutableHeaders(raw=self.initial_message['headers'])
            body = message['body']
            body = body.decode()
            body = json.loads(body)
            if 'head' in body:
                _game_ctx = self.scope[GAME_CONTEXT_KEY]
                body['head']['auto_ids'] = (await AutoIdManager.get_auto_ids(_game_ctx)).dict()
                body['head']['rewards'] = _game_ctx.rewards_to_json()
            _container_key = CONTEXT_KEY
            self.scope[_container_key].log['resp'] = body
            body = base64_encode(dumps(body, p=GLOBAL_DEBUG))
            message["body"] = body
            headers["Content-Type"] = "text/plain"
            headers["Content-Length"] = str(len(body))
            self.initial_message['headers'] = headers.items()
            await self.send(self.initial_message)
            await self.send(message)
            if REQUEST_COUNTER_KEY in self.scope:
                _game_ctx:GameContext = self.scope[GAME_CONTEXT_KEY]
                _game_ctx.update_data(self.scope[REQUEST_COUNTER_KEY], {"last_resp": body.decode()})

class CustomBodyMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST":
            await self.app(scope, receive, send)
            return

        responder = _CustomBodyResponder(self.app)
        await responder(scope, receive, send)


if config.get_conf(ENV_NEEDS_BODY_MIDDLEWARE, default=True):
    log_info(f"add custom middleware to encrypt response and decrypt request")
    app.add_middleware(CustomBodyMiddleware)


if config.get_conf(ENV_NEEDS_CHECK_SESSION, default=True):
    log_info(f"add custom middleware to check session")

    if config.get_conf(ENV_NEEDS_CHECK_REQUEST_ID, default=True):
        log_info(f"add custom middleware to check request id")

        @app.middleware("http")
        async def http_inspector_check_request_id(request, call_next):
            if request.method != "POST":
                return await call_next(request)

            _uri = request.scope['path']
            _ignores = config.get_conf(ENV_CHECK_REQUEST_ID_IGNORE_URI, [])
            _ignore = any([_uri.rfind(_i) >= 0 for _i in _ignores])
            if _ignore:
                return await call_next(request)

            _user = get_session_user(request)
            _game_ctx = get_game_context(request)
            _req = await _game_ctx.load_data(ReqData, {"uid": _user.uid})
            if _user.req_cnt + 1 < _req.req_cnt: # 和后端差了两个协议以上，异常
                _game_ctx.ctx.log.update({"cheat": f"client->{_req.req_cnt} less than server->{_user.req_cnt}"})
                return PlainTextResponse("FORBIDDEN4", status_code=status.HTTP_403_FORBIDDEN)
            elif _user.req_cnt > _req.req_cnt: # 请求超过了后端计数器，异常
                _game_ctx.ctx.log.update({"cheat": f"client->{_req.req_cnt} big than server->{_user.req_cnt}"})
                return PlainTextResponse("FORBIDDEN5", status_code=status.HTTP_403_FORBIDDEN)
            elif _user.req_cnt + 1 == _req.req_cnt: # 和后端相差一个协议，将后端记录的上次请求结果直接返回
                _game_ctx.ctx.log.update({"cheat": "repeatRequest"})
                return PlainTextResponse(_req.last_resp,
                                         headers={
                                             config.get_conf(ENV_CHECK_SESSION_HEADER_KEY, default="Authentication"): _req.last_header
                                         })
            # 请求计数器加1
            _game_ctx.update_data(_req, {"req_cnt": _req.req_cnt + 1})
            _user.req_cnt += 1
            request.scope[REQUEST_COUNTER_KEY] = _req
            resp = await call_next(request)
            return resp

    @app.middleware("http")
    async def http_inspector(request, call_next):
        if request.method != "POST":
            return await call_next(request)

        _uri = request.scope['path']
        _ignores = config.get_conf(ENV_CHECK_SESSION_IGNORE_URI, [])
        _ignore = any([_uri.rfind(_i)>=0 for _i in _ignores])

        if _ignore:
            return await call_next(request)

        _ctx = get_context(request)
        _header_key = config.get_conf(ENV_CHECK_SESSION_HEADER_KEY, default="Authentication")
        if _header_key not in request.headers:
            _ctx.log.update({"cheat": "noAuthentication"})
            return PlainTextResponse("FORBIDDEN1", status_code=status.HTTP_403_FORBIDDEN)

        _header = request.headers[_header_key]
        _payload = _header.split(" ")
        if len(_payload) != 2:
            _ctx.log.update({"cheat": "authenticationFormatError"})
            return PlainTextResponse("FORBIDDEN2", status_code=status.HTTP_403_FORBIDDEN)
        _game, _token = _payload
        _cfg = GamePropertyManager.get_config()
        if _game not in _cfg:
            _ctx.log.update({"cheat": "noGameCfg"})
            return PlainTextResponse("FORBIDDEN3", status_code=status.HTTP_403_FORBIDDEN)

        _fernet_key = _cfg[_game]['fernet_key'].encode()
        # _user = json.loads(rsa_decrypt2(_token, _cfg[_game]['pri_key']))
        _user = json.loads(fernet_decrypt(_token.encode(), _fernet_key))
        _session_user = SessionUser(**_user)
        _ctx.log.update({'uid': _session_user.uid, 'open_id': _session_user.open_id, 'version': _session_user.version,
                         'req_cnt': _session_user.req_cnt, 'req_last': _session_user.last_req,
                         'gm': _session_user.gm, 'plat': _session_user.plat.value, 'lang': _session_user.lang.value})

        _req_exist_key = "#".join([_session_user.game, _session_user.channel, RedisKey.REQ_LOCK.value,
                                   str(_session_user.uid), str(_session_user.req_cnt)])
        _r = RedisManager.get_redis()
        _exists = await _r.set(_req_exist_key, 1, ex=5, nx=True)
        if not _exists:
            _ctx.log.update({"cheat": "reqConflict"})
            return PlainTextResponse("CONFLICT", status_code=status.HTTP_409_CONFLICT)

        _now = int(time.time())
        if _now - _session_user.last_req >= SESSION_EXPIRED_TIME:
            _ctx.log.update({"cheat": "loginExpired"})
            return PlainTextResponse("UNAUTHORIZED1", status_code=status.HTTP_401_UNAUTHORIZED)

        # 调用gm接口，却没有gm权限
        if _uri.rfind("/gm/") >=0 and not _session_user.gm:
            _ctx.log.update({"cheat": "notGmUser"})
            return PlainTextResponse("UNAUTHORIZED2", status_code=status.HTTP_401_UNAUTHORIZED)

        _session_user.last_req = _now

        _ctx.user = _session_user
        response = await call_next(request)

        # 如果存在session中还存在info对象，直接删除（这里隐性约定convert接口之后的第二个协议就应该将info的属性转存起来）
        if 'info' in _user:
            del _user['info']

        # response.headers[_header_key] = " ".join([_game, rsa_encrypt2(json.dumps(_user), _cfg[_game]['pub_key'])])
        response.headers[_header_key] = " ".join([_game, fernet_encrypt(_session_user.json().encode(), _fernet_key).decode()])

        if REQUEST_COUNTER_KEY in request.scope:
            _game_ctx: GameContext = request.scope[GAME_CONTEXT_KEY]
            _game_ctx.update_data(request.scope[REQUEST_COUNTER_KEY], {"last_header": response.headers[_header_key]})
        return response


def get_context(req: Request)->Context:
    return req.scope[CONTEXT_KEY]


def get_game_context(req: Request)->GameContext:
    return req.scope[GAME_CONTEXT_KEY]

def get_session_user(req: Request)->SessionUser:
    return get_context(req).user


@app.middleware("http")
async def http_log_inspector(request, call_next):
    if request.method != 'POST':
        return await call_next(request)

    _start_time = time.perf_counter()
    _container = Context(path=request.scope['path'])
    request.scope[CONTEXT_KEY] = _container
    _game_ctx = GameContext(_container)
    request.scope[GAME_CONTEXT_KEY] = _game_ctx
    response = await call_next(request)
    _process_time = time.perf_counter() - _start_time
    if _container.user:
        await _game_ctx.save_all()
    _container.log.update({"process_time": _process_time, "path": _container.path})
    log_info(_container.log)
    return response


def run(port=None, reload=False):
    uvicorn.run(app="pg_httpserver.fapi:app", host=config.get_host(), reload=reload,
                port=config.get_port() if port is None else port)