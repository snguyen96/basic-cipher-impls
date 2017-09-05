from socket import *
import sys

port_number = int(sys.argv[-1])
# create socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('', port_number))
server_socket.listen(1)

# starts handshake and parsing commands with client when socket is accepted
while True:
    connectionSocket, addr = server_socket.accept()
    connectionSocket.send(('220 ' + gethostname()).encode())
    response = connectionSocket.recv(1024).decode()
    if 'HELO ' in response:
        connectionSocket.send(('250 Hello ' + response.split(' ')[1] + ', pleased to meet you.').encode())
    try:
        parsed = []
        temp = []
        temp1 = []
        temp2 = []
        space = True
        other_space = False
        expected_colon = False
        pass_mail_from = False
        pass_receipt_to = False

        mail_from = connectionSocket.recv(1024).decode()  # input MAIL FROM command

        if 'QUIT' in mail_from:
            connectionSocket.close()
            continue

        def parse_data_space(ws):

            if ws.__len__() <= 1:
                return False
            if ws[0] == 'D' and ws[1] == 'A' and ws[2] == 'T' and ws[3] == 'A':
                for letter in ws:
                    if letter == ' ' or letter == 'D' or letter == 'A' or letter == 'T' or letter == 'A':
                        continue
                    else:
                        return False
                return True
            return False

        def is_special(l):  # special tokens

            if l == '<' or l == '>' or l == '(' or l == ')' or l == '[' or l == ']' or l == '\\' or l == '.' or l == ',' or l == ';' or l == ':' or l == '@' or l == '"':
                return True
            else:
                return False

        def parse_element(e):  # parse element

            if e[0].isalpha() and e.__len__() > 1:
                return True
            else:
                print('501 Syntax error in parameters or arguments')
                return False

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

        def parse_local_part(lp):  # parse local part

            for letter in lp:
                if letter == ' ' or letter == '\t' or is_special(letter):
                    print('501 Syntax error in parameters or arguments')
                    return False
                else:
                    continue

            return True

        def parse_mailbox(address):  # parse Mailbox

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

        def parse_data(recipients, sender): # parse DATA Command

            data = connectionSocket.recv(1024).decode()

            if data[-1] == '.':
                connectionSocket.send('250 OK'.encode())

            for r in range(0, recipients.__len__()):  # write message to forward path file

                with open('forward/' + recipients[r].split('@')[1], 'a') as email:
                    email.write('From: ' + '<' + sender + '>' + '\n')
                    for i in range(0, recipients.__len__()):
                        email.write('To: ' + '<' + recipients[i] + '>' + '\n')
                    email.write(data[:-1])

        r = mail_from.split(':')
        r1 = ''.join(r[0]).split(' ')

        if mail_from == 'DATA' or parse_data_space(mail_from):  # out of order cases
            print('503 Bad sequence of commands')
            connectionSocket.close()
            continue
        elif mail_from.split(':')[0] == 'RCPT TO' or (r1[0] == 'RCPT' and r1[-1] == 'TO'):
            print('503 Bad sequence of commands')
            connectionSocket.close()
            continue

        if mail_from.__len__() > 1 and mail_from[-1] != '>' and mail_from[-1] != ' ':
            print('501 Syntax error in parameters or arguments')
            connectionSocket.close()
            continue

        for letter in mail_from:  # parsing Mail From Command

            if not temp:
                parsed.append(letter)
                if parsed[0] != 'M':
                    print('500 Syntax error: command unrecognized')
                    connectionSocket.close()
                    break
                if letter == ' ':
                    parsed.pop()
                    if ''.join(parsed) == 'MAIL':
                        temp.append(letter)
                        parsed = []
                        continue
                    else:
                        print('500 Syntax error: command unrecognized')
                        connectionSocket.close()
                        break
                continue

            if letter == ' ' or letter == '\t':
                if space and other_space:
                    pass
                elif space:
                    continue
                else:
                    print('500 Syntax error: command unrecognized')  # error because of unexpected space
                    connectionSocket.close()
                    break

            if not temp1:
                space = False
                parsed.append(letter)
                if parsed[0] != 'F':
                    print('500 Syntax error: command unrecognized')
                    connectionSocket.close()
                    break
                if ''.join(parsed) == 'FROM':
                    expected_colon = True
                    continue
                if expected_colon:
                    if letter == ':':
                        if ''.join(parsed) == 'FROM:':
                            space = True
                            temp1.append(letter)
                            continue
                        else:
                            print('500 Syntax error: command unrecognized')
                            connectionSocket.close()
                            break
                else:
                    continue

            if ''.join(parsed) == 'FROM:':
                if letter == '<':
                    parsed.append(letter)
                    other_space = True
                    continue
                else:
                    print('501 Syntax error in parameters or arguments')  # error because of expected '<'
                    connectionSocket.close()
                    break

            if ''.join(parsed) == 'FROM:<':
                temp2.append(letter)
                if letter == '>':
                    if temp2[-2] == ' ':
                        print('501 Syntax error in parameters or arguments')  # error because of expected '>'
                        connectionSocket.close()
                        break
                    else:
                        temp2.pop()
                        if parse_mailbox(''.join(temp2)):
                            connectionSocket.send('250 OK'.encode())     # completion of parsing MAIL FROM
                            pass_mail_from = True
                            sender = ''.join(temp2)
                            temp2 = []
                            break
                        else:
                            break

            else:
                print('500 Syntax error: command unrecognized')
                connectionSocket.close()
                break

        if pass_mail_from:  # check if MAIL FROM command passed

            recipients = []

            while True:

                temp = []
                temp1 = []
                parsed = []
                expected_colon = False
                other_space = False

                receipt_to = connectionSocket.recv(1024).decode()  # input RCPT TO command

                if 'QUIT' in receipt_to:
                    connectionSocket.close()
                    break

                m = receipt_to.split(':')
                m1 = ''.join(m[0]).split(' ')

                if receipt_to == 'DATA' or parse_data_space(receipt_to):
                    if pass_receipt_to:
                        connectionSocket.send('354 Start mail input; end with <CRLF>.<CRLF>'.encode())  # begins reading the message
                        parse_data(recipients, sender)
                        connectionSocket.close()
                        break
                    else:
                        print('503 Bad sequence of commands')  # prints sequence error if DATA is entered before RCPT TO
                        connectionSocket.close()
                        break
                elif receipt_to.split(':')[0] == 'MAIL FROM' or (m1[0] == 'MAIL' and m1[-1] == 'FROM'):
                    print('503 Bad sequence of commands')
                    connectionSocket.close()
                    break

                for letter in receipt_to:           # parsing Receipt To Command

                    if not temp:
                        parsed.append(letter)
                        if parsed[0] != 'R':
                            print('500 Syntax error: command unrecognized')
                            connectionSocket.close()
                            break
                        if letter == ' ':
                            parsed.pop()
                            if ''.join(parsed) == 'RCPT':
                                temp.append(letter)
                                parsed = []
                                continue
                            else:
                                print('500 Syntax error: command unrecognized')
                                connectionSocket.close()
                                break
                        continue

                    if letter == ' ' or letter == '\t':
                        if space and other_space:
                            pass
                        elif space:
                            continue
                        else:
                            print('500 Syntax error: command unrecognized')  # error because of unexpected space
                            connectionSocket.close()
                            break

                    if not temp1:
                        space = False
                        parsed.append(letter)
                        if ''.join(parsed) == 'TO':
                            expected_colon = True
                            continue
                        if expected_colon:
                            if letter == ':':
                                if ''.join(parsed) == 'TO:':
                                    space = True
                                    temp1.append(letter)
                                    continue
                                else:
                                    print('500 Syntax error: command unrecognized')
                                    connectionSocket.close()
                                    break
                        else:
                            continue

                    if ''.join(parsed) == 'TO:':
                        if letter == '<':
                            parsed.append(letter)
                            other_space = True
                            continue
                        else:
                            print('501 Syntax error in parameters or arguments')  # error because of expected '<'
                            connectionSocket.close()
                            break

                    if ''.join(parsed) == 'TO:<':
                        temp2.append(letter)
                        if letter == '>':
                            if temp2[-2] == ' ':
                                print('501 Syntax error in parameters or arguments')  # error because of expected '>'
                                connectionSocket.close()
                                break
                            else:
                                temp2.pop()
                                if parse_mailbox(''.join(temp2)):
                                    connectionSocket.send('250 OK'.encode())  # completion of parsing RCPT TO
                                    recipients.append(''.join(temp2))
                                    pass_receipt_to = True
                                    temp2 = []
                                    continue
                                else:
                                    connectionSocket.close()
                                    break

                    else:
                        print('501 Syntax error in parameters or arguments')
                        connectionSocket.close()
                        break

    except EOFError:  # termination on end-of-file
        continue
