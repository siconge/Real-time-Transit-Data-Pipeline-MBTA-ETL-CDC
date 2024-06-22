# Embed docker commands in Python and automate the creation, deletion, and database initialization of Docker containers by executing Python through shell commands

import os
import sys

from utils.constants import MBTA_CONTAINER_NETWORK, MBTA_MYSQL_IMAGE, MBTA_MYSQL_CONTAINER, MBTA_MONGO_CONTAINER, DATABASE_PASSWORD

# ---------------
# input arguments
# ---------------
# -network, create Docker network
# -image, build Docker image
# -remove, remove containers
# -create, create containers

# Create Docker network
def create_network(network_name):
    cmd = f'docker network create {network_name}'
    result = os.system(cmd)
    if (result == 0):
        print(f'Docker network {network_name} created')

# Build Docker image
def build_image(image_name):
    cmd = f'docker build --tag {image_name} .'
    result = os.system(cmd)
    if (result == 0):
        print(f'Docker image {image_name} built')

# Remove containers
def remove_containers(container_name):
    cmd = f'docker stop {container_name}'
    result = os.system(cmd)
    if (result == 0):
        cmd = f'docker rm {container_name}'
        result = os.system(cmd)
        print(f'{container_name} removed')

# Create containers
def create_containers(cmd, container_name):
    result = os.system(cmd)
    if (result == 0):
        print(f'{container_name} created')

# Read input argument
argument = len(sys.argv)
if (argument > 1):
    argument = sys.argv[1]

# Create Docker network if -network input argument
if (argument == '-network'):
    create_network(MBTA_CONTAINER_NETWORK)
    sys.exit()

# Build Docker image if -image input argument
if (argument == '-image'):
    build_image(MBTA_MYSQL_IMAGE)
    sys.exit()

# Remove containers if -remove input argument
if (argument == '-remove'):
    remove_containers(MBTA_MYSQL_CONTAINER)
    remove_containers(MBTA_MONGO_CONTAINER)
    sys.exit()

# Create containers if -create input argument
if (argument == '-create'):
    create_containers(f'docker run -p 3306:3306 --name {MBTA_MYSQL_CONTAINER} -e MYSQL_ROOT_PASSWORD={DATABASE_PASSWORD} --network {MBTA_CONTAINER_NETWORK} -d {MBTA_MYSQL_IMAGE}', MBTA_MYSQL_CONTAINER)
    create_containers(f'docker run -p 27017:27017 --name {MBTA_MONGO_CONTAINER} --network {MBTA_CONTAINER_NETWORK} -d mongo', MBTA_MONGO_CONTAINER)
    sys.exit()