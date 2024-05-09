import os

vidpath = os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/videos/fireEscapeMyHouse_numbered.avi')
vid=os.path.expanduser('~/Desktop/fyp_yolov8/FireSight/videos/BoatfireIslandMarina.mp4')

#Camera_number Camera_link Port_number
args_set = {
    ('1', f'{vidpath}', '4900'),
    ('2', f'{vid}', '4800'),
    ('3', '0', '5000')

}
# Save the arguments to a file
with open('cameras.txt', 'w') as file:
    for args in args_set:
        file.write(' '.join(args) + '\n')
