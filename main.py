from flask import Flask, render_template,request,redirect,url_for,send_file,send_from_directory
import requests, json, os
from werkzeug.utils import secure_filename
import time
# all config files
SERVER_HOST_ADDRESS = 'https://carrier-vendor-form.herokuapp.com/'
DOCUMENTATION_UPLOAD_FOLDER = 'static/uploads/documentationFile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['DOCUMENTATION_UPLOAD_FOLDER'] = DOCUMENTATION_UPLOAD_FOLDER




@app.route('/', methods = ['GET'])
def index():
   return render_template('index.html')

@app.route('/documentationFile/<filename>')
def documentationFile_file(filename):
    return send_from_directory(app.config['DOCUMENTATION_UPLOAD_FOLDER'],filename)

@app.route('/upload')
def upload():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       # check if the post request has the file part
       documentationFile = handle_documentationFile()

       return (str(documentationFile))


def handle_documentationFile():
    # check if the post request has the file part
    if 'documentationFile' not in request.files:
        return 'danger'
    documentationFile = request.files['documentationFile']
    if documentationFile.filename == '':
        return 'danger'
    if documentationFile and allowed_file(documentationFile.filename):
        filename = secure_filename(documentationFile.filename)
        documentationFile.save(os.path.join(app.config['DOCUMENTATION_UPLOAD_FOLDER'], filename))
        return (documentationFile.filename)

@app.route('/get-file')
def get_file():
    return send_file('static/uploads/back.JPG')


@app.route('/create', methods = ['POST'])
def create():
    if request.method == 'POST':
        bean = {"Document": [
                           {
                               "applicationName": "VENDOR_COMPLIANCE_1_D",
                               "formName": "VENDOR_COMPLIANCE_SURVEY_P",
                               "phase": "RHEEM_REVIEW_2_P",
                               "Fields": [
                                   {
                                       "fieldName": "VENDOR_CONTACT_TITLE_P",
                                       "Values": [request.form['vendorContactTitle']]
                                   },
                                   {
                                       "fieldName": "FIRST_NAME_2_P",
                                       "Values": [request.form['firstName']]
                                   },
                                   {
                                       "fieldName": "LAST_NAME_2_P",
                                       "Values":[request.form['lastName']]
                                   },
                                   {
                                       "fieldName": "COMPANY_NAME_3_P",
                                       "Values": [request.form['companyName']]
                                   },
                                   {
                                       "fieldName": "CONTACT_EMAIL_17_P",
                                       "Values": [request.form['contactEmail']]
                                   },
                                   {
                                       "fieldName": "PHONE_NUMBER_3_P",
                                       "Values": [request.form['phoneNumber']]
                                   },
                                   {
                                       "fieldName": "HOW_LONG_HAS_THE_COMPANY_BEEN_IN_EXISTENCE_P",
                                       "Values": [request.form['companyExist']]
                                   }
                     
                               ]
                           }
                       ]}
                




        data = json.dumps(bean)       
        url = "https://rheem.etq.com/reliance/rest/v1/documents"
        headers = {
             'authorization': "Basic UmhlZW1Qcm9kOjl3TDZORVtieDcwcSE3ZA==",
             'content-type': "application/json"
          }
        print("Prepare to send Request")
        response = requests.request("POST", url, data=data, headers=headers)
        print("Prepare to send Request")
        status = response.status_code
        print("Status received")
        if status == 200:
            print("200 Status")
            json_data = json.loads(response.text)
            created_voucher_id = json_data[0]["documentId"]

            if created_voucher_id < 10000:
                return render_template('waiting.html',id = created_voucher_id)
            else:
                return (response.text)
        else:
            return (response.text) #render_template('failure.html')


@app.route('/getconfirmation/')
def get_voucher_number():
    return render_template('confirmation.html')

if __name__ == '__main__':
   app.run()
