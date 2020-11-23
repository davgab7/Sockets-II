#Author: Davit Dabrielyan

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
	global word_length
	# msg_flag + word_length + num_incorrect + data
	msg_to_send = '0' + str(word_length) + str(num_incorrect) + str(data)
	connection.send(str.encode(msg_to_send))

def alert_msg(connection, msg_to_send):
	# msg_flag + msg
	msg_to_send = str(len(msg_to_send)) + msg_to_send + '\n'
	connection.send(str.encode(msg_to_send))

def pick_random_word(backdoor):
	global word_file
	global word_length

	#try opening the file
	try:
		word_list = open(word_file, 'r').readlines()
		#can optemize
		for i,v in enumerate(word_list):
			word_list[i] = v.strip()
		word_length = int(word_list[0].split()[0])
		#print("list: " + str(word_list))
	except:
		print("Error occured when opening word file")
		exit()

	r = random.randint(1, len(word_list) - 1)

	if backdoor != "\n": #the case when client just sends empty input
		return word_list[int(backdoor)] #this is indexed from 1 !!!!!
	return word_list[r]

def parse_client_resp(msg):
	#need ot skip the length index
	#print("Raw recved data: " + str(msg.decode('utf-8')))
	return msg.decode('utf-8')[1:]

def threaded_server_for_client(connection):
	global thread_count
	global word_length

	#alert_msg(connection, "Welcome to the HangMan game!")

	#Handling of initial handshake with empty "y/n" or backdoor number for guessing
	received_data = parse_client_resp(connection.recv(2048))
	#print("Here:" + received_data)
	word_to_guess_orig = pick_random_word(received_data)
	word_to_guess = list(word_to_guess_orig)
	#print("Word to be guessed: " + str(word_to_guess))

	incorrect_count = 0
	current_state = '_' * word_length
	game_msg(connection, incorrect_count, current_state)

	while True:
		client_guess = parse_client_resp(connection.recv(2048)).lower().strip()
		#print("CL guess: " + str(len(client_guess)))
		if not client_guess:
			print("Issue with recieved data from client")
			break
		if client_guess in word_to_guess:
			#print("It is!")
			#replace state
			index = word_to_guess.index(client_guess)
			word_to_guess[index] = '_'
			current_state = current_state[:index] + client_guess + current_state[index+1:]

			if '_' not in current_state:
				#Winning case
				alert_msg(connection, "You Win!")
				break
			else:
				game_msg(connection, incorrect_count, current_state)
		else:
			#print("It is NOT!")
			incorrect_count += 1
			if incorrect_count == 6:
				alert_msg(connection, "You lose! The Word: {}".format(str(word_to_guess_orig)))
				break
			else:
				game_msg(connection, incorrect_count, current_state)

	print("Ended connection with player\n")
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

	print('Waitiing for connections..\n')
	server_socket.listen(5) #number of queued connections

	while True:
		client, (ip, port) = server_socket.accept()
		if thread_count == 3:
			print("Thread capacity of 3 has been reached\n")
			alert_msg(client, "server-overloaded")
			continue
		print('A new player has connected! IP: ' + ip + ' with port: ' + str(port) + '\n')
		start_new_thread(threaded_server_for_client, (client, ))
		thread_count += 1

	server_socket.close()


if __name__ == '__main__':
	main()