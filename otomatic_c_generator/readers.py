import json
import h5py
import numpy as np

class Json_reader():
	
    def __init__(self, json_file= "model.json"):
	    self.json_file = json_file
	    self.data = None
	    self.length_of_nn = None
	    self.read_data()
	    self.get_length()
		
    def read_data(self):
        with open(self.json_file) as f :
	        self.data = json.load(f)
			
    def get_length(self):
        self.length_of_nn = len(self.data["config"]["layers"])
	
    def get_layers(self):
        layers =  [i["config"]["name"] for i in self.data["config"]["layers"]]
        return layers
		
    def get_activations(self):
        activations = [i['config']["activation"] for i in self.data["config"]["layers"]]
        return activations
	
    def get_input_size(self):
        input_size = self.data["config"]["layers"][0]["config"]['batch_input_shape']
        return input_size
	
    def get_filter_value(self,name_of_layer):
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                return i["config"]["filters"]
	
    def get_kernel_size(self, name_of_layer):
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["kernel_size"]
    
    def get_strides(self,name_of_layer):   
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["strides"]
    def get_input_shape(self,name_of_layer):   
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["batch_input_shape"]
        
    def get_dense_units(self,name_of_layer):   
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["units"]

    def get_dense_activation(self,name_of_layer):   
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["activation"]
    
    def get_pool_size(self,name_of_layer):
        for i in self.data["config"]["layers"]:
            if(i["config"]["name"] == name_of_layer):
                #return 2d array like [3,3]
                return i["config"]["pool_size"]





class H5_reader():
	
	def __init__(self, h5_file = "model.h5"):
		self.h5_file = h5_file
		self.data = h5py.File(self.h5_file)
		
	def return_bias(self, name_of_layer):
		if(name_of_layer[:6] == "conv2d"):
			return np.array(self.data[name_of_layer][name_of_layer]['bias:0'])
			
		elif(name_of_layer[:7] == "flatten"):
			return None
			
		else:
			return np.array(self.data[name_of_layer][name_of_layer]['bias:0'])
			
	def return_kernel(self,name_of_layer):
		if(name_of_layer[:6] == "conv2d"):
			return np.array(self.data[name_of_layer][name_of_layer]['kernel:0'])
			
		elif(name_of_layer[:7] == "flatten"):
			return None
			
		else:
			return np.array(self.data[name_of_layer][name_of_layer]['kernel:0']).T