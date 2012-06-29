#!/usr/bin/python

import sys
import shutil
import random
import os
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Random copy files')
    parser.add_argument('src_dir',type=str,help="Source dir",
                        metavar='<src_dir>')
    parser.add_argument('dst_dir',type=str,help="Source dir",
                        metavar='<dst_dir>')
    parser.add_argument('--number','-n',type=int,help="rating",
                        required=False,default=15)
    
    args=parser.parse_args(sys.argv[1:])

    src_list=os.listdir(args.src_dir)
    i=0
    while i<args.number:
        fn=random.randint(0,len(src_list)-1)
        filename=src_list[fn]
        src_filename=os.path.join(args.src_dir,filename)
        dst_filename=os.path.join(args.dst_dir,filename)
        del src_list[fn]
        print "Copy ",src_filename," to ", dst_filename
        shutil.copyfile(src_filename,dst_filename)
        i=i+1    
        

if __name__ == '__main__':
    main(sys.argv[1:])