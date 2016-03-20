#encoding=utf-8
import jieba
import jieba.analyse 
# 读取文档
def getSummary(text):
	# 对文档进行分词、分句
	words_list = list(jieba.cut(text, cut_all=False))
	sentences = list() # 分词后的句子集
	sentence = list() # 包含停止词
	for word in words_list:
		# 遇到句子分隔符，则拆成一个句子
		if word in ["!",  "。", "？", "\n"]:
			if len(sentence) > 0:
				sentences.append(sentence)
			sentence = []
		else:
			sentence.append(word)
	# 去重
	sentences =  [list(x) for x in set(tuple(x) for x in sentences)]
	# 提取tf-idf值
	tf_idfs = jieba.analyse.extract_tags(text, topK=len(words_list), withWeight=True)
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

	# 将分词后的sentence，去重后的tr，相关性sr整理在一起
	document = list()
	for i in range(len(sentences)):
		# 去除0分项
		if srs[i] == 0:
			continue
		sentence = dict()
		sentence["sentence"] = sentences[i]
		# 此处，原算法是加权值，但我认为加权之后偏向于输出短句，效果不好，因此修改为不加要权
		# sentence["SR"] = srs[i] / len(sentence["sentence"])
		sentence["SR"] = srs[i] # 相关性
		document.append(sentence)
	document = sorted(document, key=lambda k: k['SR'], reverse=True) # 按SR也就是相关性进行倒序

	# 计算频繁项集
	from pymining import itemmining
	item_sets = itemmining.relim(itemmining.get_relim_input(sentences), min_support=2)
	# 合并频繁项集D(I)item_sets
	D = set()
	for item in item_sets:
		D = D | item # 进行并集计算
	# 计算tf_idfs值，取出排名靠前的20个词
	words_text = " ".join(D)
	words_best = jieba.analyse.extract_tags(words_text, topK=10)
	D = set()
	for t in words_best:
		D.add(t)

	# 通过贪心算法计算
	for sentence in document:
		sentence["SC"] = 0
		for word in sentence["sentence"]:
			if word in D:
				sentence["SC"] = 1
				D.remove(word)
	# 提取出关键句，并且要求句子由至少3个词组成
	results = dict()
	results["keywords"] = list(D)
	results["document"] = document

	return results

r = getSummary(open("api//data.txt", encoding="utf-8").read())
print(r)