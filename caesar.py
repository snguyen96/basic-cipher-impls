message = input('Enter your message: ')
direction = input('direction: ')
shift = int(input('shift: '))

if direction == 'r':
    shift *= -1
elif direction == 'l':
    pass
else:
    print("error - enter 'l' or 'r' for 'left/right'")
    
arr1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
encoding = []

for i in range(shift, len(arr1)):
    encoding.append(arr1[i])

for j in range(shift):
    encoding.append(arr1[j])
    
message = message.lower()
message = list(message)

for i in range(len(message)):
    for j in range(26):
        if message[i] == arr1[j]:
            message[i] = message[i].replace(message[i], encoding[j])
            break

message = ''.join(message)

print(message)
