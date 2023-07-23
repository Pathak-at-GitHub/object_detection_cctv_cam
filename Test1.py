import cv2
import threading
from flask import Flask , render_template, Response
import cv2
from util_for_color import get_limits
from PIL import Image

app = Flask(__name__, template_folder='../YOLO_ON_Multiple_cameras')

yellow = [255, 255,0]

class camThread (threading.Thread):
    def __init__(self,previewName,camID):
        threading.Thread.__init__(self)
        self.previewName= previewName
        self.camID = camID

    def run(self):
        print("starting "+ self.previewName+"\n")
        camPreview(self.previewName,self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
        rval,frame = cam.read()


    else:
        rval = False
    while rval:
        # cv2.imshow(previewName,frame)
        rval, frame = cam.read()
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        lower_limit, upper_limit = get_limits(yellow)

        mask = cv2.inRange(hsv_image, lower_limit, upper_limit)

        mask_ = Image.fromarray(mask)

        bbox = mask_.getbbox()

        if bbox is not None:
            x1, x2, y1, y2 = bbox
            frame = cv2.rectangle(frame, (x1, x2), (y1, y2), (0, 255, 0), 5)

        # cv2.imshow('mask', mask)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if not rval:
            break;
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        key = cv2.waitKey(1)
        if key==27:
            break
    # cv2.destroyAllWindows(previewName)

# t1 = camThread("camera 1",0)
#
# t1.start()

print("Active Threads = ", threading.active_count())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(camPreview("camera 1",0), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video1')
def video1():
    return Response(camPreview("camera ",1), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
