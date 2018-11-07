import math
import copy
import numpy as np
import pygame
import sys
from pygame.locals import *

pygame.init()

scale = 3
num_nodes = 700
node_distance = 10 * scale
node_color = (255, 255, 255)


def s5(n, r):  # works better for first direction
    spirals = []
    golden_ratio = (1 + 5 ** 0.5) / 2.0
    for i in range(n + 1):
        # "** 1.2 * 0.5" gives the outer nodes more space, so we can scale them bigger.
        spirals.append((r * (i ** 0.5) ** 1.2 * 0.5, ((i * (360) / golden_ratio) % 360)))
    return spirals


# convert to cartesian to plot
def pol2cart(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


# do the cartesian conversion
coordinates = [pol2cart(r, t) for r, t in s5(num_nodes, node_distance)]

# center for the canvas
display = pygame.display.set_mode((800, 800))
display.fill((0, 0, 0))
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


# Calculate desired surface size, by taking node_distance from 0,0 to center of outermost node, then doubling that for the whole thing, and padding by factor 1.1 to include the outermost nodes and some border.
nodes = np.asarray(coordinates)
dist_2 = np.sum(coordinates, axis=1)
desired_size = int(1.1 * 2 * calculateDistance((0, 0), nodes[np.argmin(dist_2)]))

surface = pygame.Surface((desired_size, desired_size)).convert()
surface_size = surface.get_size()

# plot points
for x, y in coordinates:
    distance_to_closest_node = closest_node_distance((x, y), coordinates)
    # print "distance_to_closest_node: " + str(distance_to_closest_node)

    size = int(max(1, (distance_to_closest_node - 1) / 2.0))

    pygame.draw.circle(surface, node_color, (int(round(x + surface_size[0] / 2)), int(round(y + surface_size[1] / 2))),
                       size)

print "surface_size: " + str(surface.get_size())
scaled_surface = pygame.transform.smoothscale(surface, display_size, display)
print "scaled_surface_size: " + str(scaled_surface.get_size())
pygame.display.flip()

pygame.image.save(surface, "output.png")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
