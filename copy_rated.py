#!/usr/bin/python

# [MySQL]
# Database=DDDDDDD
# Host=1.1.1.1
# Password=XXXXXXX
# UseServer=true
# User=amarok

import sys
import csv
import shutil
import ConfigParser
import os
import MySQLdb

def getAmarokDBInfo():
    amarokrc=ConfigParser.ConfigParser()
    amarokrc.read(os.path.expanduser('~/.kde/share/config/amarokrc'))
    return {'db_name':amarokrc.get('MySQL','Database'),
            'host_name':amarokrc.get('MySQL','Host'),
            'password':amarokrc.get('MySQL','Password'),
            'user':amarokrc.get('MySQL','User'),
            'use_server':amarokrc.get('MySQL','UseServer')} 
    
## generator for results
def fetchData():
    adb=getAmarokDBInfo()
    db=MySQLdb.connect(host=adb['host_name'],user=adb['user'],passwd=adb['password'],db=adb['db_name'])
    c=db.cursor()
    c.execute("""SELECT t.title, s.rating, CONCAT(d.lastmountpoint,SUBSTR(u.rpath,2)), u.uniqueid
                FROM  `statistics` AS s, tracks AS t, urls AS u, devices as d 
                WHERE s.rating > 5
                AND s.url = t.url
                AND u.deviceid = d.id
                AND s.url=u.id""")
    while (1):
        row = c.fetchone ()
        if row == None:
            break
        print "%s, %s" % (row[0], row[1])
        try:
            shutil.copyfile(base_dir+unicode(filename,'utf-8'),export_dir+uuid+'.mp3')
        except IOError:
            print "ERROR, can't operate on ",filename


if __name__ == '__main__':
    if len(sys.argv)<4:
        print "Usage: ", sys.argv[0], "<csv_file> <base_dir> <output_dir>"
    export_filename=sys.argv[1]
    base_dir=sys.argv[2]
    export_dir=sys.argv[3]
    list_reader=csv.reader(open(export_filename,'r'),delimiter=';',quotechar='"')
    for row in list_reader:
        title=row[0]
        rating=row[1]
        filename=row[2]
        uuid=row[3][21:]
        print "Exporting ",title," ",filename," ",uuid
        try:
            shutil.copyfile(base_dir+unicode(filename,'utf-8'),export_dir+uuid+'.mp3')
        except IOError:
            print "ERROR, can't operate on ",filename

