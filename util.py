import re

def process_file( file ):
    """
    Parameters
    ----------
    String filepath
 
    Returns
    -------
    returns : list

    """
    values = []
    path = './assignment1-data/{0}'.format( file )
    with open( path , "r") as lines:
        for line in lines:
            values.append( preprocess_line( line ) )
    return values


def preprocess_line( line ):
    """
    Parameters
    ----------
    line : string 'the dog sat on a hat\n'

    Returns
    -------
    String  '##the dog sat on a hat#'

    """
    line = line.rstrip()
    line = line.lower()
    line = re.sub( '[^a-z0-9. ]', "", line )
    line = re.sub( '[0-9]', "0", line )
    line = "##" + line + "#" 
    return line


def load_LM( file ):
    """
    Parameters
    ----------
    Object: file

    Returns
    -------
    Dictionary  { 'abc': 0.75 }

    """
    dictionary = {}
    path = './assignment1-data/{0}'.format( file )
    with open( path , "r") as data_file:
        for line in data_file:
            line = line.rstrip()
            x = line.split('\t')
            dictionary[x[0]] = float(x[1])
    return dictionary


def produce_processed_txt_file( data, filename ):
    """
    Parameters
    ----------
    List : data

    Returns
    -------
    None :  File written to disk

    """
    txt = open( "processed_{0}.txt".format( filename ), "w" )
    for line in data:
        txt.write( line )
    txt.close()