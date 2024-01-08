from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
import os
import cv2
from PIL import Image

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif','pdf'}

app = Flask(__name__,template_folder="template")
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processPhoto(filename,operation):
    print(f"the operation is {operation} and filename is{filename}")
    img=cv2.imread(f"upload/{filename}")
    match operation:
        case "cgray":
            processedImg=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,processedImg)
            return newfilename
        
        case "cblur":
            blurImg=cv2.blur(img,(15,15))
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,blurImg)
            return newfilename
            

        case "cwebp":
            newfilename=f"static/{filename.rsplit(',',1)[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename

        case "jpg":
            newfilename=f"static/{filename.rsplit(',',1)[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename 

        case "png":
            newfilename=f"static/{filename.rsplit(',',1)[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpdf":
            img =Image.open(f"upload/{filename}")
            img=img.convert("RGB")
            newfilename=img.save(f"static/{filename.rsplit(',',1)[0]}.pdf")
            newfilename=f"static/{filename.rsplit(',',1)[0]}.pdf"
            return newfilename
        
                  
    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "ERROR!!No file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new= processPhoto(filename,operation)
            flash(f"Image has been processed Get it from <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")

app.run(debug=True)