import sys

def tumble(count, raster):
    height,width = len(raster),len(raster[0])
    for i in range(count): 
        for j in range(height): raster[j] = ''.join(sorted(raster[j])) # move everything to the left
        for row in raster: print(row,file=sys.stderr)
        new_raster = [] # to hold the newly rotated raster
        for k in range(width-1,-1,-1): # start at the last column in the current raster
            word = ""
            for m in range(height): word += raster[m][k] # construct the contents of the first row of the new raster
            new_raster.append(word) # populate the first column in the new raster
        raster = new_raster
        height = len(raster) # calculate new height after rotation
        width = len(raster[0]) # calculate new width after rotation
    return raster

# process input
width, height = [int(i) for i in input().split()]
count = int(input())
raster = []
for i in range(height): raster.append(input())
for row in raster: print(row,file=sys.stderr)

# process output
for row in tumble(count,raster): print(row)