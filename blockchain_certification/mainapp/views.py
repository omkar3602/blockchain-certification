from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.decorator import login_required_message

from utils import blockchain

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
        receipt = blockchain.issue_certificate(address, name, competitionName)
        if receipt == -1:
            messages.info(request, 'Certificate Issuing Failed. Please check the details and try again.')
        else:
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