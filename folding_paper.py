import sys

def opposite_side(side:str)->str:
    opposites = {}
    for i,s in enumerate(list(paper.keys())):
        side_index = list(paper.keys()).index(side)
        oppo_index = (side_index + 2) % len(list(paper.keys()))
        oppo = list(paper.keys())[oppo_index]
        opposites[s] = oppo
    return opposites[side]

def make_fold(side:str, page:dict)->dict:
    for s in [x for x in page.keys() if x not in [side,opposite_side(side)]]: page[s] *= 2 # for adjacent sides, double the layer count
    page[opposite_side(side)] += page[side] # for the opposite side, add it's current layers to the folded side's layers
    page[side] = 1 # the side that is being folded will always end up with only 1 layer
    return page

# process input
instructions = input()
print(f"Folding instructions: {instructions}",file=sys.stderr)

paper = {"R":1,"U":1,"L":1,"D":1}
for fold in instructions: paper = make_fold(fold, paper)

view_from = input()
print(f"View from: {view_from}",file=sys.stderr)
print(paper[view_from])