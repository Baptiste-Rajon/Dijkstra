import json
import Bdd
import connector
import time



def error_ckecking(SHORTER_WANTED, LOWER_WANTED):
    if SHORTER_WANTED == True and LOWER_WANTED == True:
        print("ERROR: The Shorter_wanted and Lower_wanted cannot be True as the same time")
        return False
    else:   
        return True

def algorithm(graph, start_node, end_node):
    all_paths = []
    visited_nodes = set()
    stack = [(start_node, [])]
    while stack:
        current_node, current_path = stack.pop()


        if current_node == end_node:
            all_paths.append(current_path + [current_node])
            visited_nodes = set()
            

        ##########  Add the current into the visited node list to avoid same result ##########
        else:
            visited_nodes.add(current_node)

        ##########  Add node into stack ##########
        if current_node in graph:
            for neighbor, _ in graph[current_node].items():
                if neighbor not in visited_nodes:
                    stack.append((neighbor, current_path + [current_node]))

    return all_paths


def main():

    with open("config.json", "r", encoding="utf-8") as config_file:
        CONFIGURATION = json.loads(config_file.read())

    DATABASE = CONFIGURATION.get("database")
    TABLE = CONFIGURATION.get("table")

    DATABASE_OUTPUT = CONFIGURATION.get("database_output")
    TABLE_OUTPUT = CONFIGURATION.get("table_output")

    START_NODE = CONFIGURATION.get("start")
    END_NODE = CONFIGURATION.get("end")

    CONNECTOR = CONFIGURATION.get("connector")

    SHORTER_WANTED = CONFIGURATION.get("shorter_wanted")
    LOWER_WANTED = CONFIGURATION.get("lower_wanted")


    if not error_ckecking(SHORTER_WANTED, LOWER_WANTED):
        exit()
    
    ##########  Get data ##########
    if CONNECTOR == "sqlite":
        graph = connector.sqlite_connector()
    elif CONNECTOR == "json":
        graph = connector.json_connector()

    with open("Output/dijkstra.json", "w") as file:
        file.write(json.dumps(graph))
    
    with open("Web/d.json", "w") as file:
        file.write(json.dumps(graph))

    ##########  Call the dijkstra algorithm ##########
    all_paths = algorithm(graph, START_NODE, END_NODE)
    
    if not all_paths:
        print(f"No path found from node {START_NODE} to node {END_NODE}.")

    ##########  Save items into the database ##########
    else:
        ##########  Create the database if not exist ##########
        Bdd.create_output_table(DATABASE_OUTPUT, TABLE_OUTPUT)

        ##########  List all paths found and save them into the database ##########
        min_node = 2147483646
        min_travel = 2147483646

        item_save = []

        for path in all_paths:
            travel = []
            for i in range(len(path) - 1):
                source = path[i]
                destination = path[i + 1]
                travel.append({
                    "Source": source,
                    "Destination": destination,
                    "Weight": graph[source][destination]
                })

            travel_time = sum(connection["Weight"] for connection in travel)
            travel_json = json.dumps(travel)

            ##########  If we want the lowest weight ##########
            if LOWER_WANTED:
                if len(travel) <= min_travel : 
                    if len(travel) < min_travel:
                        min_travel = len(travel)
                        item_save = [(travel_time, travel_json, len(travel))]
                    else: #(Egal)
                        item_save.append((travel_time, travel_json, len(travel)))
                    
            ########## If we want only the lowest number of node crossed ##########
            elif SHORTER_WANTED:
                if travel_time <= min_node : 
                        if travel_time < min_node:
                            min_node = travel_time
                            item_save = [(travel_time, travel_json, len(travel))]
                        else: #(Egal)
                            item_save.append((travel_time, travel_json, len(travel)))
            
        ##########  Instert data into the database ##########
        if LOWER_WANTED:
            for item in item_save:
                Bdd.insert_data(DATABASE_OUTPUT, TABLE_OUTPUT, item[0],item[1],item[2])
        elif SHORTER_WANTED:
            for item in item_save:
                Bdd.insert_data(DATABASE_OUTPUT, TABLE_OUTPUT, item[0],item[1],item[2])
        else:
            Bdd.insert_data(DATABASE_OUTPUT, TABLE_OUTPUT, travel_time, travel_json, len(travel))

        with open("Web/d1.json", "w") as file:
            file.write((item[1]))

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Script execution time: {execution_time:.4f} seconds")