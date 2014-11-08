import abc

class Extractor():       #whatever rules is specified in the Extractor, must start with 'rule' string
    __metaclass__ = abc.ABCMeta 

    rule_lexicon={}   #dictionary mapping rule weight to the rule
    rulebook = ''    #.rule file which contains the rule.

    @abc.abstractmethod
    def process(input, training=False):   #process runs a rule on the input string and returns the output. If in training mode, prompt the user for output rating
        return ''
    



