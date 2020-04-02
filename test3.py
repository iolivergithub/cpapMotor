import time
import RPi.GPIO as IO


print("Intialising")

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(26,IO.OUT)

p = IO.PWM(26,100) # GPIO 26 in BCM mode is pin 37
p.start(0)
time.sleep(2)

print("OK Ready")

ds = 0
run = True

print("Commands are u,d,s,x")

while (run==True):
   i = input("CMD>")
   if i=='u':
      ds=ds+5
      p.start(ds)
      print("Duty Cycle is ",ds)
   if i=='d':
      ds=ds-5
      p.start(ds)
      print("Duty Cycle is ",ds)
   if i=='s':
      ds=0
      p.start(ds)
      print("Duty Cycle is STOPPED")
   if i=='x':
      print("EXITING")
      ds=0
      run=False


#for ds in range(10,12):
#   print("Duty cycle is ",ds)
#   p.start(ds)
#   time.sleep(2)

p.start(0)
print("Stopping")
p.stop()


