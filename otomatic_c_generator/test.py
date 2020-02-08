from keras.models import model_from_json
import argparse
from readers import H5_reader, Json_reader
import numpy as np
import os
from cpp_details import Details
from run_c_test import Tester
parser = argparse.ArgumentParser()
parser.add_argument("--json_file", default = "model.json" , type = str , help = "set the models json file for architecture of network,  default : model.json ")
parser.add_argument("--h5_file", default= "model.h5", type = str , help = "set the models h5 file for weights of network,  default : model.h5")
parser.add_argument("--precision", default= 30, type = int, help = "set the float precision for weights of network,  default : 30 ,   This may cause problem in network output so be carefull when choosing the value")
parser.add_argument("--output_file", default = "main.c" , type = str, help = "set the output c/c++ file for test purposes " )
parser.add_argument("--output_folder_name", default = "output_cpp_test" , type = str, help = "Set the output files folder name configuration for main test cpp file" )

args = parser.parse_args()
json_file = args.json_file
h5_file = args.h5_file
precision = args.precision
output_file = args.output_file
output_folder_name = args.output_folder_name



def write_input_vector_to_c(test_vector,precision):
    string = "float  network_input[{}]".format(test_vector.shape[1]*test_vector.shape[2]) + "= {"
    for i in range(len(test_vector[0])):
        string += "{"
        for j in range(len(test_vector[0][i])):
            string += ("{0:."+str(precision)+"}").format(test_vector[0][i][j][0])
            if(not (j+1 ==len(test_vector[0][i])) and not(i+1 == len(test_vector[0]))):
                string += ", "

        if(not (i+1 ==len(test_vector[0]))):
            string += ",\n"
        else:
            string += "};\n\n"
    return string

def generate_test_vector(input_shape):
    #generate test vector for comparing c and python outputs
    return np.random.rand(1,input_shape[1],input_shape[2],input_shape[3])

def write_functions(structure,read_json):
    # remove flatten layer from structure
    for layer in range(len(structure)):
        if(structure[layer][0:7]=="flatten"):
            structure.pop(layer)
        if(layer+1 == len(structure)):
            break

    string = "\n"
    
    for layer_number in range(len(structure)):
        layer = structure[layer_number]
        if(layer[:6]=="conv2d" and layer_number==0):
            
            string += "conv_2d(input_size, network_input,filter_number_" + layer + ", filter_" + layer + " , stride_" + layer + ", bias_conv2d_1, filter_size_" + layer + ", output_of_" + layer + ",  output_size_" +layer + ");\n"


            """      
            float bias_dense_1 [10] = {0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 };
            int input_size[2] = { 16, 16 };
            int filter_size_conv2d_1[2] = {3,3};
            int filter_number_conv2d_1 = 2;
            int stride_conv2d_1[2]= {1,1};
            float output_of_conv2d_1[392];
            int output_size_conv2d_1[3] = {14,14,2};
            int output_size_max_pooling[3] = {13,13,2};
            float dense_1_out[10];
            int kernel[2] = {2,2};
            float max_pooling_out[338];

            conv_2d(input_size, network_input,filter_number_conv2d_1, filter_conv2d_1 , stride_conv2d_1, bias_conv2d_1, filter_size_conv2d_1, output_of_conv2d_1,  output_size_conv2d_1);
            max_pooling( kernel,output_of_conv2d_1,max_pooling_out,output_size_max_pooling,output_size_conv2d_1);
            dense_layer(338, 10,dense_1_out, 3 , max_pooling_out, weights_dense_1, bias_dense_1);
            """
        elif (layer[:3]=="max"):
            if(structure[layer_number-1][0:6]=="conv2d"):
                input_of_layer = "output_of_"+ structure[structure.index(layer)-1]
                output_of_layer = "output_of_"+layer
                output_size_of_layer = "output_size_of_"+layer
                output_size_of_conv = "output_size_conv2d_1"
                pool_of_layer = "pool_of_"+layer
                string+= """int pool_of_max_pooling2d_1[2] = {2,2};
int output_size_of_max_pooling2d_1[3] = {11,11,6};
float output_of_max_pooling2d_1[726];\n"""

                string += "max_pooling("+pool_of_layer+"," + input_of_layer +","+ output_of_layer +","+ output_size_of_layer+","+output_size_of_conv+");\n"

            
        elif(layer[:5]=="dense"):
            activation = 0
            if(read_json.get_dense_activation(layer) == "linear"):
                activation = 3
            elif(read_json.get_dense_activation(layer) == "sigmoid"):
                activation = 2
            else:
                activation = 1

            if(structure[layer_number-1][0:3]=="max"):
                string += ("dense_layer({}, {},"+layer+"_out,{},output_of_max_pooling2d_1,weights_"+layer+", bias_dense_1);\n").format(726,read_json.get_dense_units(layer),activation)
            else:
                string += "not done!"
    
    return string


if __name__ == "__main__" :
    read_json = Json_reader()
    ordered_layers = read_json.get_layers()
    test_vector = generate_test_vector(read_json.get_input_shape(ordered_layers[0]))
    # Model reconstruction from JSON file
    model = None
    with open(json_file, 'r') as f:
        model = model_from_json(f.read())

    # Load weights into the new model
    model.load_weights(h5_file)
    #predict
    model_test_prediction = model.predict(test_vector)


    if( not os.path.isdir(output_folder_name)):
        os.mkdir(output_folder_name)
    script_dir = os.path.dirname(__file__)
    rel_path = output_folder_name + "/" + output_file
    abs_file_path = os.path.join(script_dir, rel_path)
    print(abs_file_path)
    f= open(abs_file_path,"w")
    
    details = Details()
    h5_reader = H5_reader()
    json_reader = Json_reader()


    f.write(details.set_main_libs())
    f.write(details.set_main_initializer())
    ordered_layers = json_reader.get_layers()
    print("Ordered layer list is ready.")
    f.write(write_input_vector_to_c(test_vector,precision))
    print("input test vector is ready..")
    for i in range(len(ordered_layers)):
        name_of_layer = ordered_layers[i]
        print("initialized layer name :  ", name_of_layer)
        if(name_of_layer[:6] == "conv2d"):
            ordered_filters=[]
            for filter_lists in range(json_reader.get_filter_value(name_of_layer)):
                ordered_filters.append([]) 
            filters = h5_reader.return_kernel(name_of_layer)
            for a in filters:
                for b in a:
                    for c in range(len(b[0])):
                        ordered_filters[c].append(b[0][c])
            kernel_size = json_reader.get_kernel_size(name_of_layer)
            filter_value = json_reader.get_filter_value(name_of_layer)
            string_ = "float filter_"+ name_of_layer + "[{}][{}][{}]".format(filter_value,kernel_size[0],kernel_size[1])
            string_ += " = { {"
            for filt_num in range(len(ordered_filters)):
                
                filter_dimension = 1
                
                for filt in range(len(ordered_filters[filt_num])):
                    if(filter_dimension % kernel_size[1] == 1):
                        string_ += "{"
                    string_ += ("{0:."+str(precision)+"}").format(ordered_filters[filt_num][filt])
                    if(filter_dimension % kernel_size[1] == 0):
                        string_ += "}\n"
                    if(filt+1 != len(ordered_filters[filt_num])):
                        string_+=", "
                    filter_dimension +=1
                if(filt_num +1 != len(ordered_filters)):
                    string_+="}, \n{"
                else:
                    string_+="} }; \n"
            f.write(string_)
            f.write(details.set_conv_bias(name_of_layer))
            print(name_of_layer + "  done..")
        #blank for convolution bias------>> fill it  
        #
        #
        #

        if(name_of_layer[:5] == "dense"):
            # write dense weights
            dense_weights = h5_reader.return_kernel(name_of_layer)
            node_value = json_reader.get_dense_units(name_of_layer)
            layer_number= ordered_layers.index(name_of_layer)
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
            f.write(string_)
            f.write(details.set_dense_bias(name_of_layer))
            
            print(name_of_layer + "  done..")
            # write dense bias
            
            ### fill the bias


        if(name_of_layer[:7] == "flatten"):
            print(name_of_layer + "  done..")


    f.write(details.set_initial_arrays(ordered_layers))
    f.write(write_functions(ordered_layers,read_json))
    f.write(details.set_default_end())
    f.close()
    print("Output Of C Code :")
    tester = Tester()
    tester.run_test_c()
    print("\nOutput Of Python Code :")
    print(model_test_prediction[0])

