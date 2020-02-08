from cpp_details import Details
import argparse
import tensorflow as tf
import numpy as np
import os
import h5py 
from functools import reduce
from keras.datasets import cifar10



def hdf5(path, data_key = "data", target_key = "target", flatten = True):
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


parser = argparse.ArgumentParser()
parser.add_argument("--test_number", default = 100 , type = int )
parser.add_argument("--dataset", default = "usps", type = str)
parser.add_argument("--output_file", default = "test_inputs.cpp" , type = str, help = "set the output c/c++ file for test purposes " )
parser.add_argument("--output_folder_name", default = "output_cpp_test" , type = str, help = "Set the output files folder name configuration for main test cpp file" )
details = Details()

args = parser.parse_args()
test_number = args.test_number
dataset = args.dataset
output_file = args.output_file
output_folder_name = args.output_folder_name

if( not os.path.isdir(output_folder_name)):
    os.mkdir(output_folder_name)


script_dir = os.path.dirname(__file__)
rel_path = output_folder_name + "/" + output_file
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)
f= open(abs_file_path,"w")
def write_vector(input_vector,precision,i):
        
    string = "float  network_output_"+str(i)+"[{}]".format(input_vector.shape[0]) + "= {"
    print( "input shape of network : ",input_vector.shape)
    for k in range(input_vector.shape[0]):
                string += ("{0:."+str(precision)+"}").format(input_vector[k])
                if(not (k+1 ==input_vector.shape[0]) ):
                    string += ", "
                else:
                    string += "};\n\n"

    return string
from keras.models import model_from_json

if(dataset=="usps"):
    
    x_train, y_train, x_test, y_test = hdf5("usps.h5")
    x_train = x_train.reshape(x_train.shape[0], 16, 16, 1)
    x_test = x_test.reshape(x_test.shape[0], 16, 16, 1)

else:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

with open("model.json", 'r') as a:
    model = model_from_json(a.read())

# Load weights into the new model
model.load_weights("model.h5")
#predict
string_start = """#include<stdio.h>
#include <math.h>
struct my_data{
	 float data;
 bool last; 
}; 

void usps_stream (my_data in_stream[256], my_data out_stream[10]);
int main() 
{"""
f.write(string_start)
for i in range(1000):
    print(x_test[i].shape)
    vector = details.write_input_vector(x_test[i]/255,30,i)

    
    f.write(vector)
for i in range(1000):

    model_test_prediction = model.predict(np.array([x_test[i]/255]))
    vector = write_vector(model_test_prediction[0],30,i)
    f.write(vector)

string_end = """float sonuc [10];
my_data out_stream[10];
my_data in_stream[256];
for(int k=0;k<256;k++)
{
  in_stream[k].data = network_input_0[k];
}

usps_stream (in_stream, out_stream);

int errors = 0;
for(int i = 0 ; i<10 ;i++){
	float diff = abs(network_output_0[i] - out_stream[i].data);
    if( diff > 0.0000001){ // acceptable error
	   errors +=1;
    }
   printf("aaasonuc[%d]= %.010f",i ,out_stream[i].data) ;
   printf("diff = %0.10f", diff);
}

printf("error = %d", errors);

if (errors >0)
	printf("ERROR");
else
	printf("CORRECT");

return 0 ;
}"""
f.write(string_end)
f.close()