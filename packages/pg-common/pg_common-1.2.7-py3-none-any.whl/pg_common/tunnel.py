from sshtunnel import SSHTunnelForwarder, SSH_CONFIG_FILE
import pymysql
from pymysql.cursors import DictCursor
import redis
import pymongo


__all__ = ["RedisTunnel", "MysqlTunnel", "MongoTunnel"]
__author__ = "baozilaji@gmail.com"

class RedisTunnel(object):
    def __init__(self,
                 ssh_address_or_host=None,
                 ssh_config_file=SSH_CONFIG_FILE,
                 ssh_host_key=None,
                 ssh_password=None,
                 ssh_pkey=None,
                 ssh_private_key_password=None,
                 ssh_proxy=None,
                 ssh_proxy_enabled=True,
                 ssh_username=None,
                 local_bind_address=None,
                 local_bind_addresses=None,
                 logger=None,
                 mute_exceptions=False,
                 remote_bind_address=None,
                 remote_bind_addresses=None,
                 set_keepalive=5.0,
                 threaded=True,  # old version False
                 compression=None,
                 allow_agent=True,  # look for keys from an SSH agent
                 host_pkey_directories=None,  # look for keys in ~/.ssh
                 redis_db=0,
                 redis_pass='',
                 *args, **kwargs):
        self.ssh_address_or_host = ssh_address_or_host
        self.ssh_config_file = ssh_config_file
        self.ssh_host_key = ssh_host_key
        self.ssh_password = ssh_password
        self.ssh_pkey = ssh_pkey
        self.ssh_private_key_password = ssh_private_key_password
        self.ssh_proxy = ssh_proxy
        self.ssh_proxy_enabled = ssh_proxy_enabled
        self.ssh_username = ssh_username
        self.local_bind_address = local_bind_address
        self.local_bind_addresses = local_bind_addresses
        self.logger = logger
        self.mute_exceptions = mute_exceptions
        self.remote_bind_address = remote_bind_address
        self.remote_bind_addresses = remote_bind_addresses
        self.set_keepalive = set_keepalive
        self.threaded = threaded
        self.compression = compression
        self.allow_agent = allow_agent
        self.host_pkey_directories = host_pkey_directories
        self._server = None
        self._redis = None
        self._redis_db = redis_db
        self._redis_pass = redis_pass
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self._server = SSHTunnelForwarder(ssh_address_or_host=self.ssh_address_or_host,
                                          ssh_config_file=self.ssh_config_file,
                                          ssh_host_key=self.ssh_host_key,
                                          ssh_password=self.ssh_password,
                                          ssh_pkey=self.ssh_pkey,
                                          ssh_private_key_password=self.ssh_private_key_password,
                                          ssh_proxy=self.ssh_proxy,
                                          ssh_proxy_enabled=self.ssh_proxy_enabled,
                                          ssh_username=self.ssh_username,
                                          local_bind_address=self.local_bind_address,
                                          local_bind_addresses=self.local_bind_addresses,
                                          logger=self.logger,
                                          mute_exceptions=self.mute_exceptions,
                                          remote_bind_address=self.remote_bind_address,
                                          remote_bind_addresses=self.remote_bind_addresses,
                                          set_keepalive=self.set_keepalive,
                                          threaded=self.threaded,
                                          compression=self.compression,
                                          allow_agent=self.allow_agent,
                                          host_pkey_directories=self.host_pkey_directories,
                                          *self._args,
                                          **self._kwargs
                                          )
        try:
            self._server.start()
        except KeyboardInterrupt:
            self.__exit__()
        self._redis = redis.StrictRedis(host=self._server.local_bind_host,
                                        port=self._server.local_bind_port,
                                        db=self._redis_db,
                                        password=self._redis_pass)
        return self._redis

    def __exit__(self, *args):
        if self._redis:
            self._redis.close()

        if self._server:
            self._server.stop(force=True)


class MysqlTunnel(object):
    def __init__(self,
                 ssh_address_or_host=None,
                 ssh_config_file=SSH_CONFIG_FILE,
                 ssh_host_key=None,
                 ssh_password=None,
                 ssh_pkey=None,
                 ssh_private_key_password=None,
                 ssh_proxy=None,
                 ssh_proxy_enabled=True,
                 ssh_username=None,
                 local_bind_address=None,
                 local_bind_addresses=None,
                 logger=None,
                 mute_exceptions=False,
                 remote_bind_address=None,
                 remote_bind_addresses=None,
                 set_keepalive=5.0,
                 threaded=True,  # old version False
                 compression=None,
                 allow_agent=True,  # look for keys from an SSH agent
                 host_pkey_directories=None,  # look for keys in ~/.ssh
                 database='mysql',
                 db_user='root',
                 db_pass='',
                 *args, **kwargs):
        self.ssh_address_or_host = ssh_address_or_host
        self.ssh_config_file = ssh_config_file
        self.ssh_host_key = ssh_host_key
        self.ssh_password = ssh_password
        self.ssh_pkey = ssh_pkey
        self.ssh_private_key_password = ssh_private_key_password
        self.ssh_proxy = ssh_proxy
        self.ssh_proxy_enabled = ssh_proxy_enabled
        self.ssh_username = ssh_username
        self.local_bind_address = local_bind_address
        self.local_bind_addresses = local_bind_addresses
        self.logger = logger
        self.mute_exceptions = mute_exceptions
        self.remote_bind_address = remote_bind_address
        self.remote_bind_addresses = remote_bind_addresses
        self.set_keepalive = set_keepalive
        self.threaded = threaded
        self.compression = compression
        self.allow_agent = allow_agent
        self.host_pkey_directories = host_pkey_directories
        self._server = None
        self._db = None
        self._database = database
        self._db_user = db_user
        self._db_pass = db_pass
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self._server = SSHTunnelForwarder(ssh_address_or_host=self.ssh_address_or_host,
                                          ssh_config_file=self.ssh_config_file,
                                          ssh_host_key=self.ssh_host_key,
                                          ssh_password=self.ssh_password,
                                          ssh_pkey=self.ssh_pkey,
                                          ssh_private_key_password=self.ssh_private_key_password,
                                          ssh_proxy=self.ssh_proxy,
                                          ssh_proxy_enabled=self.ssh_proxy_enabled,
                                          ssh_username=self.ssh_username,
                                          local_bind_address=self.local_bind_address,
                                          local_bind_addresses=self.local_bind_addresses,
                                          logger=self.logger,
                                          mute_exceptions=self.mute_exceptions,
                                          remote_bind_address=self.remote_bind_address,
                                          remote_bind_addresses=self.remote_bind_addresses,
                                          set_keepalive=self.set_keepalive,
                                          threaded=self.threaded,
                                          compression=self.compression,
                                          allow_agent=self.allow_agent,
                                          host_pkey_directories=self.host_pkey_directories,
                                          *self._args,
                                          **self._kwargs
                                          )
        try:
            self._server.start()
        except KeyboardInterrupt:
            self.__exit__()
        self._db = pymysql.connect(host=self._server.local_bind_host,
                                   port=self._server.local_bind_port,
                                   database=self._database, user=self._db_user, password=self._db_pass)
        return self

    def __exit__(self, *args):
        if self._db:
            self._db.close()

        if self._server:
            self._server.stop(force=True)

    def exec_select(self, sql):
        _cur = self._db.cursor(DictCursor)
        _cur.execute(sql)
        _data = _cur.fetchall()
        _cur.close()
        return _data

    def exec_update(self, sql):
        _cur = self._db.cursor(DictCursor)
        _cur.execute(sql)
        self._db.commit()
        _cur.close()


class MongoTunnel(object):
    def __init__(self,
            ssh_address_or_host=None,
            ssh_config_file=SSH_CONFIG_FILE,
            ssh_host_key=None,
            ssh_password=None,
            ssh_pkey=None,
            ssh_private_key_password=None,
            ssh_proxy=None,
            ssh_proxy_enabled=True,
            ssh_username=None,
            local_bind_address=None,
            local_bind_addresses=None,
            logger=None,
            mute_exceptions=False,
            remote_bind_address=None,
            remote_bind_addresses=None,
            set_keepalive=5.0,
            threaded=True,  # old version False
            compression=None,
            allow_agent=True,  # look for keys from an SSH agent
            host_pkey_directories=None,  # look for keys in ~/.ssh
            *args,
            **kwargs  # for backwards compatibility
    ):
        self.ssh_address_or_host = ssh_address_or_host
        self.ssh_config_file = ssh_config_file
        self.ssh_host_key = ssh_host_key
        self.ssh_password = ssh_password
        self.ssh_pkey = ssh_pkey
        self.ssh_private_key_password = ssh_private_key_password
        self.ssh_proxy = ssh_proxy
        self.ssh_proxy_enabled = ssh_proxy_enabled
        self.ssh_username = ssh_username
        self.local_bind_address = local_bind_address
        self.local_bind_addresses = local_bind_addresses
        self.logger = logger
        self.mute_exceptions = mute_exceptions
        self.remote_bind_address = remote_bind_address
        self.remote_bind_addresses = remote_bind_addresses
        self.set_keepalive = set_keepalive
        self.threaded = threaded
        self.compression = compression
        self.allow_agent = allow_agent
        self.host_pkey_directories = host_pkey_directories
        self._server = None
        self._connect = None
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self._server = SSHTunnelForwarder(ssh_address_or_host=self.ssh_address_or_host,
                                          ssh_config_file=self.ssh_config_file,
                                          ssh_host_key=self.ssh_host_key,
                                          ssh_password=self.ssh_password,
                                          ssh_pkey=self.ssh_pkey,
                                          ssh_private_key_password=self.ssh_private_key_password,
                                          ssh_proxy=self.ssh_proxy,
                                          ssh_proxy_enabled=self.ssh_proxy_enabled,
                                          ssh_username=self.ssh_username,
                                          local_bind_address=self.local_bind_address,
                                          local_bind_addresses=self.local_bind_addresses,
                                          logger=self.logger,
                                          mute_exceptions=self.mute_exceptions,
                                          remote_bind_address=self.remote_bind_address,
                                          remote_bind_addresses=self.remote_bind_addresses,
                                          set_keepalive=self.set_keepalive,
                                          threaded=self.threaded,
                                          compression=self.compression,
                                          allow_agent=self.allow_agent,
                                          host_pkey_directories=self.host_pkey_directories,
                                          *self._args,
                                          **self._kwargs
                                          )
        try:
            self._server.start()
        except KeyboardInterrupt:
            self.__exit__()
        self._connect = pymongo.MongoClient(host=self._server.local_bind_host, port=self._server.local_bind_port)
        return self._connect

    def __exit__(self, *args):
        if self._connect:
            self._connect.close()

        if self._server:
            self._server.stop(force=True)

