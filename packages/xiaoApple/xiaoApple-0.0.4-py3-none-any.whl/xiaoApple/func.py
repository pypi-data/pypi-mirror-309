import tinysync
from .aliBackend import Aliyunpan
import os 
import time 
import hashlib
from tinysync.backendMethods import BackendHandler
from .copyfiles import copy_missing_files


class Sync():

    def __init__(self,localDir:str,aliDir:str):
        self.localDir = localDir.rstrip('/')
        self.aliDir = aliDir.rstrip('/')
        self.syncConfig = tinysync.configuration 
        self.localBackend = tinysync.backend.LocalFS(dirPath=self.localDir)
        self.aliyunBackend = Aliyunpan(dirPath=aliDir) 
        self.localBackend.workdir = '.xiaoapple'
        self.aliyunBackend.workdir = '.xiaoapple'
        self.name = hashlib.md5(f"{self.localBackend.getSyncPath()}_{self.aliyunBackend.getSyncPath()}".encode()).hexdigest()[:5]

    def run(self):
        if not os.path.exists(self.localDir):
            raise Exception(f"本地文件夹{self.localDir}不存在")
        tinysync.syncronization(self.localBackend,self.aliyunBackend,Config=self.syncConfig)  

    def auto(self,syncCycleSec=120):
        while True:
            self.run()
            time.sleep(syncCycleSec)

    # def _getLocalInfo(self):
    #     local = tinysync.backend.LocalFS(dirPath=self.localDir) 
    #     bh = BackendHandler(backend=local,linkMode=2,workdir='') 
    #     backupDir = bh.getRemoteWorkDir() + "/" + 'backup' 
    #     logsDir = bh.getRemoteWorkDir() + "/" + 'logs'
    #     return {
    #         'backupDir':backupDir,
    #         'logsDir':logsDir,
    #     }

    def _getBackupDir(self):
        bh = BackendHandler(backend=self.localBackend,workdir='',syncConfig=self.syncConfig) 
        backupDir = os.path.join( self.localDir, *bh.getRemoteWorkDir().split("/"),  'backup' ) 
        return backupDir

    def listDelteBackups(self):
        backupDir = self._getBackupDir()
        backupDT = []
        if os.path.exists(backupDir):
            for dirName in os.listdir(backupDir):
                try:
                    backupDT.append( dirName.split("_"+self.name+"_")[0] )
                except:
                    pass 
        return backupDT
    
    def recoverBackup(self,dtStr:str):
        backupDir = self._getBackupDir()
        targetDir = os.path.join(backupDir,    dtStr+ "_"+self.name+"_A"  )
        if os.path.exists(targetDir):
            copy_missing_files(src_dir=targetDir,dest_dir=self.localDir) 
        else:
            print(f"target dir {targetDir} not exists") 

        








    