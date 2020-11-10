import hashlib ,os,time
from pathlib import Path
import subprocess
import psutil
import signal

def closepros():
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        psutil.Process(child.pid).terminate()

def main(files_hash,Ppid):
    while True:
        try:
            time.sleep(2)
            files_new_hash=check_hashs()
            if not (files_new_hash == files_hash):
                if Ppid != None:
                    current_process = psutil.Process()
                    children = current_process.children(recursive=True)
                    for child in children:
                        psutil.Process(child.pid).terminate()
                    print(Ppid.pid)
                    print("killing process")
                print("file was modified")
                files_hash=files_new_hash
                Ppid=subprocess.Popen("cordova run browser",shell=True)
                #pid=p.pid
        except KeyboardInterrupt:
            print('closing the program')
            closepros()
            os.kill(os.getpid(), signal.CTRL_C_EVENT)



def check_hashs():
    files_new_hash=[]
    for file in files:
        files_new_hash.append(calculateHash(file))
    return files_new_hash
        
def calculateHash(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

files=[]
files_hash=[]
Ppid=None
Ppid=subprocess.Popen("cordova run browser",shell=True)
for path in Path('www').rglob('*.*'):
    files_hash.append(calculateHash(path))
    files.append(path)
print(files)
files_new_hash = files_hash
main(files_hash,Ppid)

