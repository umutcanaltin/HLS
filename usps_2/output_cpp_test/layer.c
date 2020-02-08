
#include <math.h>
#include <string.h>
#include <stdio.h>
#include "layer.h"
#include "sigmoid.h"
#include "relu.h"
#include "linear.h"

float weighted_sum(float inputs[], float weight[],float  bias,int input_size){

	float sum = bias;

	for(int index = 0 ; index < input_size ;  index++ ){

		sum = sum + (inputs[index] * weight[index]) ;
	}

	return sum;

}

//dense_layer(8, 3, output_1, 1, input,    weight_1, bias_1);
void dense_layer(int input_size, int len_of_layer,float * output, int activation ,
                float inputs[], float weights[len_of_layer][input_size], float  bias[]){

    for(int index = 0 ; index <len_of_layer ;  index++ ){

        if(activation == 1){
        *(output+index) = relu(weighted_sum(inputs, weights[index] ,bias[index],input_size));
            /*for(int i = 0 ; i <input_size ;  i++ ){
                printf("[%d][%d] = %.10lf\n",index,i,weights[index][i]);
            }
        printf("\n\n");*/
        }

        if(activation == 2){
        *(output+index) = sigmoid(weighted_sum(inputs, weights[index] ,bias[index],input_size));
        }

        if(activation == 3){
            
            *(output+index) = (weighted_sum(inputs, weights[index] ,bias[index],input_size));
        }
    }

}




