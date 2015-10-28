# bn.py

class Node:
	def __init__(self, name, parents):
		self.name = name
		self.parents = parents
		self.children = []
		self.marginal = 0.0
		self.conditionals = {}

	def add_child(self, child):
		self.children.append(child)

	def __str__(self):
		return "%s: marginal - %f" % (self.name, self.marginal)

class BNetwork:
	def __init__(self):
		self.nodes = {}

	def create_network(self):
		pollution = Node("pollution", None)
		smoker = Node("smoker", None)

		cancer = Node("cancer", [pollution, smoker])
		pollution.add_child(cancer)
		smoker.add_child(cancer)

		xray = Node("xray", [cancer])
		cancer.add_child(xray)

		dyspnoea = Node("dyspnoea", [cancer])
		dyspnoea.add_child(dyspnoea)


		cancer.conditionals["ps"] = 0.03
		cancer.conditionals["~ps"] = 0.05
		cancer.conditionals["p~s"] = 0.001
		cancer.conditionals["~p~s"] = 0.02

		xray.conditionals["c"] = 0.9
		xray.conditionals["~c"] = 0.2

		dyspnoea.conditionals["c"] = 0.65
		dyspnoea.conditionals["~c"] = 0.3
		
		pollution.marginal = 0.9
		smoker.marginal = 0.3

		for n in [pollution, smoker, cancer, xray, dyspnoea]:
			self.nodes[n.name] = n

		return self.nodes

