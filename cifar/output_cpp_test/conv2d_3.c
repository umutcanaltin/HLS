#include <math.h>
#include "conv2d_3.h"
#include <stdio.h>
void conv2d_3(int input_size[3], float input[384], int filter_number, float  filters[6][6][5][5], int stride[2], int filter_size[2], float * output, int output_size[3]){
 for(int filter_index = 0 ; filter_index < filter_number ;  filter_index++ ){
        for(int y_index=0 ; y_index < output_size[1] ; y_index= y_index + stride[1]  ){  //without stride   "1 for every network for now"
            for(int x_index =0; x_index < output_size[0] ; x_index = x_index + stride[0]){  // without stride
				float conv_sum = 0;
				              	
					for(int z=0; z<input_size[2] ; z++){
                    	for(int y=0; y<filter_size[1] ; y++){
                        	for(int x = 0 ; x<filter_size[0] ; x++){
                                conv_sum += filters[filter_index][z][y][x] * input[z +(y_index+y)*input_size[2]*input_size[0]+ (x_index+x)*input_size[2]];
                        	}
                            
                            	
                   		}
					}                	
                
				*(output + y_index*output_size[0]*filter_number  + x_index*filter_number + filter_index) = conv_sum;  //if stride is different from 1 shold use different var for index
            }
		}
	}
}