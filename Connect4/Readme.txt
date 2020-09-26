Project donw using Django framework
Project name : Connect4
App Name : Connect
The API takes json data from the request and response is sent in json format.
Language used : Python 3.8.6
Command to run django local server : python manage.py runserver (or) python3 manage.py runserver inside the Pratilipi project folder
URL : http://127.0.0.1:8000/gameOn  For local server
ONCE A PLAYER WINS, THE GAME IS AUTOMATICALLY RESET TO PLAY A NEW GAME AND THE WINNER NAME IS SENT AS RESPONSE MESSAGE.

Request Format :

	{
	
	"Refresh":"NIL", //Mandatory
	"Column":"1",
	"Player":"Sharath", //Mandatory
	"coinColor": "Red" //Mandatory
	
	}

	Example:
		For START
			{
			
			"Refresh":"START",
			"Column":"", // Column is optional fo START
			"Player":"Sharath",
			"coinColor": "Red"
			
			}
		For Game Moves :
			{
	
			"Refresh":"NIL", // Anything other than START - Mandatory for Moves
			"Column":"1",
			"Player":"Sharath", 
			"coinColor": "Red"
			
			}
Response Format :
	{
		"Message": "",
	}

	Example : 
		For illegal chances
			{
				"Message": "Wait for your chance", 
			}
		For Valid Moves
			{
				"Message": "Valid Move",
			}
		For Winner message(When Yellow wins)
			{
				"Message": "Yellow wins",
			}
