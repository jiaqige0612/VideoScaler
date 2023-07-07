Implementation of Local Structure Estimation method in C!!!
(took me ages but gassed)

This implementation uses the Ctypes library to interface with C functions through python
If anyone wants to use it you can pretty much do it in the same way, it just becomes extremely
tedious with memory accesses

This version is not yet complete as i have to add stage 2 and add all three channels of RGB
I may however only use the Y channel in YCbCr space. I will have this implementation fully working by the end of tomorrow 

In order to use it run the build.sh file which compiles the C implementation and creates a joint library (lib.so)


error.txt gives compiler errors when compiling c_side.c