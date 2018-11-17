import math
import copy
import numpy as np
import pygame
import sys
from pygame.locals import *
import os
import shutil
import time

# import pygame.gfxdraw

pygame.init()

scale = 3
num_nodes = 2000
node_distance = 12 * scale
node_color = (255, 255, 255)
power_factor = 1.5
power_multiplier = 0.25
space_between_nodes = 4
minimum_node_size = 2
animation = True
save_animation = True
source_image = "freddie3.png"
destination_directory = "freddie3z"
animation_fade_duration = 25

if save_animation:
    if os.path.isdir(destination_directory):
        shutil.rmtree(destination_directory)
        time.sleep(0.2)
    os.mkdir(destination_directory)


def s5(n, r):  # works better for first direction
    spirals = []
    golden_ratio = (1 + 5 ** 0.5) / 2.0
    for i in range(n + 1):
        # "** 1.2 * 0.5" gives the outer nodes more space, so we can scale them bigger.
        spirals.append((r * (i ** 0.5) ** power_factor * power_multiplier, ((i * (360) / golden_ratio) % 360)))
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


def pygame_tick():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def draw_display(surface, aliased=False):
    # print "surface_size: " + str(surface.get_size())
    if aliased:
        scaled_surface = pygame.transform.smoothscale(surface, display_size, display)
    else:
        scaled_surface = pygame.transform.scale(surface, display_size, display)
    # print "scaled_surface_size: " + str(scaled_surface.get_size())
    pygame.display.flip()

def scale_color_to_white(color, scale=0):
    """
    Scales the color to white. 0 is the original color, 1 is completely white. Returns the input color as a (R, G, B) tuple..
    """
    color = list(color)
    for i in range(0, len(color)):
        distance_to_white = 255 - color[i]
        color[i] = max(0, min(255, int(color[i] + scale * distance_to_white)))
    return tuple(color)


# Calculate desired surface size, by taking node_distance from 0,0 to center of outermost node, then doubling that for the whole thing, and padding by factor 1.1 to include the outermost nodes and some border.
nodes = np.asarray(coordinates)
dist_2 = np.sum(coordinates, axis=1)
desired_size = int(1.1 * 2 * calculateDistance((0, 0), nodes[np.argmin(dist_2)]))

surface = pygame.Surface((desired_size, desired_size)).convert()
surface_size = surface.get_size()

if source_image:
    image = pygame.image.load(source_image)

def draw_point(index, scale_to_white = 0):
    (x, y) = coordinates[index]

    distance_to_closest_node = closest_node_distance((x, y), coordinates)
    # print "distance_to_closest_node: " + str(distance_to_closest_node)

    size = int(max(minimum_node_size * scale, (distance_to_closest_node - space_between_nodes * scale) / 2.0))
    # print "distance_to_closest_node: " + str(distance_to_closest_node) + " size: " + str(size)

    target_x = int(round(x + surface_size[0] / 2))
    target_y = int(round(y + surface_size[1] / 2))

    if source_image:
        average_area = 50
        node_color = pygame.transform.average_color(image, (target_x - (average_area / 2), target_y - (average_area / 2), average_area, average_area))
        # node_color = image.get_at((target_x, target_y))
        node_color = scale_color_to_white(node_color, scale_to_white)

    pygame.draw.circle(surface, node_color, (target_x, target_y), size)
    # pygame.gfxdraw.aacircle(surface, target_x, target_y, size, node_color)
    # pygame.gfxdraw.filled_circle(surface, target_x, target_y, size, node_color)

# plot points
for index in range(0, len(coordinates) + animation_fade_duration - 1):
    pygame_tick() # Prevent hangup by pygame event overflow

    for tmp_index in range(max(0, index - animation_fade_duration), index):
        pygame_tick() # Prevent hangup by pygame event overflow
        if tmp_index < len(coordinates):
            scale_to_white = 1.0 - (index - tmp_index) / float(animation_fade_duration)
            draw_point(tmp_index, scale_to_white)

    draw_display(surface)

    if save_animation:
        pygame.image.save(surface, "%s\output%04d.jpg" % (destination_directory, index))

    index += 1

if not animation:
    pygame.image.save(surface, "output.png")

draw_display(surface, False)

while True:
    pygame_tick()
