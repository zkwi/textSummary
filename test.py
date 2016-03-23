import api.getSummary
text = open("testdata/data.txt", encoding="utf-8").read()
title = "习近平和彭丽媛出席英国女王伊丽莎白二世举行的欢迎晚宴"
results = api.getSummary.getSummary(text, title)
print(results)

text = open("testdata/data1.txt", encoding="utf-8").read()
title = "打好全面建成小康社会决胜之战"
results = api.getSummary.getSummary(text, title)
print(results)

text = open("testdata/data2.txt", encoding="utf-8").read()
title = "两位老部长释疑当你老了怎么办"
results = api.getSummary.getSummary(text, title)
print(results)

text = open("testdata/data3.txt", encoding="utf-8").read()
title = "外媒关注中国老龄化：每年新增墓地相当1/3巴黎"
results = api.getSummary.getSummary(text, title)
print(results)

text = open("testdata/data4.txt", encoding="utf-8").read()
title = "美国国会挺台入国际刑警组织 呼吁奥巴马签署法案"
results = api.getSummary.getSummary(text, title)
print(results)