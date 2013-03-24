# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)

'''redis_server.py - start a Redis instance for a single application.'''

import subprocess
import tempfile
import atexit
import redis

config = '''
daemonize no
port 0
unixsocketperm 755
loglevel notice
appendonly yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
dir {dir}
unixsocket  {sock}
logfile {log}
appendfilename {aof}
'''


class RedisServer():

    '''A per-program Redis server, controlled over a Unix socket.

    On initialization, this will create a temporary directory (prefixed with
    'redis-'), write a config file into it, and start redis-server with this
    config. This temporary directory will also hold the unix socket for
    communication as well as the log file.

    So far, the only argument to init is a path where the Redis server will
    store its append-only file. This file must either be absolute, or just a
    simple filename (without any forward slashes). In the latter case, this
    will place the append-only file in the same temporary directory as the
    config, so beware.
    '''

    _tmpdir = None
    _config = None
    _sock = None
    _log = None
    _proc = None

    def __init__(self, aof_path):
        if not aof_path.startswith('/') and '/' in aof_path.count('/'):
            raise ValueError("Can't use relative paths in filename.")

        self._tmpdir = tempfile.mkdtemp(prefix="redis-")
        self._sock = self._tmpdir + "/socket"
        self._log = self._tmpdir + "/log"
        self._config = self._tmpdir + "/config"

        cfg_file = open(self._config, "w")
        cfg_file.write(config.format(dir=self._tmpdir,
                                     sock=self._sock,
                                     log=self._log,
                                     aof=aof_path))
        cfg_file.close()

        self._proc = subprocess.Popen(
            ['redis-server', self._config])
        atexit.register(self._proc.terminate)

    def terminate(self):
        '''Send SIGTERM to the Redis server process.'''
        self._proc.terminate()

    def kill(self):
        '''Send SIGKILL to the Redis server process.'''
        self._proc.kill()

    def instance(self):
        '''Acquire a StrictRedis object using this server.'''
        return redis.StrictRedis(unix_socket_path=self._sock)
