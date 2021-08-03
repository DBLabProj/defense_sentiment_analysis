'''
# 21. 07. 28
'''
from eunjeon import Mecab
# from konlpy.tag import Okt

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
    # Examples
    '''
    txt = "나는 애플워치랑 아이패드를 너무 사고싶다....!!"
    stword = getStopWords()
    print( "1. mecab :", textPreprocessing(txt, method="mecab", stopword=stword) )
    print( "2. okt :", textPreprocessing(txt, method="okt", stopword=stword) )
    '''

    naverPath = "../data/mecab/labeling/"
    filename = "naver-ratings.csv"
    import csv
    f = open(naverPath+filename, 'rt', encoding='utf-8')
    rdr = csv.reader(f)

    data_list = []
    for line in rdr:
        # print(textPreprocessing(line[0], method="mecab", stopword=[]))
        data_list.append( [ textPreprocessing(line[0], method="mecab", stopword=[]), line[1] ] )
    f.close()

    f = open(naverPath+'naver-ratings-mecab.tsv', 'wt', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter='\t')

    for d in data_list:
        wr.writerow(d)
    f.close()

    pass