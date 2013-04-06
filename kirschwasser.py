#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)

import argparse
import redis

import util
from collection import Collection


def index(args):
    if args.verbose:
        print('Indexing files...')
    for path in args.path:
        if args.verbose:
            print("Crawling {0} for files...".format(path))
        files = util.find(path, dirs=False)
        for file in files:
            if args.verbose:
                print("Indexing {0}...".format(file))
            args.collection.index.add_path(file)

parser = argparse.ArgumentParser()

# global options
parser.add_argument('-p', '--redis-port', type=int, default=6379,
                    help='use the redis-server on this port')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='be talkative')

subparsers = parser.add_subparsers(title="Available commands")

# Index Mode
index_mode = subparsers.add_parser("index", help="search for and index files")
index_mode.add_argument('path', nargs='+',
                        help='paths to index')
index_mode.set_defaults(func=index)

if __name__ == "__main__":
    args = parser.parse_args()
    rs = redis.StrictRedis(port=args.redis_port)

    col = Collection('test', rs)
    args.collection = col
    args.func(args)
