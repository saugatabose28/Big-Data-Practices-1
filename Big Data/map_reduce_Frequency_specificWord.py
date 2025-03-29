"""
 Design a Map-Reduce job that counts the total number of the occurrences of a certain word (such as 
‘MapReduce’) in ‘MapReduce_wiki.txt’. 
"""

from mrjob.job import MRJob 
import re 
WORD_RE = re.compile(r"[\w']+") 
# Here, we count the total number of the occurrences of 'mapreduce' in the input file. 
query_word='id' 
class MRMostUsedWord(MRJob): 
    # step 1: mapper, count the number of the occurrences of query_word in each mapper 
    def mapper(self, _, line): 
        for word in WORD_RE.findall(line): 
            if word == query_word: 
                yield word, 1 
    # step 2: reducer, count the total number of the occurrences of query_word in the whole input 
    def reducer(self, word, counts): 
        yield word, sum(counts) 
if __name__ == '__main__': 
    MRMostUsedWord.run()