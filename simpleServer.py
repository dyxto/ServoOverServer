'''
# Simple HTTP Server Example
>>> https://core-electronics.com.au/guides/raspberry-pi-pico-w-create-a-simple-http-server/
# Control an LED and read a Button using a web browser
'''
import time
import network
import socket
from machine import Pin

led = Pin("LED", Pin.OUT)
ledState = 'LED State Unknown'

button = Pin("LED", Pin.IN)

ssid = '55775573656E7061695844'
password = 'uwu-senp@!-xd3'

'''
>>> https://core-electronics.com.au/guides/getting-started-with-servos-examples-with-raspberry-pi-pico/
'''
from servo import Servo

# Create our Servo object, assigning the
# GPIO pin connected the PWM wire of the servo
my_servo = Servo(pin_id=0)

delay_ms = 25  # Amount of milliseconds to wait between servo movements

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# replace the "html" variable with the following to create a more user-friendly control panel
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><center><h1>Control Panel</h1></center><br><br>
<form><center>
<center> <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
<br><br>
<center> <button class="buttonRed" name="led" value="off" type="submit">LED OFF</button>
</form>
<br><br>
<br><br>
<p>%s<p></body></html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

def testPico():
    my_servo.write(155)  # Set the Servo to the left most position
    time.sleep_ms(1000)  # Wait for 1 second
    
    my_servo.write(25)  # Set the Servo to the right most position
    time.sleep_ms(1000)  # Wait for 1 second
    
    my_servo.write(90)  # Set the Servo to the mid-point (90 is half way between zero and 180 degrees)
    time.sleep_ms(1000)  # Wait for 1 second
    
# Listen for connections, serve client
 
testPico()
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        
        if led_on == 8:
            print("led on")
            led.value(1)
        if led_off == 8:
            print("led off")
            led.value(0)
        
        ledState = "LED is OFF" if led.value() == 0 else "LED is ON" # a compact if-else statement
       
        if button.value() == 1: # button not pressed
            print("button NOT pressed")
            buttonState = "Button is NOT pressed"
            my_servo.write(145)  # Set the Servo to the left most position
            time.sleep_ms(1000)  # Wait for 1 second
            my_servo.write(90)
        else:
            print("button pressed")
            buttonState = "Button is pressed"
            my_servo.write(35)  # Set the Servo to the left most position
            time.sleep_ms(1000)  # Wait for 1 second
            my_servo.write(90)
        
        # Create and send response
        stateis = ledState + " and " + buttonState
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')