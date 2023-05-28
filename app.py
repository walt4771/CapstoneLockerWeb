from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN) # Line Tracer Sensor

GPIO.setup(18, GPIO.OUT)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

green = 27
red = 17
blue = 22
GPIO.setup(red, GPIO.OUT)
RED = GPIO.PWM(red, 100)

GPIO.setup(blue, GPIO.OUT)
BLUE = GPIO.PWM(blue, 100)

GPIO.setup(green, GPIO.OUT)
GREEN = GPIO.PWM(green, 100)

@app.route('/')
def main():
    return render_template('main.html')


# 공통 페이지

@app.route('/selectlocker')
def selectlocker():
    usertype = request.args.get('usertype', default = '', type = str)
    print(usertype)
    if   usertype == "sell":
        return render_template('selectlocker.html', data = usertype)
    elif usertype ==  "buy":
        return render_template('selectlocker.html', data = usertype)
    else:
        return render_template('main.html', error = "잘못된 접근입니다(사용자 타입 누락)")

@app.route('/passwd')
def passwd():
    usertype = request.args.get('usertype', default = '', type = str)
    if   usertype == "sell":
        return render_template('passwd.html', data = usertype)
    elif usertype ==  "buy":
        return render_template('passwd.html', data = usertype)
    else:
        return render_template('main.html', error = "잘못된 접근입니다(사용자 타입 누락)")


# 구매자 페이지
@app.route('/preview/<product_id>')
def preview(product_id):
    productId = product_id
    return render_template('preview.html', productId = productId)

@app.route('/payment')
def payment():
    return render_template('payment.html')


# 판매자 페이지
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# ㅇ뜌ㅕㅎ
@app.route('/payment_completed/')
def payment_completed():

    pg_token = request.args.get('pg_token', default = '', type = str)
    print(pg_token)

    return render_template('payment_completed.html', data = pg_token)
    
    


# Device Control
@app.route('/sensor_usonic')
def sensor_usonic():
    if not GPIO.input(24):
        print("book in not detected")
        return jsonify(False)
    else:
        print("book detected")
        return jsonify(True)
        
@app.route('/sensor_opendoor')
def sensor_opendoor():
    GPIO.output(18, 1)
    time.sleep(1)
    GPIO.output(18, 0)
    return jsonify(True)
    
@app.route('/sensor_isdooropen')
def sensor_isdooropen():
    while(True):
        door_state = GPIO.input(23)
        if door_state == False:
            return(jsonify("Door Closed"))
        
        else:
            return(jsonify("Door Opened"))
            
@app.route('/sensor_lighton')
def sensor_lighton():
    BLUE.start(100)
    RED.start(100)
    GREEN.start(100)
    
@app.route('/sensor_lightoff')
def sensor_lightoff():
    BLUE.start(0)
    RED.start(0)
    GREEN.start(0)

    
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_USONIC_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_USONIC_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_USONIC_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_USONIC_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance
    


app.run(host='localhost', port = 80)
