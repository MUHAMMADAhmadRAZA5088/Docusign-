from flask import Flask, render_template, request, redirect, url_for
import docusign_esign as docusign
from docusign_esign import ApiClient, EnvelopesApi, SignHere, Signer, Document

app = Flask(__name__)

# DocuSign API credentials
integrator_key = '0813bede-b095-433d-a7b5-bbb25daf6bd8'
base_path = 'https://demo.docusign.net'
redirect_uri = 'http://yourdomain.com/docusign/callback'
account_id = 'bd182fdb-bda4-40d6-85b5-0a452eaef7e6'

# DocuSign API client setup
api_client = ApiClient()
api_client.host = base_path
# import pdb; pdb.set_trace()
api_client.set_oauth_base_path('spider.docusign.com')
api_client.configure_jwt_authorization_flow(integrator_key, 'PRIVATE_KEY_PATH', 'USER_ID', 'AUDIENCE', 'EXPIRATION_TIME')

# DocuSign EnvelopesApi setup
envelopes_api = EnvelopesApi(api_client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_envelope', methods=['POST'])
def send_envelope():
    # Code to handle form submission and send envelope
    # Retrieve signer's email from the form
    signer_email = request.form.get('signer_email')

    # Create a document to be signed
    document = Document(
        document_base64='base64_document_content',
        name='Document Name',
        file_extension='pdf',
        document_id='1'
    )

    # Create a signer
    signer = Signer(
        email=signer_email,
        name='Signer Name',
        recipient_id='1',
        tabs={
            'signHereTabs': [SignHere(document_id='1', page_number='1', x_position='100', y_position='100')]
        }
    )

    # Create an envelope definition
    envelope_definition = docusign.EnvelopeDefinition(
        email_subject='Please sign this document',
        documents=[document],
        recipients=docusign.Recipients(signers=[signer]),
        status='sent'
    )

    # Create and send the envelope
    envelope_summary = envelopes_api.create_envelope(account_id, envelope_definition=envelope_definition)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
