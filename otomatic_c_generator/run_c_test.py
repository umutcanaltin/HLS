import os
from subprocess import check_output
class Tester():

    def run_test_c(self,python_out):
        script_dir = os.path.dirname(__file__)
        rel_path = "output_cpp_test"
        abs_file_path = os.path.join(script_dir, rel_path)
        os.chdir(abs_file_path)
        os.system("gcc -o main main.c relu.c sigmoid.c layer.c conv2d_1.c conv2d_3.c conv2d_4.c conv2d_2.c flatten.c pooling.c -lm")
        #os.system("./main")
        
        foo = check_output('./main', shell=True).decode("utf-8")
        a =foo.split(" ")
        c_out = [float(i) for i in a[:-1]]
        print("Output Of C Code :")
        print(c_out)
        print("Output Of Python Code :")
        print(python_out)
        



        distances = [python_out[i] - c_out[i] for i in range(len(c_out))]
        print("Distance : ")
        print(distances)