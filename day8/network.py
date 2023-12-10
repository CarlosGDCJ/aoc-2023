class NetworkMap:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.nodes = {}

        with open(self.input_path, "r", encoding="utf8") as f:
            self.instructions = list(f.readline().strip())

            for line in f:
                line = line.strip()
                if line != "":
                    node = Node(line)
                    if node.name not in self.nodes:
                        self.nodes[node.name] = node

        assert "AAA" in self.nodes, "Invalid input, start not present"
        assert "ZZZ" in self.nodes, "Invalid input, end not present"
        self.start = self.nodes["AAA"]
        self.end = self.nodes["ZZZ"]

        self.instruction_counter = 0

    def get_next_instruction(self):
        next_instruction = self.instructions[self.instruction_counter]
        self.instruction_counter += 1

        if self.instruction_counter >= len(self.instructions):
            self.instruction_counter = 0

        return next_instruction

    def follow_instructions(self):
        curr_node = self.start
        count = 0
        while curr_node != self.end:
            instruction = self.get_next_instruction()
            next_node_name = curr_node.get_direction(instruction)

            if next_node_name not in self.nodes:
                print(next_node_name)
                print(self.nodes)
                raise KeyError(f"Node {next_node_name} not in NetworkMap")

            curr_node = self.nodes[next_node_name]
            count += 1

        return count


class Node:
    def __init__(self, node_line: str):
        print(node_line)
        name, raw_dest = node_line.split("=", maxsplit=1)
        self.name = name.strip()
        self.left = raw_dest.strip().split(",", maxsplit=1)[0][1:]
        self.right = raw_dest.split(",", maxsplit=1)[1].strip()[:-1]

    def __repr__(self):
        return self.name

    # def get_left(self):
    #     return self.left

    # def get_right(self):
    #     return self.right

    def get_direction(self, direction):
        if direction == "L":
            return self.left
        if direction == "R":
            return self.right
