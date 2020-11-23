
import argparse
from _thread import *
import socket
import os, random

IP = "localhost"
thread_count = 0

def parse_args():
	parser = argparse.ArgumentParser(description='Process server args')
	parser.add_argument('PORT', type=str)
	parser.add_argument('word_file', nargs='?', type=str)
	args = parser.parse_args()
	return args

def game_msg(connection, num_incorrect, data):
	# msg_flag + word_length + num_incorrect + data
	msg_to_send = '0' + str(word_length) + str(num_incorrect) + str(data)
	connection.send(str.encode(msg_to_send))

def alert_msg(connection, msg_to_send):
	# msg_flag + msg
	msg_to_send = str(len(msg_to_send)) + msg_to_send + '\n'
	connection.send(str.encode(msg_to_send))

def pick_random_word():
	global word_file
	global word_length

	#try opening the file
	try:
		word_list = open(word_file, 'r').readlines()
		word_length = int(word_list[0].split()[0])
	except:
		print("Error occured when opening word file")
		exit(0)

	r = random(1, len(word_list) + 1)
	return word_list[r]

def threaded_server_for_client(connection):
	global thread_count
	global word_length

	#alert_msg(connection, "Welcome to the HangMan game!")
	word_to_guess = list(pick_random_word())
	print("Word to be guesse: " + word_to_guess)
	incorrect_count = 0
	current_state = '_' * word_length

	while True:
		received_data = connection.recv(2048).decode('utf-8')
		if not received_data:
			print("Issue with recieved data from client")
			break

		client_guess = received_data[1].lower()
		if client_guess in word_to_guess:
			#replace state
			index = word_to_guess.index(client_guess)
			word_to_guess[index] = '_'
			current_state = current_state[:index] + '_' + current_state[index+1:]

			if '_' not in current_state:
				#Winning case
				alert_msg(connection, "You Win!")
				break
			else:
				game_msg(connection, incorrect_count, current_state)
		else:
			incorrect_count += 1
			if incorrect_count == 6:
				alert_msg(connection, "You lose! The Word: {}".format(str(word_to_guess)))
				break
			else:
				game_msg(connection, incorrect_count, current_state)

	print("Ended connection with player")
	connection.close()
	thread_count -= 1

def main():
	global thread_count
	global word_file
	
	args = parse_args()

	PORT = int(args.PORT)

	if args.word_file != None:
		word_file = args.word_file
	else:
		word_file = "default_dict.txt"

	try:
		#Set up socjket and bind it
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, PORT))
	except socket.error as e:
		print(str(e))

	print('Waitiing for connections..')
	server_socket.listen(5) #number of queued connections

	while True:
		client, (ip, port) = server_socket.accept()
		if thread_count == 3:
			print("Thread capacity of 3 has been reached")
			alert_msg(client, "server-overloaded")
			continue
		print('A new player has connected! IP: ' + ip + ' with port: ' + str(port))
		start_new_thread(threaded_server_for_client, (client, ))
		thread_count += 1

	server_socket.close()


if __name__ == '__main__':
	main()