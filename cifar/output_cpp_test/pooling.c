void max_pooling( int kernel[2],float input[338],float * output,int output_size[3], int input_size[3]){



     for(int z = 0 ; z<output_size[2] ; z++)
    {
        for(int y = 0 ; y <output_size[1] ; y++)
        {
            for(int x = 0 ; x<output_size[0] ; x++)
            {
                
                
                float maximum = input[ x*output_size[2] + y*input_size[0]*output_size[2] + z] ;


                for(int y_k = 0 ; y_k < kernel[1] ; y_k++)
                {
                    for(int x_k = 0 ; x_k < kernel[0] ; x_k++)
                    {
                        if(input[ (x + x_k)*output_size[2]+ (y+ y_k)*input_size[0]*output_size[2] + z]  > maximum){
                            maximum = input[ (x + x_k)*output_size[2]+ (y+ y_k)*input_size[0]*output_size[2] + z] ;
                        }


                    }

                }
                *(output + x*output_size[2] + output_size[0]*y*output_size[2] +z)= maximum;

                

            }
        }
        
                       
    }



}