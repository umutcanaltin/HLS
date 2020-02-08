from readers import H5_reader, Json_reader
import numpy as np
read_json = Json_reader()
read_h5 = H5_reader()

class Details():

    def __init__(self):
        self.string = "initial string for file writing"
    
    def set_main_libs(self):
        self.string = '#include <stdio.h> \n#include <stdlib.h> \n#include "layer.h" \n#include "sigmoid.h" \n#include "relu.h"  \n#include "flatten.h"\n #include "pooling.h"\n'
        return self.string

    def set_main_initializer(self):


        self.string = 'float main() {\n'
        return self.string
    
    def set_main_libs_cpp(self):

        self.string = '#include <stdio.h> \n#include <stdlib.h> \n#include "layer.h" \n#include "sigmoid.h" \n#include "relu.h"  \n#include "flatten.h"\n #include "pooling.h"\n'
        return self.string

    def set_main_initializer_cpp(self):
        self.string = """struct my_data{
                        float data;
                        bool last;
                            };\n"""
        self.string += 'void usps_stream (my_data in_stream[256], my_data out_stream[10]) {\n'
        self.string += """	#pragma HLS INTERFACE axis port=in_stream
#pragma HLS INTERFACE axis port=out_stream
#pragma HLS INTERFACE ap_ctrl_none register port=return

int k=0;
float network_input_0[256];
 //	float network_input1[16][16];
//	float network_input2[16][16];
//	float network_input3[16][16];
//	float network_input4[16][16];
//	float network_input5[16][16];
//	float network_input6[16][16];
//bool input_last[10];
for(k=0;k<256;k++)
	{
	network_input_0[k] = in_stream[k].data;
    //  network_input1[l][k] = network_input[l][k];
    //  network_input2[l][k] = network_input[l][k];
    //	network_input3[l][k] = network_input[l][k];
    //	network_input4[l][k] = network_input[l][k];
    //  network_input5[l][k] = network_input[l][k];
    //	network_input6[l][k] = network_input[l][k];

	}
"""
        return self.string
    
    def set_default_end(self,ordered_list):
        layer = ordered_list[-1]
        i = read_json.get_dense_units(layer)
        for_loop = "for(int i = 0 ; i<"+str(i)+" ;i++){\n"
        for_1 = 'printf("%f ", output_of_'+layer+'[i]);\n'
        for_2 = "   }\n "
        self.string =for_loop+for_1+for_2+ " \n}"
        return self.string
    def set_end_cpp(self):
        self.string = """	for(k=0;k<9;k++){
out_stream[k].data = output_of_dense_1[k];
out_stream[k].last = false;
}

out_stream[k].data = output_of_dense_1[k];
out_stream[k].last = true;


/*for(int i = 0 ; i<10 ;i++){
printf("%f ", output_of_dense_1[i]);
}*/
  
}"""
        return self.string
    def set_conv_bias(self,name_of_layer):
        filter_number = read_json.get_filter_value(name_of_layer)
        string_ = "float bias_" + name_of_layer + ' [{}]'.format(filter_number) + " = {"
        for node in range(filter_number):
            string_ += "0 "
            if(node +1 != filter_number):
                string_ += ","
            else:
                string_ += "};\n" 
        return string_
    
    def set_dense_bias(self,name_of_layer):
        node_number = read_json.get_dense_units(name_of_layer)
        string_ = "float bias_" + name_of_layer + ' [{}]'.format(node_number) + " = {"
        for node in range(node_number):
            string_ += "0 "
            if(node +1 != node_number):
                string_ += ","
            else:
                string_ += "};\n" 
        return string_
    
    
    def generate_input_vector(self,input_shape):
        #return np.ones((1,input_shape[1],input_shape[2],input_shape[3]))
        return np.random.rand(1,input_shape[1],input_shape[2],input_shape[3])
    
    def write_input_vector(self,input_vector,precision,i):
        
        string = "float  network_input_"+str(i)+"[{}]".format(input_vector.shape[2]*input_vector.shape[1]*input_vector.shape[0]) + "= {"
        print( "input shape of network : ",input_vector.shape)
        for k in range(input_vector.shape[0]):
            for j in range(input_vector.shape[1]):

                for i in range(input_vector.shape[2]):
                    string += ("{0:."+str(precision)+"}").format(input_vector[k][j][i])
                    if(not (k+1 ==input_vector.shape[0]) or not(j+1 ==input_vector.shape[1]) or not(i+1 ==input_vector.shape[2])):
                        string += ", "
                    else:
                        string += "};\n\n"

        return string
    
    def set_initial_arrays(self,structure):
        self.string = ""
        for layer in structure :
            if(layer[:6] == "conv2d"):
                self.string += 'int input_size[2] = {'+' {}, {} '.format(read_json.get_input_shape(layer)[1],read_json.get_input_shape(layer)[2]) + '};\n'
                self.string += 'int filter_size_'+ layer +'['+ str(read_json.get_filter_value(layer)) + '] = {'+str(read_json.get_kernel_size(layer)[0])+','+ str(read_json.get_kernel_size(layer)[1])+'};\n'
                self.string += 'int filter_number_'+ layer+' = '+  str(read_json.get_filter_value(layer)) +';\n'
                self.string += 'int stride_'+ layer + '['+ str(len(read_json.get_strides(layer)))+ ']= {'+str(read_json.get_strides(layer)[0])+','+str(read_json.get_strides(layer)[1])+'};\n'
                conv_output_dim = int(((read_json.get_input_shape(layer)[1]-read_json.get_kernel_size(layer)[0]) /read_json.get_strides(layer)[0]+1)*((read_json.get_input_shape(layer)[2]-read_json.get_kernel_size(layer)[1]) /read_json.get_strides(layer)[1]+1)*read_json.get_filter_value(layer))
                self.string += 'float output_of_'+ layer +'[{}];\n'.format(conv_output_dim)
                self.string += 'int output_size_'+ layer + '[3] = {'+ str(int((read_json.get_input_shape(layer)[1]-read_json.get_kernel_size(layer)[0]) /read_json.get_strides(layer)[0]+1))+','+ str(int((read_json.get_input_shape(layer)[2]-read_json.get_kernel_size(layer)[1]) /read_json.get_strides(layer)[1]+1)) + ','+ str(read_json.get_filter_value(layer))+'};\n'

            if (layer[:5] =="dense"):
                self.string += 'float '+ layer +'_out[{}];'.format(read_json.get_dense_units(layer))

        return self.string
    def dense_settings(self,ordered_list, layer):
            activation = 0
            name_of_layer = ordered_list[layer]
            if(read_json.get_dense_activation(name_of_layer) == "linear"):
                activation = 3
            elif(read_json.get_dense_activation(name_of_layer) == "sigmoid"):
                activation = 2
            else:
                activation = 1
            before =ordered_list[layer]
            before_layer = layer
            input_ = 1
            if(layer != 0 ):
                if(ordered_list[layer -1][:3] =="fla" ):
                    before = ordered_list[layer-2]
                    before_layer = layer -2
                else:
                    before = ordered_list[layer -1]
                    before_layer = layer -1
            else:
                before = "network_input_0"
            if(before[:3]=="den"):
                input_ = read_json.get_dense_units(before)
            if(before[:3] =="max"):
                pool_size = read_json.get_pool_size(before)
                stride = read_json.get_strides(before)
                input_of_layer = ordered_list[before_layer -1]
                input_shape_conv = read_json.get_input_shape(input_of_layer)
                kernel_size_conv = read_json.get_kernel_size(input_of_layer)
                stride_conv = read_json.get_strides(input_of_layer)
                filter_conv = read_json.get_filter_value(input_of_layer)

                input_dim_max_pool = [int(((input_shape_conv[1]-kernel_size_conv[0])/stride_conv[0])+1),int(((input_shape_conv[2]-kernel_size_conv[1])/stride_conv[1])+1),filter_conv]
                output_of_max_pooling = [int(((input_dim_max_pool[0]-pool_size[0])/stride[0])+1),int(((input_dim_max_pool[1]-pool_size[1])/stride[1])+1),filter_conv]
                input_ = str(int(output_of_max_pooling[0]*output_of_max_pooling[1]*output_of_max_pooling[2]))

            string_ = 'float '+ "output_of_"+name_of_layer +'[{}];\n'.format(read_json.get_dense_units(name_of_layer))
            string_ += ("dense_layer({}, {},output_of_"+name_of_layer+",{},output_of_"+ordered_list[before_layer]+",weights_"+name_of_layer+", bias_"+name_of_layer+");\n").format(input_,read_json.get_dense_units(name_of_layer),activation)
            return string_
    
    def set_dense_weights(self,name_of_layer,precision):

       
        dense_weights = read_h5.return_kernel(name_of_layer)
        string_ = "float weights_"+ name_of_layer + "[{}][{}]".format(dense_weights.shape[0],dense_weights.shape[1]) + " = {\n"
        for node in range(len(dense_weights)):
            string_ += "{ "
            for weight in range(len(dense_weights[node])):
                string_ += ("{0:."+str(precision)+"}").format(dense_weights[node][weight])
                if(weight+1 != len(dense_weights[node])):
                    string_ += ", "
            string_ += "}"
            if(node+1 != len(dense_weights) ):
                string_ += ",\n"
            else:
                string_ += "};\n"
        return string_

    def convolution_settings(self,ordered_list,layer):
        layer_name = ordered_list[layer]
        input_shape = read_json.get_input_shape(layer_name)
        kernel_size = read_json.get_kernel_size(layer_name)
        stride = read_json.get_strides(layer_name)
        filter = read_json.get_filter_value(layer_name)
        conv_output_dim = [int(((input_shape[1]-kernel_size[0])/stride[0])+1),int(((input_shape[2]-kernel_size[1])/stride[1])+1),filter]
        string_ = 'int output_size_'+ layer_name + '['+str(len(conv_output_dim))+'] = {'+ str(conv_output_dim[0]) + ", " + str(conv_output_dim[1])+ ", "+ str(conv_output_dim[2])+ "};\n"
        string_ += "float output_of_"+ layer_name +"["+str(int(conv_output_dim[0]*conv_output_dim[1]*conv_output_dim[2]))+"];\n"
        string_ += '#include "'+layer_name+'.h"\n'
        
        if(layer != 0):
            input_of_layer = ordered_list[layer-1]
            string_ += layer_name + "( output_of_"+input_of_layer+",filter_"+layer_name+", output_of_"+layer_name+");\n"
        else:
            string_ += layer_name + "(network_input_0 ,filter_"+layer_name+",output_of_"+layer_name+");\n"

        return kernel_size,filter, conv_output_dim ,string_,input_shape[0]

        
    def filter_string(self,kernel_size,filter_value,ordered_list,layer,precision,input_channel):
        ordered_filters=[]
        
        name_of_layer = ordered_list[layer]
        filters = read_h5.return_kernel(name_of_layer)
        
        for a in range(filters.shape[3]):
            ordered_filters.append([])
            for b in range(filters.shape[2]):
                ordered_filters[a].append([])

                for c in range(filters.shape[1]):
                    ordered_filters[a][b].append([])
        filters_t = filters.T
        for i in range(filters.shape[0]):
            # shape (5,5,1,6)   a ---> filter number
            for j in range(filters.shape[1]):
                # b--> filter dim z
                for k in range(filters.shape[2]):
                    
                    for l in range(filters.shape[3]):
                        ordered_filters[l][k][j].append((filters_t[l][k][i][j]))
        print("Ordered Convolution filters is ready..")


        # write to c
        string_ = "float filter_"+ name_of_layer + "[{}]".format(filter_value*filters.shape[2]*filters.shape[1]*filters.shape[0])
        string_ += " = {"
        for filt_num in range(len(ordered_filters)):
            #string_ += "{ "          
            for filt_dim in range(len(ordered_filters[filt_num])):
                #string_ += "{ " 
                for filt_y in range(len(ordered_filters[filt_num][filt_dim])):
                    #string_ += "{ "
                    for filt_x in range(len(ordered_filters[filt_num][filt_dim][filt_y])):
                        string_ +=  ("{0:."+str(precision)+"}").format(ordered_filters[filt_num][filt_dim][filt_y][filt_x])
                        if(filt_x +1 !=len(ordered_filters[filt_num][filt_dim][filt_y] )):
                            string_ += ", "
                        else:
                            string_ += ","

                    if(filt_y +1 !=len(ordered_filters[filt_num][filt_dim] )):
                        pass
                        #string_ += ", "
                    else:
                        pass
                        #string_ += ","
                if(filt_dim +1 !=len(ordered_filters[filt_num])):
                    pass
                    #string_ += ", "
                else:
                    pass
                    #string_ += ","
            if(filt_num +1 !=len(ordered_filters)):
                pass
                #string_ += ", "
            else:
                string_ += "};\n"

        return string_

    def max_pooling_settings(self,ordered_list,layer):
        name_of_layer = ordered_list[layer]
        pool_size = read_json.get_pool_size(name_of_layer)
        stride = read_json.get_strides(name_of_layer)
        input_of_layer = ordered_list[layer -1]
        input_shape_conv = read_json.get_input_shape(input_of_layer)
        kernel_size_conv = read_json.get_kernel_size(input_of_layer)
        stride_conv = read_json.get_strides(input_of_layer)
        filter_conv = read_json.get_filter_value(input_of_layer)

        input_dim_max_pool = [int(((input_shape_conv[1]-kernel_size_conv[0])/stride_conv[0])+1),int(((input_shape_conv[2]-kernel_size_conv[1])/stride_conv[1])+1),filter_conv]
        output_of_max_pooling = [int(((input_dim_max_pool[0]-pool_size[0])/stride[0])+1),int(((input_dim_max_pool[1]-pool_size[1])/stride[1])+1),filter_conv]
    
        string_ = "int pool_size_"+name_of_layer+ "[2] = {" + "{},{}".format(pool_size[0],pool_size[1])+ "};\n"
        string_ += "int output_size_of_"+name_of_layer+"[3] = {" +"{},{},{}".format(output_of_max_pooling[0],output_of_max_pooling[1],output_of_max_pooling[2])  + "};\n"
        string_ +="float output_of_"+name_of_layer+"["+str(int(output_of_max_pooling[0]*output_of_max_pooling[1]*output_of_max_pooling[2]))+"];\n"
        string_ += "max_pooling(pool_size_"+name_of_layer+", output_of_"+ordered_list[layer-1]+", output_of_"+name_of_layer+", output_size_of_"+name_of_layer+" , output_size_"+ordered_list[layer-1] + ");\n"
        return string_ 

