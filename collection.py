# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)

import index
import util


class Collection:
    '''A collection is a set of tags and an index with which they are
    associated.'''

    # the name of this collection
    _name = None
    # the redis instance this collection uses
    _db = None
    # the index this collection uses
    # TODO: make it possible to use multiple indices in the future
    index = None

    def __init__(self, name, db):
        self._name = name
        self._db = db
        self.index = index.Index(name, db)

    def _tagkey(self, *args):
        return util.gen_key(self._name, 'tags', *args)

    def has_tag(self, keyword):
        return self._db.sismember(self._tagkey(), keyword)

    def add_tag(self, keyword):
        '''Add a tag to the collection.'''
        self._db.sadd(self._tagkey(), keyword)

    def del_tag(self, keyword):
        '''Remove a tag from the collection.'''
        self._db.srem(self._tagkey(), keyword)

    def tag_path(self, path, keyword):
        if not self.has_tag(keyword):
            self.add_tag(keyword)
        hash = self.index.get_hash(path)
        self._db.sadd(self._tagkey(keyword), hash)

    def untag_path(self, path, keyword):
        hash = self.index.get_hash(path)
        self._db.srem(self._tagkey(keyword), hash)

    def list_tags(self):
        return {keyword.decode() for keyword in
                self._db.smembers(self._tagkey())}

    def get_tag(self, keyword):
        return {hash.decode() for hash in self._db.smembers(
            self._tagkey(keyword))}
