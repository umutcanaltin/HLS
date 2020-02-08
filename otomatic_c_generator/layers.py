class Convolution():
    def __init__(self, ordered_list, layer_number, json_reader, h5_reader):
        
        self.filter_value = None
        self.kernel_size = None
        self.output_dim = None
        self.output_dim_flatten = None
        self.filter_dim = None
        self.filter_value = None
        self.input_shape = None
        self.stride = None

        self.json_reader = json_reader
        self.h5_reader = h5_reader
        
        self.layer_number = layer_number
        self.ordered_list = ordered_list
        self.name_of_layer = self.ordered_list[layer_number]
    
    def set_parameters(self):
        self.input_shape = self.json_reader.get_input_shape(self.name_of_layer)
        self.kernel_size = self.json_reader.get_kernel_size(self.name_of_layer)
        self.stride = self.json_reader.get_strides(self.name_of_layer)
        self.filter_value = self.json_reader.get_filter_value(self.name_of_layer)
        self.output_dim = [int(((self.input_shape[1]-self.kernel_size[0])/self.stride[0])+1),int(((self.input_shape[2]-self.kernel_size[1])/self.stride[1])+1),self.filter_value]
        self.output_dim_flatten = int(self.output_dim[0]*self.output_dim[1]*self.output_dim[2])

    def get_previous_layer_name(self):
        if(self.layer_number == 0):
            return "network_input"
        else:
            if(self.ordered_list[self.layer_number-1][:3] == "fla" ):
                return self.ordered_list[self.layer_number-2]
            else:
                return self.ordered_list[self.layer_number-1]

    def filter_string(self,kernel_size,filter_value,ordered_list,layer,precision,input_channel):
        ordered_filters=[]
        
        name_of_layer = ordered_list[layer]
        filters = self.h5_reader.return_kernel(name_of_layer)
        
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
        string_ = "float filter_"+ name_of_layer + "[{}][{}][{}][{}]".format(filter_value,filters.shape[2],filters.shape[1],filters.shape[0])
        string_ += " = {"
        for filt_num in range(len(ordered_filters)):
            string_ += "{ "          
            for filt_dim in range(len(ordered_filters[filt_num])):
                string_ += "{ " 
                for filt_y in range(len(ordered_filters[filt_num][filt_dim])):
                    string_ += "{ "
                    for filt_x in range(len(ordered_filters[filt_num][filt_dim][filt_y])):
                        string_ +=  ("{0:."+str(precision)+"}").format(ordered_filters[filt_num][filt_dim][filt_y][filt_x])
                        if(filt_x +1 !=len(ordered_filters[filt_num][filt_dim][filt_y] )):
                            string_ += ", "
                        else:
                            string_ += "}"

                    if(filt_y +1 !=len(ordered_filters[filt_num][filt_dim] )):
                        string_ += ", "
                    else:
                        string_ += "}\n"
                if(filt_dim +1 !=len(ordered_filters[filt_num])):
                    string_ += ", "
                else:
                    string_ += "}\n"
            if(filt_num +1 !=len(ordered_filters)):
                string_ += ", "
            else:
                string_ += "};\n"

        return string_

    def convolution_settings(self,ordered_list,layer):
        layer_name = ordered_list[layer]
        input_shape = self.json_reader.get_input_shape(layer_name)
        kernel_size = self.json_reader.get_kernel_size(layer_name)
        stride = self.json_reader.get_strides(layer_name)
        filter = self.json_reader.get_filter_value(layer_name)
        conv_output_dim = [int(((input_shape[1]-kernel_size[0])/stride[0])+1),int(((input_shape[2]-kernel_size[1])/stride[1])+1),filter]
        string_ = 'int output_size_'+ layer_name + '['+str(len(conv_output_dim))+'] = {'+ str(conv_output_dim[0]) + ", " + str(conv_output_dim[1])+ ", "+ str(conv_output_dim[2])+ "};\n"
        string_ += "float output_of_"+ layer_name +"["+str(int(conv_output_dim[0]*conv_output_dim[1]*conv_output_dim[2]))+"];\n"
        string_ += 'int kernel_size_'+ layer_name + '['+str(len(kernel_size)) +'] = {'+ str(kernel_size[0]) + ", " + str(kernel_size[1])+  "};\n"
        string_ += 'int filter_value_'+ layer_name + '= ' + str(filter) + ";\n"
        string_ += "int input_shape_"+layer_name+"[3] = {" + "{}, {}, {}".format(input_shape[1],input_shape[2],input_shape[3])+"};\n"
        string_ += "int stride_"+layer_name+"[2]= {"+"{},{}".format(stride[0],stride[1])+"};\n"
        string_ += '#include "'+layer_name+'.h"\n'
        
        if(layer != 0):
            input_of_layer = ordered_list[layer-1]
            string_ += layer_name + "(input_shape_"+layer_name+", output_of_"+input_of_layer+",filter_value_"+layer_name+", filter_"+layer_name+", stride_"+layer_name+", kernel_size_"+layer_name+", output_of_"+layer_name+",  output_size_"+layer_name+");\n"
        else:
            string_ += layer_name + "(input_shape_"+layer_name+", network_input_0 ,filter_value_"+layer_name+", filter_"+layer_name+", stride_"+layer_name+", kernel_size_"+layer_name+", output_of_"+layer_name+",  output_size_"+layer_name+");\n"

        return kernel_size,filter, conv_output_dim ,string_,input_shape[0]