from flask import Flask, render_template,request,redirect,url_for,send_file,send_from_directory
import requests, json, os
from werkzeug.utils import secure_filename
import time
# all config files
SERVER_HOST_ADDRESS = 'https://aqueous-scrubland-12306.herokuapp.com/'
DOCUMENTATION_UPLOAD_FOLDER = 'static/uploads/documentationFile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['DOCUMENTATION_UPLOAD_FOLDER'] = DOCUMENTATION_UPLOAD_FOLDER


def get_suppliers():
    companies = []
    if request.method == 'GET':
        url = "https://rheem.etq.com/reliance/rest/v1/dao/VACATION2/SUPPLIE_PROFILE_2022?columns=COMPANY_NAME,ECC_ID&ordercolumns=COMPANY_NAME&pagesize=2000"
        headers = {
             #'authorization': "Basic cmhlZW0tZGV2OmpRcHh5eHQzallRbTRLUlE=", 
             'authorization': "Basic UmhlZW1Qcm9kOjl3TDZORVtieDcwcSE3ZA==",
             'content-type': "application/json; charset=utf-8"
          }
        response = requests.request("GET", url, headers=headers)
        status = response.status_code
        if status == 200:

            print("200 Status")
            json_data = json.loads(response.content)
            print(str(json_data))
            for record in json_data.get("Records"):
                company = {}
                try:
                    print(record)
                    company['id'] = (record.get("Columns")[1].get("value"))
                    company['value'] = (record.get("Columns")[0].get("value"))
                    companies.append(company)
                except:
                    print("ERROR: Couldn't add Supplier")
            print(str(companies))
            return companies
        else:
            return ([]) #render_template('failure.html')



@app.route('/', methods = ['GET'])
def index():
   data = get_suppliers()
   return render_template('index.html', data=data)

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
    print(request.form['supplier'])
    if request.method == 'POST':
        bean = {"Document": [
                           {
                               "applicationName": "VACATION2",
                               "formName": "ACCOUNT_MANAGEMENT_ACTIVITY_D",
                               "phase": "WEBSITE_GENERATION_D",
                               "Fields": [
                                   {
                                       "fieldName": "NAME_11_D",
                                       "Values": [request.form['name']]
                                   },
                                   {
                                       "fieldName": "TITLE_11_D",
                                       "Values": [request.form['title']]
                                   },
                                   {
                                       "fieldName": "PHONE_NUMBER_25_D",
                                       "Values":[request.form['deskNumber']]
                                   },
                                   {
                                       "fieldName": "EMAIL_33_D",
                                       "Values": [request.form['email']]
                                   },
                                   {
                                       "fieldName": "SUPPLIER_13_D",
                                       "Values": [request.form['supplier']]
                                   },
                                   {
                                       "fieldName": "PHONE_NUMBER_CELL_D",
                                       "Values": [request.form['cellNumber']]
                                   }
                               ]
                           }
                       ]}
                




        data = json.dumps(bean)
        #r = requests.post('https://rheem-dev.etq.com/reliance_dev/rest/v1/documents',auth=('rheem-dev', 'jQpxyxt3jYQm4KRQ'),data = payload)
        url = "https://rheem.etq.com/reliance/rest/v1/documents"
        #url = "https://rheem-dev.etq.com/reliance_dev/rest/v1/documents" for Dev
        headers = {
             #'authorization': "Basic cmhlZW0tZGV2OmpRcHh5eHQzallRbTRLUlE=",  for Dev
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
