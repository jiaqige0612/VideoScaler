
clang++ -c -o src/localStructV1.o src/localStructV1.cpp
clang++ -shared -v -o lib/localStructV1.dll src/localStructV1.so
rm src/localStructV1.o

clang -c -o src/localStructV2.o src/localStructV2.c
clang -shared -v -o lib/localStructV2.dll src/localStructV2.so
rm src/localStructV2.o

clang -c -o src/localStructV3.o src/localStructV3.cpp
clang -shared -v -o lib/localStructV3.dll src/localStructV3.so
rm src/localStructV3.o