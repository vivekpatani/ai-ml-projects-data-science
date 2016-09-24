'''
Created on 2016.9.19

@author: zehzhang
'''

import sys
import heapq

class tables_guests:
    tables = {}
    guests = {}
    max_table_index = 0
    def __init__(self, ini_max_table_index, ini_tables, ini_guests):
        self.max_table_index = ini_max_table_index
        self.tables = ini_tables
        self. guests = ini_guests

def create_dictionary(file_path):
    count = 0
    name_list = []
    name_dictionary_temp = {}
    number_dictionary_temp = {}
    relationship_dictionary_temp = {}
    f = open(file_path, 'rU')
    for line in f:
        name_list.append( line.lstrip().rstrip().split(' ') )
    f.close()
    for line in name_list:
        for name in line:
            if name not in name_dictionary_temp:
                count += 1
                name_dictionary_temp[name] = count                
    for key in name_dictionary_temp:
        number_dictionary_temp[ name_dictionary_temp[key] ] = key
    for line in name_list:
        relationship_dictionary_temp[ name_dictionary_temp[ line[0] ] ] \
        = [ name_dictionary_temp[ line[i] ] for i in range(1, len(line)) ]
    return [name_dictionary_temp, number_dictionary_temp, relationship_dictionary_temp, count]        

def successors(current_tables_guests):
    succ_temp = []
    guests_not_seated = [i for i in range(1, total_number_of_guests + 1) \
                         if current_tables_guests.guests[i] == 0]
    available_tables = [i for i in range(1, current_tables_guests.max_table_index+1) \
                        if len(current_tables_guests.tables[i]) < N]
    #print(current_tables_guests.guests)
    #print(guests_not_seated)
    #print(current_tables_guests.tables)
    #print(available_tables)
    #print()
    for guest in guests_not_seated:
        find_table = False
        new_tables = current_tables_guests.tables.copy()
        new_guests = current_tables_guests.guests.copy()
        for table in available_tables:
            know_each_other = False
            for guest_sitting_here in current_tables_guests.tables[table]:
                if guest_sitting_here in relationship_dictionary:
                    if guest in relationship_dictionary[guest_sitting_here]:
                        know_each_other = True
                if guest in relationship_dictionary: 
                    if guest_sitting_here in relationship_dictionary[guest]:
                        know_each_other = True
            if know_each_other:
                continue
            find_table = True
            new_tables[table] = new_tables[table] + [guest]
            new_guests[guest] = table
            new_max_table_index = current_tables_guests.max_table_index
            break
        if not find_table:
            new_tables[current_tables_guests.max_table_index + 1] = [guest]
            new_guests[guest] = current_tables_guests.max_table_index + 1
            new_max_table_index = current_tables_guests.max_table_index + 1
        new_tables_guests = tables_guests(new_max_table_index, new_tables, new_guests)
        if get_signature(new_tables_guests.guests) not in visited_states_dictionary:
            succ_temp.append(new_tables_guests)
    return succ_temp            

def get_signature(current_state):
    state_signature = ''
    for item in sorted ( current_state.items() ):
        state_signature = state_signature + str(item[1])
    return state_signature

def printable_result(assignments):
    table_information = ''
    for table in sorted( assignments.tables.items() ):
        each_table_information = ','.join( [ number_dictionary[i] for i in sorted(table[1])] )
        table_information = table_information + each_table_information + '   '
    print( str(assignments.max_table_index) +'   ' + table_information)
        
def assign_table(initial_tables_guests):
    fringe = []
    count_flag = 0
    heapq.heappush(fringe, (initial_tables_guests.max_table_index, count_flag, initial_tables_guests))
    visited_states_dictionary[get_signature(initial_tables_guests.guests)] = True    
    while len(fringe) > 0:
        head = heapq.heappop(fringe)
        if 0 not in head[2].guests.values():
            return head[2]
        visited_states_dictionary[get_signature(head[2].guests)] = True
        #print(head[2].max_table_index)
        for s in successors(head[2]):
            count_flag += 1
            heapq.heappush(fringe, (s.max_table_index, count_flag, s))
        #if count_flag > 2000:
        #    break
    return  False                

N = int(sys.argv[2])
[name_dictionary, number_dictionary, relationship_dictionary, total_number_of_guests] \
= create_dictionary(sys.argv[1])
visited_states_dictionary = {}
initial_max_table_index = 0
initial_tables = {}
initial_guests = {}
for i in range(1, total_number_of_guests + 1):
    initial_guests[i] = 0
initial_tables_guests = tables_guests(initial_max_table_index, initial_tables, initial_guests)

possible_table_assignment = assign_table(initial_tables_guests)

if possible_table_assignment:
    printable_result(possible_table_assignment)
else:
    print('Life is so hard!')


#print(name_dictionary.items())
#print(number_dictionary.items())
#print(relationship_dictionary.items())
#print(total_number_of_guests)    