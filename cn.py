def cnencode(message):
  binary = ''.join([bin(ord(i))[2:].zfill(7) for i in message]) #get the binary values of the ascii values and strip off the leading "0b" and join them into a single string
  answer = "" #start with an empty answer
  i=0 #begin by looking at the first character
  while i < len(binary): #loop through all binary digits
    answer += "0" #figure out whether to output 1 ("0 ") or 0 ("00 "), either way, gotta add a 0
    if not binary[i]=="1": answer += "0" #if this character is not a 1, make the digit id a 0 by adding a second 0 to the digit id
    answer += " 0" #output a 0 indicating a quantity of at least one for the current digit, then figure out how many of the previous digit to signify (digit quantity)
    for j in range(i+1,len(binary)): #loop through the remaining digits starting with the one after the current one (i)
      if binary[j] == binary[i]: #if the currently inspected digit (j) is the same as the original digit (i)
        answer += "0" #add a 0 to increase the quantity
        i += 1 #move forward
      else: break #if the current character isn't the same as the previous, break out of this loop
    answer += " " #put a space to separate the previous digit's quantity from the next digit's id
    i += 1 #move on to the next digit
  return answer[:len(answer)-1]

def cndecode(message):
  try: int(message.replace(" ",""))
  except ValueError: return("INVALID")
  else:
    encrypt = iter(message.split(" "))
    decrypted = ""
    output = ""
    for x in encrypt:
      try: a, b = x, next(encrypt)
      except: break
      if len(a)>2: break
      decrypted += "".join(str(len(a)%2)*len(b))
    while len(decrypted) > 0 and output != "INVALID":
      currword = decrypted[:7]
      output += chr(int(currword.zfill(8),2))
      decrypted = decrypted[7:]
    if output != "INVALID" and cnencode(output) != message: return "INVALID"
    else: return output
