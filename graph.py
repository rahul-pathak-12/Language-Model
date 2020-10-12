import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import special
from itertools import *
from pylab import *

def plot_bar( freq ):
    ## TODO: FIX THIS FUNCTION
    plt.bar( range(len(freq)), sorted(freq.items(), key=itemgetter(1)))
    plt.show()

def zipf_chart( freq_dict ):
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.zipf.html
    counts = freq_dict.values()
    tokens = freq_dict.keys()
    #Convert counts of values to numpy array
    s = np.array(counts)

    #define zipf distribution parameter. Has to be >1
    a = 2. 

    # Display the histogram of the samples,
    #along with the probability density function
    count, bins, ignored = plt.hist(s, 50, normed=True)
    plt.title("Zipf plot for Frequency of Grams")
    x = np.arange(1., 50.)
    plt.xlabel("Frequency Rank of Gram")
    y = x**(-a) / special.zetac(a)
    plt.ylabel("Absolute Frequency of Gram")
    plt.plot(x, y/max(y), linewidth=2, color='r')
    plt.show()
