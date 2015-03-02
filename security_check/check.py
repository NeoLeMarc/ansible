#!/usr/bin/env python3
import requests

class ApacheCheck:
    baseUrl = ""
    modules = []
    forbiddenModules = []
    failedTests = []
    expectedTimeouts = {'connection' : 0, 'keep-alive' : 0}
    timeouts = {}

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.parseModules()
        self.parseServerSettings()
        self.parseTimeouts()

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
            key = t.firstChild.firstChild.toxml()[:-1] # Remove trailing ':'
            value = self.drill(t.getElementsByTagName("tt")[0])
            self.config[key] = value

    def drill(self, node):
        if node.firstChild != None:
            return self.drill(node.firstChild)
        else:
            return node.toxml()

    def setForbiddenModules(self, modules):
        self.forbiddenModules = modules

    def checkForbiddenModules(self):
        successful = True
        for forbiddenModule in self.forbiddenModules:
            if forbiddenModule in self.modules:
                print("Warning: Found forbidden module %s!" % forbiddenModule)
                self.addFailedTest("checkForbiddenModules")
                successful = False
        return successful

    def setExpectedTimeouts(self, connection = 0, keep_alive = 0):
        self.expectedTimeouts['connection'] = int(connection)
        self.expectedTimeouts['keep-alive'] = int(keep_alive)

    def parseTimeouts(self):
        tmpTimeouts = self.config["Timeouts"].split("  ")
        self.timeouts = {} 
        while len(tmpTimeouts) > 0:
            t = tmpTimeouts.pop().split(':')
            self.timeouts.update({t[0] : t[1]})
    
    def checkTimeouts(self):
        success = True
        for key in self.expectedTimeouts.keys():
            if int(self.expectedTimeouts[key]) != int(self.timeouts[key]):
                print("Warning: Mismatched timeout for setting: %s" % key)
                print("Is: %s - Expected: %s" % (self.timeouts[key], self.expectedTimeouts[key]))
                success = False
                self.addFailedTest("checkTimeouts")
        return success
         

    def hasFailedTests(self):
        if len(self.failedTests) > 0:
            return True
        else:
            return False

    def getFailedTests(self):
        return self.failedTests

    def addFailedTest(self, name):
        if name not in self.failedTests:
            self.failedTests.append(name)


a = ApacheCheck("https://citadel.noetech.net/server-info")
a.setForbiddenModules(["mod_dav.c", "mod_alias.c"])
a.checkForbiddenModules()
a.setExpectedTimeouts(connection = 300, keep_alive = 5)
a.checkTimeouts()

if a.hasFailedTests():
    print("There are some failed tests: %s" % a.getFailedTests())
else:
    print("No tests failed!")

