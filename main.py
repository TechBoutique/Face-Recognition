from flask import Flask, render_template, Response, request
from camera import VideoCamera
import flask_monitoringdashboard as dashboard
import os
import cv2
import glob
import numpy as np
from flask_cors import CORS
from filenamer import generateName
from cacheserver import database


global file_path

file_path = 'videos/facial_exp.mkv'
app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        global file_path
        # Get the file from post request
        try:
            db = database("crowdanalytix.db")
            f = request.files['file']
            if(f.filename.split(".")[-1] != "mp4"):
                raise Exception("Upload mp4 file")
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath, 'static/videos', f.filename)
            f.save(file_path)
            rows = db.select_video(file_path)
            if (len(rows) == 0):
                # Face Detector
                print("Face Detection Initialized")
                video_name = gen(VideoCamera(file_path))
                print("Face Detection Finished")
                db.insert_video(str(file_path), str(video_name))

            else:
                for row in rows:
                    video_name = row[0]

            return render_template('index_video.html', link={"link": video_name.replace("/templates/static/", "")})
        except Exception as e:
            print(e)
            return render_template('index.html')

def gen(camera):
    global file_path
    try:
        while True:
            frame = camera.get_frame()
        
    except:
        img_array = []
        filename = glob.glob('static/frames/*.jpg')
        frames = []
        for i in filename:
            frames.append(int(i.replace("static/frames/","").replace(".jpg","").replace("frame","")))
        

        for filename in sorted(frames):
            img = cv2.imread("static/frames/"+str(filename)+".jpg")
            height, width, _ = img.shape
            size = (width,height)
            img_array.append(img)
    
        video_name = "templates/static/detected_video/"+generateName()
        out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m','p','4','v'), camera.fps, size)
    
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        path = str(os.system("pwd"))[1:] + "/" + video_name
        new = path.split(".")
        new_path = "."+new[0].replace("/templates","") + "1.mp4"
        os.system("ffmpeg -y -i ."+ path + " -vcodec h264 " + new_path)
        os.system('rm -rf %s/*' % "static/frames")
        return (new[0] + "1.mp4")

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('./ssl/server.crt','./ssl/server.key'))
