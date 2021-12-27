import re
import os
import struct



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

def deOrder(string):
    order = re.compile(r'<[0-9][0-9][0-9][0-9]>(.*)')
    isOrder = order.search(string)
    if isOrder != None:
        return string[7:]
    return string

def replacer(string,contenceForReplace):
    result = re.sub(r'"(.*)"','"'+contenceForReplace+'"',string)
    #print(result)
    return result

def selector(string):
    sentence = re.compile(r'"(.*)"')
    result = sentence.search(string)
    return str(result[0])

def fix0d0a(file):
    print(file)
    with open(file = file+'.fixed',mode = "wb") as f_w:
        with open(file = file,mode = "rb") as f:
            con = f.read()
            for i in con:
                #print(i)
                con = struct.pack('B',i)
                if i  != 13:
                    f_w.write(con)
            f.close()
        f_w.close()
    os.remove(file)
    os.rename(file+'.fixed',file)
    
    
textSourceFileName = 'text.in'
formaterFile = '0-01-01.mjil'
outputFile = 'reFormatFile.out'

def main(textSourceFileName,formaterFile ,outputFile):
    with open(file = outputFile,mode='w',encoding='utf-8') as f_w:
        with open(file = formaterFile,mode = 'r',encoding = 'utf-8') as f_f:
            with open(file = textSourceFileName,mode = 'r',encoding = 'utf8') as f:
                textBuffer = []           
                text = f.readline().replace('\n','')
                dialog = re.compile(r'【(.*)】「(.*)')
                while text:
                    textbuffer = text.split('\\n')
                    
                    for i in textbuffer: 
                        result = dialog.search(i)
                        if result == None:
                            textBuffer.append(i)
                        else:
                            r_who = re.compile(r'【(.*)】')
                            who = r_who.search(i)
                            textBuffer.append(who[0])
                            r_what = re.compile(r'「(.*)')
                            what = r_what.search(i)
                            textBuffer.append(what[0])
                    text = f.readline().replace('\n','')          
                while '' in textBuffer:
                    textBuffer.remove('')  
                #print(textBuffer)
                formatData = f_f.readline()
                flag = True
                while formatData:
                    s = str(formatData)
                    if s[8:12] == 'text':
                        if flag:
                            flag = False
                            if len(textBuffer) > 0:
                                f_w.write(replacer(formatData,deOrder(str(textBuffer[0]))))
                            else:
                                f_w.write(replacer(formatData,deOrder(str(' '))))
                            #print(replacer(formatData,deOrder(str(textBuffer[0]))))
                            wh_w= re.compile(r'【(.*)】')
                            if len(textBuffer) > 0:
                                who = wh_w.search(textBuffer[0])
                                if who is not None:
                                    flag = True            
                                textBuffer.remove(textBuffer[0])
                                
                        else:
                            f_w.write(replacer(formatData,deOrder('')))
                            #print(replacer(formatData,deOrder('')))
                        formatData = f_f.readline()
                        continue
                    if s[8:13] == 'ldstr' and check(formatData):
                        #print(selector(formatData))
                        if selector(formatData) !='""':
                            if len(textBuffer) > 0:
                                f_w.write(replacer(formatData,deOrder(str(textBuffer[0]))))
                                #print(replacer(formatData,deOrder(str(textBuffer[0]))))
                                textBuffer.remove(textBuffer[0])
                            else:
                                f_w.write(replacer(formatData,deOrder(str(""))))

                        else:
                            f_w.write(replacer(formatData,deOrder('')))
                        formatData = f_f.readline()
                        flag = True
                        continue 
                    if s[8:12] == 'ctrl':
                        if selector(formatData)[1:-1] == 'n':
                            #print(selector(formatData)[1:-1])
                            flag = True
                        if selector(formatData)[1:-1] == 'p':
                            flag = True
                    f_w.write(formatData)
                    #print(formatData)                         
                    formatData = f_f.readline()
    fix0d0a(outputFile)
    

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

if __name__ == "__main__":
    files = os.listdir('../text_single')
    results = []
    pattern = re.compile(r'(.*).txt')
    for f in files:   
        if pattern.match(f) != None:
            results.append(f)
    for r in results:
        clearBlankLine('../text_single/'+r)
        main('../text_single/'+r,'../dis/'+r[:-3]+'mjil','../distribution/'+r[:-3]+'mjil')