import math, random

def generateName() : 
    digits = "0123456789"
    Name = "" 
    for _ in range(6) : 
        Name += digits[math.floor(random.random() * 10)] 
    return str(Name+".mp4")