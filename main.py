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
    print(str(list(request.form.getlist('securityTools'))))
    if request.method == 'POST':
        bean = {"Document": [
                           {
                               "applicationName": "VENDOR_COMPLIANCE_1_D",
                               "formName": "VENDOR_COMPLIANCE_SURVEY_P",
                               "phase": "RHEEM_REVIEW_2_P",
                               "Fields": [
                                   {
                                       "fieldName" : "CARRIER_CONFIRMATION_NUMBER_P",
                                       "Values" : [request.form['confirmationNumber']]
                                   },
                                   {
                                       "fieldName" : "CARRIER_P",
                                       "Values" : ["Yes"]
                                   },
                                   
                                   #Point of Contact Fields
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
                                   },
                                   {
                                       "fieldName" : "HAS_OR_IS_YOUR_COMPANY_CURRENTLY_CONDUCTING_BUSINESS_UNDER_ANY_OTHER_NAMES_WITHIN_THE_LAST_10_YEARS_IF_YES_WHAT_IS_ARE_THE_NAMES_P",
                                       "Values" : [request.form['currentConductQuestion']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_WHAT_IS_ARE_THE_NAMES_P",
                                       "Values" : [request.form['currentConductYes']]
                                   },
                                   {
                                       "fieldName" : "TYPE_OF_BUSINESS_P",
                                       "Values" : [request.form['businessType']]
                                   },
                                   {
                                       "fieldName" : "IS_THE_BUSINESS_PUBLICLY_TRADED_P",
                                       "Values" : [request.form['publicTradedRadio']]
                                   },
                                   {
                                       "fieldName" : "EXCHANGE_D",
                                       "Values" : [request.form['exchange']]
                                   },
                                   {
                                       "fieldName" : "SYMBOL_D",
                                       "Values" : [request.form['symbol']]
                                   },
                                   {
                                       "fieldName" : "ADD_NAMES_HERE_P",
                                       "Values" : [request.form['ownerTen']]
                                   },
                                   {
                                       "fieldName" : "PLEASE_CONFIRM_THAT_YOU_HAVE_READ_AND_ABIDE_BY_OUR_SUPPLIER_CODE_OF_CONDUCT_LOCATED_AT_RHEEM_COM_2_P",
                                       "Values" : [request.form['codeOfConductConfirm']]
                                   },
                                   {
                                       "fieldName" : "WHAT_IS_THE_COUNTRY_OF_ORIGIN_FOR_THE_GOODS_YOUR_COMPANY_PROVIDES_TO_RHEEM_IF_THERE_ARE_MORE_THAN_ONE_PLEASE_LIST_THEM_P",
                                       "Values" : [request.form['countryOfOrigin']]
                                   },
                                   {
                                       "fieldName" : "LIST_PREVIOUS_OR_CURRENT_RELATIONSHIPS_WITH_RHEEM_AND_THE_PERIOD_WHEN_SUCH_RELATIONSHIPS_WERE_ACTIVE_P",
                                       "Values" : [request.form['rheemRelationships']]
                                   },
                                   {
                                       "fieldName" : "DO_YOU_PLAN_TO_USE_ANY_THIRD_PARTIES_OTHER_THAN_TRANSPORT_SERVICES_IN_PROVIDING_GOODS_SERVICES_P",
                                       "Values" : [request.form['thirdPartiesRadio']]
                                   },
                                   #Point of Contact Fields


                                   #Legal Fields
                                   {
                                       "fieldName" : "ARE_THERE_ANY_CIVIL_CRIMINAL_OR_ADMINISTRATIVE_JUDGMENTS_CLAIMS_SUITS_OR_ARBITRATION_PROCEEDINGS_PENDING_OR_OUTSTANDING_AGAINST_YOUR_BUSINESS_OR_ITS_OFFICERS_P",
                                       "Values" : [request.form['outstandingJudgementsRadio']]
                                   },
                                   {
                                       "fieldName" : "HAS_A_CONSENT_DECREE_EVER_BEEN_ISSUED_AGAINST_YOUR_COMPANY_OFFICERS_OR_DIRECTORS_BY_ANY_GOVERNMENT_ENTITY_P",
                                       "Values" : [request.form['consentDecreeRadio']]
                                   },
                                   {
                                       "fieldName" : "IS_YOUR_COMPANY_UNDER_AUDIT_OR_INVESTIGATION_IN_CONNECTION_WITH_THE_GOODS_OR_SERVICES_THAT_YOU_PROVIDE_TO_RHEEM_P",
                                       "Values" : [request.form['auditRadio']]
                                   },
                                   #Legal Fields


                                   #Government Fields
                                   {
                                       "fieldName" : "NON_U_S_PUBLIC_OFFICIAL_MAY_INCLUDE_EMPLOYEES_OF_GOVERNMENT_AGENCIES_OWNED_BUSINESSES_SUCH_AS_STATE_OWNED_ENTERPRISES_AND_A_POLITICAL_PARTY_OR_POLITICAL_CANDIDATE_P",
                                       "Values" : [request.form['governmentEmployeeRadio']]
                                   },
                                   {
                                       "fieldName" : "DOES_ANY_KEY_EMPLOYEE_OR_SENIOR_MANAGEMENT_MEMBER_OF_THE_BUSINESS_PROVIDE_FINANCIAL_OR_ANY_OTHER_BENEFITS_TO_A_NON_U_S_PUBLIC_OFFICIAL_OR_A_MEMBER_OF_A_NON_U_S_PUBLIC_OFFICIAL_S_FAMILY_P",
                                       "Values" : [request.form['publicOfficialRadio']]
                                   },
                                   {
                                       "fieldName" : "DOES_ANY_NON_U_S_PUBLIC_OFFICIAL_OR_A_MEMBER_OF_A_NON_U_S_PUBLIC_OFFICIAL_S_FAMILY_STAND_TO_BENEFIT_IN_ANY_WAY_AS_A_RESULT_OF_THE_PROPOSED_AGREEMENT_P",
                                       "Values" : [request.form['nonUSFamiliyBenefitRadio']]
                                   },
                                   {
                                       "fieldName" : "IS_ANY_KEY_EMPLOYEE_OR_SENIOR_MANAGEMENT_OF_THE_BUSINESS_RELATED_BY_BLOOD_MARRIAGE_CURRENT_BUSINESS_ASSOCIATION_OR_OTHERWISE_TO_A_NON_U_S_PUBLIC_OFFICIAL_P",
                                       "Values" : [request.form['nonUSRelationRadio']]
                                   },
                                   #Government Fields


                                   #Affiliate Fields
                                   {
                                       "fieldName" : "HAS_ANY_KEY_EMPLOYEE_OR_SENIOR_OFFICER_OF_YOUR_BUSINESS_EVER_BEEN_EMPLOYED_BY_OR_PERFORMED_SERVICES_FOR_RHEEM_P",
                                       "Values" : [request.form['employeeRheemRadio']]
                                   },
                                   {
                                       "fieldName" : "ARE_ANY_OF_YOUR_BUSINESS_PRINCIPALS_RELATED_TO_ANYONE_AT_RHEEM_P",
                                       "Values" : [request.form['companyRelationRadio']]
                                   },
                                   #Affiliate Fields


                                   #Insurance Fields
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_COMMERCIAL_GENERAL_LIABILITY_COVERAGE_P",
                                       "Values" : [request.form['liabilityCoverageRadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_COVERAGE_LIMITS_P",
                                       "Values" : [request.form['coverageLimitLiability']]
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_WORKERS_COMPENSATION_COVERAGE_P",
                                       "Values" : [request.form['workersCompensationRadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_COVERAGE_LIMITS_1_P",
                                       "Values" : [request.form['coverageLimitWorkerComp']]
                                   },
                                   {
                                       "fieldName" : "INDICATE_RETENTION_AMOUNT_P",
                                       "Values" : [request.form['retentionAmount']]
                                   },
                                   {
                                       "fieldName" : "IF_YOU_PROVIDE_PRODUCTS_OR_PERFORM_ANY_WORK_FROM_RHEEM_DOES_THE_COMPANY_HAVE_PRODUCT_LIABILITY_COMPLETED_OPERATIONS_INSURANCE_COVERAGE_P",
                                       "Values" : [request.form['operationsInsuranceRadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YOU_PROVIDE_SERVICES_TO_RHEEM_DOES_THE_COMPANY_HAVE_ERRORS_AND_OMISSION_LIABILITY_COVERAGE_P",
                                       "Values" : [request.form['omissionLiabilityRadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_COVERAGE_LIMITS_3_P",
                                       "Values" : [request.form['coverageOmissionLiability']]
                                   },
                                   #Insurance Fields


                                   #Security Fields
                                   {
                                       "fieldName": "HAS_THE_COMPANY_HAD_A_DATA_BREACH_IN_THE_LAST_3_YEARS_P",
                                       "Values": [request.form['dataBreachRadio']]
                                   },
                                   {
                                       "fieldName": "IF_YES_PLEASE_EXPLAIN_P",
                                       "Values":[request.form['dataBreachYes']]
                                   },
                                   {
                                       "fieldName": "DOES_THE_COMPANY_HAVE_CYBER_LIABILITY_INSURANCE_P",
                                       "Values": [request.form['cyberInsuranceRadio']]
                                   },
                                   {
                                       "fieldName": "IF_YES_COVERAGE_LIMITS_4_P",
                                       "Values": [request.form['cyberInsuranceLimit']]
                                   },
                                   {
                                       "fieldName": "DOES_IT_COVER_THIRD_PART_LOSSES_P",
                                       "Values": [request.form['cyberCoverRadio']]
                                   },
                                   {
                                       "fieldName": "DOES_THE_COMPANY_HAVE_A_PRIVACY_POLICY_P",
                                       "Values": [request.form['privacyPolicyRadio']]
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_A_WRITTEN_SECURITY_POLICY_PROGRAM_P",
                                       "Values" : [request.form['writtenPolicyRadio']]
                                   },
                                   {
                                       "fieldName" : "HAS_THE_COMPANY_DESIGNATED_A_CHIEF_SECURITY_OFFICER_P",
                                       "Values" : [request.form['designateCSORadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_PLEASE_PROVIDE_CONTACT_INFORMATION_P",
                                       "Values" : [request.form['contactCSO']]
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_A_DATA_BREACH_AND_INCIDENT_RESPONSE_PLAN_P",
                                       "Values" : [request.form['dataBreachPlanRadio']]
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_A_BUSINESS_CONTINUITY_PLAN_P",
                                       "Values" : [request.form['businessContinuityPlanRadio']]
                                   },
                                   {
                                       "fieldName" : "DO_YOU_STORE_RHEEM_PERSONALLY_IDENTIFIABLE_INFORMATION_PII_P",
                                       "Values" : [request.form['PIIRadio']]
                                   },
                                   {
                                       "fieldName" : "IF_YES_IS_DATA_ENCRYPTED_AT_REST_P",
                                       "Values" : [request.form['restEncryptRadio']]
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_PERFORM_ANNUAL_HACKING_TESTING_P",
                                       "Values" : [request.form['annualPenetrationTestRadio']]
                                   },
                                   {
                                       "fieldName" : "CLICK_ALL_THAT_APPLY_P",
                                       "Values" : list(request.form.getlist('securityTools'))
                                   },
                                   {
                                       "fieldName" : "DOES_THE_COMPANY_HAVE_ANY_SECURITY_CONTROL_CERTIFICATIONS_I_E_ISO_27001_SSAE16_SOC_2_P",
                                       "Values" : [request.form['securityCertifyRadio']]
                                   },
                                   {
                                       "fieldName" : "DO_YOU_USE_SECURE_SOCKETS_LAYER_SSL_ENCRYPTION_P",
                                       "Values" : [request.form['encryptSSLRadio']]
                                   }
                                   #Security Fields
                     
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
