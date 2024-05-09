import os
import shutil
import time
import boto3

s3 = boto3.client('s3')

source_folder=os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/detection_v8')
destination_folder = os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/cloud_v8')

print(source_folder)
# List all files in the source folder
time.sleep(1)
files = os.listdir(source_folder)
print(files)
# Check for files with the same name and different extensions
for file in files:
    if file.endswith('.json') and f"{os.path.splitext(file)[0]}.jpg" in files and f"{os.path.splitext(file)[0]}.mp4" in files:
        
        filename=os.path.splitext(file)[0]

        s3.upload_file(f'{source_folder}/{filename}.json', 'fire-sight-detection', f'{filename}.json')
        s3.upload_file(f'{source_folder}/{filename}.jpg', 'fire-sight-detection', f'{filename}.jpg')
        s3.upload_file(f'{source_folder}/{filename}.mp4', 'fire-sight-detection', f'{filename}.mp4')
        
        time.sleep(1)
        
        # Move the files to the destination folder
        shutil.move(os.path.join(source_folder, file), destination_folder)
        shutil.move(os.path.join(source_folder, f"{os.path.splitext(file)[0]}.jpg"), destination_folder)
        shutil.move(os.path.join(source_folder, f"{os.path.splitext(file)[0]}.mp4"), destination_folder)
        print('~~~ Event Saved ~~~')

