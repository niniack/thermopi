import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called 'pins' to store the pin number, name, and pin state:
pins = {
   22 : {'name' : 'ThermUp', 'state' : GPIO.LOW},
   23 : {'name' : 'ThermDown', 'state' : GPIO.LOW},
   24 : {'name' : 'FanUp', 'state' : GPIO.LOW},
   25 : {'name' : 'FanDown', 'state' : GPIO.LOW} 
}

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")

def main():
    
        with open('counter.txt','r') as f:
            currentTemp = f.read()

        for pin in pins: 
                pins[pin]['state'] = GPIO.input(pin)

        templateData = {
                'pins':pins,
                'currentTemp':currentTemp
                }
        return render_template('main.html',**templateData)

@app.route("/<trigPin>/<trigger>")
def trigger (trigPin, trigger):
        # Read the pin number from URL and turn into integer from string:
        trigPin = int(trigPin)
        # Read the device name from trigPin
        deviceName = pins[trigPin]['name']
        # If the trigger part of the URL is "set," execute the following code: 
        if trigger == "set": 
                # First, set the pin to HIGH
                GPIO.output(trigPin, GPIO.HIGH)
                # Then a delay for a second
                time.sleep(0.5)
                # Finally, set he pin back to LOW
                GPIO.output(trigPin, GPIO.LOW)
                # Save the status message to be passed on to the HTML template
                message = "Triggered " + deviceName + " !"
                # Check to see if the pin name is FanDown
                if  deviceName == 'FanUp':
                	# Open counter.txt,read previous line, and then add one to the previous number 
                    with open('counter.txt','r+') as f:
                        currentTemp = f.read()
                        currentTemp = int(currentTemp)
                        currentTemp = currentTemp + 1
                        newTemp = currentTemp
                        f.write(newTemp)
                #Check to see if the pin name is FanDown	
                elif deviceName == 'FanDown':
                	# Open counter.txt,read previous line, and then sub one to the previous number 
                    with open('counter.txt','a+') as f:
                        currentTemp = f.read()
                        currentTemp = int(currentTemp)
                        currentTemp = currentTemp - 1
                        newTemp = currentTemp
                        f.write(newTemp)
                #Don't want to change counter for fan settings
  
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
                pins[pin]['state'] = GPIO.input(pin)


		# Along with the pin dictionary, put the message into the template data dictionary:
        templateData = {
            'message' : message,
            'pins' : pins,
            }

        return render_template('main.html',**templateData)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')