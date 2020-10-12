import re
from math import log
import pandas as pd

def create_all_counts( processed_data ): 
    n_value = 3
    n_counts = {}
    n_minus_one_counts = {}
    vocab_size = []
    for line in processed_data:
        n_gram_counts( line, n_counts, n=n_value )
        n_gram_counts( line, n_minus_one_counts, n=n_value-1 )

    new_trigrams = add_missing_trigrams(n_counts)

    n_counts = dict(n_counts.items() + new_trigrams.items())
    return n_counts, n_minus_one_counts

def add_missing_trigrams( current_trigrams ): 
    chars = '0.abcdefghijklmnopqrstuvwxyz #'
    new_trigrams = {}
    for key, value in current_trigrams.iteritems(): 
        for i in range( len(chars) ): 
            string_check = key[:2] + chars[i]
            if string_check not in current_trigrams:
                new_trigrams[string_check] = 0
            
    return new_trigrams
'''
def add_missing_bigram(current_bigrams):
    chars = '0.abcdefghijklmnopqrstuvwxyz #'
    new_bigrams = {}

    for key, value in current_bigrams.iteritems(): 
        for i in range( len(chars)-1 ): 
            bigram = chars[i] + chars[i+1]
            if( current_bigrams[bigram] ):
                continue
            else:
                new_bigrams[bigram] = 0
                
    return new_bigrams
'''
    # c = dict( a.items() + b.items() )
    # c = dict( a, **b )
                    
def n_gram_counts( input, countDict, n=3 ):
    """
    Parameters
    ----------
    input : string: cat
    countDict: 
    n :     int: 3

    Returns
    -------
    Dict: { 'abc' : 12 }

    """
    min = n-1
    for i in range( min, len(input) ): 
        ngram = str( input[ i-min : i+1 ] ) 
        
        if ngram in countDict.keys(): 
            countDict[ ngram ] += 1
        else:
            countDict[ ngram ] = 1

def perplexity( entropy ):
    """
    Parameters
    ----------
    input : entropy
 
    Returns
    -------
    float: perplexity

    """
    return pow( 2, entropy )

def return_entropy( smoothed_prob, all_tri_grams ):
    entropy_dict = []
    for tri_gram in all_tri_grams:
        entropy_dict.append(-log( smoothed_prob[tri_gram], 2 ))
    e = float( sum(entropy_dict))

    avg_entropy = e / float(len(all_tri_grams))
    return avg_entropy


def n_gram_string_maker( line, n ):
    """
    Parameters
    ----------
    input : line
    n :     int 3

    Returns
    -------
    List: [ 'cat' ]

    """
    n_gram_strings = []
    min = n -1
    for i in range( min, len(line) ): 
        ngram = str( line[ i-min : i+1 ] )
        n_gram_strings.append( ngram )
    return n_gram_strings

def compute_vocab_size(processed_training_data):
    """
    Parameters
    ----------
    processed_training_data: processed data from any training file

    Returns
    -------
    vocab_size = the number of unique characters in any processed training file. It includes the characters '#', '.', and ' '. They were included as these characters show up in our bi- and trigrams. 
    """

    array_of_unique_chars = []

    for line in processed_training_data:
        array_of_chars = list(line)
        for item in array_of_chars:
            if item not in array_of_unique_chars:
                array_of_unique_chars.append(item)

    vocab_size = len(array_of_unique_chars)

    return vocab_size

def writeCSV( d, output_name ): 
    fout = "{0}.txt".format(output_name)
    fo = open(fout, "w")
    for k, v in d.items():
        fo.write(str(k) + ' '+ str(v) + '\n')
    fo.close()