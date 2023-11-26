import heapq
import csv
from collections import defaultdict

mrt_line_to_code = defaultdict(set)
station_line_to_colour_code = {
    'NS': 'rgba(226, 39, 38, 255)',
    'EW': 'rgba(0, 150, 77, 255)',
    'CG': 'rgba(0, 150, 77, 255)',
    'CC': 'rgba(249,157,37,255)',
    'NE': 'rgba(143,65,153,255)',
    'DT': 'rgba(0,93,168,255)',
    'TE': 'rgba(155,90,35,255)',
    'PW': 'rgba(154,154,154,255)',
    'PE': 'rgba(154,154,154,255)',
    'PT': 'rgba(154,154,154,255)'
}

class Node:
    def __init__(self, name=None):
        self.name = name
        self.lines = set()
        self.neighbours = set()

class MRTGraph:
    def __init__(self):
        self.stations = {}
    
    def connect_stations(self, station1, station_code1, station2, station_code2, time):
        if station1 not in self.stations:
            self.stations[station1] = Node(station1)
        if station2 not in self.stations:
            self.stations[station2] = Node(station2)
        if station_code1 not in self.stations[station1].lines:
            self.stations[station1].lines.add(station_code1)
        if station_code2 not in self.stations[station2].lines:
            self.stations[station2].lines.add(station_code2)
        self.stations[station1].neighbours.add((time, station2))
        self.stations[station2].neighbours.add((time, station1))
    
    def find_shortest_path(self, station1: str, station2: str) -> tuple:
        if station1 not in self.stations or station2 not in self.stations:
            return (-1, []) # station does not exist/has not been added
        visited = {}
        heap = [(0, station1, [station1])]
        while heap:
            time, station, route = heapq.heappop(heap)
            visited[station] = time
            station_node = self.stations[station]
            if station == station2:
                return (time, route)
            for neighbour in station_node.neighbours:
                if neighbour[1] in visited and time+neighbour[0] >= visited[neighbour[1]]:
                    continue
                heapq.heappush(heap, (time+neighbour[0], neighbour[1], route+[neighbour[1]]))
    
    def path_to_mrt_lines(self, path):
        return [list(mrt_line_to_code[station]) for station in path]
    
    def mrt_lines_to_colour_code(self, mrt_lines):
        return [list(map(lambda x: station_line_to_colour_code[x[:2]], mrt_line)) for mrt_line in mrt_lines]

mrt_graph = MRTGraph()

with open('mrt_details.csv', 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        mrt_graph.connect_stations(row[0], row[1], row[2], row[3], int(row[4]))
        mrt_line_to_code[row[0]].add(row[1])
        mrt_line_to_code[row[2]].add(row[3])


