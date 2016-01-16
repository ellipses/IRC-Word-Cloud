#!/usr/bin/python -tt

import re
import sys
import scipy
import random
import numpy as ny
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


def return_stopword_list():
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
            'http', 'lol', 'ye', 'like', 'yeah', 'apollo', 'apollos', 'get', 'dont', 'fergus']

def get_tuples(tuple):
    return tuple[-1]

def match_name(name, msg, search_type):
    ##probably dont need two slashes
    time_stamp = '\[\d\d:\d\d\]'
    end_time_stamp = '(?:(?!\[\d\d:\d\d\]).)*'
    special_char = """:\-\:!,\?\.\&\(\)\'\""""
    sentence = ' <([\w*\-*\^*\@*]*)>([\w\s%s]*)'%special_char
    user_name = '%s'%name
    
    #print 'searching for ' + user_name    
    result = re.findall(time_stamp+sentence+end_time_stamp, msg)
    #print result
    #add error if list is of size 0    
    print 'adding to list'
    list = []
    for (name, sentence) in result:
        sentence = re.sub('['+special_char+'\n'+']','',sentence)
        if search_type == 'user_name':
            if re.match('\S*'+user_name.lower()+'\S*', name.lower()):
                list += sentence.split()
        else:
            if re.match('.*'+user_name.lower()+'.*', sentence.lower()):
                list += sentence.split()
                        
    if(len(list) == 0):
        print "cannot find instance of"+name+' with search type:'+search_type
        usage()
        sys.exit(-1)
    return list

#returns top 200 words and their frequency in a tuple    
def get_freq(name, msg, search_type):    
    list = match_name(name, msg, search_type)
    stop_words = return_stopword_list()  
    #stop_file = open('stop_words.txt', 'w')
    #for words in stop_words:
    print 'forming dict'
    dict = {}    
    for word in list:
        word = word.lower()
        if word not in stop_words:
            if word in dict:
                dict[word]+=1
            else:
                dict[word] = 1
    #raise error if dictionary is of size 0        
    tuples = dict.items()
            
    sorted_tuple = sorted(tuples, key = get_tuples, reverse = True)
    #print sorted_tuple
    smaller = sorted_tuple[:min(200, len(sorted_tuple))]
    file2 = open('result.txt','w')
    for tuple in smaller:
        file2.write(tuple[0]+ ' %d'%tuple[1] + '\n')
    file2.close()
    return smaller
    
def word_cloud(frequency_list):
    print 'creating cloud'
    fontsize = 100
    total = 0.0
    for tuple in frequency_list:
        total += tuple[1]
        
    relative_freq = [tuple[1]/total for tuple in frequency_list]
    normalised = [val*(1/max(relative_freq)) for val in relative_freq]
    words = [tuple[0] for tuple in frequency_list]
    #print relative_freq
    #print normalised
    #print words
        
    status = False
    while not status:
        image = Image.new('L', (600,600), color = 0)
        draw = ImageDraw.Draw(image)
        fontlist = [fontsize*val for val in normalised]
        iteration = 0
        while(iteration<len(words)):
            word = words[iteration]
            fnt = ImageFont.truetype('Calibri.ttf', int(fontlist[iteration]))
            size = fnt.getsize(word)
            #bigger rectangle than bounding box to compensate
            rect = (size[0]+10, size[1]+10)
            result = scipy.ndimage.filters.uniform_filter(image, rect, mode='constant', cval = 255)
            location = ny.argwhere(result==0)
    
            if len(location)==0:
                break_image = image
                break_rect = rect
                fontsize-=1
                print fontsize
                break
            else:
                iteration+=1
                rand_val = location[random.randint(0, len(location)-1)]
                #adjusting the location to account for offset from kernel centre
                value = (rand_val[0]-size[1]/2,rand_val[1]-size[0]/2)
                draw.text(value[::-1], word, font=fnt, fill=255)
            if word == words[-1]:
                print 'finished'
                status=True
    
    image.show()

def usage():
    print "usage: irc.py word_to_search file_to_search search_type=user_name"
    
# main function 
def main():
    
    search_types = 'user_name', 'sentence'
    if not (2<len(sys.argv)<5):
        print 'input parameters out of bounds'
        usage()
        sys.exit(-1)
    else:
        name = sys.argv[1]
        file_name = sys.argv[2]
        if (len(sys.argv) == 4):
            if sys.argv[3] in search_types:
                search_type = sys.argv[3]
                print "search type = "+search_type
            else:
                print 'invalid search type'
                usage()
                sys.exit(-1)
            
    file = open(file_name,'r')
    msg = file.read()
    file.close()
    #msg = '[17:36] <GorySnake> how ss how HOW how ss ! was your session ,, yesterday apollo\nI am dying lads\n[17:36] <Gory-Snake> dont forget to import data after you download it Cobelcog\n[17:36] <apollo> we won all but one game\n[17:37] <Cobelcog> how do i do that?'
    frequency_list = get_freq(name, msg, search_type)
    #word_cloud(frequency_list)
           
      


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
