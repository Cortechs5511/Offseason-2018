def calcNum(gameData, auto):
    if(auto=="L"):
        if(gameData[0]=='L'): return "LeftSwitchSide"
        else: return "DriveStraight"
    elif(auto=="M"):
        if(gameData[0]=='L'): return "LeftSwitchMiddle"
        else: return "RightSwitchMiddle"
    elif(auto=="R"):
        if(gameData[0]=='L'): return "DriveStraight"
        else: return "RightSwitchSide"
    else:
        return "Nothing"
    return "Nothing"
