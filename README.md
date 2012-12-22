Amarok export scripts
=====================

Preamble
--------

Amarok scripts

I use those scripts to extract tracks from Amarok DB. Ever since Amarok 2.x launch extracting number of 
songs to external media became a hassle, so I had to "compensate". To successfully use USB stick in a vehicle
entertainment system it's best to store all mp3's in a single directory. However track names may collide, thus
we're renaming them to their md5 checksums to avoid collisions. 

Typical usecase::

  ## export everything with rating higher than 3.5 stars:
  $ python export_rated.py --rating=7 /media/MyDevice
  ## add some random songs from my collection for a good measure:
  $ python copy_random.py -R5 -s .mp3 -n 50 /mnt/music/MyCollection /media/MyDevice

As a result - /media/MyDevice will contain a number of .mp3's within root directory of the form::

  aaeca6fdeecd1425a0aadeb1ad81b5a0.mp3

Now vehicle entertainment system can quickly scan the device and have no issues with file names.

copy_random.py
--------------

usage: copy_random.py [-h] [--number NUMBER] [--recursive] [--preserve-path]
                      [--all] [--md5-rename] [--md5-suffix MD5_SUFFIX]
                      src_dirs [src_dirs ...] <dst_dir>

Random copy files

positional arguments:
  src_dirs              Source dir
  <dst_dir>             Source dir

optional arguments:
  -h, --help            show this help message and exit
  --number NUMBER, -n NUMBER
                        number of files to copy
  --recursive, -R       recursive
  --preserve-path, -p   Preserve sub-path
  --all, -a             copy all
  --md5-rename, -5      rename-to-md5
  --md5-suffix MD5_SUFFIX, -s MD5_SUFFIX
                        MD5 renam suffix

export_rated.py
---------------


usage: export_rated.py [-h] [--rating RATING] <export_dir>

Amarok MP3 export util

positional arguments:
  <export_dir>     export dir

optional arguments:
  -h, --help       show this help message and exit
  --rating RATING  rating


