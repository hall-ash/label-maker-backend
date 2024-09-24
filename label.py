class Label:
	def __init__(self, name, use_aliquots=False, aliquots=None, count=0): # aliquots should be list of JSON objects / dicts
		self.name = name
		self.use_aliquots = use_aliquots

		if use_aliquots:
			self.aliquots = [Aliquot(a['text'], a['number']) for a in aliquots] 
			self.count = 0
		else:
			self.aliquots = []
			if count:
				try:
					self.count = int(count)
				except ValueError:
					raise ValueError(f"Count must be an integer, but got '{typeof count}'")
			else:
				self.count = 0


	def get_text(self):
		if self.use_aliquots:
			text = []
			for aliquot in self.aliquots:
				text.extend([f'{self.name + "\n"}{aliquot.text} {i} of {str(aliquot.number)}' for i in range(1, aliquot.number + 1)])
			return text
		
		else:
			return [self.name] * int(self.count)
	


class LabelList:
	def __init__(self, labels):

		self.labels = []
		for l in labels:
			name = l['name']
			use_aliquots = l['use_aliquots']
			aliquots = l['aliquots']
			count = int(l['count'])
			self.labels.append(Label(name, use_aliquots=use_aliquots, aliquots=aliquots, count=count))

	def get_label_texts(self):

		label_texts = []
		for label in self.labels:
			label_texts.extend(label.get_text())
		
		return label_texts


class Aliquot:
	def __init__(self, text, number):
		self.text = text
		self.number = int(number)

	