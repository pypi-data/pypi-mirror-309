import tinysync
from .aliBackend import Aliyunpan
import os 
import time 


class Sync():

    def __init__(self,localDir:str,aliDir:str):
        self.localDir = localDir
        self.aliDir = aliDir

    def run(self):
        localDir = self.localDir.rstrip('/')
        aliDir = self.aliDir.rstrip('/')
        if not os.path.exists(localDir):
            raise Exception(f"本地文件夹{localDir}不存在")
        b1 = tinysync.backend.LocalFS(dirPath=localDir)
        b2 = Aliyunpan(dirPath=aliDir) 
        tinysync.syncronization(b1,b2) 

    def auto(self,syncCycleSec=120):
        while True:
            self.run()
            time.sleep(syncCycleSec)





    