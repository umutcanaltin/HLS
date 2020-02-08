from cpp_details import Details
import argparse
import tensorflow as tf
import numpy as np
import os
import h5py 
from functools import reduce





class Test_HLS():
    def __init__(self,precision,file_w,h5_file_loc):
        print(h5_file_loc)
        x_train, y_train, x_test, y_test = self.hdf5(h5_file_loc)
        x_train = x_train.reshape(x_train.shape[0], 16, 16, 1)
        x_test = x_test.reshape(x_test.shape[0], 16, 16, 1)
        self.file_w = file_w
        
        self.network_input = x_test[0]
        self.precision = precision
        self.string = " "

    def write_network_input(self):
        dense_weights = self.network_input
        #print(self.network_input[0])
        string_ = "float "+ "network_input" + "[{}][{}]".format(dense_weights.shape[0],dense_weights.shape[1]) + " = {\n"
        for node in range(len(dense_weights)):
            string_ += "{ "
            for weight in range(len(dense_weights[node])):
                #print(dense_weights[node][weight])
                string_ += ("{0:."+str(self.precision)+"}").format(dense_weights[node][weight][0])
                if(weight+1 != len(dense_weights[node])):
                    string_ += ", "
            string_ += "}"
            if(node+1 != len(dense_weights) ):
                string_ += ",\n"
            else:
                string_ += "};\n"
        self.string += string_

    def write_start(self):
        self.string += "#include<stdio.h> \n struct my_data{ \nfloat data; \n bool last; \n}; \nvoid usps_stream (my_data in_stream[16][16], my_data out_stream[10]) ; \nint main() \n{\n"

    def write_end(self):
        self.string += '\nfloat sonuc [10];\nmy_data out_stream[10];\nmy_data in_stream[16][16];\nfor(int l=0;l<16;l++)\n{\nfor(int k=0;k<16;k++)\n{\nin_stream[k][l].data = network_input[k][l] ;\n}\n}\nusps_stream (in_stream, out_stream);\nfor(int i = 0 ; i<10 ;i++){\nprintf("aaasonuc[%d]= %.010f",i ,out_stream[i].data) ;\n}\nreturn 0 ;\n}'
    def write(self):
        self.f = open(self.file_w,"w")
        self.f.write(self.string)
        self.f.close()
        return self.network_input

    def hdf5(self,path, data_key = "data", target_key = "target", flatten = True):
        """
            loads data from hdf5: 
            - hdf5 should have 'train' and 'test' groups 
            - each group should have 'data' and 'target' dataset or spcify the key
            - flatten means to flatten images N * (C * H * W) as N * D array
        """
        with h5py.File(path, 'r') as hf:
            train = hf.get('train')
            X_tr = train.get(data_key)[:]
            y_tr = train.get(target_key)[:]
            test = hf.get('test')
            X_te = test.get(data_key)[:]
            y_te = test.get(target_key)[:]
            if flatten:
                X_tr = X_tr.reshape(X_tr.shape[0], reduce(lambda a, b: a * b, X_tr.shape[1:]))
                X_te = X_te.reshape(X_te.shape[0], reduce(lambda a, b: a * b, X_te.shape[1:]))
        return X_tr, y_tr, X_te, y_te


    