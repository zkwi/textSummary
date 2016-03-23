#encoding=utf-8
import jieba.analyse, jieba.posseg
import copy

def splitSentence(text):
	# 对文档进行分词、分句
	words_list = list(jieba.cut(text, cut_all=False))
	sentences = list() # 分词后的句子集
	sentence = list()
	for word in words_list:
		# 遇到句子分隔符，则拆成一个句子
		if word in ["!",  "。", "？", "\n"]:
			if len(sentence) > 0:
				sentences.append(sentence)
			sentence = []
		else:
			sentence.append(word)
	# 去重
	sentences = [list(x) for x in set(tuple(x) for x in sentences)]
	return sentences

def calcSentenceRank(text, sentences):
	# 提取tf-idf值
	tf_idfs = jieba.analyse.extract_tags(text, topK=100, withWeight=True)
	# 计算SR的值
	srs = list()
	for sentence in sentences:
		words_unique = list(set(sentence))
		sum = 0
		for word in words_unique:
			for t in tf_idfs:
				if t[0] == word:
					sum = sum + t[1] # tf_idfs值求和
		srs.append(sum)
	return srs

def calcKeywords(sentences):
	# 计算频繁项集
	from pymining import itemmining
	item_sets = itemmining.relim(itemmining.get_relim_input(sentences), min_support=2)
	items = set()
	for item in item_sets:
		items = items | item
	text = " ".join(items) # 进行并集计算
	# 计算tf-idfs，取出排名靠前的10个词
	words_best = jieba.analyse.extract_tags(text, topK=10)
	text = ""
	for w in words_best:
		text = text + " " + w
	# 计算词性，提取名词和动词
	words = jieba.posseg.cut(text)
	keywords = list()
	for w in words:
		flag = w.flag
		word = w.word
		if flag.find('n') >= 0 or flag.find('v') >= 0:
			keywords.append(word)
	return keywords

def calcSummary(sentences, srs, keywords):
	# 通过贪心算法计算摘要
	summary = list()
	sentences = [x for (y,x) in sorted(zip(srs,sentences))]
	sentences.reverse()
	for sentence in sentences:
		isSummary = False
		for word in sentence:
			if word in keywords:
				isSummary = True
				keywords.remove(word)
		if isSummary:
			s = "".join(sentence)
			s = s.strip()
			summary.append(s)
	return summary

def getSummary(text, title):
	print(title)
	sentences = splitSentence(text)
	srs = calcSentenceRank(text, copy.deepcopy(sentences))
	keywords = calcKeywords(copy.deepcopy(sentences))
	summary = calcSummary(sentences, srs, copy.deepcopy(keywords))
	results = dict()
	results["keywords"] = keywords
	results["summary"] = summary
	return results
