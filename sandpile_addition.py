import sys, os

debug = False
if not debug: sys.stderr = open(os.devnull, "w")
def printmatrix(list, name="", stream=sys.stderr):
    if name: print(f"{name}:", file=sys.stderr)
    for row in list: print(''.join(map(str, row)), file=stream)
    print("", file=sys.stderr)

def combine_piles(pile1, pile2):
    def cleanpile(dirtypile):
        for i in range(len(dirtypile)):
            for j in range(len(dirtypile[i])):
                if dirtypile[i][j] >= 4:
                    dirtypile[i][j] -= 4
                    if i-1 >= 0: dirtypile[i-1][j] +=1
                    if i+1 < n: dirtypile[i+1][j] +=1
                    if j-1 >= 0: dirtypile[i][j-1] +=1
                    if j+1 < n: dirtypile[i][j+1] +=1
        printmatrix(dirtypile,"dirtypile")
        return dirtypile
    n = len(pile1)
    pile3 = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n): #generate flat sum
        for j in range(n):
            pile3[i][j] = int(pile1[i][j]) + int(pile2[i][j])
    printmatrix(pile3,"pile3")
    while any(any(x >= 4 for x in row) for row in pile3):pile3 = cleanpile(pile3)
    return pile3

# gather inputs
n = int(input())
pile1 = [list(input()) for _ in range(n)]
pile2 = [list(input()) for _ in range(n)]
printmatrix(pile1,"pile1")
printmatrix(pile2,"pile2")

pile3 = combine_piles(pile1, pile2)
printmatrix(pile3,"pile3",stream=sys.stdout)
