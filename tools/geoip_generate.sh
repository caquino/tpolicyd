#!/bin/bash

wget http://ipinfodb.com/mirror/ip_database/current/ipinfodb_one_table_full_country.csv.zip
unzip ipinfodb_one_table_full_country.csv.zip
python geoip_make.py
rm -f ipinfodb_one_table_full_country.csv.zip ip_group_country.csv
