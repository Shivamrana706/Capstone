import time
import cv2 
from flask import Flask, render_template, request, redirect, url_for,Response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/capstone_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vehicle_name = db.Column(db.String(100))
    vehicle_number = db.Column(db.String(100))
    model_year = db.Column(db.String(100))
    color = db.Column(db.String(100))


    def __init__(self,id, vehicle_name, vehicle_number, model_year, color):

        self.id = id
        self.vehicle_name = vehicle_name
        self.vehicle_number = vehicle_number
        self.model_year = model_year
        self.color = color


@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        id = request.form['id']
        vehicle_name = request.form['vehicle_name']
        vehicle_number = request.form['vehicle_number']
        model_year = request.form['model_year']
        color = request.form['color']


        my_data = Data(id,vehicle_name, vehicle_number, model_year, color)
        db.session.add(my_data)
        db.session.commit()

        

        return redirect(url_for('Index'))


@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        
        
        my_data.vehicle_name = request.form['vehicle_name']
        my_data.vehicle_number = request.form['vehicle_number']
        my_data.model_year = request.form['model_year']
        my_data.color = request.form['color']

        db.session.commit()
        

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('Index'))

def gen():
    
    
    
    """Video streaming generator function."""
#=================================
    cap = cv2.VideoCapture('video.mp4')
 
     # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break
 
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True)