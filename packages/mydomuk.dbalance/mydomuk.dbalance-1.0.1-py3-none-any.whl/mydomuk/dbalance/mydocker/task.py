from .node import Node
class Task:
    def __init__(self, data) -> None:
        self.id = data['ID']
        self.nodeid = data["NodeID"] if "NodeID" in data else None
        self.dockertask = data
        self.nodename: str = ""

    def setNodeName(self, nodes: dict[str, Node]):
        if self.nodeid in nodes:
            self.nodename = nodes[self.nodeid].hostname
        else:
            self.nodename = "????????"
