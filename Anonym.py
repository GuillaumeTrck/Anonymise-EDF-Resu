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
    resu.seek(144)
    sss = "x" * 22
    resu.write(sss)
    resu.seek(1922)
    sss = "x" * 87
    resu.write(sss)
    resu.close()
    print(resu)
    return      

def UnAnonymiseEDF(EDFName, FichierTxt):                      #fonction permettant de d�anonymiser les donn�es du patient du fichier EDF
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

def UnAnonymiseResu(resuName, RawFileName, resuText ):      #fonction permettant de d�anonymiser les donn�es du patient du fichier resu
    print("iunAnonymiseresu")
    resu=open(resuName,'r+' )
    resu.seek(144)
    resu.write(RawFileName)
    resu.seek(1922)
    resu.write(resuText)
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
    
                
    
