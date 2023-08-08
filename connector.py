import Bdd
import json

with open("config.json", "r", encoding="utf-8") as config_file:
    CONFIGURATION = json.loads(config_file.read())

def test(CONFIGURATION):
    with open("config.json", "w") as file_config:
        json.dump(CONFIGURATION, file_config, indent=4)
        
def sqlite_connector():
    DATABASE = CONFIGURATION.get("database")
    TABLE = CONFIGURATION.get("table")
    ##########  Get all the input rows  ##########
    rows_input_db = Bdd.read_table(DATABASE, TABLE)
    
    graph = {}
    for row in rows_input_db:
        source = row[1]
        destination = row[2]
        weight = row[3]

        ##########  Define the node and the connection  ##########
        ##  Example : A -> B (weight : 5) & A -> C (weight : 2) & B -> D (weight : 10)
        ##  Output : {"A":{"B":5, "C":2},"B":{"D":10}}
        ##########
        if source not in graph:
            graph[source] = {}
        graph[source][destination] = weight
    
    return graph

def json_connector():
    JSON_INPUT = CONFIGURATION.get("json_input")
    return json.loads(JSON_INPUT)