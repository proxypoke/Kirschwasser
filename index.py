# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)

'''This module defines an API to communicate with the Redis server.'''

import os
import util


class Index:
    '''An index is a set of filepaths with their associated hashes.'''

    # the name of this index
    _name = None
    # the redis instance this index uses
    _db = None

    def __init__(self, name, db):
        self._name = name
        self._db = db

    def _pathkey(self, *args):
        return util.gen_key(self._name, 'paths', *args)

    def _blobkey(self, *args):
        return util.gen_key(self._name, 'blobs', *args)

    def has_path(self, path):
        path = os.path.realpath(path)
        return self._db.sismember(self._pathkey(), path)

    def add_path(self, path):
        '''Add a file to the index.'''
        path = os.path.realpath(path)
        self._add_blob_by_path(path)
        self._db.sadd(self._pathkey(), path)

    def _add_blob_by_path(self, path):
        hash = util.hash_file(path)
        self._add_blob(hash)
        self._db.set(self._pathkey(path), hash)
        self._db.sadd(self._blobkey(hash), path)

    def _add_blob(self, hash):
        self._db.sadd(self._blobkey(), hash)

    def del_path(self, path):
        '''Remove a file from the index.'''
        path = os.path.realpath(path)
        self._del_blob_by_path(path)
        self._db.srem(self._pathkey(), path)

    def _del_blob_by_path(self, path):
        if not self.has_path(path):
            #print("{0} not found.".format(path))
            return
        hash = self.get_hash(path)
        self._db.delete(self._pathkey(path))
        self._db.srem(self._blobkey(hash), path)

    def _del_blob(self, hash):
        self._db.srem(self._blobkey(), hash)

    def get_hash(self, path):
        '''Get the hash of a path if it's already in the index.'''
        path = os.path.realpath(path)
        return self._db.get(self._pathkey(path)).decode()

    def list_paths(self):
        return {path.decode() for path in self._db.smembers(self._pathkey())}

    def universe(self):
        '''Get the set of all hashes.'''
        return {hash.decode() for hash in self._db.smembers(self._blobkey())}
