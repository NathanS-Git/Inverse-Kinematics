import pygame as pg
import numpy as np

pg.init()
screen_width = 1600
screen_height = 900
screen = pg.display.set_mode((screen_width, screen_height))

#joint_pos = [(800,450),(800,550),(800,650),(800,750),(800,850)] # Initial joint positions
joint_pos = [(800,450),(800,550),(800,600)]

tol = 1 # Tolerance (How far the target must move before we recalculate the kinematics)


def get_distance(point_1, point_2):
    ''' Return euclidean distance between two points in 2D space'''
    return np.sqrt(np.power(point_1[0]-point_2[0],2)+np.power(point_1[1]-point_2[1],2))


while True:
    
    distance = [get_distance(p1,p2) for (p1,p2) in zip(joint_pos,joint_pos[1:])] # Get distances between joints
    
    screen.fill((0,0,0))
    for e in pg.event.get():
        target = pg.mouse.get_pos()
    
    dist = get_distance(target,joint_pos[0])

    if dist > sum(distance):
        # Target is unreachable (too far)
        for i in range(len(joint_pos)-1):
            r = get_distance(joint_pos[i],target)
            y = distance[i-1]/r
            joint_pos[i+1] = ((1-y)*joint_pos[i][0]+y*target[0],(1-y)*joint_pos[i][1]+y*target[1])
    else:
        # Target is reachable
        itr = 0
        b = joint_pos[0]
        diff_a = get_distance(joint_pos[-1],target)
        while diff_a > tol:
            itr += 1
            if itr > 1000:
                print("Failed to reach target.")
                break

            joint_pos[-1] = target

            for i in reversed(range(len(joint_pos)-1)):
                r = get_distance(joint_pos[i+1],joint_pos[i])
                y = distance[i]/r
                joint_pos[i] = ((1-y)*joint_pos[i+1][0]+y*joint_pos[i][0],(1-y)*joint_pos[i+1][1]+y*joint_pos[i][1])
            
            joint_pos[0] = b
            
            for i in range(len(joint_pos)-1):
                r = get_distance(joint_pos[i+1],joint_pos[i])
                y = distance[i]/r
                joint_pos[i+1] = ((1-y)*joint_pos[i][0]+y*joint_pos[i+1][0],(1-y)*joint_pos[i][1]+y*joint_pos[i+1][1])
            
            diff_a = get_distance(joint_pos[-1],target)

    for i in range(len(joint_pos)-1): # Draw arms
        pg.draw.line(screen, (255,255,255), joint_pos[i], joint_pos[i+1])
 
    pg.display.update()
quit()