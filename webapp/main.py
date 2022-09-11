import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from numpy.lib.shape_base import expand_dims
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras import utils as u
from tensorflow.keras import models as m

cnn = m.load_model('ClassifierCatDog.h5')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		filepath = 'static/uploads/' + filename

		test_image = u.load_img (filepath, target_size = (64, 64))
		test_image = image.img_to_array(test_image)
		test_image = np.expand_dims(test_image, axis = 0)
		
		result = cnn.predict(test_image)
		
		if result[0][0] == 1:
			predictValue = 'Dog'

		else:
			predictValue = 'Cat'

		return render_template('upload.html', filename=filename, prediction = predictValue)

	else:
		flash('Allowed image types are -> png, jpg, jpeg')
		return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()