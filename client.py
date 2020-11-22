
import argparse
import socket


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

def parse_server_resp(server_responce):
	decoded_msg = server_responce.decode('utf-8')
	msg_flag = decoded_msg[0]

	if msg_flag == '0':
		#game msg case
		
	else:
		#alert msg case

def connect_to_server(IP, PORT):
	client_socket = socket.socket()

	try:
		client_socket.connect((host, port))
	except socket.error as e:
		print(str(e))

	send_msg(client_socket, "start")
	
	while True:
		server_responce = client_socket.recv(1024)
		parse_server_resp(server_responce)

		client_guess = input('Letter to guess: ').lower()

		send_msg(client_socket, client_guess)

	ClientSocket.close()


def main():
	args = parse_args()
	IP = args.IP
	PORT = int(args.PORT)

	while True:
		ready = input('Ready to start game? (y/n):').lower()
		if ready == 'n':
			print("Nothing sent to the server, closing the program")
			exit(0)
		elif read == 'y':
			break
		else:
			print("Illegal intput, Please try again")

	connect_to_server(IP, PORT)




if __name__ == '__main__':
	main()