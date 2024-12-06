from docker import DockerClient
from .utils import connect
from .node import Node
from .service import Service
from .utils import filter_name
from ..logger import infolog, errorlog, debuglog


class Swarm:
    def __init__(self, client_address, quiet: bool):
        self.connected = False
        self.client: DockerClient = connect(client_address, quiet=quiet)
        self.connected = True
        self.nodes: dict[str, Node] = {}
        self.services: list[Service] = []
        nodes = self.client.nodes.list()
        for node in nodes:
           dnode = Node(node)
           self.nodes[dnode.id] = dnode

        self.getServices()

    def disconnect(self):
        if self.connected:
            self.client.close()

    def getServices(self) -> tuple[list[Service], list]:
        restrictions: list = [[x.hostname] for x in self.nodes.values()]
        restrictions.sort()
        if self.connected:
            self.services.clear()
            for service in self.client.services.list():
                srv = Service(service, self.nodes)
                if len(srv.restricted_hostnames) > 0:
                    if srv.restricted_hostnames not in restrictions:
                        restrictions.append(srv.restricted_hostnames)
                        srv.restricted_group = len(restrictions)
                    else:
                        srv.restricted_group = restrictions.index(srv.restricted_hostnames) + 1
                self.services.append(srv)
        return self.services, restrictions

    def getServiceFiltered(self, balancelabel: str, filters) -> tuple[list[Service], list]:
        infolog(f"Retrieving Services from Swarm With Balance Label : {balancelabel} and Filters : {filters}")
        services: list[Service] = []
        allservices, groupings = self.getServices()
        for service in allservices:
            if balancelabel in service.labels \
                    and service.labels[balancelabel] == "false":
                service.rebalance_enabled = False
            if filter_name(service.name, filters):
                services.append(service)
        services.sort(key=lambda x: x.name)
        return services, groupings

    def getNodeById(self, id):
        if id in self.nodes:
            return Node.nodes[id]
        return None

    def getNodes(self, role=None, sorted=False):
        nodes = []
        if role:
            nodes = [n for n in self.nodes.values() if n.role == role]
        else:
            nodes = list(self.nodes.values())
        if sorted:
            nodes.sort(key=lambda x: x.hostname)
        return nodes

    def getNodeByAddr(self, addr):
        for n in self.nodes.values():
            if n.address == addr:
                return n
        return None

    def getNodeHostName(self, id):
        if id in self.nodes:
            return self.nodes[id].hostname
        return "Unknown"

    def getNodeNames(self):
        nodenames = [x.hostname for x in self.getNodes() if x.availability == "active"]
        nodenames.sort()
        return nodenames