from hex.hex import Hex
import pygame
import math

class Hexmap:
    def __init__(self, width, height, map_data=None):
        self.width = width
        self.height = height
        self.map_data = []
        if map_data is None:
            self.map_data = self.generate_full_map()
        else:
            self.map_data = self.generate_map_data_from_hexmap(map_data)
        self.travel_path = []

    def generate_full_map(self):
        row = 0
        radius = 25
        row_h = math.sqrt(((radius * 2) ** 2) - (radius ** 2))
        col = 0

        while (row * row_h + 100) < self.height:
            while (col * (radius * 2) + (radius * 3)) < self.width:
                x_adj = 0
                y = row * row_h + radius * 2
                if row % 2 == 1:
                    x_adj = radius

                if (col * (radius * 2) + (radius * 3) + x_adj) < self.width:
                    x = col * (radius * 2) + (radius * 2) + x_adj
                    self.map_data.append(Hex(x, y))
                col += 1
            col = 0
            row += 1
        return self.map_data

    def generate_map_data_from_hexmap(self, hex_map):
        map_data = []
        for coordinates in hex_map:
            map_data.append(Hex(coordinates[0], coordinates[1]))
        return map_data

    def update_path(self, source, destination):
        """
        create new path between source and destination
        :param source: list of [x, y] coordinate
        :param destination: list of [x, y] coordinate
        :return:
        """
        tmp_ = self.find_path(source, destination)
        if not tmp_:
            return False
        else:
            self.travel_path = self.get_path_from_path_data(tmp_)
            return self.travel_path

    def set_map_data(self, map_data):
        self.map_data = map_data

    def get_map_data(self):
        return self.map_data

    def find_path(self, src, dest):
        """
        :param src: set of coordinates
        :param dest: set of coordinates
        :return: list of coordinates
        """
        distance_met = False
        distance = 0
        parent_id = 0
        ids = 1
        nodes = [{"id": ids, "parent_id": parent_id, "x": src[0], "y": src[1], "cost": 0}]
        max_children = 0
        max_child = 0
        ids += 1
        set_parent = nodes[0]
        path = False
        counter = 0
        # how many tries to find path
        max_attempt = 3
        sec_a_hit = sec_b_hit = sec_c_hit = sec_d_hit = sec_e_hit = 0

        while not path:
            # for path that take to long, keeping track of how many loops have been completed and hard stop it if reaches a hard point
            counter += 1

            if counter > max_attempt:
                path = True
                print("Unable to find path!", nodes)
                return False

            # look at the first children:
            for node in nodes:
                first_level_nodes = self.check_segment(node["x"], node["y"], dest[0], dest[1])

                if node["parent_id"] >= max_children and not path:
                    # look at second children
                    for child1_node in first_level_nodes:
                        # child2_nodes = check_segment(map_points, child1_node[0], child1_node[1], dest[0], dest[1])
                        if not self.check_if_locs_in_path(child1_node, nodes):
                            if child1_node.passable:
                                nodes.append(
                                    {"id": ids, "parent_id": node["id"], "x": child1_node.x, "y": child1_node.y,
                                     "cost": 0})
                                current_distance = self.get_distance(child1_node.x, child1_node.y, dest[0], dest[1])
                                if current_distance <= 0:
                                    distance_met = True
                                    path = True
                                    return self.build_path(nodes, ids)
                            ids += 1
            max_children = max_child + 1

    def check_segment(self, start_x, start_y, destination_x, destination_y):
        xumba = []
        # directions = do_direction_thing(level, start_x, start_y, destination_x, destination_y)
        radius = 25
        for node in self.map_data:
            if [node.x, node.y] is not [start_x, start_y]:
                distance = self.get_distance(node.x, node.y, start_x, start_y)
                attached_node_max_distance = radius * 2 + 1
                if attached_node_max_distance >= distance > 0:
                    xumba.append(node)
        return xumba

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def check_if_locs_in_path(self, coords, path_data):
        """

        :param coords: list of coordinates [x, y]
        :param path: datasets from path data: {'id': 66, 'parent_id': 62, 'x': 1125, 'y': 43.30, 'cost': 0}
        :return:
        """
        for node in path_data:

            if [node["x"], node["y"]] == [coords.x, coords.y]:
                return True
        return False

    def find_locs(self, x, y, nodes):
        for node in nodes:
            if node["x"] == x and node["y"] == y:
                return True
        return False

    def is_destination_coords_valid(level, x, y):
        return True

    def build_path(self, segments, last_id):
        parent_id = last_id
        mlist = []
        while parent_id > 0:
            result = self.get_parent_by_id(segments, parent_id)
            mlist.append(result)
            parent_id = result['parent_id']
        return mlist

    def get_path(self):
        return self.travel_path

    def find_closest_hex_coords(self, x, y, return_hex=False):
        distance = 999
        spot = [0, 0]
        buildable = False
        hex = None
        for coordinates in self.map_data:
            hex_spot = coordinates.get_coords()
            cdis = self.get_distance(hex_spot[0], hex_spot[1], x, y)
            if cdis < distance:
                buildable = coordinates.passable
                spot = [hex_spot[0], hex_spot[1]]
                distance = cdis
                hex = coordinates
        if return_hex:
            return hex
        else:
            return buildable, spot

        # Find closest points to provided x, y

    def get_hex_at_location(self, x, y):
        return self.find_closest_hex_coords(x, y, True)


    def get_parent_by_id(self, segments, idx):
        for segment in segments:
            if segment["id"] == idx:
                return segment

    def get_path_from_path_data(self, path_data):
        """
        Extract x,y datasets from path data: {'id': 66, 'parent_id': 62, 'x': 1125, 'y': 43.30, 'cost': 0} -> [1125, 43.30]
        :param path_data:
        :return: list of coordinates of a path
        """
        return_data = []
        for data in reversed(path_data):
            return_data.append([data["x"], data["y"]])
        return return_data

    def clear_paths(self):
        for hex_tile in self.map_data:
            hex_tile.color = pygame.Color(75, 139, 59, 80)

    def draw(self, win):
        for hex_tile in self.map_data:
            hex_tile.draw(win)

    def set_path(self, travel_path):
        for hex_tile in self.map_data:
            if hex_tile.get_coords() in travel_path:
                hex_tile.color = pygame.Color(80, 10, 121, 80)
