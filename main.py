from flask import Flask,render_template,Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0) #set to 0 as we only have 1 web cam attached | i think we can add a if condition to check if we have multiple cameras 
 
#we neeed a function to capture the frames and diplaying it on the website 
def cctv():
    while True:
        success,frame = camera.read() #read the data and images from the camera 
        if not success:
            break
        else:
            ret,buffer = cv2.imencode('.jpg',frame) #encoding the frames /buffers that we are gettin ifrom camera in from of jpg format 
            frame = buffer.tobytes()# to display image iwe need to use tobytes in open cv  lib 

# we will us yield to display live video and this code will refresh the frames every second and we will get the images in form of video 
        yield ( b'--frame\r\n'
              b'content-Type: image/jpg\r\n\r\n' + frame+b'\r\n'
              )


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/video")
def video():
    return Response(cctv(),mimetype='multipart/x-mixed-replace; boundary = frame') #calling the function we created cctv and it is a function call, mimetype = pass multipart value )

if __name__ == "__main__":
    app.run(debug =True)