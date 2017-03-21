import numpy as np
import os, argparse
import matplotlib.pyplot as plt
import imageio
colors = ["#FF0000", "#FFF000", "#008000", "#0000FF", "#000000", "#00FFFF", "#FF00FF", "#FFA500", "#FFE455", "#BC8F8F", "#DA70D6"]

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", type=str, help="Input file path")
parser.add_argument("-o", "--outputFile", type=str, help="Output file path")
parser.add_argument("-k", "--keepImages", action='store_true', help="Do not remove images os states")
parser.add_argument("-s", "--simulationFile", type=str, help="Simulation file name")
args = vars(parser.parse_args())
inputFile = args["inputFile"]
outputFile = args["outputFile"]
keepImages = args["keepImages"]
simulationFile = args["simulationFile"]

states = []

## Get starting state
with open(inputFile) as i:
	lines = i.readlines()
state = []
for line in lines:
	splitted = line.split(" ")
	state.append((int(splitted[0]), int(splitted[1]), int(splitted[2]), splitted[3].rstrip("\r\n")))
states.append(state)

## Get moves
with open(outputFile) as o:
	lines = o.readlines()
state = []
for line in lines:
	if len(line) > 5:
		splitted = line.split(" ")
		state.append((int(splitted[0]), int(splitted[1]), int(splitted[2]), splitted[3].rstrip("\r\n")))
	else:
		states.append(state)
		state = []

images = []
imageNames = []
for imageIndex, state in enumerate(states):
	fig = plt.figure()
	ax = plt.axes()
	imageName = "image" + str(imageIndex) + ".jpg"
	imageNames.append(imageName)
	images.append(imageName)
	for i, car in enumerate(state):
		x = car[1] * 5
		y = (6 - car[0]) * 5
		l = car[2]
		if car[3] == "h":
			w = l * 5
			h = 5
		else:
			w = 5
			h = l * 5
		targetCar = plt.Rectangle((x, y), w, h, fc=colors[i])
		ax.add_patch(targetCar)

	plt.axis('scaled')
	plt.xlim([0, 30])
	plt.ylim([0, 30])
	plt.grid()
	plt.savefig(imageName)
	plt.cla()

for imageName in imageNames:
	images.append(imageio.imread(imageName))

with imageio.get_writer('images/' + simulationFile, mode='I', duration=0.5) as writer:
	for imageName in imageNames:
		image = imageio.imread(imageName)
		writer.append_data(image)
	print simulationFile, " was created under /images folder."

if not keepImages:
	for imageName in imageNames:
		os.remove(imageName)
else:
	for imageName in imageNames:
		os.rename(imageName, "images/" + imageName)

