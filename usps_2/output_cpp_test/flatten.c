
#include "flatten.h"

void flatten(float * output_of_flatten, float * input, int input_shape[]){

    for(int x = 0 ; x<input_shape[0];x++){

        for(int y = 0 ; y<input_shape[1] ; y++){

            for(int z = 0 ; z<input_shape[2] ; z++){

            int k = x + y*input_shape[0] + z*input_shape[1] ;
            int l = y + x*input_shape[0] + z*input_shape[1] ;
            *(output_of_flatten+l) = *(input + k);
            }
        }
    }




}

/*
//flatten(output_of_flatten,output_of_conv, output_size);
void flatten(float * output_of_flatten, float * input, int input_shape[]){

	for(int x = 0 ; x<input_shape[1];x++){

		for(int y = 0 ; y<input_shape[2] ; y++){

			for(int z = 0 ; z<input_shape[0] ; z++){

			int k = y + x*input_shape[1] + z*input_shape[2] ;
			*(output_of_flatten+k) = *(input + k);
			}
		}
	}




}*/
