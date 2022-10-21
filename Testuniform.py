import numpy as np
import os

print("--------------------------------------------------NEW TEST----------------------------------------------------------------------------")

def uniformEDFF(raw):
    print(raw.shape)
    path2='./DeepSleep/dataEDF/featureEDF_8m/'

    os.makedirs(path2, exist_ok=True)

    size= 2**23
    num_pool=0
    scale_pool=2**num_pool
    num=0

    all_ids=open('./DeepSleep/dataEDF/list_id_EDF.txt','r')
    for each_id in all_ids:
        print("hello1")
        each_id=each_id.rstrip()
        # print(each_id,num)
        num+=1
        
        image=raw
        print("premier image" +str(image))
        d0=image.shape[0]
        d1=image.shape[1]
        if(d1 < size*scale_pool):
            print("hello2")
            image=np.concatenate((image,np.zeros((d0,size*scale_pool-d1))),axis=1)
            print(image.shape)
            # print("deusieme image1" +str(image))
            # print(image.shape)
        np.save(path2 + each_id , image)
    all_ids.close()
    return image
