#!/usr/bin/python

import sys
import shutil
import random
import os
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Random copy files')
    parser.add_argument('src_dirs',type=str,help="Source dir",
                        nargs='+')
    parser.add_argument('dst_dir',type=str,help="Source dir",
                        metavar='<dst_dir>')
    parser.add_argument('--number','-n',type=int,help="number of files to copy",
                        required=False,default=15)
    parser.add_argument('--recursive','-R',help="recursive",action='store_const',
                        const=True,required=False,default=False)
    parser.add_argument('--preserve-path','-p',help="Preserve sub-path",action='store_const',
                        const=True,required=False,default=False)

    
    args=parser.parse_args(sys.argv[1:])
    
    src_list=[]
    
    for src_dir in args.src_dirs:
        if args.recursive:
            
        
            for root, dirs, files in os.walk(src_dir, topdown=False):
                for filename in files:
                    src_list.append((root,filename,root[len(src_dir)+1:],src_dir))
        else:
            for filename in os.listdir(src_dir):
                if os.path.isfile(os.path.join(src_dir,filename)):
                    src_list.append((src_dir,filename,'.',src_dir))
    
    i=0
    if len(src_list)< args.number:
        n=len(src_list)
    else:
        n=args.number
    while i<n:
        fn=random.randint(0,len(src_list)-1)
        full_dir=src_list[fn][0]
        filename=src_list[fn][1]
        sub_dir=src_list[fn][2]
        src_dir=src_list[fn][3]
        src_filename=os.path.join(full_dir,filename)
        if args.preserve_path:
            dst_filename=os.path.join(args.dst_dir,sub_dir,filename)
        else:
            dst_filename=os.path.join(args.dst_dir,filename)
        del src_list[fn]
        print "Copy ",src_filename," to ", dst_filename
        try:
            os.makedirs(os.path.join(args.dst_dir,sub_dir))
        except OSError:
            pass
        shutil.copyfile(src_filename,dst_filename)
        i=i+1    
        

if __name__ == '__main__':
    main(sys.argv[1:])