
import argparse
import socket
import string

client_socket = socket.socket()

def parse_args():
	parser = argparse.ArgumentParser(description='Process client args')
	parser.add_argument('IP', type=str)
	parser.add_argument('PORT', type=str)
	args = parser.parse_args()
	return args

def send_msg(socket, msg):
	#msg_len + data
	msg = str(len(msg)) + str(msg) + '\n'
	client_socket.send(str.encode(msg))

def check_alert(msg):
	if 'win' in msg.lower():
		print("You Win!")
		print("Game Over!")
		print("Exiting Program")
	elif 'lose' in msg.lower():
		print(msg.lower())
		print("Game Over!")
		print("Exiting Program")
	elif 'overload' in msg.lower():
		print("Sorry love, server only supports 3 clients at a time!")
		print("It is currently overloaded!")
	else:
		print("UNKNOWN message from server:")
		print(msg)

	print("Exiting Program")
	client_socket.close()
	exit(0)

def parse_server_resp(server_responce):
	decoded_msg = server_responce.decode('utf-8')
	msg_flag = decoded_msg[0]

	if msg_flag == '0':
		#game msg case
		msg_type = "game"
		word_length = int(decoded_msg[1])
		num_incorrect = int(decoded_msg[2])
		data = decoded_msg[2:]
		return (msg_type, (word_length, num_incorrect, data))
	else:
		#alert msg case
		msg_type = "alert"
		alert = decoded_msg[1:]
		return (msg_type, alert)

def connect_to_server(IP, PORT):
	try:
		client_socket.connect((IP, PORT))
	except socket.error as e:
		print(str(e))

	send_msg(client_socket, cheat_code)
	
	incorrect_letters = []
	incorrect_guesses = 0
	while True:
		client_guess = input('Letter to guess: ').lower()
		if client_guess not in string.ascii_letters:
			print("Error! Please guess a letter.")
			continue
		elif client_guess in incorrect_letters:
			print("Error! Letter A has been guessed before, please guess another letter.")
			continue

		send_msg(client_socket, client_guess)

		server_responce = client_socket.recv(1024)
		msg_type, content = parse_server_resp(server_responce)

		if msg_type == 'alert':
			check_alert(content)
		else:
			if incorrect_guesses < content[1]:
				incorrect_guesses += 1
				incorrect_letters.append(client_guess)

			print(content[2])
			print("Inorrect Guesses: " + str(incorrect_letters))

	client_socket.close()


def main():
	global cheat_code

	args = parse_args()
	IP = args.IP
	PORT = int(args.PORT)

	while True:
		ready = input('Ready to start game? (y/n):').lower()
		if ready == 'n':
			print("Nothing sent to the server, closing the program")
			exit(0)
		elif ready == 'y':
			cheat_code = ''
			break
		elif ready.isdigit():
			cheat_code = ready
			break
		else:
			print("Illegal intput, Please try again")

	connect_to_server(IP, PORT)




if __name__ == '__main__':
	main()