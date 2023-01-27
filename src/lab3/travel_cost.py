'''
Lab 3: Travel Cost

Your player will need to move from one city to another in order to complete the game.
The player will have to spend money to travel between cities. The cost of travel depends 
on the difficulty of the terrain.
In this lab, you will write a function that calculates the cost of a route between two cities,
A terrain is generated for you 
'''
import numpy as np
import networkx as nx

#Python3 program for Bresenhams Line Generation
#Code found on https://www.geeksforgeeks.org/bresenhams-line-generation-algorithm/
#Contributed by akashish__, modified by me on lines 28-31
def plotPixel(x1, y1, x2, y2, dx, dy, decide):
   
  # pk is initial decision making parameter
  # Note:x1&y1,x2&y2, dx&dy values are interchanged
  # and passed in plotPixel function so
  # it can handle both cases when m>1 & m<1
  pk = 2 * dy - dx
  
  pathList = []
   
  # for (int i = 0; i <= dx; i++) {
  for i in range(0,dx+1):
    if (decide == 0):
      pathList.append((x1, y1))
    else:
      pathList.append((y1, x1))
     
    # checking either to decrement or increment the
    # value if we have to plot from (0,100) to (100,0)
    if(x1<x2):
      x1 = x1 + 1
    else:
      x1 = x1 - 1
    if (pk < 0):
       
      # decision value will decide to plot
      # either  x1 or y1 in x's position
      if (decide == 0):
         
        # putpixel(x1, y1, RED);
        pk = pk + 2 * dy
      else:
         
        #(y1,x1) is passed in xt
        # putpixel(y1, x1, YELLOW);
        pk = pk + 2 * dy
    else:
      if(y1<y2):
        y1 = y1 + 1
      else:
        y1 = y1 - 1
         
      # if (decide == 0):
      #   # putpixel(x1, y1, RED)
      # else:
      #   #  putpixel(y1, x1, YELLOW);
      pk = pk + 2 * dy - 2 * dx
      
  return pathList

def get_route_cost(route_coordinate, game_map):
    """
    This function takes in a route_coordinate as a tuple of coordinates of cities to connect, 
    example:  and a game_map as a numpy array of floats,
    remember from previous lab the routes looked like this: [(A, B), (A, C)]
    route_coordinates is just inserts the coordinates of the cities into a route like (A, C).
    route_coordinate might look like this: ((0, 0), (5, 4))

    For each route this finds the cells that lie on the line between the
    two cities at the end points of a route, and then sums the cost of those cells
      -------------
    1 | A |   |   |
      |-----------|
    2 |   |   |   |
      |-----------|
    3 |   | C |   |
      -------------
        I   J   K 

    Cost between cities A and C is the sum of the costs of the cells 
        I1, I2, J2 and J3.
    Alternatively you could use a direct path from A to C that uses diagonal movement, like
        I1, J2, J3

    :param route_coordinates: a list of tuples of coordinates of cities to connect
    :param game_map: a numpy array of floats representing the cost of each cell

    :return: a floating point number representing the cost of the route
    """
    # Build a path from start to end that looks like [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4)]
    
    x1 = route_coordinate[0][0]
    y1 = route_coordinate[0][1]
    x2 = route_coordinate[1][0]
    y2 = route_coordinate[1][1]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    if (dx > dy):
      # passing argument as 0 to plot(x,y)
      path = plotPixel(x1, y1, x2, y2, dx, dy, 0)
 
    # if slope is greater than or equal to 1
    else:
      # passing argument as 1 to plot (y,x)
      path = plotPixel(y1, x1, y2, x2, dy, dx, 1)

    return game_map[tuple(zip(*path))].sum()


def route_to_coordinates(city_locations, city_names, routes):
    """ get coordinates of each of the routes from cities and city_names"""
    route_coordinates = []
    for route in routes:
        start = city_names.index(route[0])
        end = city_names.index(route[1])
        route_coordinates.append((city_locations[start], city_locations[end]))
    return route_coordinates


def generate_terrain(map_size):
    """ generate a terrain map of size map_size """
    return np.random.rand(*map_size)


def main():
    # Ignore the following 4 lines. This is bad practice, but it's just to make the code work in the lab.
    import sys
    from pathlib import Path
    sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
    from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta', 
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    map_size = 300, 200

    n_cities = len(city_names)
    game_map = generate_terrain(map_size)
    print(f'Map size: {game_map.shape}')

    city_locations = get_randomly_spread_cities(map_size, n_cities)

    routes = get_routes(city_names)
    np.random.shuffle(routes)
    routes = routes[:10]
    route_coordinates = route_to_coordinates(city_locations, city_names, routes)

    for route, route_coordinate in zip(routes, route_coordinates):
        print(f'Cost between {route[0]} and {route[1]}: {get_route_cost(route_coordinate, game_map)}')


if __name__ == '__main__':
    main()