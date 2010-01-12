#!/bin/sh
wget http://archive.routeviews.org/oix-route-views/$(date +"%Y.%m")/oix-full-snapshot-latest.dat.bz2
bzcat oix-full-snapshot-latest.dat.bz2 | ./bgp_dump.awk | sort -u > asn.csv
rm oix-full-snapshot-latest.dat.bz2
