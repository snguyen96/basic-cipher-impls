from socket import *
import sys

host_name = sys.argv[-2]
port_number = int(sys.argv[-1])


# special tokens
def is_special(l):  # special tokens

    if l == '<' or l == '>' or l == '(' or l == ')' or l == '[' or l == ']' or l == '\\' or l == '.' or l == ',' or l == ';' or l == ':' or l == '@' or l == '"':
        return True
    else:
        return False


# parse element
def parse_element(e):  # parse element

    if e[0].isalpha() and e.__len__() > 1:
        return True
    else:
        print('501 Syntax error in parameters or arguments')
        return False


# parse domain
def parse_domain(d):  # parse domain

    x = d.split('.')

    if '.' + '.' in d:
        print('501 Syntax error in parameters or arguments')
        return False

    for letter in d:
        if letter.isalnum() or letter == '.':
            continue
        else:
            print('501 Syntax error in parameters or arguments')
            return False

    for i in x:
        if not parse_element(i):
            return False


# parse local part
def parse_local_part(lp):  # parse local part

    for letter in lp:
        if letter == ' ' or letter == '\t' or is_special(letter):
            print('501 Syntax error in parameters or arguments')
            return False
        else:
            continue

    return True


# parse the email address
def parse_address(address):

    if address[0] == ' ' or address[0] == '@':
        print('501 Syntax error in parameters or arguments')
        return False
    elif '@' in address:
        pass
    else:
        print('501 Syntax error in parameters or arguments')
        return False

    lpd = address.split('@')

    if lpd.__len__() > 2:
        print('501 Syntax error in parameters or arguments')
        return False

    a = lpd[0]
    b = lpd[1]

    if ' ' in address:
        print('501 Syntax error in parameters or arguments')
        return False

    if not parse_local_part(a):
        return False
    if parse_domain(b) == False:
        return False
    else:
        return True

# loop allows re-entry of message
while True:
    # initialize an array for the email message
    message_text = []

    # store sender address and append to message
    from_prompt = raw_input('From: ')
    message_text.append('From: <' + from_prompt + '>\n')
    if not parse_address(from_prompt):
        print('Try again: invalid email address')
        continue

    # store recipient address and append to message
    to_prompt = raw_input('To: ')
    # store multiple recipients
    if ', ' in to_prompt:
        multiple_recipients = True
        recipient_array = to_prompt.split(', ')
        for r in range(0, len(recipient_array)):
            if not parse_address(recipient_array[r]):
                print('Try again: invalid email address')
                continue
            message_text.append('To: <' + recipient_array[r] + '>\n')
    elif ',' in to_prompt:
        multiple_recipients = True
        recipient_array = to_prompt.split(',')
        for r in range(0, len(recipient_array)):
            if not parse_address(recipient_array[r]):
                print('Try again: invalid email address')
                continue
            message_text.append('To: <' + recipient_array[r] + '>\n')
    else:
        multiple_recipients = False
        message_text.append('To: <' + to_prompt + '>\n')
        if not parse_address(to_prompt):
            print('Try again: invalid email address')
            continue
    # store subject and append to message
    subject_prompt = raw_input('Subject: ')
    message_text.append('Subject: ' + subject_prompt + '\n')
    message_text.append('\n')

    print'Message:',
    # store actual message line by line with loop
    while True:
        message_prompt = raw_input()
        message_text.append(message_prompt)
        if message_prompt == '.':
            break
        message_text.append(' ' + '\n')
    break

# loop is used to end connection when there is an error
while True:
    # create socket and connect to a host server
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host_name, port_number))
    # start handshake and sending commands, checking for correct responses
    response = client_socket.recv(1024).decode()
    if '220' in response:
        client_socket.send(('HELO ' + gethostname()).encode())
    else:
        client_socket.close()
        print 'ERROR - invalid response code'
        break
    response = client_socket.recv(1024).decode()
    if '250' in response:
        client_socket.send(('MAIL FROM: <' + from_prompt + '>').encode())
        if multiple_recipients:
            for r in range(0, len(recipient_array)):
                client_socket.send(('RCPT TO: <' + recipient_array[r] + '>').encode())
                if '250' in client_socket.recv(1024).decode():
                    continue
                else:
                    break
        else:
            if '250' in client_socket.recv(1024).decode():
                client_socket.send(('RCPT TO: <' + to_prompt + '>').encode())
            else:
                client_socket.close()
                print 'ERROR - invalid response code'
                break
        if '250' in client_socket.recv(1024).decode():
            client_socket.send('DATA'.encode())
        else:
            client_socket.close()
            print 'ERROR - invalid response code'
            break
        if '354' in client_socket.recv(1024).decode():
            message = ''.join(message_text)
            client_socket.send(message.encode())
            if '250' in client_socket.recv(1024).decode():
                client_socket.send('QUIT'.encode())
                client_socket.close()
            else:
                client_socket.close()
                print 'ERROR - invalid response code'
                break
        else:
            client_socket.close()
            print 'ERROR - invalid response code'
            break
    else:
        client_socket.close()
        print 'ERROR - invalid response code'
        break

    break
