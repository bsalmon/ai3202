# CSCI 3202 Assignment 6
# Bayes Net Disease Predictor
# Brian Salmon

import getopt
import sys

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


def main():
	BN = BNetwork()
	BN.create_network()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	# Parser:
	for o, a in opts:
		if o in ("-p"):
			(variable, new_value) = a.split('=')
			BN = setPrior(BN, variable, float(new_value))
		elif o in ("-m"):
			print calculateMarginal(BN, a)
		elif o in ("-g"):
			(var, given) = a.split('|')
			calculateConditional(BN, var, given)
		elif o in ("-j"):
			print "flag", o
			print "args", a
                        print "Calculating the joint probability"
		else:
			assert False, "unhandled option"

def setPrior(BN, variable, new_value):
	# Set a marginal probability for smoking or pollution
	print "setting prior for variable {0} to {1}".format(variable, new_value)
	if variable is "P":
		BN.nodes["pollution"].marginal = new_value
	elif variable is "S":
		BN.nodes["smoker"].marginal = new_value

	return BN

def calculateConditional(BN,var, given):
	print "Calculate conditional probability of {0} given {1}".format(var, given)

        if var == given:
            print 1
        else:
            #Set given's probability to 1
            BN = setPrior(BN, given, 1)

            #calculate the marginal as if the given was certain
            print calculateMarginal(BN, var)
            return None

def calculateMarginal(BN, arg):
	print "calculate marginal probability for variable {0}".format(arg)

	if arg is "P" or arg is "p":
		return BN.nodes["pollution"]

	elif arg is "C" or arg is "c":
		pollution = BN.nodes["pollution"]
		smoker = BN.nodes["smoker"]

		cancer = BN.nodes["cancer"]
		cancer.marginal = cancer.conditionals["ps"]*pollution.marginal*smoker.marginal + cancer.conditionals["~ps"]*(1-pollution.marginal)*(smoker.marginal) + cancer.conditionals["p~s"]*pollution.marginal*(1-smoker.marginal) + cancer.conditionals["~p~s"]*(1-pollution.marginal)*(1-smoker.marginal)
		return cancer
	
	
	elif arg is "S" or arg is "s":
		return BN.nodes["smoker"]


	elif arg is "D" or arg is "d":
		dyspnoea = BN.nodes["dyspnoea"]
		cancer = BN.nodes["cancer"]
		if not cancer.marginal or cancer.marginal is 0:
			BN.nodes["cancer"] = calculateMarginal(BN, "C")
			cancer = BN.nodes["cancer"]

		dyspnoea.marginal = dyspnoea.conditionals["c"]*cancer.marginal + dyspnoea.conditionals["~c"]*(1-cancer.marginal)
		return dyspnoea

	elif arg is "X" or arg is "x":
		xray = BN.nodes["xray"]
		# calculates the cancers marginal
		cancer = BN.nodes["cancer"]
		if not cancer.marginal or cancer.marginal is 0:
			BN.nodes["cancer"] = calculateMarginal(BN, "C")
			cancer = BN.nodes["cancer"]
		xray.marginal = xray.conditionals["c"]*cancer.marginal + xray.conditionals["~c"]*(1-cancer.marginal)

		return xray



if __name__ == "__main__":
    main()
