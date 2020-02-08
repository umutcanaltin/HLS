#include <math.h>
#include <stdio.h>
void conv2d_2(float input[8748], float  filters[84672],  float * output){
for(int filter_index = 0 ; filter_index < 36 ;  filter_index++ ){
for(int y_index=0 ; y_index < 14 ; y_index= y_index + 1  ){  
for(int x_index =0; x_index < 14 ; x_index = x_index + 1){   float conv_sum = 0;  
 for(int z=0; z<12 ; z++){ 
 for(int y=0; y<14 ; y++){for(int x = 0 ; x<14 ; x++){ 
conv_sum += filters[filter_index*2352+     z*196      +     y*14     +     x] * input[z +(y_index+y)*12*27+(x_index+x)*12];}      	}
}
 *(output + y_index*14*36  + x_index*36 + filter_index) = conv_sum;  } } } }