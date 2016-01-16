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
            'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

def get_tuples(tuple):
    return tuple[-1]

def match_name(name, msg):
    ##probably dont need two slashes
    time_stamp = '\\[\\d\\d:\\d\\d\\]'
    end_time_stamp = '(?:(?!\\[\\d\\d:\\d\\d\\]).)*'
    sentence = ' <(\w*)>([\w*\s*\d*]*)'
    user_name = '%s'%name
    
    #print 'searching for ' + user_name    
    result = re.findall(time_stamp+sentence+end_time_stamp, msg)
    #add error if list is of size 0    
    #print 'adding to list'
    list = []
    for (name, sentence) in result:
        if re.match(user_name.lower(), name.lower()):
            list += sentence.split()
    #print list
    return list

#returns top 200 words and their frequency in a tuple    
def get_freq(name, msg):    
    list = match_name(name, msg)
    stop_words = return_stopword_list()    
    #print 'forming dict'
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
    
    return sorted_tuple[:max(50, len(sorted_tuple))]
    # for tuple in sorted_tuple:
        # line = ' '.join(str(x) for x in tuple)
        # file2.write(line + '\n')
    # file2.close()
    
def word_cloud(frequency_list):
    fontsize = 70
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
        image = Image.new('L', (512,512), color = 0)
        draw = ImageDraw.Draw(image)
        fontlist = [fontsize*val for val in normalised]
        iteration = 0
        while(iteration<len(words)):
            word = words[iteration]
            fnt = ImageFont.truetype('Calibri.ttf', int(fontlist[iteration]))
            size = fnt.getsize(word)
            #bigger rectangle than bounding box to compensate
            rect = (size[0]+40, size[1]+40)
            result = scipy.ndimage.filters.uniform_filter(image, rect, mode='constant', cval = 255)
            location = ny.argwhere(result==0)
    
            if len(location)==0:
                break_image = image
                break_rect = rect
                fontsize-=5
                fontsize
                #break
            else:
                iteration+=1
                rand_val = location[random.randint(0, len(location)-1)]
                #adjusting the location to account for offset from kernel centre
                value = (rand_val[0]-size[1]/2,rand_val[1]-size[0]/2)
                draw.text(value[::-1], word, font=fnt, fill=255)
            if word == words[-1]:
                print fontsize
                status=True
    
    image.show()

# main function 
def main():
    ##load file
    
    file = open('small_irc.txt','r')
    msg = file.read()
    file.close()
    name = 'reh'   #make this lower case before passing it to the function.
       
    #create and return dict
    #msg = '[17:36] <GorySnake> how ss how HOW how ss ! was your session ,, yesterday apollo\nI am dying lads\n[17:36] <GorySnake> dont forget to import data after you download it Cobelcog\n[17:36] <apollo> we won all but one game\n[17:37] <Cobelcog> how do i do that?'
    frequency_list = get_freq(name, msg)
    word_cloud(frequency_list)
           
      


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
