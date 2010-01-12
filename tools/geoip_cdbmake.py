#!/usr/bin/env python
# coding: utf-8

import cdb
import os, sys, csv

dbname = 'ipdb.cdb'

if __name__ == '__main__':
    if os.path.exists(dbname):
        os.unlink(dbname)

    db = cdb.cdbmake(dbname, "zz.tmp")
    fd = open('ip_group_country.csv')
    fd.readline()

    for row in csv.reader(fd, delimiter=';', quotechar='"'):
        db.add(row[0], row[2])

    db.finish()
    fd.close()
