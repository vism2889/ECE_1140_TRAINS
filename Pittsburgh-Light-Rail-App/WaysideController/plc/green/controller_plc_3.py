def run(input):
	for blk in range(77, 86):
	    if input['block'][blk] == True: 
	        return 
	
	if input['block'][75] == True and input['block'][100] == False:
	    input['switch'][76] = False
	    input['switch'][85] = False
	    
	elif input['block'][99] == True and input['block'][75] == False:
	    input['switch'][76] = True
	    input['switch'][85] = True