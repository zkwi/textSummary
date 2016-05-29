#encoding=utf-8
import jieba.analyse
import jieba.posseg

class TextSummary:
	text = ""
	title = ""
	keywords = list()
	sentences = list()
	summary = list()

	def SetText(self, title, text):
		self.title = title
		self.text = text

	def __SplitSentence(self):
		# 通过换行符对文档进行分段
		sections = self.text.split("\n")
		for section in sections:
			if section == "":
				sections.remove(section)

		# 通过分割符对每个段落进行分句
		for i in range(len(sections)):
			section = sections[i]
			text = ""
			k = 0
			for j in range(len(section)):
				char = section[j]
				text = text + char
				if char in ["!",  "。", "？"] or j == len(section)-1:
					text = text.strip()
					sentence = dict()
					sentence["text"] = text
					sentence["pos"] = dict()
					sentence["pos"]["x"] = i
					sentence["pos"]["y"] = k
					# 将处理结果加入self.sentences
					self.sentences.append(sentence)
					text = ""
					k = k + 1

		for sentence in self.sentences:
			sentence["text"] = sentence["text"].strip()
			if sentence["text"] == "":
				self.sentences.remove(sentence)

		# 对文章位置进行标注，通过mark列表，标注出是否是第一段、尾段、第一句、最后一句
		lastpos = dict()
		lastpos["x"] = 0
		lastpos["y"] = 0
		lastpos["mark"] = list()
		for sentence in self.sentences:
			pos = sentence["pos"]
			pos["mark"] = list()
			if pos["x"] == 0:
				pos["mark"].append("FIRSTSECTION")
			if pos["y"] == 0:
				pos["mark"].append("FIRSTSENTENCE")
				lastpos["mark"].append("LASTSENTENCE")
			if pos["x"] == self.sentences[len(self.sentences)-1]["pos"]["x"]:
				pos["mark"].append("LASTSECTION")
			lastpos = pos
		lastpos["mark"].append("LASTSENTENCE")

	def __CalcKeywords(self):
		# 计算tf-idfs，取出排名靠前的20个词
		words_best = list()
		words_best = words_best + jieba.analyse.extract_tags(self.text, topK=20)
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
		# 保留前20个关键词
		keywords = jieba.analyse.extract_tags(" ".join(keywords), topK=20)
		keywords = list(set(keywords))
		self.keywords = keywords

	def __CalcSentenceWeightByKeywords(self):
		# 计算句子的关键词权重
		for sentence in self.sentences:
			sentence["weightKeywords"] = 0
		for keyword in self.keywords:
			for sentence in self.sentences:
				if sentence["text"].find(keyword) >= 0:
					sentence["weightKeywords"] = sentence["weightKeywords"] + 1

	def __CalcSentenceWeightByPos(self):
		# 计算句子的位置权重
		for sentence in self.sentences:
			mark = sentence["pos"]["mark"]
			weightPos = 0
			if "FIRSTSECTION" in mark:
				weightPos = weightPos + 2
			if "FIRSTSENTENCE" in mark:
				weightPos = weightPos + 2
			if "LASTSENTENCE" in mark:
				weightPos = weightPos + 1
			if "LASTSECTION" in mark:
				weightPos = weightPos + 1
			sentence["weightPos"] = weightPos

	def __CalcSentenceWeightByCueWords(self):
		# 计算句子的线索词权重
		index = ["总之", "总而言之", "报导", "新华社", "报道"]
		for sentence in self.sentences:
			sentence["weightCueWords"] = 0
		for i in index:
			for sentence in self.sentences:
				if sentence["text"].find(i) >= 0:
					sentence["weightCueWords"] = 1

	def __CalcSentenceWeight(self):
		self.__CalcSentenceWeightByPos()
		self.__CalcSentenceWeightByCueWords()
		self.__CalcSentenceWeightByKeywords()
		for sentence in self.sentences:
			sentence["weight"] = sentence["weightPos"] + 2 * sentence["weightCueWords"] + sentence["weightKeywords"]

	def CalcSummary(self, ratio=0.1):
		# 清空变量
		self.keywords = list()
		self.sentences = list()
		self.summary = list()

		# 调用方法，分别计算关键词、分句，计算权重
		self.__CalcKeywords()
		self.__SplitSentence()
		self.__CalcSentenceWeight()

		# 对句子的权重值进行排序
		self.sentences = sorted(self.sentences, key=lambda k: k['weight'], reverse=True)

		# 根据排序结果，取排名占前X%的句子作为摘要
		# print(len(self.sentences))
		for i in range(len(self.sentences)):
			if i < ratio * len(self.sentences):
				sentence = self.sentences[i]
				self.summary.append(sentence["text"])

		return self.summary


