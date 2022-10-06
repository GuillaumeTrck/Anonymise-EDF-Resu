import glob 
import numpy as np
#import pandas as pd
#from edf import *
#from resu import *
import sys
import os

def AnonymiseEDF(EDFName):                                  #fonction permettant d'anonymiser les donn�es du patient du fichier EDF
    EDF = open(EDFName, "rb")                               #r = read, + signifie �crire dedans et b en bit
    EDF.read(8)
    EDFText = EDF.read(160).decode('unicode_escape')        #telle lettre egal telle code en binaire (unicode)
    EDF.close() 
    EDF = open(EDFName, "r+")
    EDF.seek(8)                                             #replacer � partir du caract�re 8
    sss = "x" * 160
    EDF.write(sss)
    EDF.close()
    
    EDF = open(EDFName, "rb")
    EDF.read(168)
    EDFText1 = EDF.read(8).decode('unicode_escape')
    EDF.close() 
    EDF = open(EDFName, "r+")
    EDF.seek(168)
    sss = "x" *8
    EDF.write(sss)
    EDF.close()

    print("EDFTXT: ", EDFText)
    print("EDFTXT1: ", EDFText1)
    return EDFText,EDFText1

def AnonymiseResu(resuName):                                #fonction permettant d'anonymiser les donn�es du patient du fichier resu
    print("Anonymiseresu")                                      
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
    print(resu)

    # fid = open(resuName, "rb")                           #permet de verifier les diff infos anonymisees
    # resu = {}
    # fid.seek(48)
    # resu['Room'] = fid.read(4)
    # fid.seek(144)
    # resu['RawFileName'] = fid.read(22)
    # fid.seek(1922)
    # resu['FileNumber'] =  fid.read(22)
    # resu['Name'] =  fid.read(27)
    # resu['FirstName'] =  fid.read(27) 
    # resu['BirthDate'] =  fid.read(10)
    # resu['Sex'] =  fid.read(1)
    
    # print(resu['Room'])
    # print(resu['RawFileName'])
    # print(resu['FileNumber'])
    # print(resu['Name'])
    # print(resu['FirstName'])
    # print(resu['BirthDate'])
    # print(resu['Sex'])

    return      

def UnAnonymiseEDF(EDFName, FichierTxt):                    #fonction permettant de d�anonymiser les donn�es du patient du fichier EDF
    matrice=np.loadtxt(FichierTxt,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    print(matrice[0][2])
    EDF = open(EDFName, "r+")
    EDF.seek(8)
    EDF.write(matrice[0][2])
    EDF.seek(31)
    EDF.write(" "*49)
    EDF.seek(80)
    EDF.write(matrice[0][3])
    EDF.seek(140)
    EDF.write(" "*28)
    EDF.seek(168)
    EDF.write(matrice[0][4])
    EDF.close()

def UnAnonymiseResu(resuName,FichierTxt):                   #fonction permettant de d�anonymiser les donn�es du patient du fichier resu
    matrice=np.loadtxt(FichierTxt,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    print(matrice[0][3])
    print(matrice[0][4])
    print(matrice[0][5])
    print(matrice[0][6])
    print(matrice[0][7])
    print(matrice[0][8])
    print(matrice[0][9])
    print(matrice[0][10])
  
    resu=open(resuName,'r+' )
    resu.seek(24)
    resu.write(matrice[0][4])
    resu.seek(48)
    resu.write(matrice[0][5])
    resu.seek(144)
    resu.write(matrice[0][1])
    resu.seek(1922)
    resu.write(matrice[0][6])
    resu.seek(1944)
    resu.write(matrice[0][7])
    resu.seek(1971)
    resu.write(matrice[0][8])
    resu.seek(1998)
    resu.write(matrice[0][9])
    resu.seek(2008)
    resu.write(matrice[0][10])
    resu.close() 
    return

def saveData(resuName,RawFileName,resuText):                #fonction permettant de sauvegarder les donn�es dans un .txt
    dataName = resuText+'.txt'                              #cr�e un fichier txt si non existant
    dataFile = open(dataName, 'w')                          #w pour whrite, v�rifier si avec w le programme cr�e un fichier texte
    dataFile.write("resu")
    dataFile.write("\t"*5)
    dataFile.write("EDF")
    dataFile.write("\t"*4)
    dataFile.write("EDFHeader")
    dataFile.write("\t"*4)
    dataFile.write("Champs identification")
    dataFile.write("\t"*11)
    dataFile.write("Date")
    dataFile.write("\t"*2)
    dataFile.write("Chambre")
    dataFile.write("\t"*2)
    dataFile.write("FileNumber")
    dataFile.write("\t"*2)
    dataFile.write("Name")
    dataFile.write("\t"*2)
    dataFile.write("FirstName")
    dataFile.write("\t"*2)
    dataFile.write("BirthDate")
    dataFile.write("\t"*2)
    dataFile.write("Sex")
    dataFile.write("\t"*2)
    dataFile.write("ID")
    dataFile.write('\n')
    
    dataFile.write(resuName) 
    dataFile.write('\t')                                    #aller � la ligne \t faire un tab 
    dataFile.write(RawFileName)
    dataFile.write('\t')

    EDF = open(RawFileName, "rb")       #Permet de prendre les infos du fichier EDF                    
    EDF.read(8)
    EDFText = EDF.read(168).decode('unicode_escape')    
    EDF.close()
    dataFile.write(EDFText[0:23])
    dataFile.write('\t')
    dataFile.write(EDFText[80:140])
    dataFile.write('\t')
    dataFile.write(EDFText[160:168])
    dataFile.write('\t')

    fid = open(resuName, "rb")                           
    resu = {}
    fid.seek(48)
    resu['Room'] = fid.read(4).decode('unicode_escape')  
    dataFile.write(resu['Room'])
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
    dataFile.write('ID 1')
    dataFile.close()


    return

def ChangeNameToAnonyme(resuName,RawFileName):                       #fonction permettant d'anonymiser le nom du fichier resu et EDF
    os.rename(resuName,'resuAnonyme.resu')                  #Ne pas mettre resuName entre quote
    os.rename(RawFileName,'RawAnonyme.EDF')
    return

def ChangeAnonymeToName(FichierTxt,resuAnonyme,RawAnonyme) :     #remettre en param�tre resuAnonyme et RawAnonyme
    matrice=np.loadtxt(FichierTxt,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    # print(matrice.shape)
    # print(matrice[0][0])
    # print(matrice[0][1])
    
    os.rename(resuAnonyme,matrice[0][0])
    os.rename(RawAnonyme,matrice[0][1])
    
                
    
