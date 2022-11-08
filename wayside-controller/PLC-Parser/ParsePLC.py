import os 
import re

class PLCParser():
    def __init__(self):
        self.IO_KEYWORDS = ["block_", "crossing_"]
        self.parsed_instructions = []
        pass

    def parseFile(self, file):  
        ## Parse each instruction in a file
        for instr in file:
            
            instruction = {}
            
            ## Split the instruction based on ':='
            tokens = re.split(r':=|if|else', instr)

            if len(tokens) == 3 or len(tokens) == 4:
                
                ## Get the output variable
                output_var = tokens[0]
                
                if '#' not in output_var:
                    continue
                else:
                    instruction['output'] = output_var.strip("#")
                                
                ## Get conditional assignment value
                if tokens[1].lower() != 'true' or tokens[1].lower() != 'false':
                    continue
                else:
                    conditional_val = True if tokens[1].strip(' ').lower() == 'true' else False
                    instruction['value'] = conditional_val

                ## Get conditional expression
                conditional_expr = tokens[2]
                

                ## Default value (if present)
                if len(tokens) == 4:
                    default_val = True if tokens[3].strip(' ').lower() == 'true' else False
                    instruction['default'] = default_val

                self.parsed_instructions.append(instruction)
            
                
                
                

            
            




if __name__ == '__main__':
    
    parser = PLCParser()
    path = os.getcwd() + "\\tests\\testplc.plc"
    file = open(path, 'r')

    parser.parseFile(file)

    file.close()