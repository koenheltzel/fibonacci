import math

import pygame, sys, os
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
screen.fill((0, 0, 0))

# player = pygame.image.load(os.path.join("test.png"))
# player.convert()

scale = 2


def s5(n, r):  # works better for first direction
    spirals = []
    golden_ratio = (1 + 5 ** 0.5) / 2.0
    for i in range(n + 1):
        spirals.append((r * (i ** 0.5) ** 1.2 * 0.5, ((i * (360) / golden_ratio) % 360)))
    return spirals


# convert to cartesian to plot
def pol2cart(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


# set size of fib sun
num_points = 1000
distance = 10 * scale

# do the cartesian conversion
coordinates = [pol2cart(r, t) for r, t in s5(num_points, distance)]

# center for the canvas
display_size = pygame.display.get_surface().get_size()


# coordinates = [(x+display_size[0]/2,y+display_size[1]/2) for x,y in coordinates]

# create gui
# master = Tk()
# canvas = Canvas(master,width = 500,height=500)
# canvas.pack()

def calculateDistance(point1, point2):
    dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return dist

def closest_node_distance(node, nodes):
    pt = []
    dist = 9999999
    for n in nodes:
        if node <> n and calculateDistance(node, n) <= dist:
            dist = calculateDistance(node, n)
            pt = n
    return calculateDistance(node, pt)

# plot points
h = 1
for x, y in coordinates:
    # print (x, y)
    # power = 1.20
    # old_x = x
    # old_y = y
    # # x *= power
    # # y *= power
    # if x > 0:
    #     x **= power
    # else:
    #     x = -(abs(x) ** power)
    #
    # if y > 0:
    #     y **= power
    # else:
    #     y = -(abs(y) ** power)
    #
    # x *= 0.5
    # y *= 0.5
    # print (x, y)
    # if x != 0 and y != 0:
    #     print "x factor: " + str(x / old_x) + "  y factor: " + str(y / old_y)
    # print ""

    distance_to_closest_node = closest_node_distance((x, y), coordinates)
    # print "distance_to_closest_node: " + str(distance_to_closest_node)

    distance = calculateDistance((0, 0), (x, y))
    size = int(max(1, (distance_to_closest_node - 2) / 2.0) * scale)

    # size = 6

    pygame.draw.circle(screen, (20, 20, 20), (int(round(x + display_size[0] / 2)), int(round(y + display_size[1] / 2))),
                       size)
    # canvas.create_oval(x+7,y+7,x-7,y-7)
    # canvas.create_text(x,y,text=h)
    h += 1

pygame.display.flip()
# mainloop()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
