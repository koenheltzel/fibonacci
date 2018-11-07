import math
import copy
import numpy as np
import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
screen.fill((0, 0, 0))

# player = pygame.image.load(os.path.join("test.png"))
# player.convert()

scale = 1


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
num_points = 700
distance = 10 * scale

# do the cartesian conversion
coordinates = [pol2cart(r, t) for r, t in s5(num_points, distance)]

# center for the canvas
display_size = pygame.display.get_surface().get_size()


def calculateDistance(point1, point2):
    dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return dist


def closest_node_distance(node, nodes):
    nodes = copy.copy(nodes)
    nodes.remove(node)
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node) ** 2, axis=1)
    return calculateDistance(node, nodes[np.argmin(dist_2)])


# plot points
for x, y in coordinates:
    distance_to_closest_node = closest_node_distance((x, y), coordinates)
    print "distance_to_closest_node: " + str(distance_to_closest_node)

    distance = calculateDistance((0, 0), (x, y))
    size = int(max(1, (distance_to_closest_node - 1) / 2.0))

    pygame.draw.circle(screen, (20, 20, 20), (int(round(x + display_size[0] / 2)), int(round(y + display_size[1] / 2))),
                       size)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
