#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>



/*arrays containing overflow correction coefficients*/
uint8_t S1o3[3] = {1, 2, 3};
uint8_t S1o2[3] = {0, 1, 2};
uint8_t S1o1[3] = {0, 0, 1};
uint8_t S1o0[3] = {0, 0, 0};

uint8_t S2o3[3] = {1, 3, 5};
uint8_t S2o2[3] = {0, 1, 3};
uint8_t S2o1[3] = {0, 0, 1};
uint8_t S2o0[3] = {0, 0, 0};

uint8_t stage1(uint8_t * val, uint16_t x, uint16_t y, uint16_t xdim, uint16_t ydim){


    /*pointers to access overvlow correction coefficiecnt arrays*/
    uint8_t * L;
    uint8_t * R;
    uint8_t * A;
    uint8_t * B;


    /*correction coefficient selector*/
    switch(xdim - x){
        case 0:    R = &S1o3[0];     break;
        case 1:    R = &S1o2[0];     break;
        case 2:    R = &S1o1[0];     break;
        default:   R = &S1o0[0];     break;
    }
    switch(x){
        case 0:    L = &S1o3[0];     break;
        case 1:    L = &S1o2[0];     break;
        case 2:    L = &S1o1[0];     break;
        default:   L = &S1o0[0];     break;
    }
    switch(ydim - y){
        case 0:    B = &S1o3[0];     break;
        case 1:    B = &S1o2[0];     break;
        case 2:    B = &S1o1[0];     break;
        default:   B = &S1o0[0];     break;
    }
    switch(y){
        case 0:    A = &S1o3[0];     break;
        case 1:    A = &S1o2[0];     break;
        case 2:    A = &S1o1[0];     break;
        default:   A = &S1o0[0];     break;
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




void stage2(uint8_t * val, uint16_t x, uint16_t y, uint16_t xdim, uint16_t ydim){


    /*pointers to access overvlow correction coefficiecnt arrays*/
    uint8_t * L;
    uint8_t * R;
    uint8_t * A;
    uint8_t * B;


    /*correction coefficient selector*/
    switch(xdim - x){
        case 0:    R = &S2o3[0];     break;
        case 1:    R = &S2o2[0];     break;
        case 2:    R = &S2o1[0];     break;
        default:   R = &S2o0[0];     break;
    }
        switch(x){
        case 0:    L = &S2o3[0];     break;
        case 1:    L = &S2o2[0];     break;
        case 2:    L = &S2o1[0];     break;
        default:   L = &S2o0[0];     break;
    }
        switch(ydim - y){
        case 0:    B = &S2o3[0];     break;
        case 1:    B = &S2o2[0];     break;
        case 2:    B = &S2o1[0];     break;
        default:   B = &S2o0[0];     break;
    }
        switch(y){
        case 0:    A = &S2o3[0];     break;
        case 1:    A = &S2o2[0];     break;
        case 2:    A = &S2o1[0];     break;
        default:   A = &S2o0[0];     break;
    }


    /*initial arbitrary interpolation of the missing HR pixel along both diagonals*/

    int16_t interpX0 = (-*(val + xdim*(y) + x-3 + *(L+1)) + 5*(*(val + xdim*(y) + x-1 + *(L))) + \
    5*(*(val + xdim*(y) + x+1 - *(R))) - *(val + xdim*(y) + x+3 - *(R+1))>>3); 


    int16_t interpX90 = (-(*(val + xdim*(y-3 + *(A+1)) + x)) + 5*((*(val + xdim*(y-1 + *(A)) + (x)))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))>>3); 


    /*arbitrary interpolation for four nearest LR neighbours of missing HR pixel*/

    /********************************************************************************************************************************************/
    int16_t interpA0 = (-(*(val + xdim*(y) + x-3 + *(L+1))) + 5*(*(val + xdim*(y) + x-1 + *(L))) +\
    5*(*(val + xdim*(y) + (x+3 - *(R+1)))) - (*(val + xdim*(y) + x+5 - *(R+3)))>>3); 

    int16_t interpA90 = (-(*(val + xdim*(y-3 + *(A+1)) + x+1 - *(R))) + 5*(*(val + xdim*(y-1 + *(A)) + x+1 - *(R))) +\
    5*(*(val + xdim*(y+1 - *(B)) + x+1 - *(R))) - (*(val + xdim*(y+3 - *(B+1)) + x+1 - *(R)))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpB0 = (-(*(val + xdim*(y-1 + *(A)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y-1 + *(A)) + (x+1 - *(R)))) - (*(val + xdim*(y-1 + *(A)) + x+3 - *(R+1)))>>3); 

    int16_t interpB90 = (-(*(val + xdim*(y-5 + *(A+2)) + x)) + 5*(*(val + xdim*(y-3 + *(A+1)) + (x))) + \
    5*((*(val + xdim*(y+1 - *(B)) + (x)))) - (*(val + xdim*(y+3 - *(B+1)) + x))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpC0 = (-(*(val + xdim*(y) + x-5 + *(L+2))) + 5*(*(val + xdim*(y) + x-3 + *(L+1))) + \
    5*(*(val + xdim*(y) + x+1 - *(R))) - (*(val + xdim*(y) + x+3 - *(R+1)))>>3); 

    int16_t interpC90 = (-(*(val + xdim*(y-3 + *(A+1)) + x-1 + *(L))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y+1 - *(B)) + x-1 + *(L))) - (*(val + xdim*(y+3 - *(B+1)) + x-1 + *(L)))>>3); 
    /********************************************************************************************************************************************/

    /********************************************************************************************************************************************/
    int16_t interpD0 = (-(*(val + xdim*(y+1 - *(B)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y+1 - *(B)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y+1 - *(B)) + x+1 - *(R))) - (*(val + xdim*(y+1 - *(B)) + x+3 - *(R+1)))>>3); 

    int16_t interpD90 = (-(*(val + xdim*(y-3 + *(A+1)) + x-3 + *(L+1))) + 5*(*(val + xdim*(y-1 + *(A)) + x-1 + *(L))) + \
    5*(*(val + xdim*(y+3 - *(B+1)) + x+1 - *(R))) - (*(val + xdim*(y+5 - *(B+2)) + x+3 - *(R+1)))>>3); 
    /********************************************************************************************************************************************/

    /*calculation of error along the diagonals for nearest neighbours*/

    uint16_t e0 = abs(interpA0-(*(val + xdim*(y) + x+1 - *(R)))) + abs(interpB0 - (*(val + xdim*(y-1 + *(A))+ x))) +\
    abs(interpC0 - (*(val + xdim*(y) + x-1 + *(L)))) + abs(interpD0 - (*(val + xdim*(y+1 - *(A)) + x)));

    uint16_t e90 = abs(interpA90-(*(val + xdim*(y) + x+1 - *(R)))) + abs(interpB90 - (*(val + xdim*(y-1 + *(A))+ x))) +\
    abs(interpC90 - (*(val + xdim*(y) + x-1 + *(L)))) + abs(interpD90 - (*(val + xdim*(y+1 - *(A)) + x)));


    /*calculation of "edge sensitive factor "*/

    uint32_t esf0 = pow(e0, 3);
    uint32_t esf90 = pow(e90, 3);

    float w0 = (esf90) / (esf90+esf0 + 0.001);
    float w90 = 1 - w0;

    *(val + xdim*(y) + x) = w0*interpX0 + w90*interpX90;

}


uint8_t * alg(uint8_t *val, uint16_t xDim, uint16_t yDim){

    /*memory for HR image is allocated during runtime*/
    uint8_t * arr = (uint8_t *) malloc(4 * xDim * yDim * sizeof(uint8_t));

    /*we keep track of row and column indexing since the data structures are simple 1D contiguous */
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

    HRx = 1;
    HRy = 0;

    for(int i = 1; i<(4*yDim*xDim); i+=2){ 

        stage2(arr, HRx, HRy, 2*xDim, 2*yDim);

        HRx+=2;
        if(HRx == 2*xDim){
            HRy++;
            HRx = 1;
        }
        if((HRx - 1) == 2*xDim){
            HRy++;
            HRx = 0;
        }

    }

    
    
    return arr;
}


