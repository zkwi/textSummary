#encoding=utf-8
import jieba
import jieba.analyse
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
	# 合并频繁项集D(I)item_sets
	keywords = set()
	for item in item_sets:
		keywords = keywords | item # 进行并集计算
	# 计算tf_idfs值，取出排名靠前的20个词
	words_text = " ".join(keywords)
	words_best = jieba.analyse.extract_tags(words_text, topK=10)
	keywords = set()
	for t in words_best:
		keywords.add(t)
	return list(keywords)

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

def getSummary(text):
	sentences = splitSentence(text)
	srs = calcSentenceRank(text, copy.deepcopy(sentences))
	keywords = calcKeywords(copy.deepcopy(sentences))
	summary = calcSummary(sentences, srs, copy.deepcopy(keywords))
	results = dict()
	results["keywords"] = keywords
	results["summary"] = summary
	return results

r = getSummary(open("api//data.txt", encoding="utf-8").read())
print(r)