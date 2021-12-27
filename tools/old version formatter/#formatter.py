import re
import os
import sys,getopt





def selector(string):
    sentence = re.compile(r'"(.*)"')
    result = sentence.search(string)
    return str(result[0])

def check(string):
    func = re.compile(r'(.*)-')
    result = func.match(string)
    func = re.compile(r'(.*)bg(.*)')
    res=func.match(string)
    func = re.compile(r'(.*)m[0-9][0-9]')
    res1 = func.match(string)
    func = re.compile(r'(.*)black(.*)')
    bla = func.match(string)
    func = re.compile(r'(.*)white(.*)')
    white = func.match(string)
    func = re.compile(r'(.*)@(.*)')
    at = func.match(string)
    func = re.compile(r'(.*)_(.*)')
    obj = func.match(string)
    if at != None or white != None or result != None or res != None or res1 != None or bla != None or obj != None:
        #print(string)
        return False
    return True

def clearBlankLine(file):
    file1 = open(file, 'r', encoding='utf-8') # 要去掉空行的文件 
    file2 = open(file+'.temp', 'w', encoding='utf-8') # 生成没有空行的文件
    
    try:
        for line in file1.readlines():
            if line == '\n':
                line = line.strip("\n")
            file2.write(line)
            
    finally:
        file1.close()
        file2.close()
    os.remove(file)
    os.rename(file+'.temp',file)

def orderText(file):
    file1 = open(file, 'r', encoding='utf-8') # 要去掉空行的文件 
    file2 = open(file+'.temp', 'w', encoding='utf-8') # 生成没有空行的文件
    try:
        order = 1
        for line in file1.readlines():
            file2.write('<'+str(order).zfill(4)+'> '+line.replace('\\u3000',' '))
            order += 1
    finally:
        file1.close()
        file2.close()
    os.remove(file)
    os.rename(file+'.temp',file)    
def main(argv):
    fileName = ''
    outFile = ''
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('formatter.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('formatter.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            fileName = arg
        elif opt in ("-o", "--ofile"):
            outFile = arg
    with open(file = outFile,mode = 'w',encoding = 'utf-8') as f_w:
        with open(file = fileName, mode = 'r',encoding = 'utf8') as f:
            data = f.readline
            fullSentence = ''
            order = 1
            while data:
                s = str(data)
                #print(selector(data))
                if s[8:12] == 'text':
                    fullSentence += selector(data)[1:-1]
                    #print(fullSentence)
                if s[8:13] == 'ldstr' and check(data):
                    f_w.write(fullSentence + '\n')
                    order += 1
                    fullSentence = ''
                    fullSentence += selector(data)[1:-1]
                    #print('<'+str(order).zfill(4)+'> '+fullSentence)
                    f_w.write(fullSentence + '\n')
                    fullSentence = ''
                    order += 1
                if s[8:12] == 'ctrl':
                    if selector(data)[1:-1] == 'n':
                        fullSentence += '\\n'
                    if selector(data)[1:-1] == 'p':
                    # print('<'+str(order).zfill(4)+'> '+fullSentence)
                        order +=1
                        f_w.write(fullSentence + '\n')
                        fullSentence = ''
                data =f.readline()
        f.close()
    f_w.close()
    clearBlankLine(outFile)
    orderText(outFile)
    
if __name__ == "__main__":
    main(sys.argv[1:])