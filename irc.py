#!/usr/bin/python -tt

import re
import sys


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

def form_dict(name, msg):
    time_stamp = '\\[\\d\\d:\\d\\d\\]'
    end_time_stamp = '(?:(?!\\[\\d\\d:\\d\\d\\]).)*'
    sentence = ' <(\w*)>([\w*\s*\d*]*)'
    user_name = '%s'%name
    
    print 'searching for ' + user_name    
    result = re.findall(time_stamp+sentence+end_time_stamp, msg)
        
    print 'adding to list'
    list = []
    for (name, sentence) in result:
        if re.match(user_name.lower(), name.lower()):
            list += sentence.split()
    
    stop_words = return_stopword_list()    
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
    
    print tuples    
    # file2 = open('result.txt','w')
    # sorted_tuple = sorted(tuples, key = get_tuples, reverse = True)
    # for tuple in sorted_tuple:
        # line = ' '.join(str(x) for x in tuple)
        # file2.write(line + '\n')
    # file2.close()
    



# main function 
def main():
    ##load file
    
    #file = open('test2.txt','r')
    #msg = file.read()
    #file.close()
    name = 'GoRy'   #make this lower case before passing it to the function.
       
    #create and return dict
    msg = '[17:36] <GorySnake> how ss how HOW how ss ! was your session ,, yesterday apollo\nI am dying lads\n[17:36] <GorySnake> dont forget to import data after you download it Cobelcog\n[17:36] <apollo> we won all but one game\n[17:37] <Cobelcog> how do i do that?'
    form_dict(name, msg)
           
      


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
