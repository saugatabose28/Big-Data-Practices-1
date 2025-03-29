"""
define the mapper and reducer functions with MRJOB to find the word of 
maximum frequency in ‘MapReduce_wiki.txt’.
"""

from mrjob.job import MRJob 
from mrjob.step import MRStep 
import re 
WORD_REGEX = re.compile(r"[\w]+") 
class MRWordCount(MRJob): 
    def steps(self): 
        return [MRStep(mapper=self.mapper_1, reducer=self.reducer_1), MRStep(mapper=self.mapper_2,reducer=self.reducer_2)]    
    def mapper_1(self, _, line): 
        for word in WORD_REGEX.findall(line): 
            yield word.lower(), 1        
    def reducer_1(self, word, counts): 
        yield word, sum(counts)        
    def mapper_2(self, word, word_count): 
        yield None, (word, word_count)     
    def reducer_2(self, _, word_count_pairs): 
        yield max(word_count_pairs, key=lambda p: p[1])     
if __name__=="__main__": 
    MRWordCount.run()   