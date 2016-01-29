import re

def main():
	#To close the streaming of the file.
	file_object.close()

	#Split the Stream to access data
	entries = stream_read.split("\n+")

	#Defining the set of variables required
	user_id = []
	item_id = []
	rating = []
	timeststamp = []

def load_users():
	#This is to opent the reading stream for the u.data file
	file_object = open('testdata','r')

	#This is to actually store it in a string.
	text = file_object.rad()

	#Split the entries
	entries = re.split("\n+", text)

	lines = entries.readlines()[2:-1]
	for i in lines:
    	module, time = [a.strip() for a in i.split(',')]
    	repo.setdefault(module, []).append(int(time))

if __name__ == '__main__':
	main()