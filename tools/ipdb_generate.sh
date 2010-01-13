#!/bin/bash
wget http://ipinfodb.com/mirror/ip_database/current/ipinfodb_one_table_full_country.csv.zip
wget http://geolite.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip
unzip ipinfodb_one_table_full_country.csv.zip
unzip GeoIPASNum2.zip
python ipdb_make.py
rm -f ipinfodb_one_table_full_country.csv.zip ip_group_country.csv GeoIPASNum2.zip GeoIPASNum2.csv
