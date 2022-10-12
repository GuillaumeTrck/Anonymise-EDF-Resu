import glob
from itertools import count
from re import I
from tokenize import Double
from xmlrpc.client import boolean 
import numpy as np
#import pandas as pd
#from edf import *
#from resu import *
import sys
import os
import argparse

def AnonymiseEDF(EDFName):                                  #fonction permettant d'anonymiser les donn�es du patient du fichier EDF
    x='xxxxxxxxxxxxxxxxxxxxxx.EDF'
    if x in EDFName:
        print("Fichier EDF déjà anonyme")
    else:
        EDF = open(EDFName, "r+")
        EDF.seek(8)                                             #replacer � partir du caract�re 8
        sss = "x" * 168
        EDF.write(sss)
        EDF.close()
    return 

def AnonymiseResu(resuName):                                #fonction permettant d'anonymiser les donn�es du patient du fichier resu                                     
    x='resuAnonyme'
    if x in resuName:
        print("Fichier resu déjà anonyme")
    else:
        resu=open(resuName,'r+')
        resu.seek(24)                                           #anonymise la date
        sss = "x"*10
        resu.write(sss)
        resu.seek(48)                                           #anonymise la chambre
        sss="x"*4
        resu.write(sss)
        resu.seek(144)
        sss = "x" * 22
        resu.write(sss)
        resu.seek(1922)
        sss = "x" * 87
        resu.write(sss)
        resu.close()
    return      

def UnAnonymiseEDF(EDFName,matriceEDF):                    #fonction permettant de d�anonymiser les donn�es du patient du fichier EDF
    EDF = open(EDFName, "r+")
    A = [8,80,160]
    for i in range(len(A)):
        EDF.seek(A[i])
        EDF.write(matriceEDF[0][i+1])
    EDF.close()
    return

def UnAnonymiseResu(resuName,matriceresu):                   #fonction permettant de d�anonymiser les donn�es du patient du fichier resu
    resu=open(resuName,'r+')
    A = [24, 48, 144, 1922, 1944, 1971, 1998, 2008,2009] #liste contenant le début des éléments d'intérêt dans le resu. 
    for i in range(len(A)):
        resu.seek(A[i])
        resu.write(matriceresu[0][i+1])
    resu.close() 
    return
                                         
def saveDataresu(resuName,resuData,ID):
    x='resuAnonyme'
    matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    y=resuName
    print(y)
    if x in resuName:
        print("Fichier resu déjà sauvé")
    elif y in matriceresu:
        print("Fichier resu déjà sauvé")
    else:
    # Writing data
        print("J'ai bien sauvé les données")
        dataFile = open(resuData, 'a')
        dataFile.write(resuName) 
        dataFile.write('\t')
        fid = open(resuName, "rb")                           
        resu = {}
        fid.seek(24)
        resu['ExamDate'] = fid.read(10).decode('unicode_escape')
        dataFile.write(resu['ExamDate'])
        dataFile.write('\t')
        fid.seek(48)
        resu['Room'] = fid.read(4).decode('unicode_escape')  
        dataFile.write(resu['Room'])
        dataFile.write('\t')
        fid.seek(144)
        resu['RawFileName'] = fid.read(22).decode('unicode_escape') 
        dataFile.write(resu['RawFileName'])
        dataFile.write('\t')
        fid.seek(1922)
        resu['FileNumber'] =  fid.read(22).decode('unicode_escape')  
        dataFile.write(resu['FileNumber'])
        dataFile.write('\t')
        resu['Name'] =  fid.read(27).decode('unicode_escape')  
        dataFile.write(resu['Name'])
        dataFile.write('\t')
        resu['FirstName'] =  fid.read(27).decode('unicode_escape')  
        dataFile.write(resu['FirstName']) 
        dataFile.write('\t')
        resu['BirthDate'] =  fid.read(10).decode('unicode_escape')  
        dataFile.write(resu['BirthDate'])
        dataFile.write('\t')
        resu['Sex'] = fid.read(1).decode('unicode_escape')
        dataFile.write(resu['Sex'])
        dataFile.write('\t')
        dataFile.write(str(ID))
        dataFile.write('\n')
        fid.close()
        dataFile.close()

    return

def saveDataEDF(RawFileName, EDFData,ID):
    x='xxxxxxxxxxxxxxxxxxxxxx.EDF'
    y=RawFileName
    matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    if x in RawFileName:
        print("Fichier EDF déjà sauvé")
    elif y in matriceEDF:
        print("Fichier EDF déjà sauvé")
    else:
    # Writing data
        dataFile = open(EDFData, "a")
        dataFile.write(RawFileName)
        dataFile.write('\t')
        EDF = open(RawFileName, "rb")                          
        EDF.read(8)
        EDFText = EDF.read(168).decode('unicode_escape')    
        EDF.close()
        dataFile.write(EDFText[0:80])
        dataFile.write(EDFText[80:160])
        dataFile.write('\t')
        dataFile.write(EDFText[152:168])
        dataFile.write('\t')
        dataFile.write(str(ID))
        dataFile.write('\n')
        dataFile.close()

    return

def FirstLineEDF(EDFData):

    dataFile = open(EDFData, 'rb')
    ligne1=dataFile.readlines(1)

    # Writting the first line
    if not ligne1:    
        dataFile = open(EDFData, 'w')
        dataFile.write("EDF/EDFHeader/champs identification/Date/ID")
        dataFile.write('\n')
        dataFile.close()

        return True
    else:
        return False 

def FirstLineresu(resuData):

    dataFile = open(resuData, 'rb')
    ligne2=dataFile.readlines(1)

    # Writting the first line
    if not ligne2:
        dataFile = open(resuData, 'w')
        dataFile.write("resuName/Date/Chambre/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID")
        dataFile.write('\n')
        dataFile.close()
        
        return True
    else:
        return False 

def CheckID():

    matriceEDFID=np.loadtxt("EDFData.txt",delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=3,ndmin=2)
    print(matriceEDFID)
    print(max(matriceEDFID))
    EDFID = int(max(matriceEDFID) +1)

    matriceresuID=np.loadtxt("resuData.txt",delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=9,ndmin=2)
    print(matriceresuID)
    print(max(matriceresuID))
    resuID = int(max(matriceresuID) +1)

    return max([EDFID,resuID])   

def ChangeNameToAnonyme(resuName, rawFileName, ID): 
    
    print(resuName)
    print(rawFileName)
    x='resuAnonyme'
    if x in resuName:
        print("Noms resu déjà anonyme")
        return
    else:
        resuAnonymeFileName="resuAnonyme{0}.resu".format(ID)                      
        os.rename(resuName,resuAnonymeFileName)   
        rawAnonymeFileName = "RawAnonyme{0}.EDF".format(ID)               
        os.rename(rawFileName,rawAnonymeFileName)
        print("J'ai bien changé le nom")
    return [resuAnonymeFileName,rawAnonymeFileName]

def ChangeAnonymeToName(resuAnonyme,rawAnonyme, matriceEDF,matriceresu,i) :

    resuFileName=matriceresu[i][0]
    print(type(resuFileName))
    os.rename(resuAnonyme,resuFileName)
    EDFFileName=matriceEDF[i][0]
    print(type(EDFFileName))
    os.rename(rawAnonyme,EDFFileName)

    return [resuFileName,EDFFileName] 

def CheckInDataFile(matriceEDF,IDFichierAnonyme):
    i=np.where(matriceEDF==IDFichierAnonyme)
    print("i= {}".format(i))
    return i[0]
