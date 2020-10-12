from pprint import pprint as pp
import pandas as pd
import numpy as np
from util import *
from stats import *
from graph import *
from smoothing import *
from numpy.random import random_sample

def lang_setup( training_file, test_file, add_1,add_k,add_k_value): 
    processed_train_set = process_file( training_file )
    processed_test_set = process_file( test_file )

    vocab_size = compute_vocab_size(processed_train_set)
    print('Vocab Size: {0}'.format(vocab_size))

    produce_processed_txt_file( processed_train_set, training_file )
    produce_processed_txt_file( processed_test_set, test_file )
    
    n_counts, n_minus_one_counts = create_all_counts( processed_train_set )
    print 'Passed create all counts'
    model = smoothed_LM(n_counts, n_minus_one_counts, processed_test_set, vocab_size,add_1,add_k,add_k_value)
    model.train_LM_probabilities()
    language_model = model.prob_dict
    entropy, perplexity = model.results()

    return entropy, perplexity, language_model

def add_counts(input_chars):

    chars = '0.abcdefghijklmnopqrstuvwxyz #'
    new_trigram_counts = {}
    new_bi_gram_counts = {}
    for i in range( len(chars) ): 
        string_check = input_chars[:2] + chars[i]
        new_trigram_counts[string_check] = 0

    new_bi_gram_counts[input_chars] = 0

    return new_bi_gram_counts, new_trigram_counts


def add_to_LM(LM, bi_gram_counts, tri_gram_counts, input_chars):

    for key, value in tri_gram_counts.iteritems():

        LM[key] = float(tri_gram_counts[key] + 1) / float(bi_gram_counts[input_chars] + 30)
    
    return LM



def get_next_char(input_chars, train_probability_dict):
    #Restricting Choice 
    
    reduced_prob_dict = {}
    for key, value in train_probability_dict.iteritems():
        if input_chars in key[:2]: 
            reduced_prob_dict[key] = value
    
    if len(reduced_prob_dict.keys()) == 0:
        print 'input chars: {0} dont exist'.format(input_chars)
        bi_gram_counts, tri_gram_counts = add_counts(input_chars)
        train_probability_dict = add_to_LM(train_probability_dict, bi_gram_counts, tri_gram_counts, input_chars)
        reduced_prob_dict = {}
        for key, value in train_probability_dict.iteritems():
            if input_chars in key[:2]: 
                reduced_prob_dict[key] = value
    
    keys = np.array(reduced_prob_dict.keys())
    probs = np.array(reduced_prob_dict.values())
    
    bins = np.cumsum(probs)
    step0 =  np.digitize(random_sample(1), bins)
    key = keys[step0]
    next_char =  key[0][2]
    return next_char
        

def generate_from_LM(train_probability_dict, string_length, start_chars):
    output_sequence = start_chars
    i = 0
    while i < string_length:
        
        input_chars = output_sequence[-2:]
         
        next_char = get_next_char(input_chars, train_probability_dict)
        output_sequence += next_char
        
        if next_char == "#": 
            input_chars = start_chars
            output_sequence += start_chars
            i += 2
            next_char = get_next_char(input_chars, train_probability_dict)
            output_sequence += next_char
            
        i+=1

    return output_sequence

if __name__ == '__main__':
    add_1 = True
    add_k = False
    add_k_value = 0
    entropy, perplexity, language_model = lang_setup( 'training.en', 'test', add_1, add_k, add_k_value)
    

    #writeCSV(language_model,'train_prob_dictionary')
    print "/----------------------[ TASK 4 ] "
    language_model_existing = load_LM('model-br.en')
    ran_gen_given = generate_from_LM( language_model_existing, 300, '##' )
    ran_gen = generate_from_LM( language_model, 300, '##' )
    print 'GENERATING RANDOM OUTPUT FROM EXISTING MODEL: {0}'.format( ran_gen_given )
    print 'GENERATING RANDOM OUTPUT FROM OUR MODEL: {0}'.format( ran_gen )
    print "\n"
    print "/----------------------[ TASK 5 ]"
    print('Entropy: {0}'.format(entropy))
    print('Perplexity: {0}'.format(perplexity))
    

    ## Graphs 
    # zipf_chart( language_model_en )
    # zipf_chart( language_model_es )
    #