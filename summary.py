#encoding=utf-8
import jieba.analyse
import jieba.posseg
import copy
import snownlp

class TextSummary:
	text = ""
	title = ""
	keywords = list()
	summary = list()
	__sentences = list() # 分句后存储句子的List
	__srs = list() # 分钟后每个句子的SentenceRank值list

	def SetTitle(self, title):
		self.title = title

	def SetText(self, text):
		self.text = text

	def __splitSentence(self):
		# 对文档进行分词、分句
		words_list = list(jieba.cut(self.text, cut_all=False))
		sentences = list() # 分词后的句子集
		sentence = list()
		for word in words_list:
			sentence.append(word)
			# 遇到句子分隔符，则拆成一个句子
			if word in ["!",  "。", "？", "\n"]:
				if len(sentence) > 0:
					sentences.append(sentence)
				sentence = []
		# 去重
		self.__sentences = [list(x) for x in set(tuple(x) for x in sentences)]

	def __calcSentenceRank(self):
		# 提取tf-idf值
		sentences = copy.deepcopy(self.__sentences)
		tf_idfs = jieba.analyse.extract_tags(self.text, topK=100, withWeight=True)
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
		self.__srs =  srs


	def __calcKeywords(self):
		# 计算tf-idfs，取出排名靠前的10个词
		words_best = list()
		words_best = words_best + jieba.analyse.extract_tags(self.text, topK=15)
		# 提取第一段的关键词
		parts = self.text.lstrip().split("\n")
		firstpart = ""
		if len(parts) >= 1:
			firstpart = parts[0]
		words_best = words_best + jieba.analyse.extract_tags(firstpart, topK=5)
		# 提取title中的关键词
		words_best =  words_best + jieba.analyse.extract_tags(self.title, topK=3)
		# 将结果合并成一个句子，并进行分词
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
				if len(word) > 1:
					keywords.append(word)
		keywords = keywords + jieba.analyse.textrank(self.text, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
		keywords = jieba.analyse.extract_tags(" ".join(keywords), topK=20)
		keywords = list(set(keywords))
		print(keywords)
		self.keywords = keywords

	def __calcSummary(self):
		# 通过贪心算法计算摘要
		srs = self.__srs
		sentences = self.__sentences
		keywords = copy.deepcopy(self.keywords)
		summary = list()
		sentences = [x for (y,x) in sorted(zip(srs, sentences))]
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
				# 通过snownlp计算句子情感值
				sentiments = snownlp.SnowNLP(s).sentiments #
				se = dict()
				se["sentence"] = s
				se["sentiments"] = sentiments
				summary.append(se)
		self.summary = summary

	def GetSummary(self):
		self.__splitSentence()
		self.__calcSentenceRank()
		self.__calcKeywords()
		self.__calcSummary()

	def PrintResults(self, length=2):
		print(self.title)
		'''
		text = ""
		for s in self.summary:
			text = text + s["sentence"]
		print(text)'''
		summary = sorted(self.summary, key=lambda k: k['sentiments'])
		if length >= len(summary)/2 or length <= 0:
			length = int(len(summary)/2)
		j = 0
		for i in range(0, length):
			j = j + 1
			index = i
			print("("+str(j)+") " + summary[index]["sentence"])
		for i in range(0, length):
			j = j + 1
			index = len(summary) - i - 1
			print("("+str(j)+") " + summary[index]["sentence"])
		print("")
