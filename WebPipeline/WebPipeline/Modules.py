import mockobjects
class Module:
  def __init__(self,name,data,description):
    self.data = data
    self.name = name
    self.description = description
  def find(self,name):
    for item in self.data:
      if item.name == name:
        return item
    return False

class Task:
  def __init__(self,data,name,description):
    self.data = data
    self.name = name
    self.description = description

class GenerateModule:
  def __init__(self):
    self.module = []
  def add(self,module):
    self.module += [module]
  def find(self,name):
    for item in self.module:
      if item.name == name:
        return item
    return False

class Grader:
  def __init__(self,injector):
    self.injector = injector

  def grade(self,cur,input):
    if self.injector.getModule().find(cur[0]).find(cur[1]).data[cur[2]][1].lower() == input.lower():
      return True
    else:
      return False

class Injector: #Allows mockdispensers to go into flask
  def __init__(self,Module):
    self.module = Module
  def overrideModule(self,Module):
    self.module = Module
  def getModule(self):
    return self.module


#Assignments:
#Beginner
BeginnerVocab1 = Task(
  [["orange","oranje"],
   ["kitchen","keuken"],
   ["juice","sap"],
   ["food","voedsel"],
   ["coffee","koffie"],
   ["garlic","knoflook"],
   ["oil","olie"],
   ["soup","soep"],
   ["fat","dik"],
   ["water","water"],
   ["ice","ijs"],
   ["knife","mes"],
   ["salt","zout"]],

   "Vocabulary 1", 
   ["English","Dutch"])

BeginnerGrammar1 = Task(
  [["She _____(eat) noodles every Monday.","eats"], 
   ["Wichai _____(play) on the computer every day.","plays"],
   ["He _____(watch) television every morning.","watches"],
   ["My father _____(drive) a new car.","drives"]],
   
   "Grammar 1 - Simple Present",
   ["English sentence with an English hint","Word"])

#Advanced
AdvancedVocab1 = Task(
  [["abandon","achterlaten"],
   ["inept","onzinnig"],
   ["jubilant","jebelend"],
   ["novice","beginner"],
   ["quaint","vreemd"],
   ["rash","uitslag"],
   ["staid","sober"],
   ["vexing","vervelend"],
   ["plethora","overvloed"],
   ["obsequious","kruiperig"],
   ["repudiate","verwerpen"],
   ["meticulous","nauwkeurig"]],

   "Vocabulary 2", 
   ["English","Dutch"])

AdvancedGrammar1 = Task(
  [["Karen _____(send) me an e-mail.","has sent"],
   ["Dave and Pat _____(visit) the museum.","have visited"],
   ["I _____(to be) at the pet shop","have been"],
   ["Marcus _____(to have) an accident.","has had"]],
   
   "Grammar 1 - Present Perfect",
   ["English sentence with an English hint","Word"])
#Assignment implementation ends here

#Module creation begins here
modules = GenerateModule()
modules.add(Module("Beginner-1",[BeginnerVocab1,BeginnerGrammar1],
                                "Beginner level exercises. These exercises are simply and provide introduction to the English language."))

modules.add(Module("Advanced-1",[AdvancedVocab1,AdvancedGrammar1],
                                "Advanced level exercises. These exercises are more difficult and truely test your knowledge."))
#Module creation ends here


injector = Injector(modules)
#injector.overrideModule(mockeries.MockDispenser())
grader = Grader(injector)
