def run(input):
	if input['block'][45] == True or input['block'][46] == True or input['block'][47] == True or input['block'][48] == True or input['block'][49] == True:
	    input['crossing'][47] = True
	else: 
	    input['crossing'][47] = False
	
	input['switch'][27] = True
	input['switch'][32] = True
	input['switch'][38] = True
	input['switch'][43] = True