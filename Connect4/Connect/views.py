from django.http import JsonResponse
import json

# Create your views here.
list = [[-1,-1,-1,-1,-1,-1,-1] for i in range(0,6)]
col = [6 for i in range(0,7)]
moveCnt = 1
def index(column):
    data = col[column - 1]
    if data > 0 and data < 7:
        return (6 - data)
    elif data == 0:
        return -1

def makeMove(moveColumn,bit):
    colu = moveColumn
    two = index(colu)
    if two != -1:
        list[5 - two][colu-1] = bit
        col[colu-1] = col[colu-1] - 1
        global moveCnt
        moveCnt = moveCnt + 1
    elif two == -1:
        return "Invalid Move"
    return "Valid Move"


def diagonal():
    winner=-1
    for i in range(0,6):
        for j in range(0,7):
            winner=-1
            cntRed = 0
            cntYellow = 0
            i1 = i+1
            i2 = i+2
            i3 = i+3
            j1 = j+1
            j2 = j+2
            j3 = j+3
            if i1 > 0 and i1 < 5 and i2 > 0 and i2 < 5 and i3 > 0 and i3 < 5 and j1 > 0 and j1 < 6 and j2 > 0 and j2 < 6 and j3 > 0 and j3 < 6 :
                forwardList = [list[i][j] , list[i1][j1] , list[i2][j2] , list[i3][j3]]
                for x in forwardList:
                    if x == 1:
                        cntRed = cntRed + 1
                    elif x == 0:
                        cntYellow = cntYellow + 1
                if cntRed == 4:
                    winner = 1
                    break
                elif cntYellow == 4:
                    winner = 0
                    break
            i1 = i-1
            i2 = i-2
            i3 = i-3
            j1 = j-1
            j2 = j-2
            j3 = j-3
            if i1 > 0 and i1 < 5 and i2 > 0 and i2 < 5 and i3 > 0 and i3 < 5 and j1 > 0 and j1 < 6 and j2 > 0 and j2 < 6 and j3 > 0 and j3 < 6 :
                backwardList = [list[i][j] , list[i1][j1] , list[i2][j2] , list[i3][j3] ]
                for x in backwardList:
                    if x == 1:
                        cntRed = cntRed + 1
                    elif x == 0:
                        cntYellow = cntYellow + 1
                if cntRed == 4:
                    winner = 1
                    return winner
                elif cntYellow == 4:
                    winner = 0
                    return winner
    return winner
def columnWin(li):
    winner=-1
    for i in range(0,6):
        for j in range(0,7):
            winner=-1
            cntRed = 0
            cntYellow = 0
            if (j+3) > 0 and (j+3) < 6 :
                columnList = [li[i][j] , li[i][j+1] , li[i][j+2] , li[i][j+3]]
                for x in columnList:
                    if x == 1:
                        cntRed = cntRed + 1
                    elif x == 0:
                        cntYellow = cntYellow + 1
                if cntRed == 4:
                    winner = 1
                    return winner
                elif cntYellow == 4:
                    winner = 0
                    return winner
    return winner

def rowWin(li):
    winner=-1
    for i in range(0,6):
        for j in range(0,7):
            winner=-1
            cntRed = 0
            cntYellow = 0
            if (i+3) > 0 and (i+3) < 6 :
                rowList = [li[i][j] , li[i+1][j] , li[i+2][j] , li[i+3][j]]
                for x in rowList:
                    if x == 1:
                        cntRed = cntRed + 1
                    elif x == 0:
                        cntYellow = cntYellow + 1
                if cntRed == 4:
                    winner = 1
                    return winner
                elif cntYellow == 4:
                    winner = 0
                    return winner
    return winner


def winnerCheck(list):
    diag = diagonal()
    column = columnWin(list)
    row = rowWin(list)

    if diag == 1 or column == 1 or row == 1:
        return 1
    elif diag == 0 or column == 0 or row == 0:
        return 0
    else:
        return -1
def refresh():
    global list
    global col
    global moveCnt
    list = [[-1,-1,-1,-1,-1,-1,-1] for i in range(0,6)]
    col = [6 for i in range(0,7)]
    moveCnt = 1

def gameOn(req):
    
    body = json.loads(req.body.decode('utf-8'))
    Refresh = body['Refresh']
    Player = body['Player']
    coinColor = body['coinColor']
    data = {'Message':'' }
    global list
    global moveCnt
    global col
    if Refresh == 'START':
        refresh()
        data['Message'] = "READY"
        return JsonResponse(data)
    if ((moveCnt % 2 == 0) and coinColor == "Yellow" ) or ((moveCnt % 2 != 0) and coinColor == "Red") :
        data['Message'] = "Wait for your chance"
        return JsonResponse(data)
    Column = int(body['Column'])
    if coinColor == 'Red':
        bit = 1
    elif coinColor == "Yellow":
        bit = 0
    move = makeMove(Column,bit)
    win = winnerCheck(list)
    text = ""
    if win == 1:
        text = "Red wins"
    elif win == 0:
        text = "Yellow wins"
    data['Message'] = move
    if text == "Red wins" or text == "Yellow wins" :
        refresh()
        data['Message'] = text
    return JsonResponse(data)


    
