import os 

class WaysideIO:
    def __init__(self):

        self.logicTable = {}
        self.blockStates = []

        pass

    def configurePorts(self, file):
        
        ## Loop through each instruction
        for line in file:
            if line[:2] == 'if':
                print("if")
    
        pass


if __name__ == '__main__':
    w = WaysideIO()
    
    