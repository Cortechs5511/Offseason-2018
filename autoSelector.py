

def getName(num):
    if(num==0):
        return "Nothing"
    elif(num==1):
        return "LeftSwitchSide"
    elif(num==2):
        return "RightSwitchSide"
    elif(num==3):
        return "LeftSwitchMiddle"
    elif(num==4):
        return "RightSwitchMiddle"
    elif(num==5):
        return "DriveStraight"
    else:
        return "Nothing"


def getNum(name):
    for i in range(0,100):
        if(getName(i)==name): return i
        

def calcNum(auto, gameData):
    if(auto=="Left"):
        if(gameData[0]=='L'): return getNum("LeftSwitchSide")
        else: return getNum("DriveStraight")
    elif(auto=="Middle"):
        if(gameData[0]=='L'): return getNum("LeftSwitchMiddle")
        else: return getNum("RightSwitchMiddle")
    elif(auto=="Right"):
        if(gameData[1]=='L'): return getNum("DriveStraight")
        else: return getNum("RightSwitchSide")
    else:
        return getNum("Nothing")

    return num
