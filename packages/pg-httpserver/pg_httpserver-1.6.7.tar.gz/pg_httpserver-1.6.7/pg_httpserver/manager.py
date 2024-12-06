import struct

from pg_common import SingletonBase, log_error, log_info, GLOBAL_DEBUG, RewardItem, ConsumeItem, log_warn, \
    ObjDecoratorManager, RuntimeException, ip_2_long
from abc import ABC, abstractmethod
from pg_environment import config
from pg_redis import RedisManager
from .define import ExCodeCfg, GameContext, AutoId, NoticeCfg, ENV_IP2REGION_XDB_FILE_KEY
from .models import RedisKey
import json
from enum import Enum


__all__ = ("GameConfigManager", "GamePropertyManager", "AutoIdManager", "GameExCodeManager", "GameNoticeManager",
           "ResourceBase", "ItemManager", "XdbManager")


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


class ResourceBase(ABC):

    @abstractmethod
    async def check_consume(self, game_ctx:GameContext, consume: ConsumeItem) -> bool:
        pass

    @abstractmethod
    async def consume(self, game_ctx: GameContext, consume: ConsumeItem):
        pass

    @abstractmethod
    async def reward(self, game_ctx: GameContext, reward: RewardItem)-> RewardItem:
        pass


class _ItemManager(SingletonBase):

    def __init__(self):
        self._item_types = None
        self._obj_types = None

    def register_types(self, _item_types, _object_type):
        if not _item_types.__class__ == Enum.__class__:
            raise RuntimeException("ItemTypesRegister", f"{_item_types} is not type of ItemType")
        if len(_item_types.__members__) <= 0:
            raise RuntimeException("ItemTypesRegister", f"{_item_types} must has one member.")
        if not _object_type.__class__ == Enum.__class__:
            raise RuntimeException("ObjectTypeRegister", f"{_object_type} is not type of ObjectType")
        self._obj_types = _object_type
        self._item_types = _item_types

    def get_resource(self, _id: int)->ResourceBase:
        if not self._item_types or not self._obj_types:
            raise RuntimeException("ItemManagerInit", f"please run ItemManager.register_types first.")
        _item_first = list(self._item_types.__members__.values())[0]
        for _val in self._item_types.__members__.values():
            if _val.value[0] <= _id <= _val.value[1]:
                if _val == _item_first:
                    for _v in self._obj_types.__members__.values():
                        if _v.value == _id:
                            return ObjDecoratorManager.get_obj(_v)
                else:
                    return ObjDecoratorManager.get_obj(_val)
        log_warn(f"not support resource id: {_id}")
        return None

    async def add_rewards(self, game_ctx: GameContext, rewards: list[RewardItem]) -> list[RewardItem]:
        ret = []
        for _item in rewards:
            _resource = self.get_resource(_item.id)
            if _resource:
                ret.append(await _resource.reward(game_ctx, _item))
        return ret

    @staticmethod
    def merge_consume(consumes: list[ConsumeItem])->list[ConsumeItem]:
        _dict = {}
        for _item in consumes:
            if _item.id not in _dict:
                _dict[_item.id] = _item
            else:
                _dict[_item.id].count += _item.count
        return list(_dict.values())

    async def check_consume(self, game_ctx: GameContext, consumes: list[ConsumeItem]) -> bool:
        _list = _ItemManager.merge_consume(consumes)
        for _item in _list:
            _resource = self.get_resource(_item.id)
            if _resource:
                _ret = await _resource.check_consume(game_ctx, _item)
                if not _ret:
                    return False
        return True

    async def consume(self, game_ctx: GameContext, consumes: list[ConsumeItem]):
        for _item in consumes:
            _resource = self.get_resource(_item.id)
            if _resource:
                await _resource.consume(game_ctx, _item)


ItemManager = _ItemManager()

HeaderInfoLength = 256
VectorIndexCols = 256
VectorIndexSize = 8
SegmentIndexSize = 14
class _XdbManager(SingletonBase):
    def __init__(self):
        self.buff = None

    def init(self):
        _file = config.get_conf(ENV_IP2REGION_XDB_FILE_KEY, "asserts/ip2region.xdb")
        with open(_file, "rb") as _f:
            self.buff = _f.read()

    def get_region(self, _ip:str):
        return self.search_by_ip(ip_2_long(_ip))

    def search_by_ip(self, ip:int):
        e_ptr = s_ptr = 0
        il0 = (ip>>24) & 0xFF
        il1 = (ip>>16) & 0xFF
        idx = il0 * VectorIndexCols * VectorIndexSize + il1 * VectorIndexSize

        s_ptr = self.get_long(self.buff, HeaderInfoLength + idx)
        e_ptr = self.get_long(self.buff, HeaderInfoLength + idx + 4)

        d_len = d_ptr = int(-1)
        l = int(0)
        h = int((e_ptr - s_ptr) / SegmentIndexSize)
        while l <= h:
            m = int((l+h)>>1)
            p = int(s_ptr+m*SegmentIndexSize)
            buffer_sip = self.read_buffer(p, SegmentIndexSize)
            sip = self.get_long(buffer_sip, 0)
            if ip < sip:
                h = m - 1
            else:
                eip = self.get_long(buffer_sip, 4)
                if ip > eip:
                    l = m + 1
                else:
                    d_len = self.get_int2(buffer_sip, 8)
                    d_ptr = self.get_long(buffer_sip, 10)
                    break
        if d_ptr < 0:
            return ""
        buffer_string = self.read_buffer(d_ptr, d_len)
        return_string = buffer_string.decode("utf-8")
        return return_string

    def read_buffer(self, offset, length):
        buffer = None
        if self.buff:
            return self.buff[offset:offset+length]
        return buffer

    @staticmethod
    def get_long(b, offset):
        if len(b[offset:offset+4]) == 4:
            return struct.unpack('I', b[offset:offset+4])[0]
        return 0

    @staticmethod
    def get_int2(b, offset):
        return (b[offset] & 0x000000FF) | (b[offset + 1] << 8)

    def close(self):
        self.buff = None

XdbManager = _XdbManager()
