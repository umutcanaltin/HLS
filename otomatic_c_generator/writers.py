import os
from readers import H5_reader, Json_reader
import numpy as np
read_json = Json_reader()
read_h5 = H5_reader()
class Writers():
    def __init__(self,location, output_folder_name):
        self.location = location
        self.output_folder_name = output_folder_name
        if( not os.path.isdir(self.output_folder_name)):
            os.mkdir(self.output_folder_name)
    
    def write_convolution_function(self, name_of_layer, input_dimension, filter_dimension, filter_value):
        kernel_size = read_json.get_kernel_size(name_of_layer)
        stride = read_json.get_strides(name_of_layer)
        filter = read_json.get_filter_value(name_of_layer)
        conv_output_dim = [int(((input_dimension[0]-kernel_size[0])/stride[0])+1),int(((input_dimension[1]-kernel_size[1])/stride[1])+1),filter]
        output_file_c = name_of_layer+".c"
        rel_path_c = self.output_folder_name + "/" + output_file_c
        abs_file_path_c = os.path.join(self.location, rel_path_c)
        f_c= open(abs_file_path_c,"w")


        output_file_h = name_of_layer+".h"
        rel_path_h = self.output_folder_name + "/" + output_file_h
        abs_file_path_h = os.path.join(self.location, rel_path_h)
        f_h= open(abs_file_path_h,"w")

        function_libs ='#include <math.h>\n#include <stdio.h>\n'
        function_definition_h = "void "+name_of_layer+"(float input"+"[{}]".format(input_dimension[2]*input_dimension[1]*input_dimension[0])+", float  filters"+"[{}]".format(filter_value*input_dimension[2]*filter_dimension[1]*filter_dimension[0])+",float * output);"
        function_head_c = "void "+name_of_layer+"(float input"+"[{}]".format(input_dimension[2]*input_dimension[1]*input_dimension[0])+", float  filters"+"[{}]".format(filter_value*input_dimension[2]* filter_dimension[1]*filter_dimension[0])+",  float * output){\n"
        function_cont_c = "for(int filter_index = 0 ; filter_index < "+str(filter)+" ;  filter_index++ ){\nfor(int y_index=0 ; y_index < "+str(conv_output_dim[1])+" ; y_index= y_index + "+str(stride[1])+"  ){  \nfor(int x_index =0; x_index < "+str(conv_output_dim[0])+" ; x_index = x_index + "+str(stride[0])+"){  "
                
        func_c_cont = " float conv_sum = 0;  \n for(int z=0; z<"+  "{}".format(input_dimension[2])+  " ; z++){ \n for(int y=0; y<"+str(kernel_size[1])+" ; y++){"
        func_1 = "for(int x = 0 ; x<"+str(kernel_size[0])+" ; x++){ \nconv_sum += filters[filter_index*"+str(kernel_size[0]*kernel_size[1]*input_dimension[2])+"+     z*"+str(kernel_size[0]*kernel_size[1])+"      +     y*"+str(kernel_size[0])+"     +     x] * input[z +(y_index+y)*"+str(input_dimension[2])+"*"+str(input_dimension[0]) +"+"+ "(x_index+x)*"+str(input_dimension[2]) +"];}"

        func_c_2= "      	}\n}\n *(output + y_index*"+str(conv_output_dim[0])+"*"+str(filter)+"  + x_index*"+str(filter)+" + filter_index) = conv_sum;  } } } }"

        f_c.write(function_libs)
        f_c.write(function_head_c)
        f_c.write(function_cont_c)
        f_c.write(func_c_cont)
        f_c.write(func_1)
        f_c.write(func_c_2)
        f_h.write(function_definition_h)

        """ 
#include <math.h>
#include "conv.h"
#include <stdio.h>

void conv_2d(int input_size[3], float input[1][16][16], int filter_number,
        float  filters[2][5][5], int stride[2], float  bias[2], int filter_size[2], float * output, int output_size[3]){


	for(int filter_index = 0 ; filter_index < filter_number ;  filter_index++ ){
	// conv operation for each filter :
		 

        for(int y_index=0 ; y_index < output_size[1] ; y_index= y_index + stride[1]  ){  //without stride   "1 for every network for now"

            for(int x_index =0; x_index < output_size[0] ; x_index = x_index + stride[0]){  // without stride
				float conv_sum = 0;

				for(int z_index=0 ; z_index < output_size[2] ; z_index++  ){ 

                    // filtreyi resim �zerinde gezdirmek i�in gerekli d�ng�
                	
					for(int z=0; z<filter_size[2] ; z++){

                    	for(int y=0; y<filter_size[1] ; y++){

                        	for(int x = 0 ; x<filter_size[0] ; x++){
                            	// filterinin geldi�i yerde conv tolam�n� almak i�in gerekli d�ng�
                            	conv_sum += filters[filter_index][z][y][x] * input[z_index][y_index+y][x_index+x];
                        	}

                   		}
					}
                	
                }
				*(output + y_index*output_size[0]*filter_number  + x_index*filter_number + filter_index) = conv_sum;  //if stride is different from 1 shold use different var for index

            }
		}

	}

}"""

    def write_dense_function(self, name_of_layer, input_dimension, filter_dimension):
        output_file_c = "layer.c"
        rel_path_c = self.output_folder_name + "/" + output_file_c
        abs_file_path_c = os.path.join(self.location, rel_path_c)
        f_c= open(abs_file_path_c,"w")


        output_file_h = "layer.h"
        rel_path_h = self.output_folder_name + "/" + output_file_h
        abs_file_path_h = os.path.join(self.location, rel_path_h)
        f_h= open(abs_file_path_h,"w")
