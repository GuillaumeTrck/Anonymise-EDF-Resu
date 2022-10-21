import numpy as np
import os

print("--------------------------------------------------NEW TEST----------------------------------------------------------------------------")

def uniformEDF(raw):
    print(raw.shape)
    path2='./DeepSleep/dataEDF/featureEDF_8m/'

    os.makedirs(path2, exist_ok=True)

    size= 2**23
    num_pool=0
    scale_pool=2**num_pool
    print("hello1")
    image=raw
    d0=image.shape[0]
    d1=image.shape[1]
    if(d1 < size*scale_pool):
        image=np.concatenate((image,np.zeros((d0,size*scale_pool-d1))),axis=1)
        print(image.shape)
    np.save(path2, image)
    
    return image
