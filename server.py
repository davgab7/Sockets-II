
import argparse
from _thread import *
import socket
import os

IP = "localhost"

def parse_args():
	parser = argparse.ArgumentParser(description='Process server args')
	parser.add_argument('PORT', type=str)
	parser.add_argument('word_file', nargs='?', type=str)
	args = parser.parse_args()
	return args

def game_msg(connection, word_length, num_incorrect, data):
	# msg_flag + word_length + num_incorrect + data
	msg_to_send = '0' + str(word_length) + str(num_incorrect) + str(data)
	connection.send(str.encode(msg_to_send))

def alert_msg(connection, msg_to_send):
	# msg_flag + msg
	msg_to_send = str(len(msg_to_send)) + msg_to_send + '\n'
	connection.send(str.encode(msg_to_send))

def threaded_server_for_client(connection):
	alert_msg(connection, "Welcome to the HangMan game!")
	while True:
		received_data = connection.recv(2048).decode('utf-8')
		if not received_data:
			break


		
	connection.close()

def main():
	
	args = parse_args()

	PORT = int(args.PORT)

	if args.word_file != None:
		word_file = args.word_file
	else:
		word_file = "default_dict.txt"

	#try opening the file
	try:
		word_list = open(word_file, 'r').readlines()
		word_length = int(word_list[0].split()[0])
		word_list = word_list[1:]
	except:
		print("Error occured when opening word file")
		exit(0)

	try:
		#Set up socjket and bind it
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((IP, PORT))
	except socket.error as e:
		print(str(e))

	print('Waitiing for connections..')
	server_socket.listen(5) #number of queued connections

	thread_count = 0
	while True:
		client, (ip, port) = server_socket.accept()
		if thread_count == 3:
			print("Thread capacity of 3 has been reached")
			continue
		print('A new player has connected! IP: ' + ip + ' with id: ' + str(port))
		start_new_thread(threaded_server_for_client, (client, ))
		thread_count += 1
		print('Thread Number: ' + str(thread_count))
	server_socket.close()


if __name__ == '__main__':
	main()