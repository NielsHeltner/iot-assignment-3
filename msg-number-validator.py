#Script to validate if there are missing message numbers

file = open('data.csv', 'r')

file.readline() #skip header

prev_msg_no = None
for line in file.readlines():
    msg_no_index = line.index(',')
    msg_no = int(line[:msg_no_index])
    if prev_msg_no and (prev_msg_no - 1) != msg_no:
        print('ERROR: missing message number ' + str(prev_msg_no - 1))
    prev_msg_no = msg_no
