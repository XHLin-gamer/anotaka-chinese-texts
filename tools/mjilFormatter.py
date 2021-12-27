import re,os

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
    name = re.compile(r'(.*)【(.*)】')
    names = name.match(string)
    if at != None or white != None or result != None or res != None or res1 != None or bla != None or obj != None or names != None:
        #print(string)
        return False
    return True

def writeSign(file_outText):
    file_outText.write('^')

def writeTextSource(file_outText,section):
    for text in section:
        if text[0:3] == '-->':
            file_outText.write('{'+text[4:-1] + '}')
        else:
            file_outText.write(text[1:-1])
    file_outText.write('\n')

def writeFormatSource(file_formatSource,string,type):
    if type == 'original':
        file_formatSource.write(string)
        #print(string)
    if type == 'begin':
        file_formatSource.write('begin\n')
        #print('begin')
    if type == 'end':
        file_formatSource.write('end\n')
        #print('end')

def main( inputFile , outputTextSource , outputFormatSource ):
    with open(file = outputFormatSource,mode='w',encoding = 'utf8') as f_outFormat:
        with open(file=outputTextSource,mode = 'w',encoding = 'utf8') as f_outText:
            with open(file = inputFile, mode = 'r',encoding ='utf8') as f_in:
                data_input = f_in.readline()
                section = []
                ldstrBuffer = []
                begin_flag = False
                proc = 0
                while data_input:
                    inputData = str(data_input)
                    #print(inputData)
                    if(inputData[8:12]) == 'text':
                        if not begin_flag:
                            writeFormatSource(f_outFormat,inputData,'begin')
                        begin_flag = True
                        section.append(selector(inputData))
                    elif(inputData[8:13]) == 'ldstr':
                        #section.append('-->'+selector(inputData))
                        ldstrBuffer.append(inputData)
                    elif(inputData[8:12]) == 'ctrl':
                        if selector(inputData)[1:-1] == 'p':
                            begin_flag = False
                            writeTextSource(f_outText,section)
                            writeFormatSource(f_outFormat,inputData,'end')
                            section.clear()
                    elif (inputData[8:12]) == 'proc' or (inputData[8:12]) =='line':
                        proc +=1
                    elif(inputData[8:12]) == 'call' and '$3198fd01 (2)' in inputData:        #注音    
                        word = '-->'+selector(ldstrBuffer.pop())
                        sub = '-->'+selector(ldstrBuffer.pop())
                        section.append(' ^ ')
                        section.append(sub)
                        section.append(word)
                        #section.insert(-2,)
                    elif(inputData[8:12]) == 'call' and '$5100e302 (0)' in inputData:   #名词解析2
                        #print(inputData)
                        data_input = f_in.readline()
                        section.append(' * ')
                        section.append('-->'+selector(data_input))
                        data_input = f_in.readline()
                    elif(inputData[8:12]) == 'call' and '$38723956 (1)' in inputData:  #名词解析
                        section.append('-->'+selector(ldstrBuffer.pop()))
                        proc +=1
                    elif 'call' in inputData: #
                        for lds in ldstrBuffer:
                            writeFormatSource(f_outFormat,lds,'original')
                        ldstrBuffer.clear()
                        writeFormatSource(f_outFormat,inputData,'original')
                    else:
                        writeFormatSource(f_outFormat,inputData,'original')
                        #print(inputData)
                    data_input = f_in.readline()


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

def checkFmtCompelition(fmtFile):
    with open(file = fmtFile, mode = 'r',encoding = 'utf8') as f:
        fmtDate = f.readline()
        flag = False
        while fmtDate:
            if fmtDate == 'begin':
                flag = True
            if fmtDate == 'end':
                flag = False
            else:
                if flag:
                    print(fmtFile)
            fmtDate = f.readline()

# if __name__ == '__main__':
#     files = os.listdir('../texts/fmt')
#     results = []
#     pattern = re.compile(r'(.*).fmt')
#     for f in files:   
#         if pattern.match(f) != None:
#             results.append(f)
#     for f in files:
#         checkFmtCompelition('../texts/fmt/'+f)

if __name__ == '__main__':
    files = os.listdir('../texts/original mjil')
    results = []
    pattern = re.compile(r'(.*).mjil')
    for f in files:   
        if pattern.match(f) != None:
            results.append(f)
    for f in files:
        print(f)
        main('../texts/original mjil/'+f,'../texts/content/'+f[0:-4]+'txt','../texts/fmt/'+f[0:-4]+'fmt')
        orderText('../texts/content/'+f[0:-4]+'txt')
    #print(interpreter('\u3000俺――^{はやぶさおとや}{隼乙矢}は四人の仲間たちとともに\u3000慌ただしく準備に追われながらも、\u3000じっと“その時”を待った。'))