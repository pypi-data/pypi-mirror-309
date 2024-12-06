from .conf import SessionUser, LangType, PlatType, GLOBAL_DEBUG, GenderType
from .util import fernet_encrypt, base64_decode, base64_encode, fernet_decrypt
from .func import log_info
try:
    from pg_objectserialization import dumps, loads
except ImportError:
    from .util import dumps, loads
import time
import requests
import aiohttp


__all__ = ("GmUser", "GameUser")
__author__ = "baozilaji@gmail.com"

class GmUser(object):
    def __init__(self, game:str, channel:str, fernet_key:str, gm:str, uid:int=-1,
                 open_id:str='gm', session_key:str='gm', version:int=0, lang:LangType=LangType.zh_CN,
                 plat:PlatType=PlatType.ios):
        self.fernet_key = fernet_key
        self.sessionUser = SessionUser(uid=uid, open_id=open_id, gm=gm, sessionKey=session_key, game=game,
                                       channel=channel, lang=lang, plat=plat, version=version,
                                       last_req=int(time.time()))
        self.token = self._build_authentication()

    def _build_authentication(self):
        return " ".join([self.sessionUser.game,
                         fernet_encrypt(self.sessionUser.json().encode(), self.fernet_key).decode()])

    def _build_header(self):
        return {"Authentication": self.token}

    def post_data(self, url:str, data:dict):
        headers = self._build_header()
        data = base64_encode(dumps(data, p=GLOBAL_DEBUG))
        resp = requests.post(url, data=data, headers=headers)
        if "Authentication" in resp.headers:
            self.token = resp.headers["Authentication"]
        out = loads(base64_decode(resp.text.encode()), p=GLOBAL_DEBUG)
        return out


class GameUser(object):
    def __init__(self, sns_uid: str, game: str, channel: str, fernet_key: str, version:int = 0,
                 lang:LangType=LangType.zh_CN, plat:PlatType=PlatType.ios,
                 config_base_url:str = "http://192.168.1.251:9001",
                 convert_base_url:str = "http://192.168.1.251:9002",
                 game_base_url:str = "http://192.168.1.251:10001"):
        self.sns_uid = sns_uid
        self.game = game
        self.channel = channel
        self.fernet_key = fernet_key
        self.version = version
        self.lang = lang
        self.plat = plat
        self.authentication = None
        self.update_auth = False
        self.config_base_url = config_base_url
        self.convert_base_url = convert_base_url
        self.game_base_url = game_base_url
        self.c_nid = 0
        self.c_mid = 0
        self.s_nid = 0
        self.s_mid = 0

    async def post(self, url, data:dict):
        log_info(f"===post url: {url} started===")
        log_info(f"req data before encrypt: {data}")
        _data = base64_encode(dumps(data, p=GLOBAL_DEBUG))
        log_info(f"req data after encrypt: {_data}")
        _headers = {"Content-Type": "application/json"}
        if self.update_auth:
            _headers["Authentication"] = self.authentication
            _h = self.authentication.split(" ")[1]
            log_info(f"req session: {fernet_decrypt(_h.encode(), self.fernet_key.encode()).decode()}")
        log_info(f"req headers: {_headers}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=_data, headers=_headers) as _resp:
                if _resp.status != 200:
                    _text = await _resp.text()
                    log_info(f"resp error: {url}, {_resp.status}, msg: {_text}")
                    log_info(f"===post url: {url} finished===")
                    return ""
                if "Authentication" in _resp.headers:
                    self.authentication = _resp.headers["Authentication"]
                    self.update_auth = True
                    _h = self.authentication.split(" ")[1]
                    log_info(f"resp session: {fernet_decrypt(_h.encode(), self.fernet_key.encode()).decode()}")
                else:
                    self.update_auth = False
                _text = await _resp.text()
                log_info(f"resp data before decrypt: {_text}")
                _out = loads(base64_decode(_text), p=GLOBAL_DEBUG)
                log_info(f"resp data after decrypt: {_out}")
                if url.rfind("/game_index") < 0 and "head" in _out:
                    self.s_nid = _out['head']['auto_ids']['nid']
                    self.s_mid = _out['head']['auto_ids']['mid']
                log_info(f"===post url: {url} finished===")
                return _out

    async def login(self):
        _url = f"{self.convert_base_url}/convert/{self.game}/{self.channel}/{self.version}/{self.plat.value}/{self.lang.value}"
        _out = await self.post(_url, {"snsUid": self.sns_uid, "sex": GenderType.unknown.value})
        self.authentication = _out['session']
        self.update_auth = True

    async def game_index(self):
        _url = f"{self.game_base_url}/common/game_index"
        await self.post(_url, {})

    async def notice_list(self):
        _url = f"{self.game_base_url}/common/get_notice_list/{self.c_nid}"
        await self.post(_url, {})

    async def message_list(self):
        _url = f"{self.game_base_url}/common/get_message_list/{self.c_mid}"
        await self.post(_url, {})
