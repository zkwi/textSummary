from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route('/api/getSummary/', methods=['GET', 'POST'])
def hello_world():
	content = dict()
	try:
		content = request.json
	except:
		return "error:-3 请求数据格式错误"
	if not type(content) == dict:
		return "error:-2 请求json格式错误"
	if 'text' not in content:
		return "error:-1 text字段为空"
	text = content['text']
	import api.getSummary
	results = api.getSummary.getSummary(text)

	return 	json.dumps(results)

@app.route('/')
def index():
	text = open("api//data4.txt", encoding='utf-8').read()
	source = dict()
	source["text"] = text
	results = json.dumps(source)
	# 不渲染变量，直接输出模板，以免和angularjs冲突
	return app.send_static_file("index.html")

if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=82)
