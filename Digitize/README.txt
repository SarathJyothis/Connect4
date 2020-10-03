Digitize documents project
Project Name : Digitize
App Name : InputOutput
IN SETTINGS, DEBUG IS SET TO TRUE.
IF IT IS SET TO FALSE, SET THE ALLOWED_HOSTS ACCORDINGLY, IN settings.py.

API endpoint : userUpload/

	POST method (For document upload from client side):
		Local server url : 127.0.0.1:8000/userUpload/
		Header : Set-Cookie : sessionid=*****
		Body :
			form-data:
				file : file to upload ex: sample.pdf
				userId : username - for authentication
		Sample response : 
			{
				"Message": "File received",
				"documentId": "53017_20201003_141053_SarathJyothis"
			}
			

	GET method (For retrieving digitization status) :
		Local server url : 127.0.0.1:8000/userUpload/
		Header : Set-Cookie : sessionid=*****
		Body :
			raw (JSON): 
				Sample request: 
					{
						
						"userId":"sharath1234", //Mandatory
						"documentId": "17591_20201002_162809_SarathJyothis", //Mandatory
						"requestType" : "Track Status"//Mandatory
						
					}
		Sample response(For digitized status) :
			{
				"Digitization Status": [
					{
						"docId": "17591_20201002_162809_SarathJyothis",
						"fileName": "",
						"digiStatus": "DIGITIZED"
					}
				]
			}
					
	GET method (For retrieving digitized data) :
		Local server url : 127.0.0.1:8000/userUpload/
		Header : Set-Cookie : sessionid=*****
		Body :
			raw (JSON): 
				Sample request: 
					{
						
						"userId":"sharath1234", //Mandatory
						"documentId": "17591_20201002_162809_SarathJyothis", //Mandatory
						"requestType" : "Digitized Data"//Mandatory
						
					}
		Sample response (For digitized documentId):
			{
				"Message": "Digitized Data",
				"Data": [
					{
						"invoiceNumber": "1234HH",
						"buyer": "Sam Fulonski",
						"seller": "{'name':'John Jones'}",
						"billTo": "",
						"shipTo": "",
						"items": "",
						"totalPrice": "12435 USD",
						"GST": "",
						"paymentInfo": "",
						"paymentStatus": "",
						"additional": ""
					}
				]
			}

API endpoint : interUser/

	GET method (For adding digitized data for a new document ):
		Local server url : 127.0.0.1:8000/interUser/
		Header : Set-Cookie : sessionid=*****
		Body : 
			raw (JSON) :
				Sample request : 
					{
					
						"userId" : "sharath1234",
						"documentId" : "28893_20201002_150016_SarathJyothis",
						"requestType" : "Add",
						"fileName" : "",
						"filePath" : "",
						"status" : "PENDING",
						"invoiceNumber" : "1234HH",
						"buyer" : "Sam Fulonski",
						"seller" : "{'name':'John Jones'}",
						"totalPrice" : "12435 USD"
					
					}
		Sample response (Successful) :
			{
				"Message": "Added"
			}
	GET method (For updating already one/more existing digitized data ):
		Local server url : 127.0.0.1:8000/interUser/
		Header : Set-Cookie : sessionid=*****
		Body : 
			raw (JSON) :
				Sample request : 
					{

						"userId" : "sharath1234",
						"documentId" : "17591_20201002_162809_SarathJyothis",
						"requestType" : "Update",
						"fileName" : "",
						"filePath" : "",
						"status" : "DIGITIZED",
						"invoiceNumber" : "1234HH",
						"buyer" : "Sam Fulonski",
						"seller" : "{'name':'John Jones'}",
						"totalPrice" : "12435 USD"
					
					
					}
		Sample response (Successful) :
			{
				"Message": "Updated"
			}

Miscellaneos APIs:
	API endpoint (To clear all data from the DB to start afresh) : deleteData/
		GET method :
			Local server url : 127.0.0.1:8000/deleteData/

	API endpoint (To add a user - one at a time) : addUser/
		GET method : 
			Local server url : 127.0.0.1/addUser/
			Header : 
			Body : 
				raw (JSON) :
					Sample request : 
						{

							"username":"sharath1234",
							"psswd":"12345",
							"requestType":"Add User"
							
						}
			Sample response : 
				{
					"Message": "User added successfully"
				}

	API endpoint (For User Authentication) : userAuth/
		GET method :
			Local server url : 127.0.0.1:8000/userAuth/
			Header :
			Body :
				raw (JSON ) : 
					Sample request :
						{
	
							"username" : "sharath1234",
							"psswd" : "12345"
						
						}
			Sample response :
				{
					"Message": "Authorised"
				}
	API endpoint (For logging out) : logout/
		GET method : 
			Local server url : 127.0.0.1:8000/logout/
			Header : 
			Body :
			Sample response :
				{
					"Message": "Logged out"
				}