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
                    if node.get_name() not in self.nodes:
                        self.nodes[node.get_name()] = node

        self.start = {self.nodes[k] for k in self.nodes.keys() if k.endswith("A")}
        self.end = {self.nodes[k] for k in self.nodes.keys() if k.endswith("Z")}

        self.instruction_counter = 0

    def get_next_instruction(self) -> int:
        next_instruction = self.instructions[self.instruction_counter]
        self.instruction_counter += 1

        if self.instruction_counter >= len(self.instructions):
            self.instruction_counter = 0

        return next_instruction

    def reset_instruction_counter(self) -> int:
        self.instruction_counter = 0

    def follow_instructions(self) -> list[int]:
        counts = []
        for start in self.start:
            curr_node = start
            self.reset_instruction_counter()
            count = 0

            while curr_node not in self.end:
                instruction = self.get_next_instruction()
                next_node_name = curr_node.get_direction(instruction)

                if next_node_name not in self.nodes:
                    print(next_node_name)
                    print(self.nodes)
                    raise KeyError(f"Node {next_node_name} not in NetworkMap")

                curr_node = self.nodes[next_node_name]
                count += 1

            counts.append(count)

        return counts


class Node:
    def __init__(self, node_line: str):
        name, raw_dest = node_line.split("=", maxsplit=1)
        self.name = name.strip()
        self.left = raw_dest.strip().split(",", maxsplit=1)[0][1:]
        self.right = raw_dest.split(",", maxsplit=1)[1].strip()[:-1]

    def __repr__(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def get_direction(self, direction) -> str:
        if direction == "L":
            return self.left
        if direction == "R":
            return self.right
