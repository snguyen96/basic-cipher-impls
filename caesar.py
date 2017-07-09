message = input('Enter your message: ')
# shift = input('shift: ')

arr1 =     ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
encoding = ['x','y','z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w']

message = list(message)

for i in range(len(message)):
    for j in range(26):
        if message[i] == arr1[j]:
            message[i] = message[i].replace(message[i], encoding[j])
            break

message = ''.join(message)

print(message)
