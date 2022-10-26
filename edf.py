from ast import Return
import mne
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
from utils import printLogs 

def readEDF(EDFName):
    ErasmeToMneEdf(EDFName)
    raw = mne.io.read_raw_edf(EDFName, preload=True)
    #print(raw)
    #print('Chan =', raw.ch_names)
   #print('Sampling frequency =', raw.info['sfreq'])
    #print('Data shape (channels, times) =', raw._data.shape)
    #print(raw.info)
    #raw.pick_types(eeg=True)
    #print('Chan =', raw.ch_names)
    #raw.plot(duration=30, start=30, n_channels=1, block=True)
    MneToErasmeEdf(EDFName)
    return raw

def readEDFHeader(EDFName):
    ErasmeToMneEdf(EDFName)
    EDF = open(EDFName, "rb")
    header = {}
    header['version'] = EDF.read(8).decode('unicode_escape')
    header['patient'] = EDF.read(80).decode('unicode_escape')
    header['recording'] = EDF.read(80).decode('unicode_escape')
    header['startDate'] = EDF.read(16).decode('unicode_escape')
    header['headerSize'] = int(EDF.read(8).decode('unicode_escape'))
    header['reserved'] = EDF.read(44).decode('unicode_escape')
    header['recordsNumber'] = int(EDF.read(8).decode('unicode_escape'))
    header['recordDuration'] = int(EDF.read(8).decode('unicode_escape'))
    header['signalsNumber'] = int(EDF.read(4).decode('unicode_escape'))
    header['labels'] = list(chunkPrint(EDF.read(header['signalsNumber']*16).decode('unicode_escape'), 16))
    header['transducers'] = list(chunkPrint(EDF.read(header['signalsNumber']*80).decode('unicode_escape'), 80))
    header['physDim'] = EDF.read(header['signalsNumber']*8).decode('unicode_escape')
    header['physMin'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['physMin'] = np.array(header['physMin'], dtype=np.float32)
    header['physMax'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['physMax'] = np.array(header['physMax'], dtype=np.float32)
    header['digMin'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['digMin'] = np.array(header['digMin'], dtype=np.float32)
    header['digMax'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['digMax'] = np.array(header['digMax'], dtype=np.float32)
    header['prefiltering'] = list(chunkPrint(EDF.read(header['signalsNumber']*80).decode('unicode_escape'), 80))
    header['samplesNumber'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['reserved2'] = list(chunkPrint(EDF.read(header['signalsNumber']*32).decode('unicode_escape'), 32))
    EDF.close() 
    EDF = open(EDFName, "rb")
    header['fullHeader'] = EDF.read(header['headerSize']).decode('unicode_escape')
    EDF.close()
    return header

def unzipEDF(EDFName, newEDFName, header):
    values=np.fromfile(EDFName,dtype='int8')
    values = values[header['headerSize']:]
    values = values+129
    Mud=EDF_mu_decode()
    values = Mud[values]
    x = np.arange(header['headerSize']/2)
    y=np.ones_like(x)
    values=np.concatenate((y, values), axis=None)
    values = np.array(values, dtype='<i2')
    values.tofile(newEDFName)
    EDF = open(newEDFName, "r") #TODO : supprimer ça
    EDF.close()
    fid = open(newEDFName, "r+")
    fid.write(header['fullHeader'])
    fid.close()
    return

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

def chunkPrint(string, length):
    return (string[0+i:length+i].strip() for i in range(0, len(string), length))

def EDF_mu_decode():
    # in C++ : 256 elements from 0 to 255
    # milieu = #129
    EDF_MuDecodingTable = np.array(np.zeros([257])) 
    EDF_MuDecodingTable[0]= -2048 
    EDF_MuDecodingTable[1]= -2016 
    EDF_MuDecodingTable[2]= -1952 
    EDF_MuDecodingTable[3]= -1888 
    EDF_MuDecodingTable [4]= -1824 
    EDF_MuDecodingTable [5]= -1760 
    EDF_MuDecodingTable [6]= -1696 
    EDF_MuDecodingTable [7]= -1632 
    EDF_MuDecodingTable [8]= -1568 
    EDF_MuDecodingTable [9]= -1504 
    EDF_MuDecodingTable [10]= -1440 
    EDF_MuDecodingTable [11]= -1376 
    EDF_MuDecodingTable [12]= -1312 
    EDF_MuDecodingTable [13]= -1248 
    EDF_MuDecodingTable [14]= -1184 
    EDF_MuDecodingTable [15]= -1120 
    EDF_MuDecodingTable [16]= -1040 
    EDF_MuDecodingTable [17]= -1008 
    EDF_MuDecodingTable [18]=  -976 
    EDF_MuDecodingTable [19]=  -944 
    EDF_MuDecodingTable [20]=  -912 
    EDF_MuDecodingTable [21]=  -880 
    EDF_MuDecodingTable [22]=  -848 
    EDF_MuDecodingTable [23]=  -816 
    EDF_MuDecodingTable [24]=  -784 
    EDF_MuDecodingTable [25]=  -752 
    EDF_MuDecodingTable [26]=  -720 
    EDF_MuDecodingTable [27]=  -688 
    EDF_MuDecodingTable [28]=  -656 
    EDF_MuDecodingTable [29]=  -624 
    EDF_MuDecodingTable [30]=  -592 
    EDF_MuDecodingTable [31]=  -560 
    EDF_MuDecodingTable [32]=  -520 
    EDF_MuDecodingTable [33]=  -504 
    EDF_MuDecodingTable [34]=  -488 
    EDF_MuDecodingTable [35]=  -472 
    EDF_MuDecodingTable [36]=  -456 
    EDF_MuDecodingTable [37]=  -440 
    EDF_MuDecodingTable [38]=  -424 
    EDF_MuDecodingTable [39]=  -408 
    EDF_MuDecodingTable [40]=  -392 
    EDF_MuDecodingTable [41]=  -376 
    EDF_MuDecodingTable [42]=  -360 
    EDF_MuDecodingTable [43]=  -344 
    EDF_MuDecodingTable [44]=  -328 
    EDF_MuDecodingTable [45]=  -312 
    EDF_MuDecodingTable [46]=  -296 
    EDF_MuDecodingTable [47]=  -280 
    EDF_MuDecodingTable [48]=  -260 
    EDF_MuDecodingTable [49]=  -252 
    EDF_MuDecodingTable [50]=  -244 
    EDF_MuDecodingTable [51]=  -236 
    EDF_MuDecodingTable [52]=  -228 
    EDF_MuDecodingTable [53]=  -220 
    EDF_MuDecodingTable [54]=  -212 
    EDF_MuDecodingTable [55]=  -204 
    EDF_MuDecodingTable [56]=  -196 
    EDF_MuDecodingTable [57]=  -188 
    EDF_MuDecodingTable [58]=  -180 
    EDF_MuDecodingTable [59]=  -172 
    EDF_MuDecodingTable [60]=  -164 
    EDF_MuDecodingTable [61]=  -156 
    EDF_MuDecodingTable [62]=  -148 
    EDF_MuDecodingTable [63]=  -140 
    EDF_MuDecodingTable [64]=  -130 
    EDF_MuDecodingTable [65]=  -126 
    EDF_MuDecodingTable [66]=  -122 
    EDF_MuDecodingTable [67]=  -118 
    EDF_MuDecodingTable [68]=  -114 
    EDF_MuDecodingTable [69]=  -110 
    EDF_MuDecodingTable [70]=  -106 
    EDF_MuDecodingTable [71]=  -102 
    EDF_MuDecodingTable [72]=   -98 
    EDF_MuDecodingTable [73]=   -94 
    EDF_MuDecodingTable [74]=   -90 
    EDF_MuDecodingTable [75]=   -86 
    EDF_MuDecodingTable [76]=   -82 
    EDF_MuDecodingTable [77]=   -78 
    EDF_MuDecodingTable [78]=   -74 
    EDF_MuDecodingTable [79]=   -70 
    EDF_MuDecodingTable [80]=   -65 
    EDF_MuDecodingTable [81]=   -63 
    EDF_MuDecodingTable [82]=   -61 
    EDF_MuDecodingTable [83]=   -59 
    EDF_MuDecodingTable [84]=   -57 
    EDF_MuDecodingTable [85]=   -55 
    EDF_MuDecodingTable [86]=   -53 
    EDF_MuDecodingTable [87]=   -51 
    EDF_MuDecodingTable [88]=   -49 
    EDF_MuDecodingTable [89]=   -47 
    EDF_MuDecodingTable [90]=   -45 
    EDF_MuDecodingTable [91]=   -43 
    EDF_MuDecodingTable [92]=   -41 
    EDF_MuDecodingTable [93]=   -39 
    EDF_MuDecodingTable [94]=   -37 
    EDF_MuDecodingTable [95]=   -35 
    EDF_MuDecodingTable [96]=   -32 
    EDF_MuDecodingTable [97]=   -31 
    EDF_MuDecodingTable [98]=   -30 
    EDF_MuDecodingTable [99]=   -29 
    EDF_MuDecodingTable [100]=   -28 
    EDF_MuDecodingTable [101]=   -27 
    EDF_MuDecodingTable [102]=   -26 
    EDF_MuDecodingTable [103]=   -25 
    EDF_MuDecodingTable [104]=   -24 
    EDF_MuDecodingTable [105]=   -23 
    EDF_MuDecodingTable [106]=   -22 
    EDF_MuDecodingTable [107]=   -21 
    EDF_MuDecodingTable [108]=   -20 
    EDF_MuDecodingTable [109]=   -19 
    EDF_MuDecodingTable [110]=   -18 
    EDF_MuDecodingTable [111]=   -17 
    EDF_MuDecodingTable [112]=   -16 
    EDF_MuDecodingTable [113]=   -15 
    EDF_MuDecodingTable [114]=   -14 
    EDF_MuDecodingTable [115]=   -13 
    EDF_MuDecodingTable [116]=   -12 
    EDF_MuDecodingTable [117]=   -11 
    EDF_MuDecodingTable [118]=   -10 
    EDF_MuDecodingTable [119]=    -9 
    EDF_MuDecodingTable [120]=    -8 
    EDF_MuDecodingTable [121]=    -7 
    EDF_MuDecodingTable [122]=    -6 
    EDF_MuDecodingTable [123]=    -5 
    EDF_MuDecodingTable [124]=    -4 
    EDF_MuDecodingTable [125]=    -3 
    EDF_MuDecodingTable [126]=    -2 
    EDF_MuDecodingTable [127]=    -1 
    EDF_MuDecodingTable [128]=     0 
    EDF_MuDecodingTable [129]=     1 
    EDF_MuDecodingTable [130]=     2 
    EDF_MuDecodingTable [131]=     3 
    EDF_MuDecodingTable [132]=     4 
    EDF_MuDecodingTable [133]=     5 
    EDF_MuDecodingTable [134]=     6 
    EDF_MuDecodingTable [135]=     7 
    EDF_MuDecodingTable [136]=     8 
    EDF_MuDecodingTable [137]=     9 
    EDF_MuDecodingTable [138]=    10 
    EDF_MuDecodingTable [139]=    11 
    EDF_MuDecodingTable [140]=    12 
    EDF_MuDecodingTable [141]=    13 
    EDF_MuDecodingTable [142]=    14 
    EDF_MuDecodingTable [143]=    15 
    EDF_MuDecodingTable [144]=    16 
    EDF_MuDecodingTable [145]=    17 
    EDF_MuDecodingTable [146]=    18 
    EDF_MuDecodingTable [147]=    19 
    EDF_MuDecodingTable [148]=    20 
    EDF_MuDecodingTable [149]=    21 
    EDF_MuDecodingTable [150]=    22 
    EDF_MuDecodingTable [151]=    23 
    EDF_MuDecodingTable [152]=    24 
    EDF_MuDecodingTable [153]=    25 
    EDF_MuDecodingTable [154]=    26 
    EDF_MuDecodingTable [155]=    27 
    EDF_MuDecodingTable [156]=    28 
    EDF_MuDecodingTable [157]=    29 
    EDF_MuDecodingTable [158]=    30 
    EDF_MuDecodingTable [159]=    31 
    EDF_MuDecodingTable [160]=    32 
    EDF_MuDecodingTable [161]=    35 
    EDF_MuDecodingTable [162]=    37 
    EDF_MuDecodingTable [163]=    39 
    EDF_MuDecodingTable [164]=    41 
    EDF_MuDecodingTable [165]=    43 
    EDF_MuDecodingTable [166]=    45 
    EDF_MuDecodingTable [167]=    47 
    EDF_MuDecodingTable [168]=    49 
    EDF_MuDecodingTable [169]=    51 
    EDF_MuDecodingTable [170]=    53 
    EDF_MuDecodingTable [171]=    55 
    EDF_MuDecodingTable [172]=    57 
    EDF_MuDecodingTable [173]=    59 
    EDF_MuDecodingTable [174]=    61 
    EDF_MuDecodingTable [175]=    63 
    EDF_MuDecodingTable [176]=    65 
    EDF_MuDecodingTable [177]=    70 
    EDF_MuDecodingTable [178]=    74 
    EDF_MuDecodingTable [179]=    78 
    EDF_MuDecodingTable [180]=    82 
    EDF_MuDecodingTable [181]=    86 
    EDF_MuDecodingTable [182]=    90 
    EDF_MuDecodingTable [183]=    94 
    EDF_MuDecodingTable [184]=    98 
    EDF_MuDecodingTable [185]=   102 
    EDF_MuDecodingTable [186]=   106 
    EDF_MuDecodingTable [187]=   110 
    EDF_MuDecodingTable [188]=   114 
    EDF_MuDecodingTable [189]=   118 
    EDF_MuDecodingTable [190]=   122 
    EDF_MuDecodingTable [191]=   126 
    EDF_MuDecodingTable [192]=   130 
    EDF_MuDecodingTable [193]=   140 
    EDF_MuDecodingTable [194]=   148 
    EDF_MuDecodingTable [195]=   156 
    EDF_MuDecodingTable [196]=   164 
    EDF_MuDecodingTable [197]=   172 
    EDF_MuDecodingTable [198]=   180 
    EDF_MuDecodingTable [199]=   188 
    EDF_MuDecodingTable [200]=   196 
    EDF_MuDecodingTable [201]=   204 
    EDF_MuDecodingTable [202]=   212 
    EDF_MuDecodingTable [203]=   220 
    EDF_MuDecodingTable [204]=   228 
    EDF_MuDecodingTable [205]=   236 
    EDF_MuDecodingTable [206]=   244 
    EDF_MuDecodingTable [207]=   252 
    EDF_MuDecodingTable [208]=   260 
    EDF_MuDecodingTable [209]=   280 
    EDF_MuDecodingTable [210]=   296 
    EDF_MuDecodingTable [211]=   312 
    EDF_MuDecodingTable [212]=   328 
    EDF_MuDecodingTable [213]=   344 
    EDF_MuDecodingTable [214]=   360 
    EDF_MuDecodingTable [215]=   376 
    EDF_MuDecodingTable [216]=   392 
    EDF_MuDecodingTable [217]=   408 
    EDF_MuDecodingTable [218]=   424 
    EDF_MuDecodingTable [219]=   440 
    EDF_MuDecodingTable [220]=   456 
    EDF_MuDecodingTable [221]=   472 
    EDF_MuDecodingTable [222]=   488 
    EDF_MuDecodingTable [223]=   504 
    EDF_MuDecodingTable [224]=   520 
    EDF_MuDecodingTable [225]=   560 
    EDF_MuDecodingTable [226]=   592 
    EDF_MuDecodingTable [227]=   624 
    EDF_MuDecodingTable [228]=   656 
    EDF_MuDecodingTable [229]=   688 
    EDF_MuDecodingTable [230]=   720 
    EDF_MuDecodingTable [231]=   752 
    EDF_MuDecodingTable [232]=   784 
    EDF_MuDecodingTable [233]=   816 
    EDF_MuDecodingTable [234]=   848 
    EDF_MuDecodingTable [235]=   880 
    EDF_MuDecodingTable [236]=   912 
    EDF_MuDecodingTable [237]=   944 
    EDF_MuDecodingTable [238]=   976 
    EDF_MuDecodingTable [239]=  1008 
    EDF_MuDecodingTable [240]=  1040 
    EDF_MuDecodingTable [241]=  1120 
    EDF_MuDecodingTable [242]=  1184 
    EDF_MuDecodingTable [243]=  1248 
    EDF_MuDecodingTable [244]=  1312 
    EDF_MuDecodingTable [245]=  1376 
    EDF_MuDecodingTable [246]=  1440 
    EDF_MuDecodingTable [247]=  1504 
    EDF_MuDecodingTable [248]=  1568 
    EDF_MuDecodingTable [249]=  1632 
    EDF_MuDecodingTable [250]=  1696 
    EDF_MuDecodingTable [251]=  1760 
    EDF_MuDecodingTable [252]=  1824 
    EDF_MuDecodingTable [253]=  1888 
    EDF_MuDecodingTable [254]=  1952 
    EDF_MuDecodingTable [255]=  2016  
    EDF_MuDecodingTable[256]= 2048 
    return EDF_MuDecodingTable



