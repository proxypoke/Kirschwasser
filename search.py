# Kirschwasser - a file indexer with tagging capabilities
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/kirschwasser
# (Shortlink: https://git.io/kirschwasser)


class BoolSearch:

    '''A simple search interface for a collection.

    BoolSearch only supports boolean operators (AND, OR, NOT, XOR).
    '''

    # The collection on which to apply the search queries.
    _collection = None

    _OPERATORS = {"AND", "OR", "NOT"}

    def __init__(self, collection):
        self._collection = collection

    def search(self, query):
        query = query.split()

        # queries implicitly start with AND if no other operator is given
        if query[0] not in self._OPERATORS:
            query = ["AND"] + query

        searchspace = self._collection.index.universe()
        while True:
            # stop if there are no tags left or only a trailing operator.
            if len(query) < 2:
                break
            operator, tags = self._parse_exp(query)
            # ignore operators without tags
            if len(tags) <= 0:
                continue
            for tag in tags:
                hashset = self._collection.get_tag(tag)
                if operator == "AND":
                    searchspace &= hashset
                if operator == "OR":
                    searchspace |= hashset
                if operator == "NOT":
                    searchspace -= hashset
        return searchspace

    def _parse_exp(self, query):
        operator = query.pop(0)
        tags = []
        while True:
            if len(query) <= 0:
                break
            next = query[0]
            if next not in self._OPERATORS:
                tags.append(query.pop(0))
            else:
                break
        return operator, tags
