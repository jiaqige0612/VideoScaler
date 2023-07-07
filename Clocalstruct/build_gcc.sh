#!/bin/bash

gcc -Wall -O3 -c -fpic src/localStructV1.c -o src/localStructV1.o 2> log/V1.txt 
gcc -shared -o lib/localStructV1.so src/localStructV1.o 2> log/V1lib.txt
rm src/localStructV1.o

gcc -Wall -O3 -c -fpic src/localStructV2.c -o src/localStructV2.o 2> log/V2.txt 
gcc -shared -o lib/localStructV2.so src/localStructV2.o 2> log/V2lib.txt
rm src/localStructV2.o

gcc -Wall -O3 -c -fpic src/localStructV3.c -o src/localStructV3.o 2> log/V3.txt 
gcc -shared -o lib/localStructV3.so src/localStructV3.o 2> log/V3lib.txt
rm src/localStructV3.o