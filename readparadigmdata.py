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

 
def printmatrix(array,top_column_labels, side_row_labels,integerflag=False):
                (number_of_rows, number_of_columns) = array.shape
                if integerflag:
                        firstcolumnwidth = 13        
                else:
                        firstcolumnwidth =15
                print ("   ", end="")
                print (" "*firstcolumnwidth, end="")
                for colno in range(number_of_columns):
                        if colno >= len(top_column_labels):
                                break
                        print ('%-8s'%makestring(top_column_labels[colno]), end="")
                print ()
                for rowno in range(number_of_rows):
                        if integerflag:
                                print ('%-11s'%side_row_labels[rowno],end="")
                        else:
                                print  ('%-15s'%side_row_labels[rowno],end="")
                        for colno in range(number_of_columns):
                                value = array.item(rowno, colno)
                                #print (value) 
                                if value < 0.01 and value >  -.01:
                                        print ('     -  ', end="")
                                elif integerflag:
                                        print ('%6d  '%int(value), end="")                    
                                else:
                                        print ( '%6.2f  '% value, end = "")
                        print ()
def scoreFV(FV):
                if FV == "past":
                        score = 2
                elif FV == "present":
                        score = 2.2
                elif FV == "1st":
                        score = 4.1
                elif FV == "2nd":
                        score = 4.2
                elif FV == "3rd":
                        score = 4.3
                elif FV == "singular" or FV == "sg":
                        score = 8.1 
                elif FV == "plural" or FV == "pl":
                        score = 8.3
                elif FV == "nom":
                        score = 7.0
                elif FV == "acc":
                        score = 7.1
                elif FV == "gen":
                        score = 7.2
                elif FV == "dat":
                        score = 7.3
                elif FV == "loc":
                        score = 7.4
                elif FV == "inst":
                        score = 7.5
                else:
                        score = 8
                return score
                        
def sortFVs(FVs):         
                return sorted(FVs,key = scoreFV)




class CParadigm:
        def __init__(self):
                self.number_of_rows_in_paradigm = 0
                #self.row_number_to_set_of_FVs =[]
                self.row_number_to_list_of_FVs = []
                self.row_number_to_morph_number =[]
                self.FV_list = []
                self.FVs= {}
                self.FV_to_morph_dict = {} # key is a feature value (string) and value is a dict, which has a morpheme as its key and a value of ?
                self.morph_to_FV_dict = {} # key is a morpheme, value is a dict whose key is a FV and whose value is a count;
                self.morph_to_FV_coordinate = {}
                self.morpheme_list= []    
                self.morpheme_to_index = {}                      # key is morpheme and value is an integer
                self.TPM_length = 0                          # number of entries in TPM (in paradigm)
                self.TPM = np.zeros
                self.B=np.zeros

        def     get_FVs(self):
                        return self.FV_list
        def     get_number_of_FVs(self):
                        return len(self.FV_list)
        def     get_FV(self, index):
                        return self.get_FVs()[index]
        def     get_FV_index(self,fv):
                        return self.FV_list.index(fv)
        def     sortFVs(self):
                        self.FV_list.sort(key = scoreFV)
        def     get_morphemes(self):
                        return  self.morpheme_list 
        def     get_morpheme(self, index):
                        return self.morpheme_list[index]
        def     get_number_of_morphemes(self):
                        return len(self.morpheme_list)
        def     get_length_of_paradigm(self):
                        return len(self.row_number_to_list_of_FVs)
        def     get_stringized_FV(self, index):
                        return "-".join(self.row_number_to_list_of_FVs[index])
        def     get_stringized_FVs(self):
                        output = list()
                        for set_of_FVs in self.row_number_to_list_of_FVs:
                                output.append("-".join(set_of_FVs))                                          
                        return output

        def     makePhi(self):
                        width =  self.get_number_of_morphemes()
                        height = self.get_length_of_paradigm()
                        self.Phi = np.zeros((height,width ))      
                        for row_number in range(height):
                                FVs = self.row_number_to_list_of_FVs[row_number]
                                for FV in FVs:
                                        FVno = self.FV_to_index[FV]
                                        self.Phi[row_number,FVno] = 1
		

        # The paradigm includes a TPM which is an np.array, and B, which is also a np.arry.
        # TPM: number of rows is the size of the paradigm, and the number of columns is the number of morphemes.
        # B:   number of rows is the number of FVs,        and the number of columns is the number of morphemes.
        # Phi is a matrix with sets of FVs (the paradigm positions) as its rows, and morphemes as its columns
        def readparadigm(self,lines):
                self.number_of_rows_in_paradigm = 0	
                for lineno in range(len(lines)):
                   line = lines[lineno]
                   items = line.split()
                   if items[0] == "#":
                      if items[1] == "end":
                        break
                      if items[1] == "pattern":
                         pattern_label = items[2]
                      else:
                         morphemes = items[1:]
                         for morphno in  range(len(morphemes)):
                            thismorph = morphemes[morphno] 
                            self.morpheme_list.append(thismorph)
                            self.morpheme_to_index[thismorph] = morphno
                   else:                                                # read the entries, one row per position in paradigm
                       self.number_of_rows_in_paradigm += 1
                       morpheme = items.pop(-1)
                       morpheme_index=self.morpheme_to_index[morpheme]
                       FVs = sorted(items, key = scoreFV)                 #the FVs are now sorted inside each row
                       self.row_number_to_list_of_FVs.append(FVs)
                       self.row_number_to_morph_number.append(morpheme_index)
                       #feature_set = set(items)
                       #feature_set_tuple=tuple(set(items))  
                       #self.row_number_to_set_of_FVs.append(feature_set)     # this is no longer used. 
                       #self.FV_tuple_to_morpheme[feature_set_tuple] = morpheme  # this is ugly and should be done better
                       for thisfv in FVs:
                          if thisfv not in self.FVs:
                                self.FVs[thisfv] = 1    
                                self.FV_list.append(thisfv)
                        
                self.sortFVs()
                         
                
                
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

               # -------------------  compute Phi   ----------------------------------
                self.Phi = np.zeros((self.get_length_of_paradigm(), self.get_number_of_FVs()))
                print ("Phi Matrix ")
                for rowno in range(self.get_length_of_paradigm()):
                        FVs = self.row_number_to_list_of_FVs[rowno]
                        for fv in FVs:
                                print ("236 ", fv)
                                FV_index = self.get_FV_index(fv)
                                self.Phi[rowno, FV_index] = 1
                
                
                printmatrix(self.Phi,self.get_FVs(), self.get_stringized_FVs())
 
               # -------------------  compute Phi times B ----------------------------------
                #Phi_times_B = =np.matmul(thisparadigm1., this.B)


        def printparadigm(self):
                number_of_rows    =  self.get_length_of_paradigm()
                number_of_columns = self.get_number_of_morphemes()
                print ("\nThis TPM matrix  ")
                printmatrix(self.TPM,self.morpheme_list, self.get_stringized_FVs(),True) 
               


                print ("\n\nList of feature value labels and paradigm space dict:\n")
                rowno =0

                string1 ="{:<10} {:20} {:<20}" 
                string2 ="  {:<10} {:20} {:<20}" 
                print (string1.format('row number', 'feature values', 'morpheme number'))
                for row_number in range(number_of_rows):
                        print (string2.format(rowno, self.get_stringized_FV(row_number), self.row_number_to_morph_number[row_number] ))
                        rowno += 1
                 
                print ("\n\nB matrix:")
                printmatrix(self.B, self.get_morphemes(),self.get_FVs() )

                


                Y,s,Vh = np.linalg.svd(self.TPM)

                pi = np.linalg.pinv(self.TPM)
                print ("\npseudoinverse of TPM" )
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
thisparadigm1.readparadigm(lines)
thisparadigm1.printparadigm()

 

thisparadigm1.TPM = np.zeros((thisparadigm1.get_length_of_paradigm(), thisparadigm1.get_number_of_morphemes()))
 



 
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
