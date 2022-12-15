def run(input):
	
	occupied = False
	for blk in range(77, 86):
	    if input['block'][blk] == True:
	        occupied = False
	        break
	
	if not occupied and (input['block'][75] == True or input['block'][74] == True):
	    input['switch'][76] = True
	    input['switch'][85] = True
	
	elif not occupied and (input['block'][99] == True or input['block'][100] == True):
	    input['switch'][76] = False
	    input['switch'][85] = False