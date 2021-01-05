import hashlib ,os,time
from pathlib import Path
import subprocess
import psutil
import signal
#this function will close any opened process wile executing the cordova run borwser command
def closepros():
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        psutil.Process(child.pid).terminate()
#this is the main program wich is responsable for testing file changes it get's tow paramater 
#the first one is the files_hash variable wich is a list of files hash in that spesific diractory 
def main(files_hash,Ppid):
    while True:
        try:
            time.sleep(2)
            files_new_hash=check_hashs()
            #if any file hash has been changed wich means if any file is modified the folwin block of code will be executed
            
            if not (files_new_hash == files_hash):
                if Ppid != None:
                    current_process = psutil.Process()
                    #this will get all prossec cheldren started by the python sheel and we mean by that all 
                    #the cmd started by the cordova run browser comand 
                    children = current_process.children(recursive=True)
                    for child in children:
                        psutil.Process(child.pid).terminate()
                    print(Ppid.pid)
                    print("killing process")
                print("file was modified")
                files_hash=files_new_hash
                #after killing the process we can start a new one now 
                #and the reason for that to have the same port number 
                #and not adding more port number 
                Ppid=subprocess.Popen("cordova run browser",shell=True)
                #pid=p.pid
        #this exception will close the program and all of the process started with it 
        except KeyboardInterrupt:
            print('closing the program')
            closepros()
            os.kill(os.getpid(), signal.CTRL_C_EVENT)


#this function will check if the files hashs is changed 
def check_hashs():
    files_new_hash=[]
    for file in files:
        files_new_hash.append(calculateHash(file))
    return files_new_hash

#this function will calculate the file hashes   
def calculateHash(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

#liste of files 
files=[]
files_hash=[]
#the current running process id
Ppid=None
Ppid=subprocess.Popen("cordova run browser",shell=True)
for path in Path('www').rglob('*.*'):
    files_hash.append(calculateHash(path))
    files.append(path)
print(files)
files_new_hash = files_hash
main(files_hash,Ppid)

