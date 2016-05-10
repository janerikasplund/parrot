import glob, os, speech_rest, time

count = 0
prompt = ":)"
print ("Enter the filename")
filename = raw_input(prompt)
os.environ['dir_name'] = filename+" transcript"
if not os.path.exists(os.environ['dir_name']):
       os.makedirs(os.environ['dir_name'])
os.chdir(os.environ['dir_name'])

for file in sorted(glob.glob(filename + "*.flac")):
	 os.system('python speech_rest.py %s >>transcrip4.txt' % file)
	 count += 1
	 print "Working on file " + str(count) + "..."
         time.sleep(50) 
