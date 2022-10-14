import numpy as np
from Anonym import *
import glob
import argparse
from utils import *

initLogs("LogsAnonyme.txt")
parser=argparse.ArgumentParser(description='Anomyse/Unanomyse EDF and resu')
parser.add_argument('-f','--file',required=True,help="File with EDF and resu")
parser.add_argument('-a','--anomyse', required=False,action="store_true", help="Anomyse edf and resu")
parser.add_argument('-d','--EDFData', required=False, help="Edf data text name")
parser.add_argument('-v','--resuData', required=False, help="resu data text name")
parser.add_argument('-u','--unAnomyse', required=False,action="store_true", help="Unanomyse edf and resu")

args=parser.parse_args()


anomyse=args.anomyse
unAnomyse=args.unAnomyse
file=args.file
os.chdir(file)

if args.EDFData:
    EDFData=args.EDFData
else:
    try:
        EDFData="EDFDatadefault.txt"
        fid=open(EDFData,'a')
        fid.close()
    except:
        printLogs("Le fichier txt n'a pas été créé")

if args.resuData:
    resuData=args.resuData
else:
    try:
        resuData="resuDataDefault.txt"
        fid=open(resuData,'a')
        fid.close()
    except:
        printLogs("Le fichier txt n'a pas été créé")


#6 unanonymiser edf et resu (nom et données)
def UN():    
    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")

    try:
        matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
        matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except:
        printLogs("Les matrices EDF et resu ne sont pas chargées")

    
    for i in range(len(EDFList)):

        #1 récupérer ID du fichier
        
        
        EDFAnonymeName=EDFList[i]
        EDFAnonymeName=EDFAnonymeName.replace(".EDF","")
        IDFichierAnonyme=EDFAnonymeName[10:]
        #2 voir où se trouve le fichier dans datafile
        print(IDFichierAnonyme)
        print(matriceEDF)
        
        pos=CheckInDataFile(matriceEDF,IDFichierAnonyme)
        
        
        #3 changer les noms anonymes et les données des edf et resu
        terminasonEDF='.EDF'
        terminaisonResu='.resu'
        originalEDFName=glob.glob('RawAnonyme'+IDFichierAnonyme+terminasonEDF)
        originalResuName=glob.glob('resuAnonyme'+IDFichierAnonyme+terminaisonResu)
        print(originalEDFName)
        print(originalResuName)
        print(pos)
        pos=int(pos)
        originalsNames=ChangeAnonymeToName(originalResuName[0],originalEDFName[0], matriceEDF,matriceresu,pos)
        print(originalsNames[0])
        print(originalsNames[1])
        UnAnonymiseEDF(originalsNames[1],matriceEDF,pos)
        UnAnonymiseResu(originalsNames[0],matriceresu,pos)
        pos=int(pos)
        print(pos)
    return

def AN():    

    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")
    print(type(resuList))
    print(resuList)
    print(EDFList)

    test=FirstLineEDF(EDFData)

    try:
        test1=FirstLineresu(resuData)
    except:
        printLogs("Problème chargement resuData")

    if test and test1:
        ID = 1
    else :
        ID = CheckID(EDFData,resuData)

    for resu in resuList:
        var=saveDataresu(resu,resuData,ID)
        if var:
            
            #1. récupérer edfname
            print(resu)
            try:
                fid = open(resu, "rb")
            except:
                printLogs("Problème ouverture resu") 

            fid.seek(144)
            RawFileName= fid.read(22).decode('unicode_escape')
            RawFileNameStrip=RawFileName.replace(" ","")
            fid.close()
            
            #2. trouver l'edf 
            term='.EDF'
            RawFileNameStripTerm=RawFileNameStrip + term
            EDFName=glob.glob(RawFileNameStripTerm)
            print(EDFName)
            #3 savedataedf
            saveDataEDF(RawFileNameStripTerm,EDFData,ID)
        
            #4 Anonymise edf et resu (nom et données)
            print(RawFileNameStripTerm)
            print(resu)

            try:
                AnonymiseEDF(RawFileNameStripTerm)
            except:
                printLogs("Problème anonymisation EDF")
            
            try:
                AnonymiseResu(resu)
            except:
                printLogs("Problème anonymisation resu")

            anonymeNames=ChangeNameToAnonyme(resu,RawFileNameStripTerm,ID)
            #5 incrémenter l'ID
            ID=int(ID)
            ID=ID+1
        
    return

if (args.unAnomyse):
    UN()

elif(args.anomyse):
    AN()


