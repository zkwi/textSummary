import api.getSummary
text = open("api/data.txt", encoding="utf-8").read()
title = "习近平和彭丽媛出席英国女王伊丽莎白二世举行的欢迎"
results = api.getSummary.getSummary(text, title)