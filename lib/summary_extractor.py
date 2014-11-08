import os
import abc
import pickle
from extractor import Extractor
from CommonUtils import CommonUtils
from summary_tool import SummaryTool

class SummaryExtractor(Extractor):    #works only for strings. Please don't send code
    def __init__(self):
        self.rulebook = "summary.rule"
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
        for name,method in SummaryExtractor.__dict__.iteritems():
            if name.startswith('rule'):
                if not name in self.rule_lexicon:
                    self.rule_lexicon[name] = 0.0

        CommonUtils.dumpToRuleBook(self.rulebook, self.rule_lexicon)

    
    def process(self, inp, training=False):
        maxWeight = -1
        function = None
        for funcname, weight in self.rule_lexicon.iteritems():
			#print '111111111111111',funcname
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

    def rule_1(self,inp):  #code for naive summary extractor
        st = SummaryTool()
        sentences_dic = st.get_senteces_ranks(inp)
        return st.get_summary('', inp, sentences_dic)
        

if __name__=='__main__':
    ob = SummaryExtractor()
    str = """Automatic Summarization is a pretty complex area - try to get your java skills first in order as well as your understanding of statistical NLP which uses machine learning. You can then work through building something of substance. Evaluate your solution and make sure you have concretely defined your measurement variables and how you went about your evaluation. Otherwise, your project is doomed to failure. This is generally considered a high risk project for final year undergraduate students as they often are unable to get the principles right and then implement it in a way that is not right either and then their evaluation measures are all ill defined and don't reflect on their own work clearly. My advice would be to focus on one area rather then many in summarization as you can have single and multi document summaries. The more varied you make your project the less likely hold of you receiving a good mark. Keep it focused and in depth. Evaluate other peoples work then the process you decided to take and outcomes of that.

Readings: -Jurafsky book on NLP there is a back section on summarization and QA. -Advances in Text Summarization by inderjeet mani is really good

Understand what things like term weighting, centroid based summarization, log-likelihood ratio, coherence relations, sentence simplification, maximum marginal relevance, redundancy, and what a focused summary actually is.

You can attempt it using a supervised or an unsupervised approach as well as a hybrid. Linguistic is a safer option that is why you have been advised to take that approach. Try attempting it linguistically then build statistical on to hybridize your solution. Use it as an exercise to learn the theory and practical implication of the algorithms as well as build on your knowledge. As you will no doubt have to explain and defend your project to the judging panel."""
    print ob.rule_1(str)
        
