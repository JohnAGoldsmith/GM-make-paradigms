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
import sys
import json

np.set_printoptions(suppress=True)
np.set_printoptions(precision=2)

def dump_array_as_list(lang, label, a):
    array_as_list = a.tolist()
    f = open('array'+lang+'.'+label+'.json', 'w')
    json.dump(array_as_list, f)
    f.close()



def makestring(arg):
    if type(arg) is list:
        return "-".join(arg)
    else:
        return  arg 

   # When PrintMax flag is set to True, then an asterisk is printed next to the largest value in each row, in certain matrices.
def printmatrix(array,top_column_labels, side_row_labels,integerflag=False,PrintMax = False,outfilename=""):
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

                        if PrintMax == True:
                                max = -1000.0
                                maxcols = []
                                for colno in range(number_of_columns):
                                        value = array.item(rowno, colno)
                                        if value > max:
                                                max = value

                        for colno in range(number_of_columns):
                                value = array.item(rowno, colno)
                                if value < 0.01 and value >  -.01:
                                        print ('     -  ', end="")
                                elif integerflag:
                                        print ('%6d  '%int(value), end="")                    
                                else:
                                        if PrintMax == True and value >= max:
                                                print ( '%5.2f*  '% value, end = "")
                                        else:
                                                print ( '%6.2f  '% value, end = "")
                        print ("")

def openlatexfile(outfilename):

                start1      = """\\documentclass{article}\n"""
                start2      = """\\usepackage{booktabs}\n"""
                start3      = """\\usepackage[margin=1in]{geometry}\n"""
                start4      = """\\begin{document}\n"""
                outfile = open (outfilename, "w")
                outfile.write (  start1 + start2 + start3 + start4 )
                return outfile

def closelatexfile(outfile):
                skiplines   = "\n \\vspace{0.2in}\n\n"
                footer3     = "\\end{document}\n\n\n"
                outfile.write(skiplines)  
                outfile.write( footer3)
                outfile.close()
                outfile.close()
 
def printmatrixtolatex(outfile, header, array, filename,top_column_labels, side_row_labels,integerflag=False,PrintMax = False):

                (number_of_rows, number_of_columns) = array.shape
                
                tablestart  = "\\begin{tabular}" + "{" + 'l' * (number_of_columns+2) + "}" 
                tableend    = "\\end{tabular}\n" 
 
                outfile.write (  header + "\n\n\\nopagebreak\n")
                outfile.write  ( tablestart + "\\toprule\n")

 

                if integerflag:
                        firstcolumnwidth = 13        
                else:
                        firstcolumnwidth =15
                outfile.write (  "   " )
                outfile.write (  " "*firstcolumnwidth )
                for colno in range(number_of_columns):
                        if colno >= len(top_column_labels):
                                outfile.write("END")
                                break
                        outfile.write(  '&%-8s'%makestring(top_column_labels[colno]))
                outfile.write ( "\\\\ \n"  )
                for rowno in range(number_of_rows):
                        if integerflag:
                                outfile.write (  '%-11s'%side_row_labels[rowno] )
                        else:
                                outfile.write  (  '%-15s'%side_row_labels[rowno] )

                        if PrintMax == True:
                                max = -1000.0
                                maxcols = []
                                for colno in range(number_of_columns):
                                        value = array.item(rowno, colno)
                                        if value > max:
                                                max = value

                        for colno in range(number_of_columns):
                                value = array.item(rowno, colno)
                                if value < 0.01 and value >  -.01:
                                        outfile.write ( '&    -   ' )
                                elif integerflag:
                                        outfile.write (  '&  %4d  '%int(value) )                    
                                else:
                                        if PrintMax == True and value >= max:
                                                outfile.write (    '& %4.2f*  '% value )
                                        else:
                                                outfile.write (  '& %5.2f  '% value )
                        outfile.write ("\\\\ \n")
                outfile.write( tableend) 
                outfile.write( "\\vspace{.2in}") 
 


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
                self.morpheme_to_index = dict()                      # key is morpheme and value is an integer
                self.TPM_length = 0                          # number of entries in TPM (in paradigm)
                self.TPM = np.zeros
                self.B=np.zeros
                self.Phi = np.zeros
                self.Phi_times_B = np.zeros
                self.Competition_Winner = list()        # A list, one per row of the paradigm; its value is the number of the morpheme which is calculated as maximum of Phi_time_B, the competition array.
                self.pattern_label = "No label assigned."
                self.language = "No language specified."


        def     get_TPM(self):
                        return self.TPM
        def     get_Phi(self):
                        return self.Phi
        def     get_morphemes(self):
                        return self.morpheme_list
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
        def readparadigm(self,data):
                self.number_of_rows_in_paradigm = 0
                morphemes = ()	
                for lineno in range(len(data)):
                   line = data[lineno]
                   items = line.split()
                   if items[0] == "#":
                      if items[1] == "end":
                        break
                      elif items[1] == "pattern":
                         self.pattern_label = items[2]
                      elif items[1] == "language":
                        self.language = items[2]
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
                for rowno in range(self.get_length_of_paradigm()):
                        FVs = self.row_number_to_list_of_FVs[rowno]
                        for fv in FVs:
                                FV_index = self.get_FV_index(fv)
                                self.Phi[rowno, FV_index] = 1
 
               # -------------------  compute Phi times B ----------------------------------
                self.Phi_times_B =np.matmul(self.Phi, self.B)
                self.Competition_Winner = list()
                for row_number in  range(self.get_length_of_paradigm()):
                        max = -1000
                        maxcolumn = -1
                        for column_number in range(self.get_number_of_morphemes()):
                                if self.Phi_times_B[row_number,column_number] > max:
                                        max = self.Phi_times_B[row_number,column_number]
                                        maxcolumn = column_number
                        TieCount = 0             
                        for column_number in range(self.get_number_of_morphemes()):
                                if self.Phi_times_B[row_number,column_number] >= max:
                                        TieCount += 1                       
                        if TieCount > 1:
                                Problem_Tie_Flag = True
                        self.Competition_Winner.append(maxcolumn)
                        
                

      
        def printparadigm(self,outfilename ):

                outfile = openlatexfile (outfilename)

                number_of_rows    =  self.get_length_of_paradigm()
                number_of_columns = self.get_number_of_morphemes()
                
                pattern1 = "Language: {:<15}\n"
                pattern2 = "\\vspace{.1in}"
                pattern3 = "Pattern:  {:<15}"
                print (pattern1.format(self.language  ), file = outfile  )
                print (pattern2,file=outfile)
                print (pattern3.format( self.pattern_label), file = outfile  )
                print (pattern2,file=outfile)
                header = "\n This TPM matrix  "
                print (header)
                printmatrix(self.TPM,self.morpheme_list, self.get_stringized_FVs(),True) 
                printmatrixtolatex(outfile, header, self.TPM, outfilename, self.morpheme_list, self.get_stringized_FVs(),True) 
                print ("\n\nRank of TPM: ", np.linalg.matrix_rank(self.TPM))

                header = "\n\nB matrix:"
                print (header)
                printmatrix(self.B, self.get_morphemes(),self.get_FVs() )
                printmatrixtolatex(outfile, header, self.B, outfilename, self.get_morphemes(),self.get_FVs() )



                # --         PHI                -- #
                header = "\n\nPhi Matrix "
                print (header)
                printmatrix(self.Phi,self.get_FVs(), self.get_stringized_FVs(),True)
                printmatrixtolatex(outfile,  header,self.Phi,outfilename, self.get_FVs(),  self.get_stringized_FVs(),True)
                # --         Summary                -- #
                header = "\n\nList of feature value labels and paradigm space dict:\n"
                print (header)
                rowno =0
                string1 ="{:<10} {:20} {:<20} {:<20}" 
                string2 ="  {:<10} {:20} {:<20} {:<20}" 
                print (string1.format('row number', 'feature values', 'morpheme number', 'morpheme'))
                for row_number in range(number_of_rows):
                        morpheme_number =  self.row_number_to_morph_number[row_number]
                        morpheme = self.morpheme_list[morpheme_number]
                        print (string2.format(rowno, self.get_stringized_FV(row_number),morpheme_number, morpheme))
                        rowno += 1
                 

                # --         PHI times B                -- #
                header ="\n\nPhi times B: Competition matrix "
                print (header)
                printmatrix(self.Phi_times_B,self.get_morphemes(),self.get_stringized_FVs(),PrintMax = True)
                printmatrixtolatex(outfile, header, self.Phi_times_B, outfilename, self.get_morphemes(),self.get_stringized_FVs(),PrintMax = True)
                
                
                
                
                string3 ="{:<3}  {:<10} {:7}" 
                string3a ="{:<3} & {:<10} &      {:7}" 
                print ("\n\nComparing truth to prediction\n")
                print ("\n\nComparing truth to prediction\n",file = outfile)
                print ("\n\n\\begin{tabular}{llll}\n",file = outfile)
                for row_number in  range(self.get_length_of_paradigm()):
                        if  self.morpheme_list[self.row_number_to_morph_number[row_number]] == self.morpheme_list[self.Competition_Winner[row_number]]:
                                ErrorFlag = False
                        else:
                                ErrorFlag = True       
                                                             
                        print (string3.format(row_number,  self.morpheme_list[self.row_number_to_morph_number[row_number]],  self.morpheme_list[self.Competition_Winner[row_number]]), end = "")
                        print (string3a.format(row_number, self.morpheme_list[self.row_number_to_morph_number[row_number]],  self.morpheme_list[self.Competition_Winner[row_number]]), file = outfile, end = "" )
                        if ErrorFlag == True:
                                print ("  error! ")
                                print ("  {\\em error!} \\\\ ",file = outfile )
                        else: 
                                print ()      
                                print ("\\\\", file=outfile)
                        
                print ("\\end{tabular} \n\n", file = outfile)
                outfile.write( "\\vspace{.2in}") 

        


                # --         Pseudo inverse                -- #
                Y,s,Vh = np.linalg.svd(self.TPM)

                pi = np.linalg.pinv(self.TPM)
                header = "\n\npseudoinverse of TPM" 
                print (header)
                printmatrix(pi, self.get_stringized_FVs(),self.morpheme_list)

                pi_times_matrix = np.matmul(pi,self.TPM)
                #(number_of_rows, number_of_columns) = pi_times_matrix.shape
                
                header = "\n\nPseudoinverse times matrix"
                print (header)
               
                printmatrix(pi_times_matrix,self.morpheme_list, self.morpheme_list,integerflag= False,PrintMax=False,)
                printmatrixtolatex(outfile,  header,pi_times_matrix,outfilename, self.morpheme_list,  self.morpheme_list,integerflag= False,PrintMax=False)
                
                                    
                        
                
                closelatexfile(outfile)
def main(argv):

        if len(sys.argv) > 1:
            lang = '.'+sys.argv[1]
        else:
            lang = ''


        print ("\n"*50)
       

        with open("config.txt"+lang) as config_file:
                lines = config_file.read().splitlines()
        number_of_cycles = len(lines)/ 2

        cycleno = 1
        while (len(lines)):
                filename=lines.pop(0)
                outfilename = lines.pop(0)
           
                print ("\n\n\n --------- Part", cycleno, "---------------")
                print (filename, " " ,outfilename)
                thisparadigm1=CParadigm()
                with open(filename) as f:
                   data = f.readlines()
                thisparadigm1.readparadigm(data)
                thisparadigm1.printparadigm(outfilename )
                cycleno += 1
              
        #Save data in json files.
        tpm = thisparadigm1.get_TPM()
        dump_array_as_list(lang, 'TPM', tpm)
        phi = thisparadigm1.get_Phi()
        dump_array_as_list(lang, 'Phi', phi)
        ml = thisparadigm1.get_morphemes()
        f = open('morphemelist'+lang+'.json', 'w')
        json.dump(ml, f)
        f.close()
        fvs = thisparadigm1.get_FVs()
        f = open('FVlist'+lang+'.json', 'w')
        json.dump(fvs, f)
        f.close()
        
         

 



if __name__=="__main__":
        main(sys.argv)

