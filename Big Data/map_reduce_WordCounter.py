"""
define the mapper and reducer functions with MRJOB to count the numbers of each word of 
‘MapReduce_wiki.txt’.
"""

from mrjob.job import MRJob 
import re 
WORD_REGEX = re.compile(r"[\w]+")  
class WordCount(MRJob): 
    def mapper(self, _, line): 
        for word in WORD_REGEX.findall(line): 
            yield word.lower(), 1 
    def reducer(self, word, counts): 
            yield word, sum(counts) 
if __name__ == "__main__": 
    WordCount.run() 