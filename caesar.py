message = input("Enter your message: ")
direction = input("direction ('l' or 'r'): ")
shift = int(input("shift (integer): "))

if direction == 'r':
    shift *= -1
elif direction == 'l':
    pass
else:
    print("error - enter 'l' or 'r' for 'left/right'")
    
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
encoding = []

for i in range(shift, len(alphabet)):
    encoding.append(alphabet[i])

for j in range(shift):
    encoding.append(alphabet[j])
    
message = message.lower()
message = list(message)

for i in range(len(message)):
    for j in range(26):
        if message[i] == alphabet[j]:
            message[i] = message[i].replace(message[i], encoding[j])
            break

message = ''.join(message)

print(message)
