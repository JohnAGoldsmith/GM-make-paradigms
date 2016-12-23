# This program reads data that describes a morphological paradigm.
# The first line is a space-separated list of the affixes.
# A line that begins "\pattern name" is the beginning of an inflectional pattern; 
# that ends only when another \pattern name2 is encountered.
# Put "\end" at the end of each paradigm

# I should use a CSV reading package, which exists in python.

import numpy as np
np.set_printoptions(suppress=True)
 
class CParadigm:
        paradigm_space_dict = {}                # key is  a tuple of a set of feature values, value is a morph
        list_of_feature_value_labels = []       # a list of set of feature values, one for each row of TPM
        list_of_morpheme_indices = []           # a list of the number of the morpheme for each row in the TPM
        feature_values = {}                     # key is name of feature-value; value is its count
        morpheme_dict = {}                      # key is morpheme
        morpheme_list= []    
        TPM_length = 0                          # number of entries in TPM (in paradigm)
        TPM = np.zeros

        def readparadigm(self,f, items):
                linecount = 0
                for line in f:
                  line = line.strip()
                  if len(line) == 0:
                     break
                  items = line.split()
                  morph_number = int(items.pop())
                  morph = self.morpheme_list[morph_number]
                  num_items = len(items)
                  if num_items > 1:
                        linecount += 1
                        feature_set = set(items)
                        self.list_of_feature_value_labels.append(feature_set)
                        print ("line count:", linecount, feature_set)
                        self.paradigm_space_dict[tuple(feature_set)] = morph
                        #print ("set", " ",feature_set)
                        for itemno in range(num_items):
                                thisfv = items[itemno]
                                if thisfv not in self.feature_values:
                                        self.feature_values[thisfv] = 1
                                else:
                                        self.feature_values[thisfv] += 1
                        self.list_of_morpheme_indices.append(morph_number)
                else:
                       print ("error: ", line, len(line), items, num_items)
                self.TPM_length = linecount
                self.TPM = np.zeros((linecount,number_of_morphemes))
                for row_no in range(linecount):
                        print (row_no, self.list_of_morpheme_indices[row_no])
                        self.TPM[row_no, self.list_of_morpheme_indices[row_no]] = 1
                print (self.TPM, "\n ---------\n")


        def printparadigm(self):
                for entry in self.list_of_feature_value_labels:
                        print ("A:", entry, self.paradigm_space_dict[tuple(entry)])
                Y,s,Vh = np.linalg.svd(self.TPM)
                print ("Y\n\n",Y)
                print ("s\n\n",s)
                print("Vh\n\n",Vh)
                pi = np.linalg.pinv(self.TPM)
                print ("pseudoinverse\n\n", pi)



np.set_printoptions(precision=2)

thisparadigm=CParadigm()
with open('russiannouns.txt', 'r') as f:
  listofmorphemes= f.readline()
  morphemes = listofmorphemes.split()
  number_of_morphemes= len(morphemes)
  for morphno in range(len(morphemes)):
    thismorph = morphemes[morphno]
    thisparadigm.morpheme_list.append(thismorph)
    thisparadigm.morpheme_dict[thismorph] = 1
  while True:
          items = f.readline().strip().split()
          if len(items) == 0:
            break
          if (items[0][0] == "\\"):
            if (items[0][1:8] =="pattern"):
              name_of_pattern = items[1]
              thisparadigm = CParadigm()
              thisparadigm.readparadigm(f,items)
              thisparadigm.printparadigm()


# example:
#nul a e u om y ov ax am ami j i  
#\pattern 1
#nom sg 0 
#gen sg 1
#acc sg 0
#loc sg 2 
#dat sg 3
#inst sg 4
#nom pl 5
#gen pl 6
#acc pl 5
#loc pl 7
#dat pl 8
#inst pl 9



paradigm2=CParadigm()
with open('russiannouns2.txt', 'r') as f:
  listofmorphemes= f.readline()
  morphemes = listofmorphemes.split()
  number_of_morphemes= len(morphemes)
  for morphno in range(len(morphemes)):
    thismorph = morphemes[morphno]
    paradigm2.morpheme_list.append(thismorph)
    paradigm2.morpheme_dict[thismorph] = 1
  while True:
          items = f.readline().strip().split()
          if len(items) == 0:
            break
          if (items[0][0] == "\\"):
            if (items[0][1:8] =="pattern"):
              name_of_pattern = items[1]
              paradigm2 = CParadigm()
              paradigm2.readparadigm(f,items)
              paradigm2.printparadigm()

       
