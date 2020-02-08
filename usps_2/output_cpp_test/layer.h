#include <math.h>
float weighted_sum(float inputs[], float weights[], float bias,int input_size);
/*void dense_layer(int len_of_layer,float * output, int activation ,float inputs[],
		float weights[][len_of_layer], float  bias[],int input_size);*/


void dense_layer(int input_size, int len_of_layer,float * output, int activation ,
                float inputs[], float weights[len_of_layer][input_size], float  bias[]);
