import serial
import time
import sys
print(sys.path)
from tmqtt import tmqtt

#brokeraddr = "10.144.176.21"
#brokeraddr = "10.144.176.249"
brokeraddr = "192.168.1.79"
brokerport = 1883
serialport = "/dev/ttyUSB0"

tm = tmqtt.TMQTT("SPM3000",brokeraddr)
tm.connect()
print("TM",tm)



####################################################
#
# ALL THE GOOD STUFF STARTS HERE
#
####################################################


print("Connecting to sensor")
s=serial.Serial(serialport,timeout=1)



####################################################
#
# DATA COLLECTION LOOP
#
####################################################


print("Waiting for system to settle...")
time.sleep(0.2)
s.flushInput()
s.flushOutput()

time.sleep(0.2)

print("Obtaining Serial Number")
s.write("s".encode())
serialnumber = s.readline(24)
print(serialnumber);

#print("Connecting to TPM")
#tpmdevice = tpm.TPM()
#print("get random returns ",tpmdevice.getRandom(8))

#print("Extending PCR 22 with serial number")


print("Soft Reset")
s.write("r".encode())
print(s.readline(10))
time.sleep(0.05)


print("Continuous Mode")
s.write("c".encode())
print(s.readline(10))
time.sleep(0.05)


print("Initial Results and Clear Sensor NVRAM - obtain 3 values")
s.write("d".encode())
print(s.readline(10))
time.sleep(0.05)
s.write("d".encode())
print(s.readline(10))
time.sleep(0.05)
s.write("d".encode())
print(s.readline(10))
time.sleep(0.05)


print("Running")
i=0
try:
   while True:
      s.write("d".encode())
      d = s.readline(10).decode('utf-8').strip('\n').strip('\r')

      msg = { 'rate':d, 'units':'slm' }
     
      print(tm,msg)
      tm.publish(msg)

      values=( i,str(d) )
      #cur.execute('''INSERT INTO slog(mindex,flowrate) VALUES(?,?)''', values)   
      i=i+1
      if (i % 100)==0:
         pass
         #print("bulk data ... split this off into a thread")
         #sendbulkdata(cur,i)
      time.sleep(0.01)
except KeyboardInterrupt:
      print("Interrupted!")




####################################################
#
# SHUTDOWN!
#
####################################################


print("Shutting down...");

print("...flushing serial buffers")
s.flushInput()
s.flushOutput()
s.close()
print("...shutting down MQTT")
tm.disconnect()
print("...closing local database ",i," entries")

print("System Stopped.\n")


#print("System Stopped.\n")
