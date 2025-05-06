import sys

def plan_cable(houses):
    total_horizontal_distance = max(h[0] for h in houses) - min(h[0] for h in houses) # Calculate the total horizontal distance
    y_coords = sorted([h[1] for h in houses]) # Get all y coordinates and sort them
    # Find the median y coordinate
    n = len(houses)
    if n % 2 == 0: optimum_y = y_coords[n//2 - 1] # If even number of houses, take the lower median
    else: optimum_y = y_coords[n//2] # If odd number of houses, take the middle value
    total_distance = total_horizontal_distance + sum(abs(h[1] - optimum_y) for h in houses) # Calculate total cable length
    return(total_distance, optimum_y)

# process input
n = int(input())
houses = [[int(j) for j in input().split()] for _ in range(n)]
print("\n".join([f"{h[0]},{h[1]}" for h in houses]), file=sys.stderr)

plan = plan_cable(houses)
print(f"{plan[0]} feet of cable should be placed at y={plan[1]}", file=sys.stderr)
print(plan[0])