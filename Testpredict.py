import os
from pyexpat import model
import sys
import numpy as np
import scipy.io
from keras import backend as K
import tensorflow as tf
import keras
import h5py
from utils import initPaths
from edf import readEDF
import utils as u
import Deepsleep.unet0


print("|-------------------------------------------------Predict---------------------------------------------------------------------------|")



K.set_image_data_format('channels_last')  # TF dimension ordering in this code

def anchor (ref, ori): # input m*n np array
    print("ori"+str(ori.shape))
    print("ref"+str(ref.shape))
    d0=ori.shape[0]
    print(d0)
    s1=float(ref.shape[1]) # size in
    s2=float(ori.shape[1]) # size out
    
    ori_new=ori.copy()
    print(ori_new.shape)
    for i in range(d0):
        tmp=np.interp(np.arange(s2)/(s2-1)*(s1-1), np.arange(s1), ref[i,:])
        print("tmp"+str(tmp.shape)) 
        ori_new[i,np.argsort(ori[i,:])]=tmp
        print(tmp.shape)
    return ori_new

def pool_avg_2(input,if_mask=False):
    index1=np.arange(0,input.shape[1],2)
    index2=np.arange(1,input.shape[1],2)
    if (len(index2)<len(index1)):
        index2=np.concatenate((index2,[input.shape[1]-1]))
    output = (input[:,index1] + input[:,index2]) / float(2)
    if (if_mask): # -1 position are masked by -1, not avg
        mask = np.minimum(input[:,index1],input[:,index2])
        output[mask<0]=-1
    return output

###### PARAMETER ###############


size=4096*2048
write_vec=True # whether generate .vec prediction file
batch=1

num_augtest=1

################################

def predictEDF(raw):

    ref555=np.load(os.path.join(u.DEEPSLEEP_PATH,'ref555.npy'))    
    path1=u.TRAINING_PATH # PARAMETER

    # 0. reso full
    print(os.getcwd())
    model01 = Deepsleep.unet0.get_unet()
    model01.load_weights(os.path.join(u.DEEPSLEEP_PATH,'weights_01.h5'))
    


    # 1. reso 1/2; old label
#    model11 = unet1.get_unet()
#    model11.load_weights('weights_11.h5')

    # 2. reso 1/8; old label
#    model21 = unet2.get_unet()
#    model21.load_weights('weights_21.h5')

    for the_id in sys.argv[1:]:

        the_id=os.path.join(u.TRAINING_PATH,'RM431010.edf')

        # image_raw: pad to 8M; image_ori: resize & shift; image: prediction input
        #image_raw = import_signals(the_id + '.mat') # PARAMETER
        image_raw = raw
        print(image_raw)
        
        d0=image_raw.shape[0]
        d1=image_raw.shape[1]
        image_raw = anchor(ref555, image_raw)
        
        if(d1 < size):
            image_raw=np.concatenate((image_raw,np.zeros((d0,size-d1))),axis=1)
    
        ## 0. reso full ####################################
        np.random.seed(450)   
        num_channel=5
        num_pool=0
        scale_pool=2**num_pool
        size1=int(size/scale_pool)
        shift=int((size1 - d1/scale_pool)/2)
    
    #    image_ori=cv2.resize(image_raw,(size1,d0),interpolation=cv2.INTER_AREA) # average pool
        image_ori=image_raw.copy()
        j=0
        while (j<num_pool):
            image_ori=pool_avg_2(image_ori)
            j+=1
    
        image_ori=np.roll(image_ori,shift,axis=1)
        print("imageori.shape" +str(image_ori.shape))
    
        index1=np.arange(7) #entre les channels 0 et 6 
        print(index1)
        index2=np.arange(2)+8 #entre channels 8 et 9
        print(index2)
        index3=np.array([7,10,12]) #entres channels 7,10,12
        print("index 3"+str(index3))
    
        j=0
        while (j<num_augtest):
            np.random.shuffle(index1)
            print(index1)
            np.random.shuffle(index2)
            print("shuffle2" +str(index2))
            index=np.concatenate((index1[0:1],index2[0:1],index3))
            print("imageori.shape" +str(image_ori.shape))
            print(index)
            image = image_ori[index,:]
            input_pred=np.reshape(image.T,(batch,size1,num_channel))
    
            output1 = model01.predict(input_pred)
            print("premiershapeoutput1"+str(output1.shape))
            output1=np.reshape(output1,(size1*batch))
            print(output1.shape)
            print(output1)
            print(np.mean(output1))

            output=output1
    
            if (j==0):
                output_new=output
            else:
                output_new = output_new+output
            j+=1
    
        output_new1=output_new/(num_augtest)
        j=0
        while (j<num_pool):
            output_new1=np.repeat(output_new1,2)
            j+=1
        output_all0=output_new1[shift*scale_pool:(shift*scale_pool+d1)]
        print("output"+str(output_all0))
        print(np.mean(output_all0))

        ## 3. stack & write ##############################################
    
        output_final=output_all0
        print("outputfinal"+str(output_final))
        print(output_final.shape) #valeurs contenues dans le fichier vec 


        if(write_vec):
            print("vecvec")
            vec = open(the_id + '.vec', 'w')
            for item in output_final:
                #vec.write("%.4f\n" % item)
                vec.write("%.3f\n" % item) #permet de ne pas afficher toutes les décimales
            vec.close()
        pass
        
        ###################################################################
    return 