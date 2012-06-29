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

base_dir='/mnt/dump/'

if __name__ == '__main__':
    if len(sys.argv)<3:
        print "Usage: ", sys.argv[0], "<csv_file> <output_dir>"
    export_filename=sys.argv[1]
    export_dir=sys.argv[2]
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

