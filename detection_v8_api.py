import cv2
import time
import torch
import os
from collections import deque
import json
from datetime import date
from datetime import datetime
from json import dumps
import subprocess
from ultralytics import YOLO
from flask import Flask, Response
from flask_cors import CORS


def upload():
    script_path = 'upload_v8.py'
    print('Uploading files to cloud ....')
    subprocess.run(['python', script_path])
    

vidpath = os.path.expanduser('~C:\Users\sssah\Downloads\Fire_Sight-main\Fire_Sight-main/videos/fireEscapeMyHouse_numbered.avi')
# vidpath = os.path.expanduser('~/Desktop/fyp_yolov8/videos/BoatfireIslandMarina.mp4') 
event_dir = os.path.expanduser('~C:\Users\sssah\Downloads\Fire_Sight-main\Fire_Sight-main/detection_v8')

model_path=os.path.expanduser('~C:\Users\sssah\Downloads\Fire_Sight-main\Fire_Sight-main/newmodelv8/newmodel4/train/weights/best.pt')
model = YOLO(model_path)


cam_number=123
cam_link=0

capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus

fire = False

detnum=0 #Number of detections in a short period
framenum=0 #frame number
last_det_frame=0

queue_3_seconds = deque(maxlen=90)  # 3 seconds at 30 fps
queue_12_seconds = deque(maxlen=460)  # 15 seconds at 30 fps


app = Flask(__name__)
CORS(app)

def gen_frame():
    global framenum, fire, last_det_frame, queue_3_seconds, queue_12_seconds,detnum, capture

    # Loop through the video frames
    while True:
        # Read a frame from the video
        ret, frame = capture.read()
        det_class='' #class name of detection 
        if not ret:
            break
            
        framenum+=1
        if fire == True: #and frame_counter%2==0:
            queue_12_seconds.append(frame.copy())

            if len(queue_12_seconds) >= 360:  # 15 seconds
                # Save the 20-second queue as a video
                combined_frames = list(queue_3_seconds) + list(queue_12_seconds)
                video_filename = f"detection_{curr_time}.mp4"
                video_filepath = os.path.join(f'{event_dir}', video_filename)
                height, width, layers = combined_frames[0].shape

                video_writer = cv2.VideoWriter(video_filepath, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))
                for frame in combined_frames:
                    video_writer.write(frame)
                video_writer.release()

                print('~~~ Event Video Saved ~~~')
                fire = False
                queue_3_seconds.clear()
                queue_12_seconds.clear()

                #upload()  ##########################################

            #print(frame_counter)
        elif fire != True:# and frame_counter%2==0:
            queue_3_seconds.append(frame.copy())
            # thumbnail=frame.copy()
        else:
            continue 

        if framenum%30==0 and fire == False: #make predictions after skipping frames
            results = model(frame.copy())
            names = model.names
            for r in results:
                for c in r.boxes.cls:
                    det_class=names[int(c)]

        if det_class == 'fire' or det_class == 'smoke':
            frame = results[0].plot()
            detnum+=1
            if detnum >=3 and framenum-last_det_frame>500:#after 500 frames attempt new detection
                thumbnail=frame.copy()

                fire=True
                
                today =  str(date.today())
                now = datetime.now()
                current_time = str(now.strftime("%H:%M:%S"))

                print('####################')
                print(f'## {det_class} Detection ##')
                print('####################')

                curr_time=int(time.time())
                cv2.imwrite(f'{event_dir}/detection_{curr_time}.jpg', thumbnail)
                print("~~~ Event JPG Saved ~~~")

                json_data = {
                    "Class": det_class,
                    "Date": today,
                    "Time": current_time,
                    "Camera": cam_number,
                    "Camera_Link":cam_link
                }
                with open(f"{event_dir}/detection_{curr_time}.json", "w") as outfile:
                    json.dump(json_data, outfile)
                print('~~~ Event JSON Saved ~~~')

                last_det_frame=framenum
            elif detnum>3:
                detnum=0
                print('~~~~~~~~~  reset ~~~~~~~~~~~')

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=4900)


