import sys

def alien_encode(msg):
    a = ""
    end = True # start by putting the chunks on the right (first chunk included)
    j=1
    while msg:
        a = a + msg[:j] if end else msg[:j] + a # put this chunk at the beginning or end depending on left or right side
        msg = msg[j:] # remove the chunk from the msg
        j += 1 # increase the chunk size
        end = not end # switch to the other side
    return a

def alien_decode(msg):
    debug = False
    if debug: print(f"Decoding \"{msg}\"",file=sys.stderr)
    if len(msg) == 1: return msg # recursion exit
    chunks = []
    i = 1
    decode_this = msg
    while decode_this: # break the msg into chunks and count them
        chunks.append(decode_this[:i])
        decode_this = decode_this[i:]
        i += 1
    tail       = len(chunks[-1]) # how full is the last chunk?
    chunks     = len(chunks)     # how many chunks overall
    chunk_side = chunks % 2 == 0 # true if the first chunk is on the left
    if debug: print(f"Determined that there are {chunks} chunks with the final chunk being {tail} characters long on the {'left' if chunk_side else 'right'}.",file=sys.stderr)
    if tail != chunks: # the last chunk is partially filled
        if chunk_side: return alien_decode(msg[tail:]) + msg[:tail] # remove the tail and decode the rest (put the tail at the end)
        else: return alien_decode(msg[:-1*tail]) + msg[-1*tail:] # remove the tail and decode the rest (put the tail at the end)
    else: # all chunks are filled
        if chunk_side: return alien_decode(msg[chunks:]) + msg[:chunks] # decode starting with the chunk on the left
        else: return alien_decode(msg[:-1*chunks]) + msg[-1*chunks:] # decode starting with the chunk on the right

# process input
n, message = int(input()), input()
print(f"Message needs to be {'encoded' if n < 0 else 'decoded'}: {message}",file=sys.stderr)

if n < 0: # negative so encode
    for i in range(abs(n)): message = alien_encode(message) # encode n times
else: # positive to decode
    for i in range(n): message = alien_decode(message) # decode n times
print(message)

