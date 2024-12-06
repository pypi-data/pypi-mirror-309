
from tinysync.backend.abc import Backend as baseBackend
from aligo import Aligo
import datetime 
import logging
import os 
from pathlib import Path,PurePosixPath
from collections import defaultdict


from typing import List
from aligo import Aligo, BatchRequest, BatchSubRequest


class _AligoWithDelete(Aligo):
    """自定义 aligo """
    V3_FILE_DELETE = '/v3/file/delete'

    def delete_file(self, file_id: str, drive_id: str = None) -> bool:
        """删除文件"""
        drive_id = drive_id or self.default_drive_id
        response = self.post(self.V3_FILE_DELETE, body={
            'drive_id': drive_id,
            'file_id': file_id
        })
        return response.status_code == 204

    def batch_delete_files(self, file_id_list: List[str], drive_id: str = None):
        """批量删除文件"""
        drive_id = drive_id or self.default_drive_id
        result = self.batch_request(BatchRequest(
            requests=[BatchSubRequest(
                id=file_id,
                url='/file/delete',
                body={
                    'drive_id': drive_id,
                    'file_id': file_id
                }
            ) for file_id in file_id_list]
        ), dict)
        return list(result)

    def clear_recyclebin(self, drive_id: str = None):
        """清空回收站"""
        drive_id = drive_id or self.default_drive_id
        response = self.post('/v2/recyclebin/clear', body={
            'drive_id': drive_id
        })
        return response.status_code == 202





class Aliyunpan(baseBackend):

    def __init__(self,dirPath):
        super().__init__()
        self.dirPath = dirPath
        if self.dirPath.endswith("/"):
            self.dirPath = self.dirPath[:-1] 
        if self.dirPath in ("","."):
            self.prefix = "" 
        else:
            self.prefix = self.dirPath + "/" 
        self.ali = _AligoWithDelete()
        self.idPath = {"":'root'}
        self._UploadQueue = {}
        self._DownloadQueue = {}
        self._setDirPathID(self.dirPath) 

    def __del__(self):
        self.cleanQueue() 

    def _setDirPathID(self,absPath): 
        if absPath in self.idPath:return  
        segs = [s for s in absPath.split("/") if len(s) > 0 ] 
        fdir,name = "/".join(segs[:-1]),segs[-1]
        self._setDirPathID(fdir) 
        listed = [ item['name'] for item in self._absPathlistPath(fdir)]
        if name not in listed:
            pid = self.idPath[fdir]
            res = self.ali.create_folder(parent_file_id=pid,name= name ,check_name_mode='refuse' )
            file_id = getattr(res,'file_id',None) 
            if file_id is None:
                raise Exception(f"cannot return file_id for a created directory at {absPath}")
            self.idPath[absPath] = file_id 


    def getSyncPath(self)->str:
        """print path position 

        Returns:
            str: _description_
        """        
        return "aliyunpan" + self.dirPath
    
    def _geValidPath(self,path):
        if path in ("","."):
            return self.dirPath
        else:
            return   self.prefix + "/".join([s for s in path.split("/") if len(s) > 0]) 
    
    def _absPath_dir_name(self,rpath):
        p = self.prefix + rpath
        segs = [ s for s in p.split("/") if len(s)>0 ] 
        if len(segs) == 0:
            return "","" 
        elif len(segs) == 1:
            return "",segs[0]
        else:
            return "/".join(segs[:-1]),segs[-1]



    def _absPathlistPath(self,abspath:str,mtime:bool=True,hash:bool=False)->list[ dict ]:
        """list files and directories (not recursively) in a given (relative) path. 

        Args:
            rpath (_type_): relative path , example: rpath = "this/path", rpath = "" 
            mtime (bool, optional): contains mtime or not.
            hash (bool, optional): contains hash value or not.

        Returns:
            list[ dict ]: dict = { "Size":int, "name":str,  "mtime":float, 'type':'d'/'f'/'l',  'target':str (for link case), 'ltype':'d'/'f' (for link case)  }
            if hash, dict should contain dict["Hashes"] = {...}, for example dict["Hashes"]={"sha1":"66c..."}
        """   
        if abspath in (".", ""):
            pid = 'root'
            prefix = ''
        else:
            pid = self.idPath.get(abspath,None) 
            if pid is None:
                self._setDirPathID(abspath) 
            pid = self.idPath.get(abspath,None)
            prefix = abspath+'/'
        files = self.ali.get_file_list(parent_file_id=pid)
        res = []
        for f in files:
            info = {}
            info['type'] = "d" if f.type == 'folder' else 'f'
            info['name'] = f.name 
            info['mtime'] = int(datetime.datetime.fromisoformat(f.updated_at[:-1]).timestamp()) + 28800
            info['Size'] = int(f.size) if f.size else 0
            info['Hashes'] = { "sha1":f.content_hash.lower() } if f.content_hash else {}
            path = prefix + f.name 
            self.idPath[path] = f.file_id
            res.append(info)   
        return res 
    
    def listPath(self,rpath:str,mtime:bool=True,hash:bool=False)->list[ dict ]:
        absPath = self._geValidPath(rpath)
        return self._absPathlistPath(absPath,mtime,hash)
    
    def mkdir(self,rpath:str)->int:
        """ mkdir

        Args:
            rpath (str): path


        Returns:
            int: error code, =0 for success
        """   
        fdir,name = self._absPath_dir_name(rpath=rpath) 
        parentid = self.idPath[fdir]
        res = self.ali.create_folder(parent_file_id=parentid,name= name ,check_name_mode='refuse' )
        self.idPath[self._geValidPath(rpath)] = res.file_id
        return 0 
    
    def purge(self, rPathRemote):
        absPath = self._geValidPath(rPathRemote)
        if absPath not in self.idPath:
            logging.error(f"cannot delete resource {rPathRemote}, idPath cannot find it")
            return -1 
        else:
            self.ali.delete_file(file_id=self.idPath[absPath]) 
            return 0 
    
    rmdir = purge
    
    deleteFile = purge


    def putFile(self,localPath:str,rPathRemote:str): 
        """a local file <localPath> is uploading to the remote at be <rPathRemote>
        remember to keep the meta-data

        Args:
            localPath (str): abs-path of a local path
            rPathRemote (str): relative path of a remote place 
        """     
        fdir,name = self._absPath_dir_name(rPathRemote)
        self.ali.upload_file(file_path=localPath,parent_file_id=self.idPath[fdir],name=name,check_name_mode='overwrite')
    # def putFile(self,localPath:str,rPathRemote:str): 
    #     """a local file <localPath> is uploading to the remote at be <rPathRemote>
    #     remember to keep the meta-data

    #     Args:
    #         localPath (str): abs-path of a local path
    #         rPathRemote (str): relative path of a remote place 
    #     """     
    #     fdir,name = self._absPath_dir_name(rPathRemote)
    #     dirID = self.idPath.get(fdir,None) 
    #     if dirID is None:
    #         pass 
    #     else:
    #         l = self._UploadQueue.get(dirID,None)
    #         if l is None:
    #             self._UploadQueue[dirID] = [] 
    #             l = self._UploadQueue[dirID]       
    #         l.append( ( localPath , name )    )





    def getFile(self,rPathRemote:str,localPath:str)->int: 
        """download a remote file <rPathRemote> to be local file <localPath> 
        remember to keep the meta-data

        Args:
            rPathRemote (str): relative path of a remote place 
            localPath (str): abs-path of a local path
        Returns:
            int: 0 -> success,  -1 -> file not exist
        """   
        absPath = self._geValidPath(rPathRemote)
        if absPath not in self.idPath:
            logging.error(f"downloading file {rPathRemote} (abspath = {absPath}) not in idPath")
            return -1 
        dlDir = os.path.dirname(localPath)
        downloadedPath = self.ali.download_file(file_id=self.idPath[absPath],local_folder=dlDir) 
        os.rename(downloadedPath,localPath)
        return 0 

    def remoteMove(self,rPathSrc:str,rPathDst:str)->int:
        """ OPTIONAL IMPLEMENTATION 
        move a source (of file or dir) to target path

        Args:
            rPathSrc (str): source path
            rPathDst (str): target path 

        Returns:
            int: error code, 0
        """    
        srcid = self.idPath.get(self._geValidPath(rPathSrc),None) 
        if srcid is None:
            logging.error(f'remoteMove: fid of {rPathSrc} not found')
            return -1 
        fdir,name = self._absPath_dir_name(rPathDst)
        dstid = self.idPath.get(fdir,None)  
        if dstid is None:
            logging.error(f"remoteMove: fid of dst dir {fdir} not found")  
        self.ali.move_file(file_id=srcid,to_parent_file_id=dstid,new_name=name) 
        return 0

    def remoteBatchMove(self,pairs:list[tuple[str,str]])->int:
        """ OPTIONAL IMPLEMENTATION 
        move a source (of file or dir) to target path

        Args:
            pairs (list[tuple[str,str]]): each item = (src,dst)

        Returns:
            int: error code, 0
        """       
        directory_dict = defaultdict(list)

        for src, dst in pairs:
            dst_path = PurePosixPath(dst) 
            directory = dst_path.parent  #
            directory_dict[str(directory)].append((src, dst))  

        for dir_path, files in directory_dict.items():
            fids = []
            for src, dst in files:
                srcid = self.idPath.get(self._geValidPath(src),None) 
                if srcid is None:
                    logging.error(f"{src} not in idPath, why?")
                else:
                    fids.append(srcid)
            dstid = self.idPath.get(self._geValidPath(dir_path),None)  
            if dstid is None:
                logging.error(f"remoteBatchMove: fid of dst dir {dir_path} not found")  
            else:
                self.ali.batch_move_files(file_id_list=fids,to_parent_file_id=dstid) 
        return 0 
    
    def remoteCopy(self,rPathSrc:str,rPathDst:str)->int:
        """ OPTIONAL IMPLEMENTATION 
        copy a source (of file or dir) to target path

        Args:
            rPathSrc (str): source path
            rPathDst (str): target path 

        Returns:
            int: error code, 0
        """        
        srcid = self.idPath.get(self._geValidPath(rPathSrc),None) 
        if srcid is None:
            logging.error(f'remoteMove: fid of {rPathSrc} not found')
            return -1 
        fdir,name = self._absPath_dir_name(rPathDst)
        dstid = self.idPath.get(fdir,None)  
        if dstid is None:
            logging.error(f"remoteMove: fid of dst dir {fdir} not found")  
        self.ali.copy_file(file_id=srcid,to_parent_file_id=dstid,new_name=name) 
        return 0

    def remoteBatchCopy(self,pairs:list[tuple[str,str]])->int:
        """ OPTIONAL IMPLEMENTATION 
        move a source (of file or dir) to target path

        Args:
            pairs (list[tuple[str,str]]): each item = (src,dst)

        Returns:
            int: error code, 0
        """       
        directory_dict = defaultdict(list)

        for src, dst in pairs:
            dst_path = PurePosixPath(dst) 
            directory = dst_path.parent  #
            directory_dict[str(directory)].append((src, dst))  

        for dir_path, files in directory_dict.items():
            fids = []
            for src, dst in files:
                srcid = self.idPath.get(self._geValidPath(src),None) 
                if srcid is None:
                    logging.error(f"{src} not in idPath, why?")
                else:
                    fids.append(srcid)
            dstid = self.idPath.get(self._geValidPath(dir_path),None)  
            if dstid is None:
                logging.error(f"remoteBatchCopy: fid of dst dir {dir_path} not found")  
            else:
                self.ali.batch_copy_files(file_id_list=fids,to_parent_file_id=dstid) 
        return 0 

    def remoteBatchDelete(self,items:list[str])->int:
        """ OPTIONAL IMPLEMENTATION 
        batch delete remote files (only files, not dir)

        Args:
            items (list[str]): each item = file path

        Returns:
            int: error code, 0
        """       
        fids = []
        for item in items:
            srcid = self.idPath.get(self._geValidPath(item),None) 
            if srcid is None:
                logging.error(f"remoteBatchDelete: fid of item {item} not found")
            else:
                fids.append(srcid)
        self.ali.batch_delete_files(file_id_list=fids)  
        return 0 


    def cleanQueue(self):
        """ OPTIONAL IMPLEMENTATION
        In some cases, to seedup download/upload, you can put missions into a queue to avoid real actions.
        However, if this method is called, you must finish all waiting missions. 
        """
        # for fid,missions in self._UploadQueue.items():
        #     paths = [ m[0] for m in missions]
        #     names = [ m[1] for m in missions]
        #     # self.ali.upload_files(file_paths= )