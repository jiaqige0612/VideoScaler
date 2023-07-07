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

uint8_t S2o5[3] = {1, 3, 5};
uint8_t S2o4[3] = {0, 2, 4};
uint8_t S2o3[3] = {0, 1, 3};
uint8_t S2o2[3] = {0, 0, 2};
uint8_t S2o1[3] = {0, 0, 1};
uint8_t S2o0[3] = {0, 0, 0};



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

    int16_t interpX45 = (5*(*(val + xdim*(y+1 - *(B)) + (x+1 - *(R)))) - *(val + xdim*(y+3 - *(B +1)) + x+3 - *(R+1))); 

    int16_t interpX135 = (5*((*(val + xdim*(y+1 - *(B)) + (x-1 + *(L))))) - (*(val + xdim*(y+3 - *(B+1)) + x-3 + *(L+1)))); 

    int16_t interpX225 = (5*((*(val + xdim*(y-1 - *(B)) + (x-1 + *(L))))) - (*(val + xdim*(y-3 - *(B+1)) + x-3 + *(L+1)))); 

    int16_t interpX315 = (5*(*(val + xdim*(y-1 - *(B)) + (x+1 - *(R)))) - *(val + xdim*(y-3 - *(B +1)) + x+3 - *(R+1))); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA45 = (-(*(val + xdim*(y+5 - *(B+2)) + x+5 - *(R+2))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x+3 - *(R+1))))));

    int16_t interpA225 = (5*((*(val + xdim*(y-1 + *(A)) + (x-1 + *(L))))) - (*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1)))); 

    int16_t interpA135 = (-(*(val + xdim*(y+5 - *(B+2)) + x-3 + *(L+1))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x-1 + *(L))))));

    int16_t interpA315 =  (5*((*(val + xdim*(y-1 + *(A)) + (x+3 - *(B+1))))) - (*(val + xdim*(y-3 + *(A+1)) + x+5 - *(R+2)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB45 = (-(*(val + xdim*(y+3 - *(B+1)) + x+5 - *(R+2))) + 5*((*(val + xdim*(y+1 - *(B)) + (x+3 - *(R+1))))));

    int16_t interpB225 = (5*(((*(val + xdim*(y-3 + *(A+1)) + (x-1 + *(L))))) - (*(val + xdim*(y-5 + *(A+2)) + x-3 + *(L+1))))); 

    int16_t interpB135 = (-(*(val + xdim*(y+3 - *(B+1)) + x-3 + *(L+1))) + 5*((*(val + xdim*(y+1 - *(B)) + (x-1 + *(L))))));

    int16_t interpB315 = (5*((*(val + xdim*(y-3 + *(A+1)) + (x+3 - *(R+1))))) - (*(val + xdim*(y-5 + *(A+2)) + x+5 - *(R+2)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC45 = (-(*(val + xdim*(y+3 - *(B+1)) + x+3 - *(R+1))) + 5*((*(val + xdim*(y+1 - *(B)) + (x+1 - *(R))))));

    int16_t interpC225 = (5*((*(val + xdim*(y-3 + *(A+1)) + (x-3 + *(L+1))))) - (*(val + xdim*(y-5 + *(A+2)) + x-5 + *(L+2)))); 

    int16_t interpC135 = (-(*(val + xdim*(y+3 - *(B+1)) + x-5 + *(L+2))) + 5*((*(val + xdim*(y+1 - *(B)) + (x-3 + *(L+1))))));
    
    int16_t interpC315 = (5*((*(val + xdim*(y-3 + *(A+1)) + (x+1 - *(R))))) - (*(val + xdim*(y-5 + *(A+2)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD45 = (-(*(val + xdim*(y+5 - *(B+2)) + x+3 - *(R+1))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x+1 - *(R))))));

    int16_t interpD225 = (5*((*(val + xdim*(y-1 + *(A)) + (x-3 + *(L+1))))) - (*(val + xdim*(y-3 + *(A+1)) + x-5 + *(L+2)))); 

    int16_t interpD135 = (-(*(val + xdim*(y+5 - *(B+2)) + x-5 + *(L+2))) + 5*((*(val + xdim*(y+3 - *(B+1)) + (x-3 + *(L+1))))));

    int16_t interpD315 = (5*((*(val + xdim*(y-1 + *(A)) + (x+1 - *(R))))) - (*(val + xdim*(y-3 + *(A+1)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    uint16_t e45 = abs(interpA45-(*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))) + abs(interpB45 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC45 - (*(val + xdim*(y-1 + *(A)) + x-1 + *(B)))) + abs(interpD45 - (*(val + xdim*(y+1 - *(B)) + x-1 + *(L))));

    uint16_t e135 = abs(interpA135-(*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))) + abs(interpB135 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC135 - (*(val + xdim*(y-1 + *(A)) + x-1 + *(L)))) + abs(interpD135 - (*(val + xdim*(y+1 - *(B)) + x-1 + *(L))));

    uint16_t e225 = abs(interpA225-(*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))) + abs(interpB225 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC225 - (*(val + xdim*(y-1 + *(A)) + x-1 + *(L)))) + abs(interpD225 - (*(val + xdim*(y+1 - *(B)) + x-1 + *(L))));

    uint16_t e315 = abs(interpA315-(*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))) + abs(interpB315 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC315 - (*(val + xdim*(y-1 + *(A)) + x-1 + *(L)))) + abs(interpD315 - (*(val + xdim*(y+1 - *(B)) + x-1 + *(L))));


    if (interpX45 < 0) {interpX45 = 0;}
    if (interpX135 < 0) {interpX135 = 0;}
    if (interpX225 < 0) {interpX225 = 0;}
    if (interpX315 < 0) {interpX315 = 0;}

    double esf45 = e45;
    double esf135 = e135;
    double esf225 = e225;
    double esf315 = e315;

    /*calculation of "edge sensitive factor "*/

    double w45 = (esf135 + esf225 + esf315 + 0.001) / 3*(esf135 + esf225 + esf315 + esf45 + 0.004);
    double w135 = (esf135 + esf225 + esf315 + 0.001) / 3*(esf135 + esf225 + esf315 + esf45 + 0.004);
    double w225 = (esf135 + esf45 + esf315 + 0.001) / 3*(esf135 + esf225 + esf315 + esf45 + 0.004);
    double w315 = (esf135 + esf225 + esf45 + 0.001) / 3*(esf135 + esf225 + esf315 + esf45 + 0.004);

    *(val + y*(xdim) + x) = (uint8_t) round(w45*interpX45 + w135*interpX135 + w225*interpX225 + w315*interpX315);

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

    int16_t interpX180 = ((-*(val + xdim*(y) + x-3 + *(L+1))) + 5*(*(val + xdim*(y) + x-1 + *(L))));

    int16_t interpX0 = (5*(*(val + xdim*(y) + x+1 - *(R))) - (*(val + xdim*(y) + x+3 - *(R+1)))); 

    int16_t interpX270 = (-(*(val + xdim*(y-3 + *(A+1)) + x)) + 5*((*(val + xdim*(y-1 + *(A)) + (x)))));

    int16_t interpX90 = (5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA180 = (-(*(val + xdim*(y) + x-3 + *(L+1))) + 5*(*(val + xdim*(y) + x-1 + *(L))));

    int16_t interpA0 = (5*(*(val + xdim*(y) + (x+3 - *(R+1)))) - (*(val + xdim*(y) + x+5 - *(R+3)))); 

    int16_t interpA270 = (-(*(val + xdim*(y-3 + *(A+1)) + x+1 - *(R))) + 5*(*(val + xdim*(y-1 + *(A)) + x+1 - *(R))));

    int16_t interpA90 = (5*(*(val + xdim*(y+1 - *(B)) + x+1 - *(R))) - (*(val + xdim*(y+3 - *(B+1)) + x+1 - *(R)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB180 = (-(*(val + xdim*(y-1 + *(A)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))));

    int16_t interpB0 = (5*(*(val + xdim*(y-1 + *(A)) + (x+1 - *(R)))) - (*(val + xdim*(y-1 + *(A)) + x+3 - *(R+1)))); 

    int16_t interpB270 = (-(*(val + xdim*(y-5 + *(A+2)) + x)) + 5*(*(val + xdim*(y-3 + *(A+1)) + (x)))); 

    int16_t interpB90 = (5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC180 = (-(*(val + xdim*(y) + x-5 + *(L+2))) + 5*(*(val + xdim*(y) + x-3 + *(L+1))));

    int16_t interpC0 = (5*(*(val + xdim*(y) + x+1 - *(R))) - (*(val + xdim*(y) + x+3 - *(R+1)))); 

    int16_t interpC270 = (-(*(val + xdim*(y-3 + *(A+1)) + x-1 + *(L))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))));
    
    int16_t interpC90 = (5*(*(val + xdim*(y+1 - *(B)) + x-1 + *(L))) - (*(val + xdim*(y+3 - *(B+1)) + x-1 + *(L)))); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD180 = (-(*(val + xdim*(y+1 - *(B)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y+1 - *(B)) + x-1 + *(L))));
    
    int16_t interpD0 = (5*(*(val + xdim*(y+1 - *(B)) + x+1 - *(R))) - (*(val + xdim*(y+1 - *(B)) + x+3 - *(R+1)))); 

    int16_t interpD270 = (-(*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))));
    
    int16_t interpD90 = (5*(*(val + xdim*(y+3 - *(B+1)) + x+1 - *(R))) - (*(val + xdim*(y+5 - *(B+2)) + x+3 - *(R+1)))); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    int16_t e0 = abs(interpA0-(*(val + xdim*(y-*(R)+2*(*A)) + x+1 - *(R)))) + abs(interpB0 - (*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))) +\
    abs(interpC0 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))) + abs(interpD0 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L))));

    int16_t e90 = abs(interpA90-(*(val + xdim*(y-*(R) + 2*(*A)) + x+1 - *(R)))) + abs(interpB90 - (*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))) +\
    abs(interpC90 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))) + abs(interpD90 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L))));

    int16_t e180 = abs(interpA180-(*(val + xdim*(y-*(R) + 2*(*A)) + x+1 - *(R)))) + abs(interpB180 - (*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))) +\
    abs(interpC180 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))) + abs(interpD180 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L))));

    int16_t e270 = abs(interpA270-(*(val + xdim*(y-*(R) + 2*(*A)) + x+1 - *(R)))) + abs(interpB270 - (*(val + xdim*(y-1 + *(A))+ x - *(A) + 2*(*L)))) +\
    abs(interpC270 - (*(val + xdim*(y - *(L) + 2*(*A)) + x-1 + *(L)))) + abs(interpD270 - (*(val + xdim*(y+1 - *(B)) + x - *(B) + 2*(*L))));

    /*calculation of "edge sensitive factor "*/

    if (interpX0 < 0) {interpX0 = 0;}
    if (interpX90 < 0) {interpX90 = 0;}
    if (interpX180 < 0) {interpX180 = 0;}
    if (interpX270 < 0) {interpX270 = 0;}

    double esf0 = e0;
    double esf90 = e90;
    double esf270 = e270;
    double esf180 = e180;


    double w0 = (esf90 + esf180 + esf270 + 0.001) / 3*(esf0+esf90+esf180+esf270+0.004);
    double w90 = (esf0 + esf180 + esf270 + 0.001) / 3*(esf0+esf90+esf180+esf270+0.004);
    double w180 = (esf90 + esf0 + esf270 + 0.001) / 3*(esf0+esf90+esf180+esf270+0.004);
    double w270 = (esf90 + esf180 + esf0 + 0.001) / 3*(esf0+esf90+esf180+esf270+0.004);

    *(val + xdim*(y) + x) = (uint8_t) round(w0*interpX0 + w90*interpX90 + w180*interpX180 + w270*interpX270);

}


void alg(uint8_t * val, uint8_t * arr, uint16_t yDim, uint16_t xDim){

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










