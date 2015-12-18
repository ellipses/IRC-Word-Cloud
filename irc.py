#!/usr/bin/python -tt

import re
import sys


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
    #add words said by user to list 
    list = ['']
    for lines in result:
        if user_name in lines[0]:
            list = list + lines[1].split()
            
    print 'forming dict'
    dict = {}    
    #form dict
    for word in list:
        word = word.lower()
        if word in dict:
            dict[word]+=1
        else:
            dict[word] = 1
            
    tuples = dict.items()
    
    file2 = open('result.txt','w')
    sorted_tuple = sorted(tuples, key = get_tuples, reverse = True)
    for tuple in sorted_tuple:
        line = ' '.join(str(x) for x in tuple)
        file2.write(line + '\n')
    file2.close()
    



# main function 
def main():
    ##load file
    
    file = open('test2.txt','r')
    msg = file.read()
    file.close()
    name = 'Fergus'   #make this lower case before passing it to the function.
       
    #create and return dict
    #msg = '[17:36] <GorySnake> how ss how HOW how ss ! was your session ,, yesterday apollo\nI am dying lads\n[17:36] <GorySnake> dont forget to import data after you download it Cobelcog\n[17:36] <apollo> we won all but one game\n[17:37] <Cobelcog> how do i do that?'
    form_dict(name, msg)
           
      


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
