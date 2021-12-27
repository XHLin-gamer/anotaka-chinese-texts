

import  re

def checkDialogues(string):
    dialogue_r = re.compile(r'【(.*)】「(.*)」')
    dialogues = dialogue_r.search(string)
    if dialogues != None:
        return True
    return False

def interpreter(string):
    bus = ''
    token = []
    status = ''
    for s in string:
        if s == '*':
            token.append(bus)
            bus = s
            status = 'specialFunc'
        elif s == '^':
            token.append(bus)
            bus = s
            status = 'sign'
        elif s == '{':
            if status != 'specialFunc' and status != 'sign':
                token.append(bus)
                bus = s   
            else:
                bus += s
                status = 'func'   
        elif s == '【':
            bus = '【'
            status = 'name'
        elif s == '}' or s == '】':
            bus+=s
            token.append(bus)
            bus = ''
            status = '' 
        elif s == '\n':
            token.append(bus)
            bus = ''
        else:
            bus +=s           
    if '' in token:
        token.remove('')
    return token 

def writeText(outputFile,text):
    outputFile.write('  0000: text          "%s"' % text)
    print()

def checkType(token):
    #print(token)
    specialFunc_r = re.compile(r'\*{(.*)}')
    specialFunc = specialFunc_r.search(token)
    func_r = re.compile(r'{(.*)}')
    func = func_r.search(token)
    sign_r = re.compile(r'\^{(.*)}')
    sign = sign_r.search(token)
    name_r = re.compile(r'【(.*)】')
    names = name_r.search(token)
    if specialFunc != None:
        return 'specialFunc'
    elif sign != None:
        return 'sign'
    elif func != None:
        return 'func'
    elif names != None:
        return 'name'
    else:
        return 'text'

def writeTokens(outputFile,tokens):
    signFlag = False
    signBus1 = ''
    signBus2 = ''
    for token in tokens:
        if not signFlag:
            tokenType = checkType(token)
            if tokenType == 'text':
                outputFile.write('  0000: text          "%s"\n' % token)
                outputFile.write('  0000: proc\n')
            if tokenType == 'func':
                outputFile.write('  0000: ldstr         "%s"\n' % token[1:-1])
                outputFile.write('  0000: callp         $38723956 (1)\n')
            if tokenType == 'specialFunc':
                outputFile.write('  0000: callp         $5100e302 (0)\n')
                outputFile.write('  0000: ldstr         "%s"\n' % token[2:-1])
                outputFile.write('  0000: callp         $38723956 (1)\n')
            if tokenType == 'sign':
                #print(token)
                signFlag = True
                signBus1 = token[2:-1]
            if tokenType == 'name':
                outputFile.write('  0000: text          "%s"\n' % token)
        else:
            signBus2 = token[1:-1]
            outputFile.write('  0000: ldstr         "%s"\n' % signBus1)
            outputFile.write('  0000: ldstr         "%s"\n' % signBus2)
            outputFile.write('  0000: callp         $3198fd01 (2)\n')
            signFlag = False
            
            
                
                
def writeEnd(outputfile):
    outputfile.write('  0000: ctrl          "p"\n  0000: ctrl          "w"\n')
          
def main(outputFile , inputTextSource ,inputFormatSource ):
    with open(file = outputFile, mode = 'w',encoding='utf-8') as f_out:
        with open(file = inputFormatSource,mode = 'r',encoding = 'utf8') as f_format:
            with open(file = inputTextSource,mode='r',encoding='utf8') as f_text:
                textData = f_text.readline()
                formatData = f_format.readline()
                while formatData: 
                    #print(formatData)
                    if formatData == 'begin\n':
                        #print(formatData)
                        writeTokens(f_out,interpreter(textData))
                        textData = f_text.readline()
                        
                    elif formatData == 'end\n':
                        #print(formatData)
                        writeEnd(f_out)
                    else:
                        f_out.write(formatData)
                    formatData = f_format.readline()

main()