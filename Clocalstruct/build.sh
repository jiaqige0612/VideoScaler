#!/bin/bash

gcc -c -fpic c_side.c 2> error.txt > "c_side.o"
gcc -shared -o lib.so c_side.o > "lib.so"