#!/usr/bin/env python
# coding: utf-8

import os, sys, csv, sqlite3

dbname = 'ipdb.sqlite'
chunks = 100000

def insert(conn, curs, data):
    curs.executemany('INSERT INTO ip_group_country VALUES (?, ?)', data)
    conn.commit()

if __name__ == '__main__':
    if os.path.exists(dbname):
        os.unlink(dbname)

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("""
	CREATE TABLE ip_group_country (
	    ip_start	    INTEGER PRIMARY KEY,
	    country_code    CHAR(2) );
	""")

    count = 0
    entities = []

    fd = open('ip_group_country.csv')
    fd.readline()

    for row in csv.reader(fd, delimiter=';', quotechar='"'):
        fields = [row[0], row[2]]
        entities.append(fields)

        if count == chunks:
            insert(conn, curs, entities)
            entities = []
            count = 0
        else:
            count += 1
    
    if entities:
        insert(conn, curs, entities)
    conn.close()
