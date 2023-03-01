#from github repo https://github.com/danielrioslinares/python-misc/blob/master/csv2wav.py
import csv
import wave
import struct
import statistics
from datetime import datetime

# Target
filenames = ['waveformlonger.csv'] # .csv file
properties = ['' for f in filenames] # added information
f = 500 # sampling frequency

for filename, property in zip(filenames, properties):
	print('###### FILE ' + str(filename) + ' ######')
	# Data read and amplitude normalization
	print('-> Normalizing data...')
	data = [value for time, value in csv.reader(open(filename, 'U'), delimiter=',')]
	# Remove useless data (may add glitches)
	for i in reversed(range(len(data))):
		try: a = float(data[i])
		except: del(data[i])
	# Convert to float the remaining
	data = [float(d) for d in data]
	# Nomalize data (per 1 and perfect High pass at 0 Hz)
	data = [(d-sum(data)/len(data))/abs(max(data)) for d in data]
	# Saturation rate (typical deviation)
	saturation = 3*statistics.pstdev(data)
	data = [d/saturation if abs(d) < saturation else d/abs(d) for d in data]

	# Create a new .wav named with the format "<name>_<date>"
	print('-> Opening the file...')
	wavfilename = filename + '_' + str(datetime.now().strftime('%Y%m%d_%H%M%S')) + property + '.wav'
	wavfile = wave.open(wavfilename, 'w')

	# Audio file parameters
	wavfile.setparams(
	    (1, # mono
	    2, # bytes
	    f, # Sampling frequency
	    len(data), # number of samples
	    'NONE', # compression type (only 'NONE available')
	    'not compressed' # compression method (only 'not compressed' available)
	    ))

	# Because Wave_file.writeframes(data) requires a "bytes-like" object
	print('-> Converting to bytes...')
	data_bytes = b''.join([struct.pack('<h', int(d*1024*24)) for d in data])

	# Write the frames into the Wave_write file
	print('-> Writing the .wav')
	wavfile.writeframes(data_bytes)
	wavfile.close()