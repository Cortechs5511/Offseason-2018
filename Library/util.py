kEpsilon = 1e-12

#limits the given input to the given magnitude
def limit(v, maxMag):
    if(v>maxMag): v=maxMag
    if(v<-maxMag): v=-maxMag
    return v

def limit(v, min, max):
    if(v<min): v=min
    if(v>max): v=max
    return v

def interpolate(a, b, x):
    x = limit(x, 0, 1)
    return a + (b-a) * x

def epsilonEquals(a, b, epsilon = kEpsilon):
    return (a-epsilon<= b) and (a+epsilon >=b)

def sign(x):
    if(epsilonEquals(x,0)): return 0
    if(x>0): return 1
    else: return -1
