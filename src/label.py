class Label:
	def __init__(self, name, use_aliquots=False, aliquots=None, count=0): # aliquots should be list of JSON objects / dicts
		self.name = name
		self.use_aliquots = use_aliquots
		self.aliquots = [Aliquot(a['text'], a['number']) for a in aliquots] if use_aliquots else []
		self.count = 0 if self.use_aliquots else int(count)


	def get_text(self):
		if self.use_aliquots:
			# list of aliquot texts
			return [
				f"{self.name}\n{aliquot.text} {i} of {aliquot.number}"
				for aliquot in self.aliquots
				for i in range(1, aliquot.number + 1)
			]
		
		else:
			return [self.name] * self.count


class LabelList:
	def __init__(self, labels):
		self.labels = [Label(**l) for l in labels]

	def get_label_texts(self):
		return [text for label in self.labels for text in label.get_text()]


class Aliquot:
	def __init__(self, text, number):
		self.text = text
		self.number = int(number)

	