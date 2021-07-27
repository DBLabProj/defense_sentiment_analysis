'''
# 21. 07. 27
'''
from eunjeon import Mecab
from konlpy.tag import Okt

def textPreprocessing(txt, method="mecab", stopword=[]):
    temp = []
    if method == "mecab":
        
        mecab = Mecab()
        txt = mecab.pos(txt)

        for i in txt:
            if i[1][0] == "J" or i[1][0] == "S":
                if i[1] == "SL":
                    continue
                temp.append(txt.index(i))

    elif method == "okt":
        
        okt = Okt()
        txt = okt.normalize(txt)

        txt = okt.pos(txt)

        for i in txt:
            if i[1] == "Josa" or i[1] == "Number" or i[1] == "Punctuation":
                temp.append(txt.index(i))
    '''
    for i in txt:
        if method == "mecab":
            if i[1][0] == "J" or i[1][0] == "S":
                if i[1] == "SL":
                    continue
                temp.append(txt.index(i))
        
        elif method == "okt":
            if i[1] == "Josa" or i[1] == "Number" or i[1] == "Punctuation":
                temp.append(txt.index(i))
    '''
    temp.reverse()

    for i in temp:
        del txt[i]
    
    result = [i[0] for i in txt]

    for i in stopword:
        while i in result:
            result.remove(i)

    return " ".join(result)

def getStopWords():
    stopword_filename = "stopwords"
    with open(stopword_filename+'.txt', 'rt', encoding="utf-8") as f:
        stopword = f.readlines()
        
    return [ line.strip('\n') for line in stopword ] # stopword_list



if __name__ == "__main__":
    txt = "애플워치를 너무 사고싶다!!"
    stword = getStopWords()
    print( "1.", textPreprocessing(txt, method="mecab", stopword=stword) )
    print( "2.", textPreprocessing(txt, method="okt", stopword=stword) )
    pass