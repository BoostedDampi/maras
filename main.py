
from maraslib.codeengine import CodeEngine

print("Code Animation")


engine = CodeEngine("RobotoMono.ttf", 25)

slide0 = engine.new_slide("""
def dijkstra(graph, start):
    # Priority queue to hold nodes to be explored
    priority_queue = [(0, start)]
    # Dictionary to hold the shortest distance to each node
    distances = {start: 0}
    # Dictionary to hold the previous node on the shortest path
    previous_nodes = {start: None}

    while priority_queue:
        // HIDDEN CODE // 
    return distances, previous_nodes""")


slide1 = engine.new_slide("""
def dijkstra(graph, start):
    # Priority queue to hold nodes to be explored
    priority_queue = [(0, start)]
    # Dictionary to hold the shortest distance to each node
    distances = {start: 0}
    # Dictionary to hold the previous node on the shortest path
    previous_nodes = {start: None}

    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Check if this distance is already larger than the known shortest distance
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, {}).items():
           // HIDDEN CODE // 
    return distances, previous_nodes""")


slide2 = engine.new_slide("""
def dijkstra(graph, start):
    # Priority queue to hold nodes to be explored
    priority_queue = [(0, start)]
    # Dictionary to hold the shortest distance to each node
    distances = {start: 0}
    # Dictionary to hold the previous node on the shortest path
    previous_nodes = {start: None}

    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Check if this distance is already larger than the known shortest distance
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes""")




engine.render()

