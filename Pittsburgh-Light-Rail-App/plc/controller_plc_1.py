def run(input):
	if input['block']['18'] == True or input['block']['19'] == True or input['block']['20'] == True:
	    print( input['crossing']['19'] )
	    input['crossing']['19'] = True
	    print( input['crossing']['19'] )
	else:
	    print("false")
	    input['crossing']['19'] = False