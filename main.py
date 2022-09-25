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

class NonDeterministicFinitAutomaton:
  def __init__(self, graph, alphabet, initial, accepting, states):
      self.__graph = graph
      self.__alphabet = alphabet
      self.__initial = initial
      self.__accepting = accepting
      self.__states = states
  
  def tableOfAllStates(self):
      statesTable = []
      statesCombination = self.allStatesCombinations()
      alphabet = self.__alphabet
      alphabetSize = len(alphabet)
      statesCombinationSize = len(statesCombination)
      increment = 0

      for i in range(statesCombinationSize*alphabetSize):
        statesTable.append([])

      for i in range(statesCombinationSize):
        for j in range(alphabetSize):
          for c in range(0, len(self.__graph),2):
            vertix = self.__graph[c]
            adj = self.__graph[c+1][0]
            peso = self.__graph[c+1][1]
          
          if vertix in statesCombination[i] and peso == alphabet[j]:
              statesTable[increment].append(adj)
          increment += 1
          
      return statesTable, alphabet, statesCombination

  def validateWord(self, word):
      graph = self.tableofValidStates()
      currentState = self.__initial
      for letter in word:
        for peso, adj in graph[currentState].items():
          if peso == letter:
            currentState = adj
          
      for fState in self.__accepting:
        if fState in currentState:
          return True, graph
      
      return False, graph
      
  def tableofValidStates(self):
      graph = self.generateGraph()
      
      validGraph = {}
      visited = []
      queue = [self.__initial]
      
      while queue:
        validGraph[queue[0]] = {}
        for peso, adj in graph[queue[0]].items():
          validGraph[queue[0]][peso] = adj
          if adj not in visited:
            queue.append(adj)
      visited.append(queue.pop(0))
      
      return validGraph
          
          
  def generateGraph(self):
      statesTable, alphabet, statesCombination = self.tableOfAllStates()
      stringStatesCombination = []
      stringStatesTable = []
      graph = {}

      for i in range(len(statesCombination)):
        stringStatesCombination.append("")

      for i in range(len(statesTable)):
        stringStatesTable.append("")

      for i in range(len(statesCombination)):
        for j in statesCombination[i]:
          stringStatesCombination[i] += j

      for i in range(len(statesTable)):
        for state in statesTable[i]:
          stringStatesTable[i] += state
      
      count = 0
      for i in range(len(statesCombination)):
        state = stringStatesCombination[i]
        graph[state] = {}
      for letter in alphabet:
          graph[state][letter] = stringStatesTable[count]
          count +=1
      return graph

  def allStatesCombinations(self):
      statesSize = len(self.__states)
      combinationStates = []
      for i in range(statesSize):
        for combination in combinations(self.__states, i+1):
          combinationStates.append(combination)        
      return combinationStates

class ENonDeterministicFiniteAutomaton:
  def __init__(self, graph, alphabet, initial, accepting, states):
      self.__graph = graph
      self.__alphabet = alphabet
      self.__initial = initial
      self.__accepting = accepting
      self.__states = states
      
  def eClosure(self):
      statesTable = []
      for i in range(len(self.__states)):
        statesTable.append(self.__states[i])
        statesTable.append([])

      for i in range(0,len(self.__graph),2):
        vertix = self.__graph[i]
        adj = self.__graph[i+1][0]
        peso = self.__graph[i+1][1]
      for c in range(0,len(statesTable),2):
        tableVertix = statesTable[c]
        if tableVertix == vertix and peso == '$':
          statesTable[c+1].append(adj)
      
      for i in range(0, len(statesTable),2):
        vertix = statesTable[i]
        statesTable[i+1].insert(0,vertix)
      
      return statesTable

while True:
  word = input("Digite a palavra: ")

  print("================================")
  print("""
      [1]< DFA
      [2]< NFA
      [3]< ENFA
      [4]< Sair
  """)
  select = int(input("Escolha uma opção: "))

  print("================================")
  if select == 1:
    automaton = DeterministicFiniteAutomaton(transData,alphabet,initial, accepting, states)
    validWord =  automaton.validateWord(word)
    print(validWord)
  elif select == 2:
    automaton = NonDeterministicFinitAutomaton(transData,alphabet,initial, accepting, states)
    validWord, graph =  automaton.validateWord(word)
    print(validWord)
    print(graph)
  elif select == 3:
    automaton = ENonDeterministicFiniteAutomaton(transData,alphabet,initial, accepting, states)
    eclosure =  automaton.eClosure()
    print(eclosure)
  elif select == 4:
    break