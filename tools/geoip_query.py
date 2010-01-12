#!/usr/bin/env python
# coding: utf-8

dbname = "ipdb.cdb"

import sys, cdb

def convert(addr):
    a, b, c, d = map(lambda x:int(x), addr.split("."))
    for n in (a, b, c, d):
        assert n >= 0 and n <= 255
    return str(((a*256+b)*256+c)*256+d)

def query(db, keys, nbip):
    for k in keys:
        if k <= nbip:
            print db.get(k)
            break

if __name__ == "__main__":
    try:
        nbip = convert(sys.argv[1])
    except:
        print "use: query <ip>"
        sys.exit(0)

    db = cdb.init(dbname)
    keys = reversed(sorted(db.keys()))
    query(db, keys, nbip)
