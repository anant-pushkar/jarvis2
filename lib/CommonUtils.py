import os
import pickle

class CommonUtils():
    @classmethod
    def dumpToRuleBook(self,fileName, dictionary):
        rulef = open(fileName,"wb")
        pickle.dump(dictionary, rulef)
        rulef.close()
    
