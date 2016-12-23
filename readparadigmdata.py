# This program reads data that describes a morphological paradigm.
# The first line is a space-separated list of the affixes.
# A line that begins "\pattern name" is the beginning of an inflectional pattern; 
# that ends only when another \pattern name2 is encountered.
# Put "\end" at the end of each paradigm

# I should use a CSV reading package, which exists in python.

import numpy as np
import csv 

np.set_printoptions(suppress=True)
np.set_printoptions(precision=2)

 
class CParadigm:
        FV_tuple_to_morph = {}             # key is  a tuple of a set of feature values, value is a morph
        row_number_to_set_of_FVs =[]
        row_number_to_morph_number =[]
        feature_values = {}                     # key is name of feature-value; value is its count
        morpheme_to_index = {}                      # key is morpheme and value is an integer
        morpheme_number_to_morph= []    
        TPM_length = 0                          # number of entries in TPM (in paradigm)
        TPM = np.zeros
        
        def readparadigm(self,lines):

                for lineno in range(len(lines)):
                   line = lines[lineno]
                   items = line.split()
                   if items[0] == "#":
                      if items[1] == "pattern":
                         pattern_label = items[2]
                      else:
                         morphemes = items[1:]
                         number_of_morphemes = len(morphemes)
                         for morphno in range(len(morphemes)):
                            thismorph = morphemes[morphno] 
                            self.morpheme_number_to_morph.append(thismorph)
                            self.morpheme_to_index[thismorph] = morphno
                   else:
                       morph = items.pop(-1)
                       morphindex=thisparadigm.morpheme_to_index[morph]
                       feature_set=set(items)
                       self.row_number_to_set_of_FVs.append(feature_set)      
                       self.FV_tuple_to_morph[tuple(feature_set)] = morph
                       for itemno in range(len(items)):
                          thisfv = items[itemno]
                          if thisfv not in thisparadigm.feature_values:
                             self.feature_values[thisfv] = 1
                          else:
                             self.feature_values[thisfv] += 1
                       self.row_number_to_morph_number.append(morphindex)
                 
                numberofrows = len(self.row_number_to_set_of_FVs)
                self.TPM_length = numberofrows
                self.TPM = np.zeros((numberofrows,number_of_morphemes))
                for row_no in range(numberofrows):
                   self.TPM[row_no, thisparadigm.row_number_to_morph_number[row_no]] = 1

               

       


        def printparadigm(self):
                print (thisparadigm.TPM )
                number_of_rows= len(self.row_number_to_morph_number)

                print ("List of feature value labels and paradigm space dict:")
                for entry in self.row_number_to_set_of_FVs:
                        tuple_of_entry = tuple(entry)
                        this_morph=self.FV_tuple_to_morph[tuple_of_entry]
                        print (entry, this_morph, self.morpheme_to_index[this_morph])
                print ("List of morpheme indices")
                for no in  range(number_of_rows) :
                        morph_number = self.row_number_to_morph_number[no]
                        morph = self.morpheme_number_to_morph[morph_number]
                        morph_number_recompute = self.morpheme_to_index[morph]
                        print ("row: ", no,"   ",morph_number, morph, morph_number_recompute  )
                Y,s,Vh = np.linalg.svd(self.TPM)
                #print ("Y\n\n",Y)
                #print ("\ns\n\n",s)
                #print("Vh",Vh)
                pi = np.linalg.pinv(self.TPM)
                print ("pseudoinverse\n\n", pi)
                print ("\npseudoinverse times matrix\n\n", np.matmul(pi,self.TPM))
                print ("\nmatrix times pseudoinverse \n\n", np.matmul(self.TPM,pi))


print (" --------- Part 1---------------")

filename = "russiannouns1.txt"

thisparadigm=CParadigm()
 
lines = [line.strip() for line in open(filename)]

thisparadigm.readparadigm(lines)

 
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

 
       
