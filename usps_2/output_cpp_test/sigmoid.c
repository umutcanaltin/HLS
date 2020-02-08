#include <math.h>
#include "sigmoid.h"
float sigmoid(float input){

	return(1.0/(1.0 + exp(-input)));


}


