import numpy as np
import heapq
import collections


def getPosition(currentState,need):
    match need:
        case "player":
            posible_postitions = np.argwhere(currentState==2)
            return tuple(posible_postitions[0]) # Only one player
        case "walls":
            possible_positions = np.argwhere(currentState==1)
            return tuple(tuple(position) for position in possible_positions)
        case "bombs":
            possible_positions =  np.argwhere((currentState==4)| (currentState==5)) #includes box with bomb
            return tuple(tuple(position) for position in possible_positions)
        case "boxes":
            possible_positions =  np.argwhere((currentState==3)| (currentState==5)) #includes box with bomb
            return tuple(tuple(position) for position in possible_positions)
        case _:
            return (-1,-1)       # Invalid

def getHeuristic(boxPosition):
    "Sum of Manhatan distance between Boxes and Bombs which are yet to be Pushed"
    heuristic = 0

    Pushed_Boxes = set(boxPosition) & set(BOMB_POSITION)

    # Remove the already solved cases

    Unpushed_Boxes = list(set(boxPosition).difference(Pushed_Boxes))
    Unpushed_Bombs = list(set(BOMB_POSITION).difference(Pushed_Boxes))

    for i in range(len(Unpushed_Bombs)):
        heuristic += (abs(Unpushed_Bombs[i][0]-Unpushed_Boxes[i][0]) + abs(Unpushed_Boxes[i][1]-Unpushed_Bombs[i][1]))
    
    return heuristic

def isSolved(boxPosition):
    return len(set(boxPosition) & set(BOMB_POSITION))==len(BOMB_POSITION)

def getCost(moves):
    """ Return the number of non-Pushable moves"""

    # Non-Pushable moves can be represented in lower
    return len([x for x in moves if x.islower()])

def Explore(playerPosition,boxPosition):
    possibleStates = []
    # Direction Map
    directions = {
        (-1,0):["U","u"],
        (1,0):["D","d"],
        (0,1):["R","r"],
        (0,-1):["L","r"]
    }
    x,y = playerPosition[0],playerPosition[1]
    
    for direc,action in directions.items():

        new_x,new_y = x+direc[0],y+direc[1]
        
        # If it collides with box, then considered as push
        if (new_x,new_y) in boxPosition:
            _type = action[0]
        else:
            _type = action[1]   
        
        
        if _type.isupper():
            check_x,check_y = x + 2 * direc[0] , y + 2 * direc[1]
        else:
            check_x,check_y = x + direc[0],y+direc[1]
        
        
        if (check_x,check_y) not in boxPosition + WALL_POSITION:
            possibleStates.append((direc[0],direc[1],_type))
        else:
            continue

    return possibleStates  

def updateGame(playerPosition,boxPosition,state):

    updatedPlayerPostion = [playerPosition[0]+state[0],playerPosition[1]+state[1]]
    boxPosition = [list(x) for x in boxPosition]
    if state[-1].isupper():
        boxPosition.remove(updatedPlayerPostion)
        # print("posbox",boxPosition)
        boxPosition.append([playerPosition[0] + 2 * state[0], playerPosition[1] + 2 * state[1]])
        # print("check",boxPosition)
    boxPosition= tuple(tuple(x) for x in boxPosition)
    updatedPlayerPostion = tuple(updatedPlayerPostion)
    return updatedPlayerPostion,boxPosition

        
def A_STAR():
    iterations = 0
    OPENING_STATE = (INITIAL_PLAYER_POSITION,INIITAL_BOX_POSITION)
    Moves = []
    States = []
    visited = set()

    heapq.heappush(States , (getHeuristic(INIITAL_BOX_POSITION),[OPENING_STATE]))
    heapq.heappush(Moves, (getHeuristic(INIITAL_BOX_POSITION),[0]))
    while States:
        _,_state = heapq.heappop(States)
        _,_action = heapq.heappop(Moves)
        iterations+=1
        if isSolved(_state[-1][-1]):
            print(f"\nTotal iterations: {iterations}")
            print(f"The path:         {':'.join(_action[1:])}\n")
            break
        if _state[-1] not in visited:
            visited.add(_state[-1])   
            cost = getCost(_action[1:])

            for state in Explore(_state[-1][0],_state[-1][-1]):
                updatedPlayer,updatedBox = updateGame(_state[-1][0],_state[-1][-1],state)
                heuristic = getHeuristic(updatedBox)

                heapq.heappush(States,(heuristic+cost,_state+[(updatedPlayer,updatedBox)]))
                heapq.heappush(Moves,(heuristic+cost,_action+[state[-1]]))

def BFS():
    iterations = 0
    OPENING_STATE = (INITIAL_PLAYER_POSITION,INIITAL_BOX_POSITION)
    States = collections.deque([[OPENING_STATE]])
    Moves = collections.deque([[0]])
    visited = set() 

    while States:
        _state = States.popleft()
        _action = Moves.popleft()  
        iterations+=1
        if isSolved(_state[-1][-1]):
            print(f"\nTotal iterations: {iterations}")
            print(f"The path:         {':'.join(_action[1:])}\n")
            break
        if _state[-1] not in visited:
            visited.add(_state[-1])
            
            for state in Explore(_state[-1][0],_state[-1][-1]):
                updatedPlayer,updatedBox = updateGame(_state[-1][0],_state[-1][-1],state)
                States.append(_state+[(updatedPlayer,updatedBox)])
                Moves.append(_action+[state[-1]])

def DFS():
    iterations = 0
    OPENING_STATE = (INITIAL_PLAYER_POSITION,INIITAL_BOX_POSITION)
    States = collections.deque([[OPENING_STATE]])
    Moves = [[0]]
    visited = set() 

    while States:
        _state = States.pop()
        _action = Moves.pop()
        iterations+=1
        if isSolved(_state[-1][-1]):
            print(f"\nTotal iterations: {iterations}")
            print(f"The path:         {':'.join(_action[1:])}\n")
            break
        if _state[-1] not in visited:
            visited.add(_state[-1])
            
            for state in Explore(_state[-1][0],_state[-1][-1]):
                updatedPlayer,updatedBox = updateGame(_state[-1][0],_state[-1][-1],state)
                States.append(_state+[(updatedPlayer,updatedBox)])
                Moves.append(_action+[state[-1]])
        

if __name__=="__main__":

    with open('stage.txt','r') as f:
        INITIAL_STATE = f.readlines()
    
    for i in range(len(INITIAL_STATE)):
        INITIAL_STATE[i] = INITIAL_STATE[i].strip("\n")
        INITIAL_STATE[i] = [int(value) for value in INITIAL_STATE[i]]
    
    """
    0 - Represents the empty Space,
    1 - Represents the Blocking Wall,
    2 - Represents the Player,
    3 - Represents the Box,
    4 - Represents the Bomb,
    5 - Represents the Box with Bomb
    """

    INITIAL_STATE = np.array(INITIAL_STATE)

    INIITAL_BOX_POSITION = getPosition(INITIAL_STATE,need="boxes")
    INITIAL_PLAYER_POSITION = getPosition(INITIAL_STATE,need="player")

    WALL_POSITION = getPosition(INITIAL_STATE,need="walls")
    BOMB_POSITION = getPosition(INITIAL_STATE,need="bombs")
    