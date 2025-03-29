""" 
Multi-step job 
Description: Design a Map-Reduce job that finds the most commonly used word in the input 
This is a kind of multi-step job which needs to override steps() to return a 
list of MRSteps 

""" 
from mrjob.job import MRJob 
from mrjob.step import MRStep 
import re 
WORD_RE = re.compile(r"[\w']+") 

class MRMostUsedWord(MRJob): 
    #This is a multi-step job, so we need to override steps() function 
    def steps(self): 
    # step 1: mapper, get each word in each line 
    # step 2: combiner, count the numbers of the words after each mapper (it can decrease total data transfer) 
    # step 3: reducer, count the total numbers of the words in the whole input 
    # step 4: reducer, find the most commonly used (the maximum number) word in the whole input 
        return [ 
        MRStep(mapper=self.mapper_get_words, 
        combiner=self.combiner_count_words, 
        reducer=self.reducer_count_words), 
        MRStep(reducer=self.reducer_find_max_word) 
        ] 
    # step 1: mapper, get each word in each line 
    def mapper_get_words(self, _, line): 
    # yield each word in the line 
        for word in WORD_RE.findall(line): 
            yield (word.lower(), 1) 
    # step 2: combiner, count the numbers of the words after each mapper 
    # this step can decrease total data transfer, you can remove this step, but it will spend more time 
    def combiner_count_words(self, word, counts): 
    # optimization: sum the words we've seen so far 
        yield (word, sum(counts)) 
    # step 3: reducer, count the total numbers of the words in the whole input 
    def reducer_count_words(self, word, counts): 
    # send all (num_occurrences, word) pairs to the same reducer. 
    # num_occurrences is so we can easily use Python's max() function. 
        yield None, (sum(counts), word) 
    # step 4: reducer, find the most commonly used (the maximum number of occurrences) word in the whole input 
    # discard the key; it is just None 
    def reducer_find_max_word(self, _, word_count_pairs): 
    # each item of word_count_pairs is (count, word), 
    # so yielding one results in key=counts, value=word 
        yield max(word_count_pairs) 
if __name__ == '__main__': 
    MRMostUsedWord.run()