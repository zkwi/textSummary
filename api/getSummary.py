#encoding=utf-8
import jieba
import jieba.analyse 
# 读取文档
def getSummary(text):
	# 对文档进行分词、分句
	jieba.analyse.set_stop_words("api//stop_words.txt")
	words_generator = jieba.cut(text, cut_all=False)
	words_list = list()
	sentences = list() # 分词后的句子集
	sentences_filter = list() # 去掉停止后的句子集合
	sentence = list() # 包含停止词
	sentence_filter = list() # 去掉停止词
	stopwords = list()
	for line in open("api//stop_words.txt", encoding='utf-8').readlines():
		stopwords.append(line.strip('\n'))
	for word in words_generator:
		# 遇到句子分隔符，则拆成一个句子
		if word in ["!",  "。", "？", "\n"]:
			sentences.append(sentence)
			sentences_filter.append(sentence_filter)
			sentence = []
			sentence_filter =[]
		else:
			words_list.append(word)
			sentence.append(word)
			if word not in stopwords:
				sentence_filter.append(word)
	# 提取tf-idf值
	tf_idfs = jieba.analyse.extract_tags(text, topK=len(words_list), withWeight=True)
	# 计算SR的值
	srs = list()
	for sentence in sentences_filter:
		sentence_filter_unique = list(set(sentence))
		sum = 0
		for word in sentence_filter_unique:
			for t in tf_idfs:
				if t[0] == word:
					sum = sum + t[1] # tf_idfs值求和
		if len(sentence_filter_unique) == 0:
			sr = 0
		else:
			sr = sum
		srs.append(sr)
	# 将分词后的sentence，去重后的tr，相关性sr整理在一起
	document = list()
	for i in range(len(sentences)):
		# 去除0分项
		if srs[i] == 0:
			continue
		# 去重
		existd = False
		for d in document:
			if sentences[i] == d["sentence"]:
				existd = True
				break
		if existd:
			continue
		sentence = dict()
		sentence["sentence"] = sentences[i]
		sentence["sentence_join"] = "".join(sentences[i]).strip()
		# 此处，原算法是加权值，但我认为加权之后偏向于输出短句，效果不好，因此修改为不加要权
		# sentence["SR"] = srs[i] / len(sentence["sentence"])
		sentence["SR"] = srs[i] # 相关性
		document.append(sentence)
	document = sorted(document, key=lambda k: k['SR'], reverse=True) # 按SR也就是相关性进行倒序

	# 计算频繁项集
	from pymining import itemmining
	item_sets = itemmining.relim(itemmining.get_relim_input(sentences_filter), min_support=2)
	# 合并频繁项集D(I)item_sets
	D = set()
	for item in item_sets:
		if len(item) >= 2:
			D = D | item # 进行并集计算
	# 计算tf_idfs值，取出排名靠前的20个词
	words_text = " ".join(D)
	tf_idfs = jieba.analyse.extract_tags(words_text, topK=len(words_list), withWeight=True)
	print("通过频繁项集计算出来的词组", D)
	for t in tf_idfs:
		if len(D) <= 20:
			D.add(t[0])

	# 通过贪心算法计算
	for sentence in document:
		sentence["SC"] = 0
		for word in sentence["sentence"]:
			if word in D:
				sentence["SC"] = 1
				D.remove(word)
	print("摘要句子, 相关性")
	# 提取出关键句，并且要求句子由至少3个词组成
	results = dict()
	results["keywords"] = list(D)
	results["sentences"] = list()
	for sentence in document:
		if sentence["SC"] == 1 and len(sentence["sentence"]) > 2:
			results_sentence = dict()
			results_sentence["SR"] = round(sentence["SR"], 2)
			results_sentence["sentence_join"] = sentence["sentence_join"]
			results["sentences"].append(results_sentence)
			print(sentence["sentence_join"], sentence["SR"])
	return results

r = getSummary(open("api//data.txt", encoding="utf-8").read())
print(r)

