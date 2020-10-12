from stats import *

class LM_Data:
    def __init__(self, n_gram_counts, n_minus_gram_counts, processed_test_file, vocabulary_size):
        self.n_gram_counts = n_gram_counts
        self.n_minus_one_gram_counts = n_minus_gram_counts
        self.processed_test_file = processed_test_file
        self.vocabulary_size = vocabulary_size

class smoothed_LM( LM_Data ):
    
    def __init__(self, n_gram_counts, n_minus_gram_counts, processed_test_file, vocabulary_size, add_1, add_k, add_k_value):
        LM_Data.__init__( self, n_gram_counts, n_minus_gram_counts, processed_test_file, vocabulary_size)
        self.add_1 = add_1
        self.add_k = add_k
        self.add_k_value = add_k_value
        self.prob_dict = {}

    def add_1_smoothing(self, key, smaller_key):
        
        probability = float(self.n_gram_counts[key] + 1) / float(self.n_minus_one_gram_counts[smaller_key] + self.vocabulary_size )

        return probability

    def add_k_smoothing(self, key, smaller_key):

        probability = float(self.n_gram_counts[key] + self.add_k_value) / float(self.n_minus_one_gram_counts[smaller_key] + self.vocabulary_size *self.add_k_value)

        return probability
             

    def train_LM_probabilities(self):
        
        for key, value in self.n_gram_counts.iteritems():
            # print(key)
            smaller_key = key[:-1]
            #print 'add1: {0}'.format(self.add_1)
            if self.add_1:
                self.prob_dict[key] = self.add_1_smoothing(key, smaller_key)

            elif self.add_k:
                self.prob_dict[key] = self.add_k_smoothing(key, smaller_key)

            else:
                print 'Did not choose a smoothing method: {0}'.format(key)
        
        



    def create_test_ngram_probabilities( self ): 
        """
        Parameters
        ----------
        input : object : file
        lang_model : dict { 'abc' : 0.35 }
        smoothing = boolean T/F
        type = string ( smoothing option )
        n : int : 3

        Returns
        -------
        Float

        """
        new_ngrams = {}
        all_ngram_strings= []

        for line in self.processed_test_file: 
            array_of_ngram_strings = n_gram_string_maker( line, 3 ) #TODO CHANGE 
            for ngram in array_of_ngram_strings:
                all_ngram_strings.append(ngram)
                if ngram in self.n_gram_counts:
                    new_ngrams[ngram] = self.prob_dict[ngram]
                else:
                    if ngram[:2] not in self.n_minus_one_gram_counts:
                        if self.add_1:
                            new_ngrams[ngram] = float(1) / float( self.vocabulary_size )

                        elif self.add_k:
                            new_ngrams[ngram] = self.add_k_value / float(self.vocabulary_size * self.add_k_value)

                        else:
                            print 'Did not choose a smoothing method'

                    else:
                        if self.add_1:
                            new_ngrams[ngram] = float(1) / float( self.n_minus_one_gram_counts[ ngram[:2] ] + self.vocabulary_size )
                        elif self.add_k:
                            new_ngrams[ngram] = float(self.add_k_value) / float(self.n_minus_one_gram_counts[ngram[:2]] + self.vocabulary_size*self.add_k_value)
                        else:
                            print 'Did not choose a smoothing method'
        
        return new_ngrams, all_ngram_strings

    def results( self ): 

        smoothed_test_probability_dict, all_tri_gram_strings = self.create_test_ngram_probabilities()
        writeCSV(smoothed_test_probability_dict, 'test_prob_dictionary')
        entropy_of_test_set = return_entropy( smoothed_test_probability_dict, all_tri_gram_strings )
        perplexity_of_test_set = perplexity( entropy_of_test_set )
        return entropy_of_test_set, perplexity_of_test_set
        

    