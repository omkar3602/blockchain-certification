from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.decorator import login_required_message
from utils.email_sender import send_mail
from utils import blockchain
import os
from dotenv import load_dotenv
from datetime import datetime

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
        ID_receipt = blockchain.addCertificateID(str(receipt['transactionHash'].hex()))
        if receipt == -1 or ID_receipt == -1:
            messages.info(request, 'Certificate Issuing Failed. Please check the details and try again.')
        else:
            load_dotenv()
            send_mail(email, 'Certificate Issued', f"Your certificate from BlockChain Certification has been issued successfully. Please find the link: {os.getenv('WEB_URL')}certificate/{receipt['transactionHash'].hex()}. The Certificate ID is {receipt['transactionHash'].hex()}.")
            messages.info(request, 'Certificate Issued Successfully at Credential ID: ' + receipt['transactionHash'].hex())
        return render(request, 'issue_certificate.html')
    return render(request, 'issue_certificate.html')

@login_required_message(message="Please log in, in order to view all certificates.")
@login_required
def view_all(request):
    certificates = blockchain.view_all()
    
    if len(certificates) == 0:
        messages.info(request, 'No certificates found.')
        return redirect('home')
    return render(request, 'view_all.html', {'certificates': certificates})


def view(request):
    if request.method == 'POST':
        id = request.POST['id']

        return redirect('certificate', id=id)
    return render(request, 'view.html')

def certificate(request, id):

    certificate = blockchain.view_certificate(id)
    if certificate == -1:
        messages.info(request, 'Certificate Not Found.')
        return redirect('view')
    print(certificate)
    return render(request, 'certificate.html', {'certificate': certificate})

def issued_certificates(request):
    if request.method == 'POST':
        address = request.POST['address']
        certificates = blockchain.view_certificate_by_address(address)


        if len(certificates) == 0:
            messages.info(request, 'No certificates found for the given address.')
            return render(request, 'issued_certificates.html')
        else:
            return render(request, 'issued_certificates.html', {'certificates': certificates, 'address': address})
    certificates = False
    return render(request, 'issued_certificates.html', {'certificates': certificates})