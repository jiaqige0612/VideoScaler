#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

//uint8_t oA1, oA2, oA3, oB1, oB2, oB3, *(L), *(L+1), oL3, oR1, oR2, oR3


uint8_t o3[3] = {1, 2, 3};
uint8_t o2[3] = {0, 1, 2};
uint8_t o1[3] = {0, 0, 1};
uint8_t o0[3] = {0, 0, 0};

/*
uint8_t o3[3] = {0, 0, 0};
uint8_t o2[3] = {0, 0, 0};
uint8_t o1[3] = {0, 0, 0};
uint8_t o0[3] = {0, 0, 0};
*/

uint8_t * L;
uint8_t * R;
uint8_t * A;
uint8_t * B;








uint8_t stage1(uint8_t * val, uint16_t x, uint16_t y, uint16_t xdim, uint16_t ydim){



    switch(xdim - x){
        case 0:    R = &o3[0];     break;
        case 1:    R = &o2[0];     break;
        case 2:    R = &o1[0];     break;
        default:   R = &o0[0];     break;
    }
        switch(x){
        case 0:    L = &o3[0];     break;
        case 1:    L = &o2[0];     break;
        case 2:    L = &o1[0];     break;
        default:   L = &o0[0];     break;
    }
        switch(ydim - y){
        case 0:    B = &o3[0];     break;
        case 1:    B = &o2[0];     break;
        case 2:    B = &o1[0];     break;
        default:   B = &o0[0];     break;
    }
        switch(y){
        case 0:    A = &o3[0];     break;
        case 1:    A = &o2[0];     break;
        case 2:    A = &o1[0];     break;
        default:   A = &o0[0];     break;
    }







    /*initial arbitrary interpolation of the missing HR pixel along both diagonals*/

    int16_t interpX45 = ((-*(val + xdim*(y-2 + *(A+1)) + x-1 + *(L)) + 5*(*(val + xdim*(y-1 + *(A)) + (x))) + \
    5*(*(val + xdim*(y) + (x+1 - *(R)))) - *(val + xdim*(y+1 - *(B)) + x+2 - *(R+1)))>>3); 


    int16_t interpX135 = (-(*(val + xdim*(y-2 + *(A+1)) + x+2 - *(R+1))) + 5*((*(val + xdim*(y-1 + *(A)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y) + (x)))) - (*(val + xdim*(y+1 - *(B)) + x+1 - *(R)))>>3); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA45 = (-(*(val + xdim*(y-2 + *(A+1)) + x-1 + *(L))) + 5*((*(val + xdim*(y-1 + *(A)) + \
    (x)))) + 5*((*(val + xdim*(y+1 - *(B)) + (x+2 - *(R+1))))) - (*(val + xdim*(y+2 - *(B+1)) + x+3 - *(R+2)))>>3); 

    int16_t interpA135 = (-(*(val + xdim*(y-2 + *(A+1)) + x+3 - *(R+2))) + 5*((*(val + xdim*(y-1 + *(A)) + \
    (x+2 - *(R+1))))) + 5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+2 - *(B+1)) + x-1 + *(L)))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB45 = (-(*(val + xdim*(y-3 + *(A+2)) + x-1 + *(L))) + 5*((*(val + xdim*(y-2 + *(A+1)) + (x)))) + \
    5*((*(val + xdim*(y) + (x+2 - *(R+1))))) - (*(val + xdim*(y+1 - *(B)) + x+3 - *(R+2)))>>3); 

    int16_t interpB135 = (-(*(val + xdim*(y-3 + *(A+2)) + x+3 - *(R+2))) + 5*((*(val + xdim*(y-2 + *(A+1)) + (x+2 - *(R+1))))) + \
    5*((*(val + xdim*(y) + (x)))) - (*(val + xdim*(y+1 - *(B)) + x-1 + *(L)))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC45 = (-(*(val + xdim*(y-3 + *(A+2)) + x-2 + *(L+1))) + 5*((*(val + xdim*(y-2 + *(A+1)) + (x-1 + *(L))))) + \
    5*((*(val + xdim*(y) + (x+1 - *(R))))) - (*(val + xdim*(y+1 - *(B)) + x+2 - *(R+1)))>>3); 

    int16_t interpC135 = (-(*(val + xdim*(y-3 + *(A+2)) + x+2 - *(R+1))) + 5*((*(val + xdim*(y-2 + *(A+1)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y) + (x-1 + *(L))))) - (*(val + xdim*(y+1 - *(B)) + x-2 + *(L+1)))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD45 = (-(*(val + xdim*(y-2 + *(A+1)) + x-2 + *(L+1))) + 5*((*(val + xdim*(y-1 + *(A)) + (x-1 + *(L))))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x+1 - *(R))))) - (*(val + xdim*(y+2 - *(B+1)) + x+2 - *(R+1)))>>3); 

    int16_t interpD135 = (-(*(val + xdim*(y-2 + *(A+1)) + x+2 - *(R+1))) + 5*((*(val + xdim*(y-1 + *(A)) + (x+1 - *(R))))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x-1 + *(L))))) - (*(val + xdim*(y+2 - *(B+1)) + x-2 + *(L+1)))>>3); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    uint16_t e45 = abs(interpA45-(*(val + xdim*(y) + x+1 - *(R)))) + abs(interpB45 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC45 - (*(val + xdim*(y-1 + *(A)) + x))) + abs(interpD45 - (*(val + xdim*(y) + x)));

    uint16_t e135 = abs(interpA135-(*(val + xdim*(y) + x+1 - *(R)))) + abs(interpB135 - (*(val + xdim*(y-1 + *(A))+ x+1 - *(R)))) +\
    abs(interpC135 - (*(val + xdim*(y-1 + *(A)) + x))) + abs(interpD135 - (*(val + xdim*(y) + x)));


    /*calculation of "edge sensitive factor "*/

    uint32_t esf45 = pow(e45, 3);
    uint32_t esf135 = pow(e135, 3);

    float w45 = (esf135) / (esf135+esf45 + 0.001);
    float w135 = 1 - w45;

    uint8_t res = w45*interpX45 + w135*interpX135;

    return res;
}





uint8_t * alg(uint8_t *val, uint16_t xDim, uint16_t yDim){

    /*memory is allocated during runtime*/
    uint8_t * arr = (uint8_t *) malloc(4 * xDim * yDim * sizeof(uint8_t));

    uint16_t HRx = 0;
    uint16_t HRy = 0;
    uint32_t LRloc = 0;
    
    for(int i = 0; i<(4*yDim*xDim); i++){
        
        

        if((HRy%2) == 0){
            if((HRx%2) ==0){
                *(arr + i) = *(val + LRloc);
                LRloc++;
            }
            else{
                *(arr + i) = 0;
            }
        }
        else{
            if((HRx%2) == 0){
                *(arr + i) = 0;
            }
            else{
                *(arr + i) = stage1(val, ceil(HRx/2), HRy/2 , xDim, yDim);
            }
        }

        HRx++;
        if(HRx == (2*xDim)){
            HRx = 0;
            HRy++;
        }
        

    }
        
    
    
    return arr;
}


