import sys

def battle(war=False):
    global ispat, rounds
    # Transfer all cards from battle piles to the winner's deck
    def transfer_cards(winner):
        winner.extend(p1_b)
        winner.extend(p2_b)
        p1_b.clear()
        p2_b.clear()
    # Handle the war scenario by adding three cards to the battle pile
    def handle_war(player, battle_pile):
        if len(player) >= 4:
            battle_pile.extend([player.pop(0) for _ in range(3)])
        else:
            global ispat
            ispat = True
            transfer_cards(p2 if player is p1 else p1)
    # Players draw cards
    p1_b.append(p1.pop(0))
    p2_b.append(p2.pop(0))
    # Compare cards
    p1_card = order.index(p1_b[-1][:-1])
    p2_card = order.index(p2_b[-1][:-1])
    if p1_card > p2_card: transfer_cards(p1)
    elif p1_card < p2_card: transfer_cards(p2)
    else:
        print(f"WAR! ({p1_b[-1]} == {p2_b[-1]})", file=sys.stderr)
        handle_war(p1, p1_b)
        handle_war(p2, p2_b)
        if len(p1) > 0 and len(p2) > 0: battle(True)
        elif len(p1) == 0: transfer_cards(p2)
        elif len(p2) == 0: transfer_cards(p1)
    if not war: rounds += 1

# setup constants
order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

# process input
p1,p2=[],[]
for p in [p1,p2]:
    for i in range(int(input())): p.append(input())
    print(f"Player 1 starting deck: {p}", file=sys.stderr)

# setup variables
rounds = 0
ispat = False

#start battle
p1_b,p2_b = [],[]
while len(p1)>0 and len(p2)>0: battle()
if ispat: 
    print("PAT")
    print("rounds: {rounds}",file=sys.stderr)
else: print(f"1 {rounds}" if len(p1)>0 else f"2 {rounds}")
