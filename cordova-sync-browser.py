import hashlib ,os,time
from pathlib import Path
import http.server
import socketserver
import subprocess



def main(files_hash):
    Ppid=None
    while True:
        time.sleep(2)
        print("testing")
        files_new_hash=check_hashs()
        if not (files_new_hash == files_hash):
            if Ppid != None:
                os.killpg(os.getpgid(Ppid.pid), signal.SIGTERM)
            print("file was modified")
            files_hash=files_new_hash
            Ppid=subprocess.Popen("cordova run browser",shell=True)
            #pid=p.pid


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
for path in Path('../www').rglob('*.*'):
    files_hash.append(calculateHash(path))
    files.append(path)
files_new_hash = files_hash
main(files_hash)
"""PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()"""

