import glob, os, speech_rest, time

count = 0
prompt = ":)"
print ("Enter the filename")
os.chdir("/home/jan/parrot/")
filename = raw_input(prompt)

for file in sorted(glob.glob(filename + "*.flac")):
 os.system('python speech_rest.py %s >>transcript4.txt' % file)
 count += 1
 print "Working on file " + str(count) + "..."
 time.sleep(10)
