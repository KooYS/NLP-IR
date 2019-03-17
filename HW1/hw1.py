import os, time  
import nltk
import matplotlib.pyplot as plt
from nltk import regexp_tokenize
from nltk.tokenize import sent_tokenize


file_list = os.listdir("./data")

for file in file_list:
	if not file.endswith(".txt"):
		continue
	content = ""
	array = []
	with open("./data/"+file, "r", encoding="utf-8") as f:
		print(file)
		content = f.read()
		tokens=nltk.word_tokenize(content)
		
		en = nltk.FreqDist(tokens)
		plt.ion()
		plt.figure(figsize=(20, 8))
		en.plot(100,title=file)
		plt.savefig('./result/'+file+'.png')
		plt.ioff()
		plt.show()
		for x in en.most_common():
			array.append(x)

		array = sorted(array,key=lambda x:(-int(x[1]),x[0]))
		f.close()


	with open("./result/"+ file, 'w+', encoding="utf-8") as f:
		for x in array:
			f.write(x[0]+"\t"+str(x[1])+"\n")
		f.close()

