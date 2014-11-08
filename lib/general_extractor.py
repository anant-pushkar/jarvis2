import os
import abc
import pickle
import utils
from extractor import Extractor
from summary_tool import SummaryTool
from CommonUtils import CommonUtils

class GeneralExtractor(Extractor):
    
    def __init__(self):
        self.rulebook = "general.rule"
        self.rule_lexicon = Extractor.rule_lexicon
        #print os.path.isfile(rulebook)
        if os.path.isfile(self.rulebook):
            #load pickle
            rulef = open(self.rulebook,"rb")
            try:
                self.rule_lexicon = pickle.load(rulef)
            except EOFError:
                print 'pickle loads empty file'
            rulef.close()

        #load the rules of this class in rule_lexicon, dump them in rule book
        for name,method in GeneralExtractor.__dict__.iteritems():
            if name.startswith('rule'):
                if not name in self.rule_lexicon:
                    self.rule_lexicon[name] = 0.0

        CommonUtils.dumpToRuleBook(self.rulebook, self.rule_lexicon)

    
    def process(self, inp, training=False):
        maxWeight = -1
        function = None
        for funcname, weight in self.rule_lexicon.iteritems():
            f = getattr(self,funcname)
            if weight>maxWeight:
                maxWeight = weight
                function = getattr(self,funcname)
            if training:
                print '######Please give rating(1-10)####'
                print f(inp)
                self.rule_lexicon[funcname] = self.rule_lexicon[funcname]+int(raw_input())

        if training:
            CommonUtils.dumpToRuleBook(self.rulebook, self.rule_lexicon)
        return maxWeight, function(inp)

    def rule_1(self,inp):   #this rule assumes that code is best. Just print out the code
        return 'Code Segment:\n'+"\n".join(inp.codes)

    def rule_2(self,inp):   
        st = SummaryTool()
        sentences_dic = st.get_senteces_ranks(inp.text)
        return utils.get_color("blue") + st.get_summary('', inp.text, sentences_dic)+"\n\nFollowing codes might be helpful : \n"+ utils.reset_color() + utils.get_color("cyan") + "\n".join(inp.codes) + utils.reset_color()



if __name__=='__main__':
   ob = GeneralExtractor()
   lis = G()
   print ob.rule_1(lis)
        
