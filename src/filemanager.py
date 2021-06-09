import git
import json

class FileManager():
    def __init__(self, filepath: str, filehash: str):
        self.filepath = filepath
        self.filehash = filehash

    def parse(self):
        rawcontent = git.get_filecontent(self.filepath, self.filehash)
        return json.loads(rawcontent)
