# This program reads data that describes a morphological paradigm.
# The first line is a space-separated list of the affixes.
# A line that begins "\pattern name" is the beginning of an inflectional pattern; 
# that ends only when another \pattern name2 is encountered.
# Put "\end" at the end of each paradigm

# I should use a CSV reading package, which exists in python.

# feature-value space: 

import numpy as np
import csv 
import math

np.set_printoptions(suppress=True)
np.set_printoptions(precision=2)


def makestring(arg):
    if type(arg) is list:
        return "-".join(arg)
    else:
        return  arg 

# this is not being used, and should be deleted
class FVSpace:
        def __init__(self, paradigm):
                self.FV_to_morph_dict = {} # key is a feature value (string) and value is a dict, which has a morpheme as its key and a value of ?
                self.morph_to_FV_dict = {} # key is a morpheme, value is a dict whose key is a FV and whose value is a count;
                self.morph_to_FV_coordinate = {}
                numberofrows = len(paradigm.row_number_to_set_of_FVs)
                for row_number in  range(numberofrows):
                        print ("row number", row_number, end=" ")
                        morphemeno = paradigm.row_number_to_morph_number[row_number]
                        morpheme = paradigm.morpheme_number_to_morph[morphemeno]
                        print ("morpheme and number", morpheme, morphemeno)
                        if morpheme not in self.morph_to_FV_dict:
                                self.morph_to_FV_dict[morpheme] = dict()
                        for FV in paradigm.row_number_to_list_of_FVs[row_number]:
                                if FV not in self.morph_to_FV_dict[morpheme]:
                                        self.morph_to_FV_dict[morpheme][FV] = 0
                                self.morph_to_FV_dict[morpheme][FV] += 1
                                print ("counts ", FV, " ", self.morph_to_FV_dict[morpheme][FV] )
                for morpheme  in  paradigm.morpheme_number_to_morph :
                        print ("45 morpheme ", morpheme)
                        total = 0.0
                        if morpheme in self.morph_to_FV_dict:
                                print ("48", morpheme)
                                self.morph_to_FV_coordinate[morpheme] = dict()
                                for FV in self.morph_to_FV_dict[morpheme]:
                                        total += float(self.morph_to_FV_dict[morpheme][FV]) * self.morph_to_FV_dict[morpheme][FV]
                                denominator = math.sqrt(total)
                                print ("denominator total", denominator, total)
                                if FV not in self.morph_to_FV_coordinate[morpheme]:
                                        self.morph_to_FV_coordinate[morpheme][FV] = 0.0
                                print ("56  morpheme FV", morpheme, FV)
                                self.morph_to_FV_coordinate[morpheme][FV] += self.morph_to_FV_dict[morpheme][FV] / denominator
                                print (morpheme, FV, self.morph_to_FV_coordinate[morpheme][FV])
               

def printmatrix(array,top_column_labels, side_row_labels):
                #number_of_columns= len(top_column_labels)
                #number_of_rows= len(side_row_labels)
                (number_of_rows, number_of_columns) = array.shape
                firstcolumnwidth =13
                print ("   ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        #print ("69 colno" , colno, " ", end="")
                        #print ("69", top_column_labels)
                        #print ("71 ", top_column_labels[colno], colno,  "number of cols", number_of_columns, end= " ")
                        if colno >= len(top_column_labels):
                                break
                        print ('%-8s'%makestring(top_column_labels[colno]), end="")
                print ()
                for rowno in range(number_of_rows):
                        #print ("75 number of rows", rowno, number_of_rows)
                        print ('%-15s'%side_row_labels[rowno],end="")
                        for colno in range(number_of_columns):
                                print ('%6.2f  '% array.item(rowno, colno), end = "")
                        print ()

 
class CParadigm:
        def __init__(self):
                self.row_number_to_set_of_FVs =[]
                self.row_number_to_list_of_FVs = []
                self.row_number_to_morph_number =[]
                self.FVs = {}                     # key is name of feature-value; value is its count
                self.morpheme_to_index = {}                      # key is morpheme and value is an integer
                self.morpheme_list= []    
                self.TPM_length = 0                          # number of entries in TPM (in paradigm)
                self.TPM = np.zeros
                self.B=np.zeros
                self.FV_tuple_to_morpheme = {}             # key is  a tuple of a set of feature values, value is a morph
                self.FV_to_morph_dict = {} # key is a feature value (string) and value is a dict, which has a morpheme as its key and a value of ?
                self.morph_to_FV_dict = {} # key is a morpheme, value is a dict whose key is a FV and whose value is a count;
                self.morph_to_FV_coordinate = {}
                self.number_of_rows_in_paradigm = 0
        def     get_FVs(self):
                        return list(self.FVs.keys())
        def     get_number_of_FVs(self):
                        return len(self.get_FVs())
        def     get_FV(self, index):
                        return (self.get_FVs()[index])
        def     get_morphemes(self):
                        return  self.morpheme_list 
        def     get_morpheme(self, index):
                        return self.morpheme_list[index]
        def     get_number_of_FVs(self):
                        return len(self.get_FVs())
        def     get_number_of_morphemes(self):
                        return len(self.get_morphemes())
        def     get_length_of_paradigm(self):
                        return len(self.row_number_to_list_of_FVs)
        def     get_stringized_FV(self, index):
                        return "-".join(self.row_number_to_list_of_FVs[index])
        def     get_stringized_FVs(self):
                        output = list()
                        for set_of_FVs in self.row_number_to_set_of_FVs:
                                output.append("-".join(set_of_FVs))                                          
                        return output

      

        # The paradigm includes a TPM which is an np.array, and B, which is also a np.arry.
        # TPM: number of rows is the size of the paradigm, and the number of columns is the number of morphemes.
        # B:   number of rows is the number of FVs,        and the number of columns is the number of morphemes.
        def readparadigm(self,lines):
                for lineno in range(len(lines)):
                   line = lines[lineno]
                   items = line.split()
                   if items[0] == "#":
                      if items[1] == "pattern":
                         pattern_label = items[2]
                      else:
                         morphemes = items[1:]
                         for morphno in  range(len(morphemes)):
                            thismorph = morphemes[morphno] 
                            self.morpheme_list.append(thismorph)
                            self.morpheme_to_index[thismorph] = morphno
                   else:
                       morpheme = items.pop(-1)
                       morpheme_index=self.morpheme_to_index[morpheme]
                       self.row_number_to_list_of_FVs.append(items)
                       feature_set = set(items)
                       feature_set_tuple=tuple(set(items))  
                       self.row_number_to_set_of_FVs.append(feature_set)     # this is no longer used. 
                       self.FV_tuple_to_morpheme[feature_set_tuple] = morpheme  # this is ugly and should be done better
                       for itemno in range(len(items)):
                          thisfv = items[itemno]
                          if thisfv not in self.FVs:
                             self.FVs[thisfv] = 1
                          else:
                             self.FVs[thisfv] += 1
                       self.row_number_to_morph_number.append(morpheme_index)
                #self.numberofrows_in_paradigm = len(self.row_number_to_list_of_FVs)
                self.TPM = np.zeros((self.get_length_of_paradigm(), self.get_number_of_morphemes()))
                for row_no in range(self.get_length_of_paradigm()):
                   self.TPM[row_no, self.row_number_to_morph_number[row_no]] = 1
                self.TPM_inverse = np.linalg.pinv(self.TPM)

                # -------------------  compute the matrix B ----------------------------------
               
                # iterate through each row in the paradigm; each row has a set of FVs and a single morpheme associated with it. 
                for row_number in  range(self.get_length_of_paradigm()):
                        morphemeno = self.row_number_to_morph_number[row_number]
                        morpheme = self.morpheme_list[morphemeno]
                        # Make sure that the morph_to_FV_dict is ready for this morpheme.
                        if morpheme not in self.morph_to_FV_dict:
                                self.morph_to_FV_dict[morpheme] = dict()
                        # add a count for each FV in this row to the morpheme we are looking at.
                        for FV in self.row_number_to_list_of_FVs[row_number]:
                                if FV not in self.morph_to_FV_dict[morpheme]:
                                        self.morph_to_FV_dict[morpheme][FV] = 0
                                self.morph_to_FV_dict[morpheme][FV] += 1
                                #print ("counts, morpheme", morpheme,"Feature value", FV, " ", self.morph_to_FV_dict[morpheme][FV] )
                
                self.B = np.zeros((self.get_number_of_FVs(), self.get_number_of_morphemes()))

                # Now we normalize for each morpheme 
                for morpheme_number in range(self.get_number_of_morphemes()):
                        morpheme = self.get_morpheme(morpheme_number)
                        total = 0.0
                        if morpheme in self.morph_to_FV_dict:
                                for FV_number in range(self.get_number_of_FVs()):
                                        FV = self.get_FV(FV_number)
                                        if FV in self.morph_to_FV_dict[morpheme]:
                                                total += float(self.morph_to_FV_dict[morpheme][FV]) * self.morph_to_FV_dict[morpheme][FV]
                                denominator = math.sqrt(total)
                                for FV_number in range(self.get_number_of_FVs()):
                                        FV = self.get_FVs()[FV_number]
                                        if FV in self.morph_to_FV_dict[morpheme]:
                                                self.B[FV_number][morpheme_number]  += self.morph_to_FV_dict[morpheme][FV] / denominator


        def printparadigm(self):
                #print (self.TPM )
                number_of_rows    =  self.get_length_of_paradigm()
                number_of_columns = self.get_number_of_morphemes()
                print ("\nThis TPM matrix Phi")
                printmatrix(self.TPM,self.morpheme_list, self.get_stringized_FVs() ) 
               


                print ("\n\nList of feature value labels and paradigm space dict:\n")
                rowno =0

                string1 ="{:<10} {:20} {:<20}" 
                string2 ="  {:<10} {:20} {:<20}" 
                print (string1.format('row number', 'feature values', 'morpheme number'))
                for row_number in range(number_of_rows):
                        #tuple_of_entry = tuple(set(entry))
                        #this_morph=self.FV_tuple_to_morpheme[tuple_of_entry]
                        print (string2.format(rowno, self.get_stringized_FV(row_number), self.row_number_to_morph_number[row_number] ))
                        rowno += 1
                 
                print ("\n\nB matrix:")
                printmatrix(self.B, self.get_morphemes(),self.get_FVs() )

                


                Y,s,Vh = np.linalg.svd(self.TPM)

                pi = np.linalg.pinv(self.TPM)
                print ("\npseudoinverse of Phi" )
                #printmatrix(pi,self.row_number_to_list_of_FVs, self.morpheme_list)
                printmatrix(pi, self.get_stringized_FVs(),self.morpheme_list)


                pi_times_matrix = np.matmul(pi,self.TPM)

                print ("\npseudoinverse times matrix")
                firstcolumnwidth =15
                print ("  ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        print ('%-8s'%self.morpheme_list[colno], end="")
                print ()
                for rowno in range(number_of_rows):
                        print ('%-15s'%self.morpheme_list[rowno],end="")
                        for colno in range(number_of_columns):
                                print ('%6.2f  '% pi_times_matrix.item(rowno, colno), end = "")
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

if (True):
        print (" --------- Part 2---------------")
        filename = "russiannouns2.txt"
        thisparadigm2=CParadigm()
        with open(filename) as f:
           lines = f.readlines()
        #lines = [line.strip() for line in open(filename)]
        thisparadigm2.readparadigm(lines)
        thisparadigm2.printparadigm()
         
         



        matrix1 = np.zeros ((12,12))

        print ("\nTPM1 inverse:")
        pi = np.linalg.pinv(thisparadigm1.TPM)
        printmatrix(pi,thisparadigm1.row_number_to_list_of_FVs, thisparadigm1.morpheme_list)

        print ("\nTPM2")
        printmatrix(thisparadigm2.TPM,thisparadigm2.morpheme_list, thisparadigm2.row_number_to_list_of_FVs)

        matrix1=np.matmul(thisparadigm1.TPM_inverse, thisparadigm2.TPM)
        print ("\nTPM1 inverse times TPM2\n", matrix1)
        printmatrix(matrix1,thisparadigm1.morpheme_list,thisparadigm2.morpheme_list)
