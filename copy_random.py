#!/usr/bin/python

import sys
import shutil
import random
import os
import argparse
import hashlib

class RandomCopy:

    _recursive=False
    _preserve_path=False
    _all=False
    _md5_rename=False
    _md5_suffix=None

    def __init__(self):
        pass
    
    def set_recursive(self,recursive):
        self._recursive=recursive
        
    def set_preserve_path(self,preserve_path):
        self._preserve_path=preserve_path
        
    def set_all(self,all):
        self._all=all
        
    def set_md5_rename(self,md5_rename):
        self._md5_rename=md5_rename
        
    def set_md5_suffix(self,md5_suffix):
        self._md5_suffix=md5_suffix
        
    def copy(self,src_dirs, dst_dir,number):
        src_list=[]
        
        for src_dir in src_dirs:
            if self._recursive:
                for root, dirs, files in os.walk(src_dir, topdown=False):
                    for filename in files:
                        src_list.append((root,filename,root[len(src_dir)+1:],src_dir))
            else:
                for filename in os.listdir(src_dir):
                    if os.path.isfile(os.path.join(src_dir,filename)):
                        src_list.append((src_dir,filename,'.',src_dir))
        
        i=0
        if len(src_list)< number:
            n=len(src_list)
        else:
            n=number
            
        if self._all:
            n=len(src_list)
        while i<n:
            fn=random.randint(0,len(src_list)-1)
            full_dir=src_list[fn][0]
            filename=src_list[fn][1]
            sub_dir=src_list[fn][2]
            src_dir=src_list[fn][3]
            src_filename=os.path.join(full_dir,filename)
    
            if self._md5_rename:
                m = hashlib.md5()
                m.update(filename)
                filename=m.hexdigest()
                if self._md5_suffix:
                    filename=filename+self._md5_suffix
            if self._preserve_path:
                dst_filename=os.path.join(dst_dir,sub_dir,filename)
            else:
                dst_filename=os.path.join(dst_dir,filename)
            del src_list[fn]
            print "Copy ",src_filename," to ", dst_filename
            try:
                if self._preserve_path:
                    os.makedirs(os.path.join(dst_dir,sub_dir))
            except OSError:
                pass
            shutil.copyfile(src_filename,dst_filename)
            i=i+1    
    

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
    parser.add_argument('--all','-a',help="copy all",action='store_const',
                        const=True,required=False,default=False)
    parser.add_argument('--md5-rename','-5',help="rename-to-md5",action='store_const',
                        const=True,required=False,default=False)
    parser.add_argument('--md5-suffix','-s',type=str,help="MD5 renam suffix",
                        required=False)

    
    args=parser.parse_args(sys.argv[1:])
    
    rc=RandomCopy()
    
    rc.set_recursive(args.recursive)
    rc.set_preserve_path(args.preserve_path)
    rc.set_all(args.all)
    rc.set_md5_rename(args.md5_rename)
    rc.set_md5_suffix(args.md5_suffix)
    
    rc.copy(args.src_dirs,args.dst_dir,args.number)
    

if __name__ == '__main__':
    main(sys.argv[1:])