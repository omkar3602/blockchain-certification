from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.decorator import login_required_message
from utils.email_sender import send_mail
from utils import blockchain
import os
from dotenv import load_dotenv

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required_message(message="Please log in, in order to issue certificates.")
@login_required
def issue_certificate(request):
    if request.method == 'POST':
        address = request.POST['address']
        name = request.POST['name']
        competitionName = request.POST['competitionName']
        email = request.POST['email']
        receipt = blockchain.issue_certificate(address, name, competitionName, email)
        if receipt == -1:
            messages.info(request, 'Certificate Issuing Failed. Please check the details and try again.')
        else:
            load_dotenv()
            send_mail(email, 'Certificate Issued', f"Your certificate from TeachAR has been issued successfully. Please find the link: {os.getenv('WEB_URL')}certificate/{receipt['transactionHash'].hex()}. The Certificate ID is {receipt['transactionHash'].hex()}.")
            messages.info(request, 'Certificate Issued Successfully at Credential ID: ' + receipt['transactionHash'].hex())
        return render(request, 'issue_certificate.html')
    return render(request, 'issue_certificate.html')


# For view_all in utils.py 
# hash = input("Enter the hash of the block: ")
# info = contract.functions.viewCertificates().call(block_identifier=hash)
# print(info)



def view(request):
    if request.method == 'POST':
        id = request.POST['id']

        return redirect('certificate', id=id)
    return render(request, 'view.html')

def certificate(request, id):

    certificate = blockchain.view_certificate(id)
    return render(request, 'certificate.html', {'certificate': certificate})