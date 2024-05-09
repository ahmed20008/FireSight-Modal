import cv2
import time
import os
import sys
from collections import deque
import json
from datetime import datetime, date
import subprocess
from ultralytics import YOLO
from flask import Flask, Response
from flask_cors import CORS

class FireDetection:
    def __init__(self, cam_number, cam_link, portnum):
        self.cam_number = cam_number
        self.cam_link = cam_link
        self.portnum = portnum
        self.vidpath = os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/videos/fireEscapeMyHouse_numbered.avi')
        self.event_dir = os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/detection_v8')
        self.model_path = os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/newmodelv8/newmodel4/train/weights/best.pt')
        self.model = YOLO(self.model_path)
        self.capture = cv2.VideoCapture(self.vidpath)
        self.fire = False
        self.detnum = 0
        self.framenum = 0
        self.last_det_frame = 0
        self.queue_3_seconds = deque(maxlen=90)
        self.queue_12_seconds = deque(maxlen=460)
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.route('/video_feed')(self.video_feed)

    def upload(self):
        script_path = 'upload_v8.py'
        print('Uploading files to cloud ....')
        subprocess.run(['python', script_path])

    def gen_frame(self):
        # Loop through the video frames
        while True:
            # Read a frame from the video
            ret, frame = self.capture.read()
            det_class='' #class name of detection 
            if not ret:
                break
                
            self.framenum += 1
            if self.fire: 
                self.queue_12_seconds.append(frame.copy())

                if len(self.queue_12_seconds) >= 360:  # 15 seconds
                    # Save the 20-second queue as a video
                    combined_frames = list(self.queue_3_seconds) + list(self.queue_12_seconds)
                    video_filename = f"detection_{curr_time}.mp4"
                    video_filepath = os.path.join(f'{self.event_dir}', video_filename)
                    height, width, layers = combined_frames[0].shape

                    video_writer = cv2.VideoWriter(video_filepath, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))
                    for frame in combined_frames:
                        video_writer.write(frame)
                    video_writer.release()

                    print('~~~ Event Video Saved ~~~')
                    self.fire = False
                    self.queue_3_seconds.clear()
                    self.queue_12_seconds.clear()

                    #self.upload()  ##########################################

            elif not self.fire:
                self.queue_3_seconds.append(frame.copy())

            if self.framenum % 30 == 0 and not self.fire: #make predictions after skipping frames
                results = self.model(frame.copy())
                names = self.model.names
                for r in results:
                    for c in r.boxes.cls:
                        det_class = names[int(c)]

            if det_class == 'fire' or det_class == 'smoke':
                frame = results[0].plot()
                self.detnum += 1
                if self.detnum >= 3 and self.framenum - self.last_det_frame > 500: #after 500 frames attempt new detection
                    thumbnail = frame.copy()

                    self.fire = True
                    self.queue_12_seconds.append(frame.copy())  # Save the frame with detection in the queue
                    
                    today =  str(date.today())
                    now = datetime.now()
                    current_time = str(now.strftime("%H:%M:%S"))

                    print('####################')
                    print(f'## {det_class} Detection ##')
                    print('####################')

                    curr_time = int(time.time())
                    cv2.imwrite(f'{self.event_dir}/detection_{curr_time}.jpg', thumbnail)
                    print("~~~ Event JPG Saved ~~~")

                    json_data = {
                        "Class": det_class,
                        "Date": today,
                        "Time": current_time,
                        "Camera": self.cam_number,
                        "Camera_Link": self.cam_link
                    }
                    with open(f"{self.event_dir}/detection_{curr_time}.json", "w") as outfile:
                        json.dump(json_data, outfile)
                    print('~~~ Event JSON Saved ~~~')

                    self.last_det_frame = self.framenum
                elif self.detnum > 3:
                    self.detnum = 0
                    print('~~~~~~~~~  reset ~~~~~~~~~~~')

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        pass

    def video_feed(self):
        return Response(self.gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self):
        self.app.run(port=self.portnum)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        cam_number = sys.argv[1]
        cam_link = sys.argv[2]
        portnum = sys.argv[3]
        print(f"Camera Number: {cam_number}, Camera Link: {cam_link}, Port: {portnum}")
        fire_detection = FireDetection(cam_number, cam_link, portnum)
        fire_detection.run()
    else:
        print("Please provide arguments for camra_number, cam_link, and port_number.")
