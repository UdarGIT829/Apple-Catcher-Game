#Apple class
import os, sys, math, pygame, pygame.mixer, random
from pygame.locals import *
import euclid

black = 0, 0, 0
eraser = 0, 0, 0, 255

class MyApple:
    def __init__(self, position, location, size, dtime, uid, color = (255,255,255),color2 = (255,255,255), velocity = euclid.Vector2(0,0), width = 0):
        self.uid = uid
        self.position = position
        self.size = size
        self.skinColor = color
        self.stemColor = color2
        self.width = width
        self.velocity = velocity
        self.dtime = dtime
        self.location = (int(self.position.x),int(self.position.y))

    def display(self, screen):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.skinColor, (rx-(self.size//3), ry), self.size, self.width)
        pygame.draw.circle(screen, self.skinColor, (rx+(self.size//3), ry), self.size, self.width)
        stemRect = ((rx-(9)),(ry-(self.size+5)),10,10)
        pygame.draw.arc(screen, self.stemColor, stemRect, (0.0),(math.pi/3), 5)
        #Bounding box for clicks
        #pygame.draw.circle(screen, black, (rx,ry),((int)(self.size + self.size//2)),1)

    def move(self):
        self.position += self.velocity * self.dtime
        self.location = (int(self.position.x),int(self.position.y))

    def would_catch(self,click_location):
        xDiff = abs(self.location[0] - click_location[0])
        yDiff = abs(self.location[1] - click_location[1])
        totalDistance = xDiff+yDiff
        if(totalDistance < (self.size*1.5)):
            return True
        print("miss by: ",totalDistance-self.size)
        return False

    def distance_to_point(self, given_point):
        xDiff = self.location[0] - given_point[0]
        yDiff = self.location[1] - given_point[1]
        totalDistance = xDiff+yDiff
        return totalDistance

class helpButton:
    def __init__(self, location, size, image_file, help_message, help_message_location, sec_help_message=None):
        self.location = location
        self.size = size
        self.image = image_file
        self.help_message = help_message
        self.help_message_location = help_message_location
        self.sec_help_message = sec_help_message

    def display(self,screen):
        screen.blit(self.image, self.location)

    def would_show(self, click_location):
        xDiff = abs(self.location[0] - click_location[0])
        yDiff = abs(self.location[1] - click_location[1])
        total_distance = xDiff+yDiff
        if(total_distance < (self.size*1.5)):
            return True
        return False

    def display_help(self,screen):
        screen.blit(self.help_message,self.help_message_location)
        
    def display_sec_help(self,screen):
        screen.blit(self.sec_help_message,self.help_message_location)