import os,re

def oddifyLine(doubleFile,outputFile):
    with open(file=outputFile,mode = 'w',encoding = 'utf-8') as f_w:
        with open(file = doubleFile,mode='r',encoding='utf-8') as f:
            data = f.readline()
            cnt = 1
            while data:
                if cnt % 2 == 0:
                    #print(data)
                    f_w.write(data)
                data = f.readline()
                cnt += 1
                
def main():
    files = os.listdir('../text_double')
    results = []
    pattern = re.compile(r'(.*).txt')
    for f in files:   
        if pattern.match(f) != None:
            results.append(f)
    #print(results)
    #results.clear()
    #results.append('00-01-01.sjs')
    for r in results:
        oddifyLine('../text_double/'+r,'../text_single/'+r)
main()