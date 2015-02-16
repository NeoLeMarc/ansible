#!/usr/bin/env python3
import requests

class ApacheCheck:
    baseUrl = ""
    modules = []

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.parseModules()
        self.parseServerSettings()

    def parseModules(self):
        r = requests.get(self.baseUrl + "?list")
        
        import xml.dom.minidom
        from xml.dom.minidom import parse, parseString
        
        dom = parseString(r.text)
        self.modules = [n.firstChild.toxml() for n in dom.getElementsByTagName("dd")]

    def parseServerSettings(self):
        r = requests.get(self.baseUrl + "?server")
        self.config = {}

        import xml.dom.minidom
        from xml.dom.minidom import parse, parseString

       
        dom = parseString(r.text)
        for t in dom.getElementsByTagName("dt"):
            key = t.firstChild.firstChild.toxml()
            value = self.drill(t.getElementsByTagName("tt")[0])
            self.config[key] = value

    def drill(self, node):
        if node.firstChild != None:
            return self.drill(node.firstChild)
        else:
            return node.toxml()

a = ApacheCheck("https://citadel.noetech.net/server-info")
