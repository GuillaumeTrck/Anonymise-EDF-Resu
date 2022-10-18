from cProfile import label
from hashlib import new
import numpy as np
import scipy.io
import os
import mne

print("--------------------------------------------------NEW TEST----------------------------------------------------------------------------")

def readEDF(EDFName):
    ErasmeToMneEdf(EDFName)
    raw = mne.io.read_raw_edf(EDFName, preload=True)
    MneToErasmeEdf(EDFName)
    print(type(raw))
    print(len(raw))
    info = raw.info
    print(info)
    #print(info['sfreq'])
    new_raw=raw.get_data()
    return new_raw


def ErasmeToMneEdf(EDFName):
    fid = open(EDFName, "r+")
    fid.seek(170)
    fid.write(".")
    fid.seek(173)
    fid.write(".")
    fid.seek(178)
    fid.write(".")
    fid.seek(181)
    fid.write(".")
    fid.close()
    return

def MneToErasmeEdf(EDFName):
    fid = open(EDFName, "r+")
    fid.seek(170)
    fid.write("/")
    fid.seek(173)
    fid.write("/")
    fid.seek(178)
    fid.write(":")
    fid.seek(181)
    fid.write(":")
    fid.close()

a=readEDF("PM807100.EDF")
path2='./dataEDF/featureEDF_8m/'

os.makedirs(path2, exist_ok=True)

size= 2**23
num_pool=0
scale_pool=2**num_pool
num=0

all_ids=open('./dataEDF/list_id_EDF.txt','r')
for each_id in all_ids:
    print("hello1")
    each_id=each_id.rstrip()
    print(each_id,num)
    num+=1
    signal_file = "PM807100.EDF"
    image = readEDF(signal_file)


    print("premier image" +str(image))
    d0=image.shape[0]
    d1=image.shape[1]
    if(d1 < size*scale_pool):
        print("hello2")
        image=np.concatenate((image,np.zeros((d0,size*scale_pool-d1))),axis=1)
        print("deusieme image1" +str(image))
        print(image.shape)
    np.save(path2 + each_id , image)
all_ids.close()
