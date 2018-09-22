def calcNum(auto, gameData):
    if(auto=="Left"):
        if(gameData[0]=='L'): "LeftSwitchSide"
        else: return "DriveStraight"
    elif(auto=="Middle"):
        if(gameData[0]=='L'): return "LeftSwitchMiddle"
        else: return "RightSwitchMiddle"
    elif(auto=="Right"):
        if(gameData[1]=='L'): return "DriveStraight"
        else: return "RightSwitchSide"
    else:
        return "Nothing"

    return num
