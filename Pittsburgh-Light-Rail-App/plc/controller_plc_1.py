def run(input):
	if input['block']['18'] == True or input['block']['19'] == True or input['block']['20'] == True:
	    input['crossing']['19'] = True
	else:
	    input['crossing']['19'] = False