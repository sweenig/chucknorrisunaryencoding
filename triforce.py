n = int(input())
answer = ""
for i in range(1,n+1): answer += " " * (n+n-i) + "*" * (i+i-1) + "\n"
for i in range(1,n+1): answer += " " * (n-i) + "*" * (i+i-1) + " " * (n-i+n-i+1) + "*" * (i+i-1) + "\n"
print("." + answer[1:-1])
