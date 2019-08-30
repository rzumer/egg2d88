#!/bin/bash

[ "$#" -ge 1 ] || {
    echo "An input file is required." 1>&2;
    exit -1;
}

rm -r img/*;

quickbms -F "*.exe" -o project_egg.bms $1 img;

idx=0
ret=0

while [ $ret -eq 0 ]
    do
        python egg2d88.py img/EGGFDIMG$idx ${1%.*}-$idx.d88;
        ret=$?;
        ((idx++));
    done

echo "Done.";

