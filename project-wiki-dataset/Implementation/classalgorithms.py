from __future__ import division  # floating point division
import numpy as np
import utilities as utils
import math
import random
import string



class Classifier:    
    """ Generic classifier interface; returns random classification
    Assumes y in {0,1}, rather than {-1, 1}
    """
    
    def __init__( self, params=None ):
        """ Params can contain any useful parameters for the algorithm """
        
    def learn(self, Xtrain, ytrain):
        """ Learns using the traindata """
        
    def predict(self, Xtest):
        probs = np.random.rand(Xtest.shape[0])
        ytest = utils.threshold_probs(probs)
        return ytest

    
class LogitReg(Classifier):
    """ Logistic regression; need to complete the inherited learn and predict functions """
    
    def sigmoid(self, number):
        return 1.0/(1.0+np.exp(number))

    def __init__( self, params=None ):
        self.weights = None
    
        
    def learn(self, Xtrain, ytrain):
        #print Xtrain.shape[1],ytrain.shape[0]
        p=range(Xtrain.shape[0])
        oldweights=np.dot(np.dot(np.linalg.inv(np.dot(Xtrain.T,Xtrain)),Xtrain.T),ytrain)
        #print oldweights.shape
        NewWeights=np.zeros(oldweights.shape[0])
        tolerance=0.00001
        while self.getTolerance(NewWeights, oldweights)>tolerance:
            NewWeights=oldweights
            for i in range(ytrain.shape[0]):
                p[i]=self.sigmoid(np.dot(-oldweights.T,Xtrain[i]))
            P=np.diag(p);
            IdentityMat=np.identity(len(P))
            Hessian=np.linalg.inv(np.dot(np.dot(np.dot(Xtrain.T,P),np.subtract(IdentityMat,P)), Xtrain))
            Gradient=np.dot(Xtrain.T, np.subtract(ytrain, p))
            oldweights=NewWeights + np.dot(Hessian,Gradient)
        self.weights=oldweights
        
            
    def getTolerance(self,NewWeights, oldweights):
        sum=0
        for i in range(NewWeights.shape[0]):
            sum = sum + (NewWeights[i] - oldweights[i])**2
        
        return math.sqrt(sum)

    def predict(self,Xtest):
        ytest= []
        for i in range(Xtest.shape[0]):
            threshold=self.sigmoid(np.dot(-self.weights.T,Xtest[i]))
            if threshold >= 0.5:
                ytest.append(1)
            else:
                ytest.append(0)
        return ytest
   