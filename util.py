# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)

import hashlib
import os
import re


def gen_key(*args):
    '''Generate a redis key.'''
    return '.'.join(args)


def hash_file(path, algo=hashlib.md5):
    '''Hash a given files' contents.

    Arguments:
        path -- the file to hash.
        algo -- a hash function from hashlib. Defaults to md5.

    Returns:
        A hexadecimal hash of the file's contents.
    '''
    if not os.access(path, os.F_OK):
        raise IOError("File {0} does not exist.".format(path))
    if not os.access(path, os.R_OK):
        raise IOError("File {0} is not readable.".format(path))

    file_ = open(path, 'rb')
    hash_ = algo()
    hash_.update(file_.read())
    return hash_.hexdigest()


def find(start_dir=".", dirs=True, files=True, filter='.*'):
    '''Return a list of all files and/or directories contained by start_dir and
    all its sub-directories.

    Arguments:
        start_dir -- the directory from which to search. Defaults to $PWD.
        dirs -- include directories. Defaults to True.
        files -- include regular (non-dir) files. Defaults to True.
        filter -- a regexp to whitelist files. Default '.*'.
    '''

    result = []
    for dirpath, _, filenames in os.walk(start_dir):
        if dirs and re.search(filter, dirpath):
            result.append(dirpath)
        if files:
            for file in filenames:
                if re.search(filter, file):
                    result.append(os.sep.join([dirpath, file]))
    return result
