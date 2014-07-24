from flask import Flask, request
import serial
import atexit
import ConfigParser
import sys

config = ConfigParser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
device = config.get('serial', 'device')
try:
    ser = serial.Serial(device, 9600)
except:
    print "Could not find device %s" % device
    sys.exit()

def is_ascii(string):
    try:
        string.decode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

def is_valid(string):
    return is_ascii(string) and len(string) < 200


@app.route('/write', methods=['GET', 'POST'])
def receve_message():
    message = ""
    if request.method == 'GET':
        message = request.args.get('message')
    else:
        message = request.form['message']
    print "Received message: {}".format(message)

    if (is_valid(message)):
        print "Message is valid, writing to serial port."
        serial_write(message)
        return "Wrote message '{}' to serial port.".format(message)
    else:
        print "Message is not valid, not writing."
        return "Message {} not valid, not writing to serial port.".format(message)


def serial_write(message):
    ser.write(str(message))
    ser.write('\n')


def exit_handler():
    print "Closing serial port."
    ser.close()

if __name__ == '__main__':
    atexit.register(exit_handler)
    app.run(host='0.0.0.0')
