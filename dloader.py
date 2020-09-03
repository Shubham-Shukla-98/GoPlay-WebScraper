import os
import subprocess
import time

f = open('links.txt')
# use readline() to read the first line 
line = f.readline()
# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty
lines = list(f)
j=1
print(lines)
for code in lines:
    cs1 = 'dc.bat Prison_Playbook_Ep.'+str(j)+' '+code;
    print(repr(cs1))
    subprocess.Popen(['cmd','/K',cs1])
    time.sleep(2)
    # use realine() to read next line
    j = j+1

f.close()
