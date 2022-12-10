
# Builds a list of blocks for the green line in
# the correct order to leave the yard, 
# make one full loop around the track, 
# and return to the yard.
sec1 = [i for i in range(63, 101)]
sec2 = [i for i in range(85, 76, -1)]
sec3 = [i for i in range(101, 151)]
sec4 = [i for i in range(29, 0, -1)]
sec5 = [i for i in range(13, 58)]

sections = sec1 + sec2 + sec3 + sec4 + sec5

print(sections)