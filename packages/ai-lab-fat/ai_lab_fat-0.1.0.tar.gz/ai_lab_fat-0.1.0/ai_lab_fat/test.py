# ai_lab_fat/test.py

from itertools import permutations

def choice():
    print("Press 1 to print the code for the Travelling Salesman Problem")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        code = '''

def travelling_salesman_problem(graph, start_node):
    nodes = list(graph.keys())
    nodes.remove(start_node)
    all_routes = permutations(nodes)
    shortest_path = None
    min_cost = float('inf')
    for route in all_routes:
        current_cost = 0
        current_path = [start_node] + list(route) + [start_node]  # Start and end at the same node
        for i in range(len(current_path) - 1):
            current_cost += graph[current_path[i]][current_path[i + 1]]
        if current_cost < min_cost:
            min_cost = current_cost
            shortest_path = current_path

    return shortest_path, min_cost


def inputGraph():
    graph={}
    nodes=input("Enter nodes space separated:").split()
    for node in nodes:
        graph[node]={}
        print(f"Enter distances from node {node} to other nodes:")
        for neighbour in nodes:
            weight=int(input(f"Enter distance from {node} to {neighbour}: "))
            graph[node][neighbour]=weight

    return graph

graph = inputGraph()
start_node = input("Enter start node: ")

shortest_path, min_cost = travelling_salesman_problem(graph, start_node)

print("Shortest Path:", shortest_path)
print("Minimum Cost:", min_cost)
'''
        print(code)

if __name__ == "__main__":
    choice()
