"""
randomly select some text content and save them into a text file. e.g., copy the definition of 
MapReduce in wiki (https://en.wikipedia.org/wiki/MapReduce) and save it into ‘MapReduce_wiki.txt’. Then, define the mapper and reducer functions with MRJOB to count the numbers of chars, words, 
and lines of ‘MapReduce_wiki.txt’.
"""
from mrjob.job import MRJob 
class MRWordFrequencyCount(MRJob): 
    def mapper(self, _, line): 
        yield "chars", len(line) # count num of characters 
        yield "words", len(line.split()) # count num of words 
        yield "lines", 1 # count num of lines – with each line, add 1 
    def reducer(self, key, values): 
        yield key, sum(values) 
if __name__ == '__main__': 
    MRWordFrequencyCount.run() # main program to call/run MRWordFrequencyCount
