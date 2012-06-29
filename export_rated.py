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
import argparse

def getAmarokDBInfo():
    amarokrc=ConfigParser.ConfigParser()
    amarokrc.read(os.path.expanduser('~/.kde/share/config/amarokrc'))
    return {'db_name':amarokrc.get('MySQL','Database'),
            'host_name':amarokrc.get('MySQL','Host'),
            'password':amarokrc.get('MySQL','Password'),
            'user':amarokrc.get('MySQL','User'),
            'use_server':amarokrc.get('MySQL','UseServer')} 
    
## generator for results
def dbCopyFiles(dst_dir,rating=5):
    adb=getAmarokDBInfo()
    db=MySQLdb.connect(host=adb['host_name'],user=adb['user'],passwd=adb['password'],db=adb['db_name'])
    c=db.cursor()
    c.execute("""SELECT t.title, s.rating, CONCAT(d.lastmountpoint,SUBSTR(u.rpath,2)), u.uniqueid
                FROM  `statistics` AS s, tracks AS t, urls AS u, devices as d 
                WHERE s.rating > ?
                AND s.url = t.url
                AND u.deviceid = d.id
                AND s.url=u.id""",rating)
    while (1):
        row = c.fetchone ()
        if row == None:
            break
        filename=row[2]
        uuid=row[3][21:]
        print "Exporting %s" % (filename)
        try:
            shutil.copyfile(unicode(filename,'utf-8'),export_dir+uuid+'.mp3')
        except IOError:
            print "ERROR, can't operate on ",filename

def csvCopyFiles(src_dir,dst_dir,csv_filename):
    list_reader=csv.reader(open(csv_filename,'r'),delimiter=';',quotechar='"')
    for row in list_reader:
        title=row[0]
        rating=row[1]
        filename=row[2]
        uuid=row[3][21:]
        print "Exporting ",title," ",filename," ",uuid
        try:
            shutil.copyfile(os.path.join(src_dir,unicode(filename,'utf-8')),os.path.join(dst_dir,uuid+'.mp3'))
        except IOError:
            print "ERROR, can't operate on ",filename

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Amarok MP3 export util')
    parser.add_argument('export_dir',type=str,help="export dir",
                        metavar='<export_dir>', default=None)
    parser.add_argument('--rating',type=int,help="rating",
                        required=False,default=5)
    
    args=parser.parse_args(sys.argv)
    dst_dir=args.export_dir
    rating=args.rating
    dbCopyFiles(dst_dir,rating)
    
    return

    ### if len(sys.argv)<4:
       ### print "Usage: ", sys.argv[0], "<csv_file> <base_dir> <output_dir>"
    ### export_filename=sys.argv[1]
    ### base_dir=sys.argv[2]
    ### export_dir=sys.argv[3]
    ### csvCopyFiles(base_dir,export_dir,export_filename)

