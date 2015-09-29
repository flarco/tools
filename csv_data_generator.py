'''
args example:
python csv_data_generator.py "int_n=2; dec_n=1; string_n=5; date_n=2; datetime_n=2; lines_n = 2000; target_file_path =/_/coding/Python/other/data_test_1.csv"
'''

import sys, time, datetime
import string, random

def rand_int(min_v=0, max_v=10):
    return random.randint(min_v, max_v)

def rand_dec(min_v=0, max_v=10):
    return random.uniform(min_v, max_v)
    
def rand_string(min_l=1,max_l=10):
    N = random.randint(min_l, max_l)
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def rand_date(min_delta=0, max_delta=10):
    N = random.randint(min_delta, max_delta)
    return (datetime.datetime.now().now() - datetime.timedelta(days=N)).strftime('%Y-%m-%d')

def rand_datetime(min_delta=0, max_delta=10):
    N = random.uniform(min_delta, max_delta)
    return datetime.datetime.now().now() - datetime.timedelta(days=N)

start_time = time.clock()

if len(sys.argv) == 1: args = "int_n=2; dec_n=1; string_n=5; date_n=2; datetime_n=2; lines_n = 2000; target_file_path =/_/coding/Python/other/data_test_1.csv"
else: args = sys.argv[1]

parameters_string = args.replace(' ', '').split(';')
parameters = {}

# default values
parameters['int_n'] = 0
parameters['dec_n'] = 0
parameters['string_n'] = 0
parameters['date_n'] = 0
parameters['delimiter'] = '\t'
parameters['linefeed'] = '\n'
parameters['enclosing'] = ''


for f in parameters_string:
    f2 = f.split('=')
    try: parameters[f2[0]] = int(f2[1])
    except: parameters[f2[0]] = f2[1]

delimiter = parameters['delimiter']
linefeed = parameters['linefeed']
enclosing = parameters['enclosing']



# Open the File
target_file = open(parameters['target_file_path'], 'w')

# Write headers
line_text_array = []

for ii in range(parameters['string_n']):
    line_text_array.append('string_col_' + str(ii))

for ii in range(parameters['date_n']):
    line_text_array.append('date_col_' + str(ii))

for ii in range(parameters['datetime_n']):
    line_text_array.append('datetime_col_' + str(ii))

for ii in range(parameters['int_n']):
    line_text_array.append('int_col_' + str(ii))

for ii in range(parameters['dec_n']):
    line_text_array.append('dec_col_' + str(ii))

target_file.write(delimiter.join(line_text_array) + linefeed)

# Write data rows
for i in range(parameters['lines_n']):
    line_text_array = []
    
    for ii in range(parameters['string_n']):
        line_text_array.append(enclosing + rand_string(2,25) + enclosing )
    
    for ii in range(parameters['date_n']):
        line_text_array.append(enclosing + str(rand_date(1,100*365)) + enclosing )
    
    for ii in range(parameters['datetime_n']):
        line_text_array.append(enclosing + str(rand_datetime(1,100*365)) + enclosing )

    for ii in range(parameters['int_n']):
        line_text_array.append(enclosing + str(rand_int(0,9999999)) + enclosing )

    for ii in range(parameters['dec_n']):
        line_text_array.append(enclosing + str(rand_dec(0,999999)) + enclosing )
        
    target_file.write(delimiter.join(line_text_array) + linefeed)
    

target_file.close()

print("Generated " + str(parameters['lines_n']) + " lines in " + parameters['target_file_path'])

elapsed_time = time.clock() - start_time
print "Time elapsed: {} seconds".format(elapsed_time)

