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


def printmatrix(array,top_column_labels, side_row_labels):
                number_of_columns= len(top_column_labels)
                number_of_rows= len(side_row_labels)
                firstcolumnwidth =15
                print ("  ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        print ('%-8s'%top_column_labels[colno], end="")
                print ()
                for rowno in range(number_of_rows):
                        print ('%-15s'%side_row_labels[rowno],end="")
                        for colno in range(number_of_columns):
                                print ('%6.2f  '% array.item(rowno, colno), end = "")
                        print ()


 
class CParadigm:
        def __init__(self):
                self.FV_tuple_to_morph = {}             # key is  a tuple of a set of feature values, value is a morph
                self.row_number_to_set_of_FVs =[]
                self.row_number_to_list_of_FVs = []
                self.row_number_to_morph_number =[]
                self.feature_values = {}                     # key is name of feature-value; value is its count
                self.morpheme_to_index = {}                      # key is morpheme and value is an integer
                self.morpheme_number_to_morph= []    
                self.TPM_length = 0                          # number of entries in TPM (in paradigm)
                self.TPM = np.zeros
                
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
                       morphindex=self.morpheme_to_index[morph]
                       self.row_number_to_list_of_FVs.append(items)
                       feature_set=set(items)
                       self.row_number_to_set_of_FVs.append(feature_set)      
                       self.FV_tuple_to_morph[tuple(feature_set)] = morph
                       for itemno in range(len(items)):
                          thisfv = items[itemno]
                          if thisfv not in self.feature_values:
                             self.feature_values[thisfv] = 1
                          else:
                             self.feature_values[thisfv] += 1
                       self.row_number_to_morph_number.append(morphindex)
                 
                numberofrows = len(self.row_number_to_set_of_FVs)
                self.TPM_length = numberofrows
                self.TPM = np.zeros((numberofrows,number_of_morphemes))
                for row_no in range(numberofrows):
                   self.TPM[row_no, self.row_number_to_morph_number[row_no]] = 1
                self.TPM_inverse = np.linalg.pinv(self.TPM)
               

       


        def printparadigm(self):
                #print (self.TPM )
                number_of_rows= len(self.row_number_to_morph_number)
                number_of_columns = len(self.morpheme_number_to_morph)
                print ("This TPM matrix")
                printmatrix(self.TPM,self.morpheme_number_to_morph, self.row_number_to_list_of_FVs)

 





               
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



                pi = np.linalg.pinv(self.TPM)
                print ("pseudoinverse\n\n" )
                printmatrix(pi,self.morpheme_number_to_morph, self.row_number_to_list_of_FVs)


                pi_times_matrix = np.matmul(pi,self.TPM)

                print ("\npseudoinverse times matrix\n\n")
                firstcolumnwidth =15
                print ("  ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        print ('%-8s'%self.morpheme_number_to_morph[colno], end="")
                print ()
                for rowno in range(number_of_rows):
                        print ('%-15s'%self.row_number_to_list_of_FVs[rowno],end="")
                        for colno in range(number_of_columns):
                                print ('%6.2f  '% pi_times_matrix.item(rowno, colno), end = "")
                        print ()




                print ("\nmatrix times pseudoinverse \n\n" )
                MtimesPI =  np.matmul(self.TPM,pi)
                firstcolumnwidth =15
                print ("  ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        print ('%-8s'%self.morpheme_number_to_morph[colno], end="")
                print ()
                for rowno in range(number_of_rows):
                        print ('%-15s'%self.row_number_to_list_of_FVs[rowno],end="")
                        for colno in range(number_of_columns):
                                print ('%6.2f  '% MtimesPI.item(rowno, colno), end = "")
                        print ()


print (" --------- Part 1---------------")

filename = "russiannouns1.txt"
thisparadigm1=CParadigm()

with open(filename) as f:
   lines = f.readlines()
#lines = [line.strip() for line in open(filename)]
thisparadigm1.readparadigm(lines)
thisparadigm1.printparadigm()
 
 
 
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

 
print (" --------- Part 2---------------")
filename = "russiannouns2.txt"
thisparadigm2=CParadigm()
with open(filename) as f:
   lines = f.readlines()
#lines = [line.strip() for line in open(filename)]
thisparadigm2.readparadigm(lines)
thisparadigm2.printparadigm()
 
 
matrix1 = np.zeros ((12,12))
matrix1=np.matmul(thisparadigm1.TPM_inverse, thisparadigm2.TPM)
matrix2=np.matmul(thisparadigm2.TPM_inverse, thisparadigm1.TPM)
print ("matrix1\n", matrix1)
print ("matrix2\n", matrix1)
