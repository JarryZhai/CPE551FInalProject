'''
Ruijie Zhai
'''

import js
import sys
import js2py
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QPushButton

class google():
	def __init__(self):
		self.headers = {
						'User-Agent': 'XXX',
					}
		self.url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}'
	def translate(self, word):
		if len(word) > 4891:
			raise RuntimeError('The length of word should be less than 4891...')
		languages = ['zh-CN', 'en']
		if not self.isChinese(word):
			target_language = languages[0]
		else:
			target_language = languages[1]
		res = requests.get(self.url.format(target_language, self.getTk(word), word), headers=self.headers)
		return [res.json()[0][0][0]]
	def getTk(self, word):
		evaljs = js2py.EvalJs()
		js_code = js.gg_js_code
		evaljs.execute(js_code)
		tk = evaljs.TL(word)
		return tk
	def isChinese(self, word):
		for w in word:
			if '\u4e00' <= w <= '\u9fa5':
				return True
		return False


class Demo(QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setWindowTitle('Translator (between Chinese and English) powered by Google')
		self.Label1 = QLabel('Input what you do not anderstand (word or sentence): ')
		self.Label2 = QLabel('Here is the answer: ')
		self.LineEdit1 = QLineEdit()
		self.LineEdit2 = QLineEdit()
		self.translateButton3 = QPushButton()
		self.translateButton3.setText('translate')
		self.grid = QGridLayout()
		self.grid.setSpacing(15)
		self.grid.addWidget(self.Label1, 1, 0)
		self.grid.addWidget(self.LineEdit1, 2, 0)
		self.grid.addWidget(self.Label2, 3, 0)
		self.grid.addWidget(self.LineEdit2, 4, 0)
		self.grid.addWidget(self.translateButton3, 5, 2)
		self.setLayout(self.grid)
		self.resize(400, 150)
		self.translateButton3.clicked.connect(lambda : self.translate(api='google'))
		self.gg_translate = google()
	def translate(self, api='google'):
		word = self.LineEdit1.text()
		if not word:
			return
		elif api == 'google':
			results = self.gg_translate.translate(word)
		else:
			raise RuntimeError('something went wrong')
		for result in results:
			self.LineEdit2.setText(result)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = Demo()
	demo.show()
	sys.exit(app.exec_())