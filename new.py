# -*- coding: utf-8 -*-
# Author: 1410088 - NDA
# 1. Input level from 1 to 33
# 2. Input 1: DFS, 2: BFS, 3: Hill Climbing
# 3. Output: Steps to go X destination: 1 Up, -1 Down, 2 Right, -2 Left, 5 Space


# DFS, BFS in in little good include Teleport case.
# Hill Clibming is under solving. But Soon .Wait the next commit
#
import copy
from copy import deepcopy

# 1: Unbreakable Tile
# 0: Space
# 2: Breakable Tile 
# X: Destination
# LS,i,j....: Light Switch of Bridge [i][j]
# HS,i,j: Height Switch of Bridge [i][j]
# RB0; RB1: Reversable Bridge
# UB: Unreversable Bridge
# T,i1,j1,i2,j2: Teleport to positon [i1][j1], [i2][j2]


maps = []
moves = []
passed = []
bestMoves = []
part = -1
tele = ()
maps.append([['0','0','0','0','0','0','1','1','1','0'],
             ['0','0','0','0','0','1','1','X','1','1'],
             ['0','1','1','1','1','1','1','1','1','1'],
             ['1','1','1','1','1','1','1','1','1','0'],
             ['1','1','1','1','1','1','0','0','0','0'],
             ['1','1','1','0','0','0','0','0','0','0']])

maps.append([['1','1','1','1','0','0','1','1','1','1','0','0','0','0','0'],
             ['1','1','1','1','RB0','RB0','1','1','1','1','RB0','RB0','1','1','1'],
             ['1','1','1','1','0','0','1','1','1','1','0','0','1','1','1'],
             ['1','1','LS,1,4,1,5','1','0','0','1','1','1','1','0','0','1','1','1'],
             ['1','1','1','1','0','0','1','1','HS,1,10,1,11','1','0','0','1','X','1'],
             ['0','0','0','0','0','0','1','1','1','1','0','0','1','1','1']])
maps.append([['0','0','0','0','0','0','0','0','0','0','0','0','1','1','1'],
             ['1','1','1','1','0','0','0','0','0','0','0','1','1','1','1'],
             ['1','1','1','1','0','0','0','0','0','0','0','1','1','X','1'],
             ['1','1','1','1','1','1','1','1','1','0','0','1','1','1','1'],
             ['1','1','1','1','0','0','1','1','1','0','0','1','1','0','0'],
             ['0','0','0','0','0','0','1','1','1','1','1','1','1','0','0']])
maps.append([['1','0','1','1'],
             ['LS,3,1','0','1','1'],
             ['1','0','1','1'],

             ['T,2,0,3,2','RB0','1','X']])
#'LS,1,4,1,5'
#HS,1,11,1,12

start = []

start.append(((4,1,0),(4,1,1)))
start.append(((1,1,0),(1,1,1)))
start.append(((2,1,0),(2,1,1)))
start.append(((0,0,0),(0,0,1)))
         

class Node:
    def __init__(self,key = 1,cur =  None, parIdx = 1, thismap = [], thispassed = [], thispart = -1):
        self.key = key
        self.parIdx = parIdx
        self.cur = cur
        self.map = thismap
        self.passed = thispassed
        self.part = thispart
class PNode:
    def __init__(self, cur = None, thispart = -1):
        self.cur = cur
        self.part = thispart

def callEvent(cur = ((0,0,0),(0,0,0))) :
    global mapi
    global part
    print (mapi)
    
    if cur[0] == cur[1]:
        print('2 in 1')
        return -1
    elif cur[0][0] < 0 or cur[0][0] > len(mapi) - 1 or cur[0][1] < 0 or cur[0][1] > len(mapi[0]) - 1 or cur[1][0] < 0 or cur[1][0] > len(mapi) - 1 or cur[1][1] < 0 or cur[1][1] > len(mapi[0]) - 1:
        #print("out of range")
        return -1
    elif mapi[cur[0][0]][cur[0][1]] == '0' or mapi[cur[1][0]][cur[1][1]] == '0' :
        #print("Rot")
        return -1
    elif mapi[cur[0][0]][cur[0][1]] == 'RB0' or mapi[cur[1][0]][cur[1][1]] == 'RB0' or mapi[cur[0][0]][cur[0][1]] == 'UB' or mapi[cur[1][0]][cur[1][1]] == 'UB':
        #print("Next Bridge")
        return -1
    elif mapi[cur[0][0]][cur[0][1]] == 'X' and cur[1][2] == 1:
        #print("Win")
        return 1
    elif mapi[cur[0][0]][cur[0][1]][0] == 'L' :
        #print("Light Bridge")

        inf = mapi[cur[0][0]][cur[0][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
    elif mapi[cur[1][0]][cur[1][1]][0] == 'L':
        #print("Light Bridge")
        inf = mapi[cur[1][0]][cur[1][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
    elif mapi[cur[0][0]][cur[0][1]][0] == 'H' and cur[1][2] == 1:
        #print("Height Bridge")
        inf = mapi[cur[0][0]][cur[0][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
    elif mapi[cur[0][0]][cur[0][1]][0] == 'T' and cur[1][2] == 1:
        print("Teleport")
        inf = mapi[cur[0][0]][cur[0][1]].split(',')
        teleport(int(inf[1]), int(inf[2]), int(inf[3]), int(inf[4]))
        return 3
    elif mapi[cur[0][0]][cur[0][1]] == '2' and cur[1][2] == 1:
        #print("Soft Tile")
        return -1

def isPassed(cur = None):
    global passed
    for ii in passed:
        if ii == cur:
            return 1
    return 0
def isBlock(cur = ()):
    if abs((cur[0][0]) - (cur[1][0])) == 1 and abs((cur[0][1] - cur[1][1]) == 0) or abs((cur[0][1] - cur[1][1])) == 1 and abs((cur[0][0] - cur[1][0]))==0 :
        return 1
def reversePart(part = 0):
    if part == 0:
        return 1
    elif part == 1:
        return 0
def dfs(cur = ((0,0,0),(0,0,0)), part = -1):
    global bestMoves
    global moves
    global passed
    print cur
    global tele
    if isPassed(cur) == 1:
       
        return -1
    if part > -1 and isBlock(cur) == 1:
        part = -1
        if (cur [0][2] - cur[1][2] == 1 or cur [0][0] - cur[1][0] == 1 or cur [0][1] - cur[1][1] == 1):
           cur = swap(cur)
    
    
    
        
    
    #print('append()', cur)
    flag = callEvent(cur)
    if flag == -1:
        return flag
    elif flag == 3:
        passed.append(cur)
        dfs(tele, 0)
        passed.pop()
    elif flag == 1:
        if len(bestMoves) == 0 or len(moves) < len(bestMoves) :
            bestMoves = list(moves)
        return 1
    elif part == -1:
        if len(bestMoves) != 0 and len(moves) >= len(bestMoves) :
            unCallEvent(cur)
            return -1;
        passed.append(cur)
        
        for i in range(1,3):
            
            
            moves.append(i)
            print('append -1', move(i,cur))
            
            dfs(move(i, cur))
           
            moves.pop()
            
            moves.append(-1*i)
            print('append - 1', move(-1*i, cur))

            dfs(move(-1*i, cur))
            
            moves.pop()
        passed.pop()
        
    elif part > -1:
        
        if len(bestMoves) != 0 and len(moves) >= len(bestMoves) :
            unCallEvent(cur)
            return -1;
        passed.append(cur)
        for i in range(1,3):
            #print (i)
            print('append', i, move(i,cur, part))
            moves.append(i)
            dfs(move(i, cur, part), part)
            moves.pop()
            #print(-1*i)
            moves.append(-1*i)
            print('append', -1*i,move(i,cur, part))
            dfs(move(-1*i, cur, part), part)
            moves.pop()
        #print(5)
        moves.append(5)
        dfs(cur, reversePart(part))
        moves.pop()
        passed.pop()
    #print('passed.pop()')    
    unCallEvent(cur)



def isEmptyBridge() :
    for i in mapi:
        for j in i:
            if j == 'RB0' or j == 'UB':
                return 1
    return 0

def bfs(cur = ((0,0,0),(0,0,0))):
    global part
    global bestMoves
    global mapi
    global passed
    global tele
    passed = []
    i = -1
      
    q = []
    q.append(Node(0, cur, -1, copy.deepcopy(mapi), copy.deepcopy(passed)))
    while i < len(q) - 1 :
        i+=1
        curNode = q[i]
        cur = curNode.cur
        passed = copy.deepcopy(curNode.passed)
        mapi = copy.deepcopy(curNode.map)
        part = curNode.part
        curPNode = PNode(cur, part)
        #print('cur = ',cur)
        #print('before map',mapi)
        
        if part > -1 and isBlock(cur) == 1:
            part = -1
            if (cur [0][2] - cur[1][2] == 1 or cur [0][0] - cur[1][0] == 1 or cur [0][1] - cur[1][1] == 1):
               cur = swap(cur)
        if isPassed(curPNode) == 1:
            
            #print('passed')
            continue
        passed.append(curPNode)
        
        flag = callEvent(cur)
        #print('after map', mapi)
        
        if flag == -1:
            
            continue
        elif flag == 3:
            passed.append(tele)
            q[i].cur = tele
            q[i].part = 0
            i = i - 1
            continue
        elif flag == 1:
            bestMoves.append(curNode.key)
            idx = curNode.parIdx
            while idx > 0 :
                bestMoves.append(q[idx].key)
                idx = q[idx].parIdx
                
            break
        elif part == -1:
            
            for ii in range(1,3):
                
                
                q.append(Node(ii,move(ii,cur), i, copy.deepcopy(mapi), copy.deepcopy(passed)))
                
                q.append(Node(-1*ii,move(-1*ii,cur), i,copy.deepcopy(mapi), copy.deepcopy(passed)))
               
        elif part > -1:
            passed.append(curPNode)
            for ii in range(1,3):
                
                
                q.append(Node(ii,move(ii,cur, part), i, copy.deepcopy(mapi), copy.deepcopy(passed), part))
                
                q.append(Node(-1*ii,move(-1*ii,cur, part), i,copy.deepcopy(mapi), copy.deepcopy(passed), part))
            q.append(Node(5, cur, i,copy.deepcopy(mapi), copy.deepcopy(passed), reversePart(part)))

    bestMoves.reverse()

def simpleHC(cur = ((0,0,0),(0,0,0))):
    s = []
    s.append(cur)
    cur = s.pop()
    while(len(s) != 0):
        
        
        flag = callEvent(cur)
        if flag == -1:
            return flag
        elif flag == 1:
            if len(bestMoves) > 0 and len(moves) < len(bestMoves) :
                bestMoves = list(moves)
            else:
                bestMove = moves
        elif part == -1:
            if len(moves) >= len(bestMoves):
                break
            for i in range(1,3):
                moves.append(i)
                s.append(move(i,cur))
                moves.pop()
                moves.append(-1*i)
                s.append(move(-1*i, cur))
                moves.pop()
        elif part > -1:
            if len(moves) >= len(bestMoves):
                break
            for i in range(1,3):
                moves.append(i)
                s.append(move(i,cur))
                moves.pop()
                moves.append(-1*i)
                s.append(move(-1*i, cur))
                moves.pop()
    
            if part == 0:
                part = 1
            elif part == 1:
                part = 0

            for i in range(1,3):
                moves.append(i)
                s.append(move(i,cur))
                moves.pop()
                moves.append(-1*i)
                s.append(move(-1*i, cur))
                moves.pop()
        cur = s.pop()
        unCallEvent(cur)
                
                

def swap(cur = ((0,0,0),(0,0,0))):
    cur = (cur[1], cur[0])
    return cur
    


def move(key = 1, cur = ((0,0,0),(0,0,0)), part = -1):
    nex = [[0,0,0],[0,0,0]]
    if part != -1:
        if key == 1 or key == -1:
            nex[part][0] = key
        elif key == 2 or key == -2:
            nex[part][1] = key/2
    elif cur[1][2] == 1:
        #print("cur[1][2] == 1")
        nex[1][2] = -1
        if key == 1 or key == -1:
            nex[0][0] = key
            #print(nex[0][0])
            nex[1][0] = 2 * key
        else :
            nex[0][1] = 1 * (key/2)
            nex[1][1] = 2 * (key/2)
    elif cur[1][0] - cur[0][0] == 1:
        if key == 1:
            nex[0][0] = 2
            nex[1][0] = 1
            nex[0][2] = 1
        elif key == -1:
            nex[0][0] = -1
            nex[1][0] = -2
            nex[1][2] = 1 
        elif key == 2 or key == -2:
            nex[0][1] = key/2
            nex[1][1] = key/2
    elif cur[1][1] - cur[0][1] == 1:
        if key == 1 or key == -1:
            nex[0][0] = nex[1][0] = key
        elif key == 2:
            nex[0][1] = 2
            nex[1][1] = 1
            nex[0][2] = 1
        else:
            nex[0][1] = -1
            nex[1][1] = -2
            nex[1][2] = 1
        
        
    
    cur = ((cur[0][0] + nex[0][0], cur[0][1] + nex[0][1], cur[0][2] + nex[0][2]), (cur[1][0] + nex[1][0], cur[1][1] + nex[1][1], cur[1][2] + nex[1][2]))
    #print(cur)
   
          
    if part == -1 and (cur [0][2] - cur[1][2] == 1 or cur [0][0] - cur[1][0] == 1 or cur [0][1] - cur[1][1] == 1):
           cur = swap(cur)
    
    #print(cur)

    return cur
def switch(y = 0, x = 0) :
    global mapi
    if mapi[y][x] == 'UB':
         mapi[y][x] = '1'
        
    elif mapi[y][x] == 'RB0':
        mapi[y][x] = 'RB1'
    elif mapi[y][x] == 'RB1':
        mapi[y][x] = 'RB0'
    elif mapi[y][x] == '1':
        mapi[y][x] = 'UB'
    #print(y,x,mapi[y][x])
def teleport(y0 = 0, x0 = 0, y1 = 0, x1 = 0) :
    global tele
    global part
    tele = ((y0, x0, 0),(y1, x1, 0))
    print(tele)
    part = 0
    





def unCallEvent(cur = ((0,0,0),(0,0,0))):
    if mapi[cur[0][0]][cur[0][1]][0] == 'L':
        inf = mapi[cur[0][0]][cur[0][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
    elif mapi[cur[1][0]][cur[1][1]][0] == 'L':
        inf = mapi[cur[1][0]][cur[1][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
    elif mapi[cur[0][0]][cur[0][1]][0] == 'H' and cur[1][2] == 1:
        inf = mapi[cur[0][0]][cur[0][1]].split(',')
        for i in range(0,(len(inf)-1)/2):
            switch(int(inf[2*i+1]), int(inf[2*i+2]))
def printMoves():
    for i in bestMoves:
        print(i, '->')

level = input('Level = ')

mapi = copy.deepcopy(maps[level - 1])
algo = input('Algorithm: \n1. DFS\n2. BFS\n3. Hill Climbing\nAlgorithm = ')
if algo == 1:
    dfs(start[level - 1])
elif algo == 2:
    bfs(start[level - 1])
else:
    simpleHC(start[level - 1])
printMoves()


#['1','1','1','0','0','0','0','0','0','0']
#['1','1','1','1','1','1','0','0','0','0']
#['1','LS,1,2','1','1','1','1','1','1','1','0']
#['0','1','1','1','1','1','1','1','1','1']
#['2','0','0','0','0','1','1','X','1','1']
#['0','0','0','0','0','0','1','1','1','0']
             

#x = ((1,1,0),(1,2,0))
#print(move(-2, x))
#callEvent(x)

        

