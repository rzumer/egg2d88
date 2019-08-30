#!/bin/bash

[ "$#" -ge 1 ] || {
    echo "An input file is required." 1>&2;
    exit -1;
}

rm -r img/*;

set -e
quickbms -F "*.exe" -o project_egg.bms $1 img;

idx=0
error=0

while [ $? -eq 0 ]
    do
        python egg2d88.py img/EGGFDIMG$idx ${1%.*}-$idx.d88
        ((idx++))
    done

echo "Done.";

