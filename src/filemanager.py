import git
import json

class FileManager():
    def __init__(self, file_path: str, file_hash: str):
        self.file_path = file_path
        self.file_hash = file_hash

    def parse(self):
        rawcontent = git.get_file_content(self.file_path, self.file_hash)
        return json.loads(rawcontent)
