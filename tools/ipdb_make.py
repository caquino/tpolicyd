#!/usr/bin/env python
# coding: utf-8

import os, sys, csv, sqlite3

dbname = 'ipdb.sqlite'
chunks = 100000

def insertgeoip(conn, curs, data):
    curs.executemany('INSERT INTO ip_group_country VALUES (?, ?)', data)
    conn.commit()

def insertasn(conn, curs, data):
    curs.executemany('INSERT INTO ip_group_asn VALUES (?, ?, ?)', data)
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

    curs.execute("""
	CREATE TABLE ip_group_asn (
	    ip_start	    INTEGER,
		ip_end			INTEGER,
		asn				INTEGER,
		PRIMARY KEY (ip_start, ip_end));
	""")

    count = 0
    entities = []

    fd = open('ip_group_country.csv')
    fd.readline()

    for row in csv.reader(fd, delimiter=';', quotechar='"'):
        fields = [row[0], row[2]]
        entities.append(fields)

        if count == chunks:
            insertgeoip(conn, curs, entities)
            entities = []
            count = 0
        else:
            count += 1
    
    if entities:
        insertgeoip(conn, curs, entities)

    fd.close()
    count = 0
    entities = []

    fd = open('GeoIPASNum2.csv')
    fd.readline()

    for row in csv.reader(fd, delimiter=',', quotechar='"'):
          asn = row[2].lstrip().lstrip('"').split(' ')[0][2:]
          fields = [row[0], row[1], asn]
          entities.append(fields)

          if count == chunks:
              insertasn(conn, curs, entities)
              entities = []
              count = 0
          else:
              count += 1
    
    if entities:
        insertasn(conn, curs, entities)

    conn.close()
