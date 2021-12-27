import os
import re
from typing import Pattern

def main():
    files = os.listdir('../texts/content')
    results = []
    pattern = re.compile(r'(.*).txt')
    for f in files:   
        if pattern.match(f) != None:
            results.append(f)
    #results.clear()
    #results.append('00-01-01.sjs')
    for r in results:
        duplicate(r)

def checkOrder(key):
    pattern = re.compile(r'<[0000-9999]*> ')
    results = pattern.match(key)
    return results

def checkFunc(key):
    pattern = re.compile(r'<[0000-9999]*> (.*)_(.*)')
    results = pattern.match(key)
    if results != None:
        return True
    return False   
def checkSwich(key):
    pattern = re.compile(r'<[0000-9999]*> (.*)分岐[0-9]')     
    results = pattern.match(key)
    if results != None:
        return True
def checkName(key):
    pattern = re.compile(r'<[0000-9999]*> 【(.*)】\n')
    results = pattern.match(key)
    if results != None:
        return True
def format(key):
    pattern_full = re.compile(r'<[0000-9999]*> 【(.*)】「(.*)」')
    pattern_left = re.compile(r'<[0000-9999]*> 【(.*)】「')
    pattern_right = re.compile(r'<[0000-9999]*> (.*)」')
    results = pattern_full.match(key)
    if results != None:
        ####
        pattern = re.compile(r'「(.*)」')
        contence = pattern.search(key)
        #print(key.replace(contence[0],'「」'))
        return key.replace(contence[0],'「」')
    results = pattern_left.match(key)
    if results != None:
        pattern_sentence = re.compile(r'「(.*)')
        contence = pattern_sentence.search(key)
        return results[0].replace(key,'「') + '\n'
    if key[-2] == '」':
        #print(checkOrder(key)[0] + ' 」\n')
        return checkOrder(key)[0] + ' 」\n'
    return checkOrder(key)[0] + '\n'

def duplicate(file):
    with open(file= '../texts/txt_double/' + file,mode='w',encoding='utf8') as f_w:
        with open(file = '../texts/content/' + file, mode='r',encoding='utf-8') as f:
            data = f.readline()
            while data:
                f_w.write(data)
                if checkFunc(data) or checkSwich(data) or checkName(data):
                    f_w.write(data)
                else:
                    f_w.write(format(data))
                data = f.readline()
            f.close()
        f_w.close()    
main()