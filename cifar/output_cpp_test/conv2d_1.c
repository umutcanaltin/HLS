#include <math.h>
#include <stdio.h>
void conv2d_1(float input[3072], float  filters[900],  float * output){
for(int filter_index = 0 ; filter_index < 12 ;  filter_index++ ){
for(int y_index=0 ; y_index < 28 ; y_index= y_index + 1  ){  
for(int x_index =0; x_index < 28 ; x_index = x_index + 1){   float conv_sum = 0;  
 for(int z=0; z<3 ; z++){ 
 for(int y=0; y<5 ; y++){for(int x = 0 ; x<5 ; x++){ 
conv_sum += filters[filter_index*75+     z*25      +     y*5     +     x] * input[z +(y_index+y)*3*32+(x_index+x)*3];}      	}
}
 *(output + y_index*28*12  + x_index*12 + filter_index) = conv_sum;  } } } }