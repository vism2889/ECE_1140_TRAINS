def run(input):
	if input['block']['18'] == True or input['block']['19'] == True or input['block']['20'] == True:
	    input['crossing']['19'] = True
	else:
	    input['crossing']['19'] = False
	
	if input['block']['149'] == True and input['block']['2'] == False:
	    print('If statement 1')
	    input['switch']['29'] = True
	    input['switch']['12'] = True
	
	if input['block']['2'] == True and input['block']['149'] == False:
	    print('If statement 2')
	    input['switch']['29'] = False
	    input['switch']['12'] = False