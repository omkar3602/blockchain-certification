from django.shortcuts import render, redirect
from django.contrib import messages
from . import utils
# Create your views here.
def index(request):
    return render(request, 'index.html')


def issue_certificate(request):
    if request.method == 'POST':
        address = request.POST['address']
        name = request.POST['name']
        competitionName = request.POST['competitionName']
        print(type(address), address)
        receipt = utils.issue_certificate(address, name, competitionName)

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

    certificate = utils.view_certificate(id)

    return render(request, 'certificate.html', {'certificate': certificate})