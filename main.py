import re
from itertools import combinations

def getListOfLines():
    f = open("automato.txt", "r")
    lines = f.readlines()
    newLines = []
        
    for line in lines:
        sp = line.split("\n")
        newLines.append(sp[0])
        
        f.close()
        
    return newLines

class Utils:

    def __init__(self, list):
        self.__list = list
  
    def generateTransitionsData(self):
        index = self.findIndexes()
        
        graph = []
        transitions = self.__list[index["transitions"] + 1:]
        splitedTransitions = self.splitTransitions(transitions)
        for transitionArray in splitedTransitions:
            vertix = transitionArray[0]
            peso = transitionArray[1]
            listAdj = transitionArray[2:]
            
            for adj in listAdj:
              graph.append(vertix)
              graph.append([adj, peso])

         
        return graph

    def splitTransitions(self, transitions):
        splitedTrans = []
        for transition in transitions:
          splitedTrans.append(re.split("[:>,]+", transition))
        return splitedTrans
    
    def getAlphabet(self):
      alphabet = []
      alphabetIndex = self.findIndexes()["alphabet"]
      transitionIndex = self.findIndexes()["transitions"]
      for i in range(alphabetIndex + 1, transitionIndex):
        alphabet.append(self.__list[i])
      return alphabet
    
    def getInitial(self):
      initial = self.findIndexes()["initial"]
      return self.__list[initial+1]
    
    def getAccepting(self):
      accepting = []
      indexDict = self.findIndexes()
      acceptingIndex = indexDict["accepting"]
      alphabetIndex = indexDict["alphabet"]
      for i in range(acceptingIndex + 1, alphabetIndex):
        accepting.append(self.__list[i])
      return accepting
    
    def getStates(self):
      index = self.findIndexes()
      initialIndex = index["initial"]
      states = []
      for i in range(1,initialIndex):
        states.append(self.__list[i])
      return states

    def findIndexes(self):
        allIndex = {}
        for i in range(len(self.__list)):
            if self.__list[i] == "#states":
                allIndex["states"] = i
            elif self.__list[i] == "#initial":
                allIndex["initial"] = i
            elif self.__list[i] == "#accepting":
                allIndex["accepting"] = i
            elif self.__list[i] == "#alphabet":
                allIndex["alphabet"] = i
            elif self.__list[i] == "#transitions":
                allIndex["transitions"] = i
        return allIndex


utils = Utils(getListOfLines())
transData = utils.generateTransitionsData()
alphabet = utils.getAlphabet()
initial = utils.getInitial()
accepting = utils.getAccepting()
states = utils.getStates()


class DeterministicFiniteAutomaton:
  def __init__(self, graph, alphabet, initial, accepting, states):
    self.__graph = graph
    self.__alphabet = alphabet
    self.__initial = initial
    self.__accepting = accepting
    self.__states = states
  
  def validateWord(self, word):
    graph = self.generateGraph()
    currentState = self.__initial
    for letter in word:
      for peso, adj in graph[currentState].items():
        if peso == letter:
          currentState = adj
    if currentState in self.__accepting:
      return True
    return False

  def generateGraph(self):
    graph = {}
    for state in self.__states:
      graph[state] = {}
      for letter in self.__alphabet:
        graph[state][letter] = ""
    
    for i in range(0,len(self.__graph),2):
      vertix = self.__graph[i]
      adj = self.__graph[i+1][0]
      peso = self.__graph[i+1][1]
      graph[vertix][peso] = adj
    return graph