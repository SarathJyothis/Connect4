from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os,datetime,random


from InputOutput.models import docMas
from InputOutput.models import docDtls
from InputOutput.models import users


# Create your views here.
docDir='Data/Documents/'
#For user Authentication - Login
def userAuth(req):
    if 'userId' in req.session:
        return JsonResponse({"Message":"Logout from the active session first"})
    bodyJson = req.body.decode('utf-8')
    body = json.loads(bodyJson)
    username = body['username']
    psswd = body['psswd']
    user = users.objects.filter(username=username,psswd=psswd).only('username')
    if len(user) > 1:
        return JsonResponse({"Message":"Please enter valid credentials"})
    req.session['userId'] = user[0].username
    return JsonResponse({"Message":"Authorised"})
#API endpoint for users to upload PDF document and retrieve document digitization related data
@csrf_exempt
def userUpload(req):
    if req.method == 'POST':
        if 'userId' not in req.POST:
            return JsonResponse({"Message":"Invalid POST request format"})
        if req.session['userId'] != req.POST['userId']:
            return JsonResponse({"Message":"Unauthorised access detected"})
        fileName=req.FILES['file'].name
        document = str(random.randrange(0,99999))+"_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+fileName
        filePath = docDir+document
        document = document.split(".")
        docId = document[0]
        fout = open(filePath,"wb+")
        fout.write(req.FILES['file'].read())
        userId=req.POST['userId']

        docMasSave = docMas(userId=userId,docId=docId,origFileName=fileName,filePath=filePath,status="PENDING")
        docMasSave.save()
        docDtlsCreate = docDtls(docId=docId)
        docDtlsCreate.save()


        return JsonResponse({"Message":"File received","documentId":docId})
    elif req.method == 'GET':
        if 'userId' not in req.session:
            return JsonResponse({"Message":"Login to access the feature"})
        bodyJson = req.body.decode('utf-8')
        body = json.loads(bodyJson)
        if req.session['userId'] != body['userId']:
            return JsonResponse({"Message":"Unauthorised access detected"})
        if 'userId' in body and 'requestType' in body and 'documentId' in body:
            statData = docMas.objects.filter(docId=body['documentId'])
            if body['requestType'] == 'Track Status':
                status = []
                stat={}
                for x in statData:
                    stat['docId'] = x.docId
                    stat['fileName'] = x.origFileName
                    stat['digiStatus'] = x.status
                    status.append(stat)
                    
                return JsonResponse({"Digitization Status" : status})

            elif body['requestType'] == 'Digitized Data':
                if len(statData) <= 0 :
                    return JsonResponse({"Message":"Document not found."})
                if statData[0].status != 'DIGITIZED':
                    return JsonResponse({"Message":"Document not digitized yet. Track it\'s status and try again when it is DIGITIZED"})
                docDtl = docDtls.objects.filter(docId = body['documentId'])
                if body['documentId'] == 'AllData':
                    docDtl = docDtls.objects.all()
                jsoN = []
                js={}
                for x in docDtl:
                    js['invoiceNumber'] = x.invoiceNumber
                    js['buyer'] = x.buyer
                    js['seller'] = x.seller
                    js['billTo'] = x.billTo
                    js['shipTo'] = x.shipTo
                    js['items'] = x.items
                    js['totalPrice'] = x.totalPrice
                    js['GST'] = x.GST
                    js['paymentInfo'] = x.paymentInfo
                    js['paymentStatus'] = x.paymentStatus
                    js['additional'] = x.additional
                    jsoN.append(js)
                return JsonResponse({"Message" : "Digitized Data","Data":jsoN})
            else:
                return JsonResponse({"Message":"Invalid request format"})

    return JsonResponse({"Message":"File received"})
dataFormat = {'fileName':'','filePath':'','status':'PENDING','invoiceNumber':'','buyer':'','seller':'','billTo':'','shipTo':'','items':'','totalPrice':'','GST':'','paymentInfo':'','paymentStatus':'','additional':''}
def formatChecker(body):
    global dataFormat
    for x,y in body.items():
        dataFormat[x]=y

#API to Add ot update digitized data
def interUser(req):
    if req.method == 'GET':
        if 'userId' not in req.session:
            return JsonResponse({"Message":"Login to access the feature"})
        bodyJson = req.body.decode('utf-8')
        body = json.loads(bodyJson)
        if req.session['userId'] != body['userId']:
            return JsonResponse({"Message":"Unauthorised access detected"})
        if 'requestType' in body and 'userId' in body and 'documentId' in body :
            formatChecker(body)
            global dataFormat
            reqType = body['requestType']
            if reqType == 'Add':
                if 'fileName' in body and 'filePath' in body and 'status' in body:
                    docMasCreate = docMas(userId=body['userId'],docId=body['documentId'],origFileName=dataFormat['fileName'],filePath=dataFormat['filePath'],status=dataFormat['status'])
                    docMasCreate.save()
                    docDtlsAdd= docDtls()
                    docDtlsAdd.docId = body['documentId']
                    for x,y in dataFormat.items():
                        if x != 'userId' and x != 'documentId' and x != 'requestType' and x != 'fileName' and x != 'filePath' :
                            docDtlsAdd.x = y
                    docDtlsAdd.save()
                    return JsonResponse({"Message":"Added"})
                else:
                    return JsonResponse({"Message" : "Invalid Inputs"})
            elif body['requestType'] == 'Update' :
                if 'status' in body and 'fileName' in body and 'filePath' in body:
                    docMasUpdate = docMas.objects.filter(docId = body['documentId']).update(origFileName=dataFormat['fileName'],filePath=dataFormat['filePath'],status=dataFormat['status'])
                docDtlsUpdate = docDtls.objects.filter(docId = body['documentId']).update(invoiceNumber=dataFormat['invoiceNumber'],buyer=dataFormat['buyer'],seller=dataFormat['seller'],billTo=dataFormat['billTo'],shipTo=dataFormat['shipTo'],items=dataFormat['items'],totalPrice=dataFormat['totalPrice'],GST=dataFormat['GST'],paymentInfo=dataFormat['paymentInfo'],paymentStatus=dataFormat['paymentStatus'],additional=dataFormat['additional'])
                docDtlsU = docDtls.objects.filter(docId = body['documentId'])
                return JsonResponse({"Message" : "Updated"})
        else:
            return JsonResponse({"Message" : "Invalid request"})
    else:
        return JsonResponse({"Message" : "Invalid request method"})

#To add a user
def addUser(req):
    if req.method == 'GET':
        bodyJson = req.body.decode('utf-8')
        body = json.loads(bodyJson)
        if 'userId' in body and 'psswd' in body and 'requestType' in body:
            if body['requestType'] == 'Add User':
                user = users(username=body['userId'],psswd=body['psswd'])
                user.save()
                return JsonResponse({"Message":"User added successfully"})
        else:
            return JsonResponse({"Message":"Invalid request format"})

#To delete all data from the system
def deleteAllData(req):
    docMasDel = docMas.objects.all()
    docDtlsDel = docDtls.objects.all()
    usersDel = users.objects.all()
    for x in docMasDel:
        if os.path.exists(x.filePath):
            os.remove(x.filePath)
        x.delete()
    for x in docDtlsDel:
        x.delete()
    for x in usersDel:
        x.delete()
    return JsonResponse({"Message":"Deleted"})

#To logout
def logout(req):
    if 'userId' in req.session:
        del req.session['userId']
        return JsonResponse({"Message":"Logged out"})
    return JsonResponse({"Message":"No active login detected"})