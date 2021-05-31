import git
import json

class FileManager():
    def __init__(self,filepath,filehash):
        self.filepath = filepath
        self.filehash = filehash
        self.content = ""
    
    def parse(self):
        if self.content == "":
            rawcontent = git.get_filecontent(self.filepath,self.filehash)
            self.content = json.loads(rawcontent)