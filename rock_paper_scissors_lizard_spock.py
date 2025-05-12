import sys

def who_wins_between(player1:tuple, player2:tuple)->tuple:
    rules = { # shows which signs (keys) beat which other signs (values)
        'R': ['C', 'L'],
        'P': ['R', 'S'],
        'C': ['P', 'L'],
        'L': ['P', 'S'],
        'S': ['R', 'C']
    }
    if player1[1] == player2[1]: return (player1,player2) if player1[0] < player2[0] else (player2,player1) # if it's a tie, the player with the lower number wins
    elif player2[1] in rules[player1[1]]: return (player1,player2) # if player2's sign is beaten by player1's sign
    else: return (player2,player1) # not a tie and player1 didn't win: player2 wins

def tournament(players:list)->tuple:
    round_results = {i[0]:[] for i in players} # blank dictionary to contain each player's history
    while len(players) > 1: # play until there's one player left
        next_round_players = [] # winners from this round
        for i in range(0,len(players),2): # two players at a time
            winner,loser = who_wins_between(players[i],players[i+1]) # have them compete
            round_results[winner[0]].append(loser[0]) # put the loser in the winner's history
            next_round_players.append(winner) # move the winner to the next round
        players = next_round_players # move to the next round
    return (players[0][0],round_results) # return the player's number with all player's history

# process input
n = int(input())
players = [(int(num),char) for num, char in (input().split() for _ in range(n))]
print(players,file=sys.stderr)

winner,history = tournament(players)
print(f"{winner}\n{' '.join(map(str,history[winner]))}")