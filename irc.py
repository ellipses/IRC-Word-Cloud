#!/usr/bin/python -tt

import re
import sys
import scipy
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


def return_stopword_list():
    """ Returns stops as a list of strings.
    """
    return ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'https', 
            'http']

def get_tuples(tuple):
    return tuple[-1]                                                        

def match_name(word, msg, search_type):
    """ Returns list of sentences by user or sentences with
        the word depending on search type.
    """
    time_stamp = '\[\d\d:\d\d\]'
    end_time_stamp = '(?:(?!\[\d\d:\d\d\]).)*'
    special_char = """:\-\:!,\?\.\&\(\)\'\""""
    sentence = ' <([\w*\-*\^*\@*]*)>([\w\s%s]*)'%special_char
    search_word = '%s'%word
    
      
    result = re.findall(time_stamp+sentence+end_time_stamp, msg)
    print 'adding to list'
    list = []
    for (name, sentence) in result:
        sentence = re.sub('['+special_char+'\n'+']','',sentence)
        if search_type == 'user_name':
            if re.match('\S*' + search_word.lower()+'\S*', name.lower()):
                list += sentence.split()
        else:
            if re.match('.*' + search_word.lower()+'.*', sentence.lower()):
                list += sentence.split()
                        
    if(len(list) == 0):
        print "cannot find instance of " + word +' with search type:'+search_type
        usage()
        sys.exit(-1)
    return list

#returns top 200 words and their frequency in a tuple    
def get_freq(name, msg, search_type, extra_stopwords):
    """ Returns the 200 most common, words by user or words in
    the same sentence depending on the search type.
    """
    list = match_name(name, msg, search_type)
    stop_words = return_stopword_list() + extra_stopwords  

    print 'forming dict'
    dict = {}    
    for word in list:
        word = word.lower()
        if word not in stop_words:
            if word in dict:
                dict[word]+=1
            else:
                dict[word] = 1
      
    tuples = dict.items()
    sorted_tuple = sorted(tuples, key = get_tuples, reverse = True)
    smaller = sorted_tuple[:min(200, len(sorted_tuple))]
    file2 = open('result.txt','w')
    for tuple in smaller:
        file2.write(tuple[0]+ ' %d'%tuple[1] + '\n')
    file2.close()
    return smaller
    
def word_cloud(frequency_list):
    """ Creates and saves a word cloud based on their frequency.
    """
    print 'creating cloud'
    
    total = 0.0
    for tuple in frequency_list:
        total += tuple[1]
    
    #Normalise the relative frequencies
    relative_freq = [tuple[1]/total for tuple in frequency_list]
    normalised = [val*(1/max(relative_freq)) for val in relative_freq]
    words = [tuple[0] for tuple in frequency_list]
    
    fontsize = 100
    status = False
    
    #Iterate through the fontsizes till one allows all words to fit.
    while not status:
        image = Image.new('L', (512,512), color = 0)
        draw = ImageDraw.Draw(image)
        fontlist = [fontsize*val for val in normalised]
        iteration = 0
        
        while(iteration<len(words)):
            word = words[iteration]
            fnt = ImageFont.truetype('Calibri.ttf', int(fontlist[iteration]))
            size = fnt.getsize(word)
            #bigger rectangle than bounding box to compensate
            rect = (size[0] + 30, size[1] + 30)
            #Convolve with uniform filter and find index where its still 0
            result = scipy.ndimage.filters.uniform_filter(image, rect, mode='constant', cval = 0)
            location = np.argwhere(result==0)
            
            #Reduce fontsize and try again if word cant fit else draw it.
            if len(location)==0:
                fontsize-=1
                print fontsize
                break
            else:
                iteration += 1
                #Choose a random index and draw text centered there
                rand_val = location[random.randint(0, len(location)-1)]
                #adjusting the location to account for offset from kernel centre
                value = (rand_val[0]-size[0]/2,rand_val[1]-size[1]/2)
                draw.text(value[::-1], word, font=fnt, fill=255)
            if word == words[-1]:
                print 'finished'
                status=True
                  
    image.show()
    image.save("irc_cloud.jpg")

def usage():
    print 'usage: irc.py word_to_search file_to_search',\
          'search_type=user_name extra_stopwords=None'
    
 
def main():    
    search_types = 'user_name', 'sentence'
    search_type = 'user_name'
    extra_stopwords = []
    input_length = len(sys.argv)
    
    if not (2 < input_length < 6):
        print 'input parameters out of bounds'
        usage()
        sys.exit(-1)
    else:
        name = sys.argv[1]
        file_name = sys.argv[2]
        if (input_length >= 4):
            if sys.argv[3] in search_types:
                search_type = sys.argv[3]
                print "search type = " + search_type
            else:
                print 'invalid search type'
                usage()
                sys.exit(-1)
            if(input_length == 5):
                extra_stopwords = sys.argv[4].split()
                
            
    file = open(file_name,'r')
    msg = file.read()
    file.close()
    frequency_list = get_freq(name, msg, search_type, extra_stopwords)
    word_cloud(frequency_list)
           
      


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
