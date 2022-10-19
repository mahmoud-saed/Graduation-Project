from urllib import response
from rest_framework import viewsets
from .serializers import *
from cancerDetect.models import *
from rest_framework.response import Response 
from keras.models import load_model
import tensorflow as tf
import numpy as np
import tensorflow as tf
import cv2
from pathlib import Path
import os
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# the input 

def scan(z):
    img = cv2.imread(str(z))
    img = cv2.resize(img, (32,32))
    img = np.array(img, dtype="float32")
    img = np.reshape(img, (1,32,32,3))


# Load the TFLite model and allocate tensors.

    interpreter = tf.lite.Interpreter(model_path='model.tflite')
    interpreter.allocate_tensors()

# Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

# Test the model on random input data.
    input_shape = input_details[0]['shape']

    print("*"*50, input_details)
# the input 
    interpreter.set_tensor(input_details[0]['index'], img)

    interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.


# the o/p -= if conditions none or true & a ,b,c,d,.....
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # print('aaaaaaaaaaaaaaaaaaaa')
    # print(output_data)
    # print('aaaaaaaaaaaaaaaaaaaa')
    # print(type(output_data))
    return output_data


class CancerDetectViewSet(viewsets.ModelViewSet):
    queryset = CancerDetect.objects.all()
    serializer_class = CancerDetectSerializer


    def create(self, request, *args, **kwargs):        
        scan_data = request.data
        new_scan = CancerDetect.objects.create(picture=scan_data["picture"], patient_name=scan_data["patient_name"])  
        new_scan.save()

        path_img = os.path.join(BASE_DIR, 'media')+'\\'+str(scan_data["picture"])
        s = scan(path_img) 
        az = str(s)
        x = request.POST.get('has_cancer', False)
        if str(x) == 'true':
            x = True
        cancer_type = 'akiec'
        if(az.index('1') == 2):
            cancer_type = 'akiec'
            x = True
        elif(az.index('1') == 5):
            cancer_type = 'bcc'
            x = True
        elif(az.index('1') == 8):
            cancer_type = 'bkl'
            x = True
        elif(az.index('1') == 11):
            cancer_type = 'df'
            x = True
        elif(az.index('1') == 14):
            cancer_type = 'mel'
            x = True
        elif(az.index('1') == 17):
            cancer_type = 'nv'
            x = True
        elif(az.index('1') == 20):
            cancer_type = 'vasc'
            x = True
        else:
            cancer_type = 'none'
            x = False
        new_scan2 = CancerDetail.objects.create(patient_name=scan_data["patient_name"], has_cancer=x,cancer_type=cancer_type)  
        new_scan2.save()                



        serializer = CancerDetectSerializer(new_scan)
        return Response(serializer.data)
    


class CancerDetailViewSet(viewsets.ModelViewSet):
    queryset = CancerDetail.objects.all()
    serializer_class = CancerDetailSerializer

                        

