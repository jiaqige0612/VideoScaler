#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

//using namespace std;

#define STAGE_2_ACTIVE 1
#define INLINE 0
#define STAGE_ONE 1



/*arrays containing overflow correction coefficients*/
uint8_t S1o3[3] = {1, 2, 3};
uint8_t S1o2[3] = {0, 1, 2};
uint8_t S1o1[3] = {0, 0, 1};
uint8_t S1o0[3] = {0, 0, 0};

uint8_t S2o5[5] = {1, 3, 5, 2, 4};
uint8_t S2o4[5] = {0, 2, 4, 1, 3};
uint8_t S2o3[5] = {0, 1, 3, 0, 2};
uint8_t S2o2[5] = {0, 0, 2, 0, 1};
uint8_t S2o1[5] = {0, 0, 1, 0, 0};
uint8_t S2o0[5] = {0, 0, 0, 0, 0};



void stage1(uint8_t * val, uint16_t x, uint16_t y, uint16_t xdim, uint16_t ydim){


    /*pointers to access overvlow correction coefficiecnt arrays*/
    uint8_t * L;
    uint8_t * R;
    uint8_t * A;
    uint8_t * B;


    /*correction coefficient selector*/
        switch(xdim - x){
        case 0:    R = &S2o5[0];     break;
        case 1:    R = &S2o4[0];     break;
        case 2:    R = &S2o3[0];     break;
        case 3:    R = &S2o2[0];     break;
        case 4:    R = &S2o1[0];     break;
        default:   R = &S2o0[0];     break;
    }
    switch(x){
        case 0:    L = &S2o5[0];     break;
        case 1:    L = &S2o4[0];     break;
        case 2:    L = &S2o3[0];     break;
        case 3:    L = &S2o2[0];     break;
        case 4:    L = &S2o1[0];     break;
        default:   L = &S2o0[0];     break;
    }
    switch(ydim - y){
        case 0:    B = &S2o5[0];     break;
        case 1:    B = &S2o4[0];     break;
        case 2:    B = &S2o3[0];     break;
        case 3:    B = &S2o2[0];     break;
        case 4:    B = &S2o1[0];     break;
        default:   B = &S2o0[0];     break;
    }
    switch(y){
        case 0:    A = &S2o5[0];     break;
        case 1:    A = &S2o4[0];     break;
        case 2:    A = &S2o3[0];     break;
        case 3:    A = &S2o2[0];     break;
        case 4:    A = &S2o1[0];     break;
        default:   A = &S2o0[0];     break;
    }


    /*initial arbitrary interpolation of the missing HR pixel along both diagonals*/

    int16_t interpX45 = ((-(*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + (x-1 + *(L)))) + \
    5*(*(val + xdim*(y+1 - *(B)) + (x+1 - *(R)))) - *(val + xdim*(y+3 - *(B +1)) + x+3 - *(R+1)))); 


    int16_t interpX135 = (-(*(val + xdim*(y-3 + *(A+1)) + x+3 - *(R+1))) + 5*((*(val + xdim*(y-1 + *(A)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x-1 + *(L))))) - (*(val + xdim*(y+3 - *(B+1)) + x-3 + *(L+1)))); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA45 = (-(*(val + xdim*(y+5 - *(B+2)) + x+5 - *(R+2))) + 5*((*(val + xdim*(y+3 - *(B+1)) + \
    (x+3 - *(R+1))))) + 5*((*(val + xdim*(y-1 + *(A)) + (x-1 + *(L))))) - (*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1)))); 

    int16_t interpA135 = (-(*(val + xdim*(y+5 - *(B+2)) + x-3 + *(L+1))) + 5*((*(val + xdim*(y+3 - *(B+1)) + \
    (x-1 + *(L))))) + 5*((*(val + xdim*(y-1 + *(A)) + (x+3 - *(B+1))))) - (*(val + xdim*(y-3 + *(A+1)) + x+5 - *(R+2)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB45 = (-(*(val + xdim*(y+3 - *(B+1)) + x+5 - *(R+2))) + 5*((*(val + xdim*(y+1 - *(B)) + (x+3 - *(R+1))))) + \
    5*((*(val + xdim*(y-3 + *(A+1)) + (x-1 + *(L))))) - (*(val + xdim*(y-5 + *(A+2)) + x-3 + *(L+1)))); 

    int16_t interpB135 = (-(*(val + xdim*(y+3 - *(B+1)) + x-3 + *(L+1))) + 5*((*(val + xdim*(y+1 - *(B)) + (x-1 + *(L))))) + \
    5*((*(val + xdim*(y-3 + *(A+1)) + (x+3 - *(R+1))))) - (*(val + xdim*(y-5 + *(A+2)) + x+5 - *(R+2)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC45 = (-(*(val + xdim*(y+3 - *(B+1)) + x+3 - *(R+1))) + 5*((*(val + xdim*(y+1 - *(B)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y-3 + *(A+1)) + (x-3 + *(L+1))))) - (*(val + xdim*(y-5 + *(A+2)) + x-5 + *(L+2)))); 

    int16_t interpC135 = (-(*(val + xdim*(y+3 - *(B+1)) + x-5 + *(L+2))) + 5*((*(val + xdim*(y+1 - *(B)) + (x-3 + *(L+1))))) + \
    5*((*(val + xdim*(y-3 + *(A+1)) + (x+1 - *(R))))) - (*(val + xdim*(y-5 + *(A+2)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD45 = (-(*(val + xdim*(y+5 - *(B+2)) + x+3 - *(R+1))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y-1 + *(A)) + (x-3 + *(L+1))))) - (*(val + xdim*(y-3 + *(A+1)) + x-5 + *(L+2)))); 

    int16_t interpD135 = (-(*(val + xdim*(y+5 - *(B+2)) + x-5 + *(L+2))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x-3 + *(L+1))))) + \
    5*((*(val + xdim*(y-1 + *(A)) + (x+1 - *(R))))) - (*(val + xdim*(y-3 + *(A+1)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    uint16_t e45 = abs(interpA45-((*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))<<3)) + abs(interpB45 - ((*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))<<3)) +\
    abs(interpC45 - ((*(val + xdim*(y-1 + *(A)) + x-1 + *(B)))<<3)) + abs(interpD45 - ((*(val + xdim*(y+1 - *(B)) + x-1 + *(L)))<<3));

    uint16_t e135 = abs(interpA135-((*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))<<3)) + abs(interpB135 - ((*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))<<3)) +\
    abs(interpC135 - ((*(val + xdim*(y-1 + *(A)) + x-1 + *(L)))<<3)) + abs(interpD135 - ((*(val + xdim*(y+1 - *(B)) + x-1 + *(L)))<<3));

    if (interpX45 < 0) {interpX45 = 0;}
    if (interpX135 < 0) {interpX135 = 0;}

    /*calculation of "edge sensitive factor "*/

    if(e135 == 0 && e45 == 0){
        e135 = 1;
        e45 = 1;
    }

    double esf45 = pow(e45, 3);
    double esf135 = pow(e135, 3);

    double w45 = (esf135) / (esf135+esf45);
    double w135 = 1 - w45;

    double res = (w45*interpX45 + w135*interpX135)/8;

    *(val + y*(xdim) + x) = (uint8_t) round(res);



    

}



void stage2(uint8_t * val, uint16_t x, uint16_t y, uint16_t xdim, uint16_t ydim){


    /*pointers to access overvlow correction coefficiecnt arrays*/
    uint8_t * L;
    uint8_t * R;
    uint8_t * A;
    uint8_t * B;


    /*correction coefficient selector*/
    switch(xdim - x){
        case 0:    R = &S2o5[0];     break;
        case 1:    R = &S2o4[0];     break;
        case 2:    R = &S2o3[0];     break;
        case 3:    R = &S2o2[0];     break;
        case 4:    R = &S2o1[0];     break;
        default:   R = &S2o0[0];     break;
    }
    switch(x){
        case 0:    L = &S2o5[0];     break;
        case 1:    L = &S2o4[0];     break;
        case 2:    L = &S2o3[0];     break;
        case 3:    L = &S2o2[0];     break;
        case 4:    L = &S2o1[0];     break;
        default:   L = &S2o0[0];     break;
    }
    switch(ydim - y){
        case 0:    B = &S2o5[0];     break;
        case 1:    B = &S2o4[0];     break;
        case 2:    B = &S2o3[0];     break;
        case 3:    B = &S2o2[0];     break;
        case 4:    B = &S2o1[0];     break;
        default:   B = &S2o0[0];     break;
    }
    switch(y){
        case 0:    A = &S2o5[0];     break;
        case 1:    A = &S2o4[0];     break;
        case 2:    A = &S2o3[0];     break;
        case 3:    A = &S2o2[0];     break;
        case 4:    A = &S2o1[0];     break;
        default:   A = &S2o0[0];     break;
    }


    /*initial arbitrary interpolation of the missing HR pixel along both diagonals*/

    int16_t interpX0 = ((-*(val + xdim*(y) + x-3 + *(L+1))) + 5*(*(val + xdim*(y) + x-1 + *(L))) + \
    5*(*(val + xdim*(y) + x+1 - *(R))) - (*(val + xdim*(y) + x+3 - *(R+1)))); 


    int16_t interpX90 = (-(*(val + xdim*(y-3 + *(A+1)) + x)) + 5*((*(val + xdim*(y-1 + *(A)) + (x)))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA0 = (-(*(val + xdim*(y) + x-3 + *(L+1))) + 5*(*(val + xdim*(y) + x-1 + *(L))) +\
    5*(*(val + xdim*(y) + (x+3 - *(R+1)))) - (*(val + xdim*(y) + x+5 - *(R+3)))); 

    int16_t interpA90 = (-(*(val + xdim*(y-4 + *(A+4)) + x+1 - *(R))) + 5*(*(val + xdim*(y-2 + *(A+3)) + x+1 - *(R))) +\
    5*(*(val + xdim*(y+2 - *(B+3)) + x+1 - *(R))) - (*(val + xdim*(y+4 - *(B+4)) + x+1 - *(R)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB0 = (-(*(val + xdim*(y-1 + *(A)) + x-4 + *(L+4))) + 5*(*(val + xdim*(y-1 + *(A)) + x-2 + *(L+3))) + \
    5*(*(val + xdim*(y-1 + *(A)) + (x+2 - *(R+3)))) - (*(val + xdim*(y-1 + *(A)) + x+4 - *(R+4)))); 

    int16_t interpB90 = (-(*(val + xdim*(y-5 + *(A+2)) + x)) + 5*(*(val + xdim*(y-3 + *(A+1)) + (x))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC0 = (-(*(val + xdim*(y) + x-5 + *(L+2))) + 5*(*(val + xdim*(y) + x-3 + *(L+1))) + \
    5*(*(val + xdim*(y) + x+1 - *(R))) - (*(val + xdim*(y) + x+3 - *(R+1)))); 

    int16_t interpC90 = (-(*(val + xdim*(y-4 + *(A+4)) + x-1 + *(L))) + 5*(*(val + xdim*(y-2 + *(A+3)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y+2 - *(B+3)) + x-1 + *(L))) - (*(val + xdim*(y+4 - *(B+4)) + x-1 + *(L)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD0 = (-(*(val + xdim*(y+1 - *(B)) + x-4 + *(L+4))) + 5*(*(val + xdim*(y+1 - *(B)) + x-2 + *(L+3))) + \
    5*(*(val + xdim*(y+1 - *(B)) + x+2 - *(R+3))) - (*(val + xdim*(y+1 - *(B)) + x+4 - *(R+4)))); 

    int16_t interpD90 = (-(*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y+3 - *(B+1)) + x+1 - *(R))) - (*(val + xdim*(y+5 - *(B+2)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    uint16_t e0 = abs(interpA0-((*(val + xdim*(y-*(R)+2*(*A)) + x+1 - *(R)))<<3)) + abs(interpB0 - ((*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))<<3)) +\
    abs(interpC0 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))<<3) + abs(interpD0 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L)))<<3);

    uint16_t e90 = abs(interpA90-(*(val + xdim*(y-*(R) + 2*(*A)) + x+1 - *(R)))<<3) + abs(interpB90 - ((*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))<<3)) +\
    abs(interpC90 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))<<3) + abs(interpD90 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L)))<<3);


    /*calculation of "edge sensitive factor "*/

    if (interpX0 < 0) {interpX0 = 0;}
    if (interpX90 < 0) {interpX90 = 0;}

    if(e90 == 0 && e0 == 0){
        e90 = 1;
        e0 = 1;
    }

    double esf0 = pow(e0, 3);
    double esf90 = pow(e90, 3);

    double w0 = (esf90) / (esf90+esf0);
    double w90 = 1 - w0;

    double res = (w0*interpX0 + w90*interpX90)/8;

    *(val + xdim*(y) + x) = (uint8_t) (round(res));

}

extern "C"

__declspec(dllexport) void alg(uint8_t * val, uint8_t * arr, uint16_t yDim, uint16_t xDim){

    uint32_t valLoc = 0;

    
    for(uint16_t i = 0; i<(2*yDim); i+=2){
        for(uint16_t j = 0; j<(2*xDim); j+=2){
            *(arr+(i*xDim*2 + j)) = *(val+valLoc);
            valLoc++;
        }
    }    


    #if STAGE_ONE

    for(uint16_t i = 0; i<(2*yDim); i++){
        for(uint16_t j = 0; j<(2*xDim);j++){
                
            if((i%2 == 1) && (j%2 == 1)){
                stage1(arr, j, i, xDim*2, yDim*2);
            }
        }
    }

    #endif

    

    #if STAGE_2_ACTIVE

    uint8_t inc = 0;

    for(uint16_t i = 0; i<(2*yDim); i++){

        if(i%2 == 0){
            inc = 1;
        }else{inc = 0;}

        for(uint16_t j = inc; j<(2*xDim);j++){
            
            
            
            if(((j%2) == 1 && inc == 1) || ((j%2) == 0 && inc == 0)){

            stage2(arr, j, i, 2*xDim, 2*yDim);



            }

        }


    }
    #endif

    



}


void freeme(uint8_t* ptr){
    free(ptr);
}










