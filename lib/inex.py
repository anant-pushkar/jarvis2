from general_extractor import GeneralExtractor
from summary_extractor import SummaryExtractor
from DrakSuggestionsFetcher import *

class Inex():
    def processInput(self,inp,training=False): #input is a list of DrakSuggestion objects

        sob = SummaryExtractor()
        gob = GeneralExtractor()
        sw=-1
        ss= ""
        assert inp!=None
        for i in inp:
            confidence = i.score+i.confidence
            if i.is_ticked:
                confidence = confidence+2*i.confidence
            w, s = sob.process(i.text, training)
            w = w+confidence
            if w>sw:
                ss = s
                sw = w
            w, s = gob.process(i, training)
            w = w+confidence
            if w>sw:
                ss = s
                sw = w
        
        return ss
'''

if __name__=='__main__':
    ob = Inex()
    ob1 = DrakSuggestion()
    ob2 = DrakSuggestion()
    lis = []
    lis.append(ob1)
    lis.append(ob2)
    print ob.processInput(lis, True)    #training mode on
'''
