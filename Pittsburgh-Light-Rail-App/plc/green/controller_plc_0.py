def run(input):
	if input['block'][18] == True or input['block'][19] == True or input['block'][20] == True or input['block'][21] == True:
	    input['crossing'][19] = True
	else:
	    input['crossing'][19] = False
	
	occupied = False
	for blk in range(13, 30):
	    if input['block'][blk] == True:
	        occupied == True 
	
	if (input['block'][150] == True or input['block'][149] == True) and not occupied:
	    input['switch'][29] = False
	    input['switch'][12] = True
	
	if (input['block'][1] == True  or input['block'][2] == True) and not occupied:
	    input['switch'][29] = True
	    input['switch'][12] = False