import api.getSummary
def printResults(results):
	print(results["keywords"])
	for r in results["summary"]:
		print(r)
	print("")

text = open("testdata/rujia1.txt", encoding="utf-8").read()
title = "如家道歉遇袭事件称努力改正 当事人曾就职浙江某媒体"
results = api.getSummary.getSummary(text, title)
printResults(results)

text = open("testdata/rujia2.txt", encoding="utf-8").read()
title = "女生如家遇袭事件发酵 如家承认管理有瑕疵"
results = api.getSummary.getSummary(text, title)
printResults(results)


text = open("testdata/rujia3.txt", encoding="utf-8").read()
title = "如家发布会仅5分钟不设提问环节被指没诚意 专家：难辞其咎"
results = api.getSummary.getSummary(text, title)
printResults(results)


