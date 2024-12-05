from pg_common import SingletonBase, log_error, log_info, GLOBAL_DEBUG
from pg_environment import config
from pg_redis import RedisManager
from .define import ExCodeCfg, GameContext, AutoId, NoticeCfg
from .models import RedisKey
import json


__all__ = ("GameConfigManager", "GamePropertyManager", "AutoIdManager", "GameExCodeManager", "GameNoticeManager")


GAME_CONFIG_REDIS_KEY = "__GAME_CONFIG__"
GAME_PROPERTY_REDIS_KEY = "__GAME_PROPERTY__"


class _AutoIdManager(SingletonBase):

    def __init__(self):
        pass

    @staticmethod
    def get_redis_key(game_ctx: GameContext):
        return "#".join([game_ctx.get_redis_prefix(), RedisKey.AUTO_ID.value, str(game_ctx.ctx.user.uid)])

    @staticmethod
    async def get_auto_ids(game_ctx: GameContext)->AutoId:
        _r = RedisManager.get_redis(game_ctx.get_redis_server_name())
        _r_k = _AutoIdManager.get_redis_key(game_ctx)
        _out = await _r.hgetall(_r_k)
        _nid = GameNoticeManager.get_max_id(game_ctx.ctx.user.game)
        if not _out:
            return AutoId(nid=_nid)
        _ret = AutoId(**_out)
        _ret.nid = _nid
        return _ret

    @staticmethod
    async def increase_id_by_key(game_ctx: GameContext, key: str)->int:
        _r = RedisManager.get_redis(game_ctx.get_redis_server_name())
        _r_k = _AutoIdManager.get_redis_key(game_ctx)
        return await _r.hincrby(_r_k, key, 1)


class _GamePropertyManager(SingletonBase):
    def __init__(self):
        self._cfg: dict[str, dict] = {}

    async def reload(self):
        _r = await RedisManager.get_redis()
        if _r:
            _prop = await _r.get(GAME_PROPERTY_REDIS_KEY)
            if _prop:
                self._cfg = json.loads(_prop)
                log_info("load game property success.")
            else:
                log_error(f"!!!can not get key {GAME_PROPERTY_REDIS_KEY} in redis.")
        else:
            log_error("!!!!can not get redis client.")

        if GLOBAL_DEBUG:
            log_info(f"game_property:{self._cfg}")

    def get_config(self):
        if self._cfg:
            return self._cfg
        else:
            return config.get_conf("game_property", {})


class _GameExCodeManager(SingletonBase):
    def __init__(self):
        self._ex_cfg:dict[str, dict[int, ExCodeCfg]] = {}
        self._manual_code:[str, dict[str, ExCodeCfg]]= {}

    def reload(self, data:[], game: str):
        for d in data:
            _c = ExCodeCfg(**d)
            if game not in self._ex_cfg:
                self._ex_cfg[game] = {}
            _manual_key = "_".join([game, _c.channel])
            if _manual_key not in self._manual_code:
                self._manual_code[_manual_key] = {}
            self._ex_cfg[game][d['id']] = _c
            if not _c.auto_gen:
                _codes = _c.code.split(",")
                for _code in _codes:
                    if _code:
                        self._manual_code[_manual_key][_code] = _c

        if GLOBAL_DEBUG:
            log_info(f"game:{game},ex_cfg:{self._ex_cfg},manual_code:{self._manual_code}")

    def get_by_id(self, game, _id)->ExCodeCfg:
        if game in self._ex_cfg and _id in self._ex_cfg[game]:
            return self._ex_cfg[game][_id]
        return None

    def get_by_code(self, game, channel, code)->ExCodeCfg:
        key = "_".join([game, channel])
        if key in self._manual_code and code in self._manual_code[key]:
            return self._manual_code["_".join([game, channel])][code]
        return None


class _GameNoticeManager(SingletonBase):
    def __init__(self):
        self._notice: dict[str, dict[int, NoticeCfg]] = {}
        self._max_id:dict[str, int] = {}

    def reload(self, data: [], game:str):
        for d in data:
            _c = NoticeCfg(**d)
            if _c.pre_login:
                continue
            if game not in self._notice:
                self._notice[game] = {}
            if game not in self._max_id:
                self._max_id[game] = 0
            self._notice[game][_c.id] = _c
            if _c.id > self._max_id[game]:
                self._max_id[game] = _c.id

        if GLOBAL_DEBUG:
            log_info(f"game:{game}, max_id:{self._max_id}, notices:{self._notice}")

    def get_by_id(self, game, _id)->NoticeCfg:
        if game in self._notice and _id in self._notice[game]:
            return self._notice[game][_id]
        return None

    def get_max_id(self, game):
        if game not in self._max_id:
            return 0
        return self._max_id[game]

    def get_by_min_id(self, game, _mid):
        ret = []
        if game in self._notice:
            for _d in self._notice[game].keys():
                if _d > _mid:
                    ret.append(self._notice[game][_d])
        return ret


class _GameConfigManager(SingletonBase):
    def __init__(self):
        self._cfg: dict[str, dict] = {}

    async def reload(self):
        _r = await RedisManager.get_redis()
        if _r:
            _games = await _r.smembers(GAME_CONFIG_REDIS_KEY)
            for _g in _games:
                _json = await _r.get("%s:%s" % (GAME_CONFIG_REDIS_KEY, _g))
                if _json:
                    self._cfg[_g] = json.loads(_json)
                    log_info(f"===[{_g}]:[{self._cfg[_g]['version']}]===")

                    if "excodes" in self._cfg[_g]:
                        GameExCodeManager.reload(self._cfg[_g]['excodes'], _g)
                    else:
                        log_info(f"---[{_g}]:has no ex code config---")

                    if "notices" in self._cfg[_g]:
                        GameNoticeManager.reload(self._cfg[_g]['notices'], _g)
                    else:
                        log_info(f"---[{_g}]: has no after login notice config---")

            if GLOBAL_DEBUG:
                log_info(f"game_config:{self._cfg}")

        else:
            log_error("!!!!!!!can not get redis client.")

    def get_config(self, game: str) -> dict:
        if game in self._cfg:
            return self._cfg[game]
        return None


GameConfigManager = _GameConfigManager()
GamePropertyManager = _GamePropertyManager()
GameExCodeManager = _GameExCodeManager()
AutoIdManager = _AutoIdManager()
GameNoticeManager = _GameNoticeManager()
