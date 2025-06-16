import numpy as np
import IA.Fonctions


class Dense:
    def __init__(self, inputShape, outputShape, activationFunction):
        self.inputShape = inputShape
        self.outputShape = outputShape
        self.activationFunction = activationFunction

        self.aggregations = np.zeros(outputShape)        
        self.outputs = np.zeros(outputShape)

        self.bias =  np.zeros(outputShape)
        # Choix de l'initialisation en fonction de la fonction d'activation
        if activationFunction == IA.Fonctions.relu:
            # Initialisation He pour ReLU
            std = np.sqrt(2.0 / inputShape[0])
        elif activationFunction == IA.Fonctions.tanh or activationFunction == IA.Fonctions.sigmoid:
            # Initialisation Xavier pour tanh
            std = np.sqrt(1.0 / inputShape[0])
        else:
            std = 1.0 / np.sqrt(inputShape[0])
            
        self.weights = np.random.randn(inputShape[0], outputShape[0]) * std
        
    def compute(self, inputs):
        self.inputs = inputs
        self.aggregations = np.dot(inputs, self.weights)+self.bias
        self.outputs = self.activationFunction(self.aggregations)
        return self.outputs
    
    def __str__(self):
        activation = "logistic"
        match self.activationFunction:
            case IA.Fonctions.identite : activation = "identity"
            case IA.Fonctions.sigmoid : activation = "logistic"
            case IA.Fonctions.relu : activation = "relu"
            case IA.Fonctions.elu : activation = "elu"
            case IA.Fonctions.tanh : activation = "tanh"
        return f"Couche full-connectée à {self.outputShape[0]} neurones : input={self.inputShape}, output={self.outputShape}, activation={activation}\n"
    
    def clone(self):
        copie = Dense(self.inputShape, self.outputShape, self.activationFunction, self.activationDerivate)
        copie.bias = self.bias.copy()
        copie.weights = self.weights.copy()
        return copie
    
    def getNbParams(self):
        return self.outputShape[0] + self.outputShape[0]*self.inputShape[0]