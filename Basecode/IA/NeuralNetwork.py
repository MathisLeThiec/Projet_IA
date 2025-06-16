import numpy as np
import random
from IA.Dense import *
from IA.Fonctions import *

class NeuralNetwork:
    def __init__(self, inputShape):
        self.inputShape = inputShape
        self.layers = []

    def clone(self):
        nn = NeuralNetwork(self.inputShape)
        for layer in self.layers:
            nn.layers.append(layer.clone())
        return nn

    def addLayer(self, size, activationFunctionStr):
        activationFunction = relu
        d_activationFunction = d_relu
        match activationFunctionStr:
            case "logistic":
                activationFunction = sigmoid
            case "relu":
                activationFunction = relu
            case "elu":
                activationFunction = elu
            case "identity":
                activationFunction = identite
            case "tanh":
                activationFunction = tanh
            case _:
                activationFunction = sigmoid
        inputShape = self.inputShape if len(self.layers)==0 else self.layers[-1].outputShape
        self.layers.append(Dense(inputShape, (size,), activationFunction))
    
    def compute(self, inputs):
        outputs = inputs
        for layer in self.layers:
            outputs = layer.compute(outputs)
        return outputs

    def __str__(self):
        res = ""
        for layer in self.layers:
            res+=layer.__str__()
        return res
    
    def getNbParams(self):
        res = 0
        for layer in self.layers:
            res+=layer.getNbParams()
        return res
    
    def save(self, filename):
        with open(filename, "w") as fichier:
            fichier.write(" ".join([str(self.inputShape[0])]+[str(layer.outputShape[0]) for layer in self.layers])+"\n")
            activations = ["none"]
            for layer in self.layers:
                match layer.activationFunction:
                    case IA.Fonctions.identite : activations.append("identity")
                    case IA.Fonctions.sigmoid : activations.append("logistic")
                    case IA.Fonctions.relu : activations.append("relu")
                    case IA.Fonctions.elu : activations.append("elu")
                    case IA.Fonctions.tanh : activations.append("tanh")
            fichier.write(" ".join(activations)+"\n")
            for i in range(len(self.layers)):
                fichier.write(" ".join([str(bias) for bias in self.layers[i].bias])+"\n")
                for j in range(self.layers[i].inputShape[0]):
                    fichier.write(" ".join([str(weight) for weight in self.layers[i].weights[j]])+"\n")

    def load(self, filename):
        with open(filename, "r") as fichier:
            lines = fichier.readlines()
            fichier.close()

            layerSizes = [int(n) for n in lines[0][:-1].split(" ")]
            activations = lines[1].rstrip().split(" ")
            self.inputShape = (layerSizes[0],)
            self.layers = []

            for i in range(1, len(layerSizes)): self.addLayer(layerSizes[i], activations[i])

            line = 2
            for i in range(len(self.layers)):
                self.layers[i].bias = [float(n) for n in lines[line][:-1].split(" ")]
                line+=1
                for j in range(self.layers[i].inputShape[0]):
                    weights = [float(n) for n in lines[line][:-1].split(" ")]
                    for k in range(self.layers[i].outputShape[0]):
                        self.layers[i].weights[j][k] = weights[k]
                    line+=1