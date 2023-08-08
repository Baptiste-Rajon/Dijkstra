# Dijkstra Algorithm Implementation

## This Project
This project is an implementation of the Dijkstra algorithm.

## Installation & Requirements
Install dependencies: 
```shell
pip3 install -r requirements.txt
```


## What is the Dijkstra algorithm
In graph theory, the Dijkstra algorithm is used to calculate the shortest path between 2 points.

This algorithm can be used to calculate the shortest road path between 2 cities or determine the shorter way to achieve a point (attack path).

![img](/img/dijkstra_schema.png)

Here you can see that each path has a weight that is used to determine which travel is the shorter.

## Usage
To run this code, you need to fill the `config.json`` file. By default, it takes data from an SQLITE database and saves them into another SQLITE database.

Before running this code, fill the Input folder by adding your data in the Dijkstra.sqlite or in the **Dijkstra.json** following the same format as in the example.

Run the code:
```shell
python3 api.py
```

After running this program, go to the **index.html** page. You will be able to see this page:
![img](/img/web_img1.png)


## JSON Structure
```json
{
    "database":"Input/Dijkstra.sqlite",
    "table":"Dijkstra_Table",

    "database_output":"Output/Dijkstra-Output.sqlite",
    "table_output":"Dijkstra_Table",

    "shorter_wanted":true,
    "lower_wanted":false
}
```
- database: The path of the input database
- table: The name of the input table where data is stored
- database_output: The path of the output database
- table_output: The name of the output table where data will be stored
- shorter_wanted: Save on the database only the shorter way to travel to the objective. That means the path with the smallest number of weight.
- lower_wanted: Save on the database only the lowest number of nodes crossed.



## Specificity & Architecture of this program

This program can take multiple input data formats:
- sqlite

and multiple output formats:
- sqlite

We can also specify which information we want: the shorter way or the lowest node.

#### Input SQLITE Format

The input SQLITE is structured like this:

| ID | Link A | Link B | Weight |
|----|--------|--------|--------|
| 1  | A      | D      | 3      |

- `ID`: The ID of the connection
- `Link A`: The name of Link A (Also an ID)
- `Link B`: The name of Link B (Also an ID)
- `Weight`: The weight of the connection

#### Output SQLITE Format

The output SQLITE is structured like this:

| ID | TIME | JSON                                              | NODE |
|----|------|---------------------------------------------------|------|
| 1  | 12   | [{"Source":"A","Destination":"B","Weight":9},... | 5    |

- `ID`: The ID of the travel
- `Time`: The time needed for this travel (based on the weight)
- `JSON`: The connection
- `NODE`: The number of nodes crossed.

#### JSON Structure

The JSON configuration file (`config.json`) contains the following fields:

| Field           | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `database`      | The path of the input database                               |
| `table`         | The name of the input table where data is stored            |
| `database_output` | The path of the output database                              |
| `table_output`  | The name of the output table where data will be stored       |
| `shorter_wanted`| Save on the database only the shorter way to travel to the objective. That means the path with the smallest number of weight. |
| `lower_wanted`  | Save on the database only the lowest number of nodes crossed.|

Example JSON:
```json
{
    "database": "Input/Dijkstra.sqlite",
    "table": "Dijkstra_Table",
    "json_input": "Input/Dijkstra.json",
    "database_output": "Output/Dijkstra-Output.sqlite",
    "table_output": "Dijkstra_Table",
    "start": "A",
    "end": "C",
    "connector": "sqlite",
    "shorter_wanted": true,
    "lower_wanted": false
}
```


