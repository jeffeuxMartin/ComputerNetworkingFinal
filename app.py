from flask import Flask, render_template, Response 
import io 
import time 
 
app = Flask(__name__)                                                  

def gen(): 
    import cv2 
    # cv2.namedWindow("TryIt!") 
    vc = cv2.VideoCapture(0) 
     
    rval, frame = vc.read() 

    while True: 
        if frame is not None: 
            #cv2.imshow("TryIt!", frame) 
            succ, frame_code = cv2.imencode('.jpg', frame)
            # frame_code = cv2.imencode(, cv2.IMREAD_COLOR) 
            yield(b'--jpgboundary' 
            b'Content-type: image/jpeg\r\n\r\n' + frame_code.tobytes() + b'\r\n')

             
        rval, frame = vc.read() 
         
                                                                       

@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/source.mjpg') 
def feed_stream(): 
    #Response is a object 
    #Streaming Contents 
    #http://flask.pocoo.org/docs/0.12/patterns/streaming/ 
    return Response(gen(), 
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary') 
                                                                       

if __name__ == '__main__': 
    print('run') 
    try: 
        # app.run(host='127.0.0.1', port=8000, debug=True) 
        app.run(host=__import__('sys').argv[1], port=8000, debug=True, threaded=True) 
    except IndexError:
        app.run(host='140.112.247.246', port=8000, debug=True) 
