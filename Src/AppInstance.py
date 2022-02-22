import os
import subprocess
import toml
import json
import jinja2
from ModelM import ModelMan
from Utils import IP
class App :
    def __init__(self , name ,  modelUrl , labelName , shape , redownload:bool , toBuildIp :str ):
        self.name = name
        self.modelUrl = modelUrl
        self.redownload = bool(redownload)
        self.labelName = labelName
        self.toBuildIp = toBuildIp
        self.IsSameIp = self.IsSame()

        if self.name == 'basic':
            self.fileName = 'basic'
        else:
            self.fileName = f's_{name}'
        self.shape =shape

    def ModelManuplation(self):
        model = ModelMan(self.modelUrl , self.name)
        model.CreateRar()

    def MakeCode(self):

        jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader('Tmp'))
        templeteName = None
        if self.name == 'basic':
            templeteName = 'Basic.py'
        else :
            templeteName = "Second.py"

        templete = jinjaEnv.get_template(templeteName)
        port = 5000

        if self.name !='basic':
            port+=int(self.name )+1

        file = templete.render({
            'ip': '0.0.0.0' ,
            'port': port ,
            'fileName':self.fileName ,
            'shape':self.shape})

        f = open(f"./Apps/{self.fileName}.py", "w+")
        f.write(file)
        f.close()

    def IsSame(self):
        myIp = IP.MyIpv4()
        return myIp == self.toBuildIp

    def Create(self):
        if self.IsSameIp:
            self.DownloadModel()
            self.MakeJson()
            self.MakeCode()
