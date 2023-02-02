from pygame import Vector2
import math

def distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx * dx + dy * dy)

def normalize(vector):
    invLen = 1 / math.sqrt(vector.x * vector.x + vector.y * vector.y)
    return Vector2(vector.x * invLen, vector.y * invLen)

def findArithmeticMean(vertices):
    sumX = 0
    sumY = 0

    for v in vertices:
        sumX = v.x
        sumY = v.y
    
    return Vector2(sumX/len(vertices), sumY/len(vertices))