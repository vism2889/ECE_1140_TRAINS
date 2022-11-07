import os 

class WaysideIO:
    def __init__(self):

        self.logicTable = {}
        self.blockStates = []

        pass



    def configurePorts(self, file):
        
        ## Loop through each instruction
        for line in file:
            ## Split the line at ','
            instr = line.split(',')
            
            if len(instr) <= 3:
                continue
            
            ## Go through each element of the instruction
            #   (i.e. [AND, 1, 2, 50]) AND ports 1 and 2 and
            #   set that output to block 50 
            op = instr[0]
            output = instr[-1]
            inputs = []
            for el in instr[1:len(instr)-1]:
                inputs 



        pass