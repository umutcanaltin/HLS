#include <math.h>
#include <stdio.h>
void conv2d_2(float input[216], float  filters[2400],  float * output){
for(int filter_index = 0 ; filter_index < 16 ;  filter_index++ ){
for(int y_index=0 ; y_index < 2 ; y_index= y_index + 1  ){  
for(int x_index =0; x_index < 2 ; x_index = x_index + 1){   float conv_sum = 0;  
 for(int z=0; z<6 ; z++){ 
 for(int y=0; y<5 ; y++){for(int x = 0 ; x<5 ; x++){ 
conv_sum += filters[filter_index*150+     z*25      +     y*5     +     x] * input[z +(y_index+y)*6*6+(x_index+x)*6];}      	}
}
 *(output + y_index*2*16  + x_index*16 + filter_index) = conv_sum;  } } } }