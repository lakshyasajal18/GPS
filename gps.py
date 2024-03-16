"""Create routes between cities on a map."""
import sys
import argparse

class City:
    """Represents a city on the map."""

    def __init__(self, name):
        """Initialize a city with its name and an empty list of neighbors."""
        self.name = name
        self.neighbors = {}

    def __repr__(self):
        """Return the name of the city when represented as a string."""
        return self.name

    def add_neighbor(self, neighbor, distance, interstate):
        """Add a neighboring city with the distance and interstate connecting them."""
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (distance, interstate)
            neighbor.add_neighbor(self, distance, interstate)


class Map:
    """Represents a map with cities and their connections."""

    def __init__(self, relationships):
        """Initialize the map with given relationships between cities."""
        self.cities = []
        # Iterate through the given relationships
        for city_name in relationships:
            # Check if the city is already added to the map
            if city_name not in [c.name for c in self.cities]:
                # If not, create a new city and add it to the map
                city = City(city_name)
                self.cities.append(city)
            # Get the index of the current city in the list
            city_index = [c.name for c in self.cities].index(city_name)
            # Iterate through neighbors of the current city
            for neighbor_name, distance, interstate in relationships[city_name]:
                # Check if the neighbor city is already added to the map
                if neighbor_name not in [c.name for c in self.cities]:
                    # If not, create a new city and add it to the map
                    neighbor_city = City(neighbor_name)
                    self.cities.append(neighbor_city)
                # Get the index of the neighbor city in the list
                neighbor_index = [n.name for n in self.cities].index(neighbor_name)
                # Add the neighbor to the current city
                self.cities[neighbor_index].add_neighbor(self.cities[city_index], distance, interstate)

    def __repr__(self):
        """Return a string representation of the map."""
        return str(self.cities)


def bfs(graph, start, goal):
    """Performs a breadth-first search to find the shortest path between two cities."""
    
    # List to track explored nodes
    explored = []
    # Initialize the queue with the starting node
    queue = [[start]]
    
    # If start and goal are the same, return start as a list
    if start == goal:
        return [start]

    # Continue searching 
    while queue:
        # Take the first path from the queue
        path = queue.pop(0)
        # Get the last node (city) in the path
        node = path[-1]

        # If the node has not been explored
        if node not in explored:
            # Get the index of cities in the graph
            index = [c.name for c in graph.cities]
            # Get the neighbors of the current node
            neighbors = graph.cities[index.index(str(node))].neighbors

            # Iterate through the neighbors of the current node
            for neighbor in neighbors:
                # Create a new path by appending the neighbor to the current path
                new_path = list(path)
                new_path.append(neighbor)
                # Add the new path to the queue
                queue.append(new_path)
                # If the neighbor is the goal, return the path to it
                if str(neighbor) == goal:
                    return [str(city) for city in new_path]
            # Mark the current node as explored
            explored.append(node)

    # If no path is found, print a message and return None
    print("No path found")
    return None

def main(start, destination, connections):
    """Main function to find the route between start and destination cities."""
    
    # Create a map object using the provided connections
    my_map = Map(connections)
    
    # Use breadth-first search to find the shortest path between start and destination cities
    instructions = bfs(my_map, start, destination)
    
    # If a path is found
    if instructions:
        result = ""
        # Iterate through the instructions (cities) in the path
        for index, city in enumerate(instructions):
            # If it's the first city in the path
            if index == 0:
                result += f"Starting at {city}"  # Add starting city to result
                print(f"Starting at {city}")     # Print starting city
            # If it's not the last city in the path
            if index < len(instructions) - 1:
                next_city = instructions[index + 1]  # Get the next city in the path
                maps = [abc.name for abc in my_map.cities].index(city)  # Get index of current city in the map
                city_neighbor = my_map.cities[maps].neighbors  # Get neighbors of current city
                cn = {}  # Initialize dictionary to store city and distance
                
                # Iterate through neighbors of the current city
                for city, distance in city_neighbor.items():
                    cn[str(city)] = distance  # Add city and distance to dictionary
                    
                distance, interstate = cn[next_city]  # Get distance and interstate to the next city

                # Add driving instructions to the result
                result += f"Drive {distance} miles on {interstate} towards {next_city}, then"
                print(f"Drive {distance} miles on {interstate} towards {next_city}, then")
            # If it's the last city in the path
            else:
                result += "You will arrive at your destination"  # Add destination message to result
                print("You will arrive at your destination")     # Print destination message
        
        return result  # Return the result string
    else:
        raise Exception("No path found")  # If no path is found, raise an exception


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis,", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 283, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "80"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 183, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburg": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 304, "76"), ("New York", 391, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburg", 107, "76")], #COMEBACK
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence,", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 101, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)