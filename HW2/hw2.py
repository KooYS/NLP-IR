from collections import defaultdict
import math
import sys
from functools import reduce
import re

document_filenames = {0 : "data/Beauty and the Beast.txt",
                      1 : "data/Get Out.txt",
                      2 : "data/Big Sick, The.txt",
                      3 : "data/Guardians of the Galaxy Vol 2.txt",
                      4 : "data/La La Land.txt",
                      5 : "data/Logan.txt",
                      6 : "data/War for the Planet of the Apes.txt",
                      7 : "data/It.txt",
                      8 : "data/Thor Ragnarok Script.txt",
                      9 : "data/COCO.txt"}


prog = re.compile(r'^[a-zA-Z0-9]+$')
removal = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'.split(",")

# document 개수
N = len(document_filenames)

dictionary = set()
terms = defaultdict(dict)
document_frequency = defaultdict(int)
length = defaultdict(float)

def main():
    initialize_terms()
    initialize_document_frequencies()
    initialize_lengths()
    while True:
        do_search()

def initialize_terms():
    # 각 문서마다 tokenize하고 dictionary 구성한뒤 posting에 term의 개수와 저장
    global dictionary, terms
    for id in document_filenames:
        f = open(document_filenames[id],'r', encoding="utf-8")
        document = f.read()
        f.close()
        terms_per_doc = tokenize(document)
        unique_terms = set(terms_per_doc)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            terms[term][id] = terms_per_doc.count(term) #term 빈도


def tokenize(document):
    # token으로 만드는 작업
    _terms = document.lower().split()
    return [ term for term in _terms  if term not in removal and prog.match(term) ]

def initialize_document_frequencies():
    # 문서당 term의 빈도수
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(terms[term])

def initialize_lengths():
    # 각 문서의 유클리드 거리를 구한다.
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += weight(term,id)**2
        length[id] = math.sqrt(l)

def weight(term,id):
    # tf.idf 구한다.
    if id in terms[term]:
        return terms[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    #idf 구한다.
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0

def do_search():
    query = tokenize(input("찾을 쿼리 입력 : "))
    if query == []:
        sys.exit()
    
    # 토큰화 된 query 와 교집합을 이루는 doc id를 가져온다.
    print(terms)
    relevant_document_ids = intersection(
            [set(terms[term].keys()) for term in query])

    # 아무런 문서가 없다면..
    if not relevant_document_ids:
        print("매치되는 doc이 없습니다.")
    else:
        # 보낸 query와 문서의 similarity를 구하여 ranking을 도출한다.
        scores = sorted([(id,similarity(query,id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        print("ranking")
        for (id,score) in scores:
            print(str(score)+": "+document_filenames[id])

def intersection(sets):
    #주어진 집합리스트 중에서 교집합을 구하기 위하여 만든 함수.
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
    # query and id에 해당하는 document 사이의 cosine similarity을 구한다.
    # 구한 유클리드 거리를 나눌 때 쿼리의 유클리드 거리는 사실상 랭크의 순위를 구하는데 영향을 주지 않는다. 그래서 document 거리만 나눈다. query vector와 document의 weight를 곱하여 similarity에 누적시킨 후 그 document 유클리드 거리로 나눈다.
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*weight(term,id)
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()
