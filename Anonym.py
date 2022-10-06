import glob 
import numpy as np
#import pandas as pd
#from edf import *
#from resu import *
import sys
import os

def AnonymiseEDF(EDFName):                                  #fonction permettant d'anonymiser les donn�es du patient du fichier EDF
    EDF = open(EDFName, "r+")
    EDF.seek(8)                                             #replacer � partir du caract�re 8
    sss = "x" * 168
    EDF.write(sss)
    EDF.close()
    return 

def AnonymiseResu(resuName):                                #fonction permettant d'anonymiser les donn�es du patient du fichier resu                                     
    resu=open(resuName,'r+' )
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
                                         
def saveDataresu(resuName,resuData):
    dataFile = open(resuData, 'w')

    # Writting the first line
    dataFile.write("resuName/Date/Chambre/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID")
    dataFile.write('\n')

    # Writing data
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
    dataFile.write('ID')
    dataFile.close()

    return

def saveDataEDF(RawFileName, EDFData):
    dataFile = open(EDFData, 'w')

    # Writting the first line
    dataFile.write("EDF/EDFHeader/champs identification/Date/ID")
    dataFile.write('\n')

    # Writing data
    dataFile.write(RawFileName)
    dataFile.write('\t')
    EDF = open(RawFileName, "rb")                          
    EDF.read(8)
    EDFText = EDF.read(168).decode('unicode_escape')    
    EDF.close()
    dataFile.write(EDFText[0:80])
    dataFile.write('\t')
    dataFile.write(EDFText[80:160])
    dataFile.write('\t')
    dataFile.write(EDFText[152:168])
    dataFile.write('\t')
    dataFile.write('ID')
    dataFile.close()
    return

def ChangeNameToAnonyme(resuName,RawFileName):                       
    os.rename(resuName,'resuAnonyme.resu')                  
    os.rename(RawFileName,'RawAnonyme.EDF')
    return

def ChangeAnonymeToName(resuAnonyme,RawAnonyme, matriceEDF,matriceresu) :     
    os.rename(resuAnonyme,matriceresu[0][0])
    os.rename(RawAnonyme,matriceEDF[0][0])
    
                
    
