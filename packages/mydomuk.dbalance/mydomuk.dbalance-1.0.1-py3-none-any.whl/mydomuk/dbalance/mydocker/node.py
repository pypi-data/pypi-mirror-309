from docker import DockerClient
from .utils import connect
from .container import Container
from .utils import filter_name, exec_with_retry
from ..logger import infolog, errorlog, debuglog, verboselog
from requests import exceptions


class Node:
    def __init__(self, node):
        nodeattr = node.attrs
        spec = nodeattr["Spec"] if "Spec" in nodeattr else {}
        description = nodeattr["Description"] \
            if "Description" in nodeattr else {}
        status = nodeattr["Status"] if "Status" in nodeattr else {}
        managerstatus = nodeattr["ManagerStatus"] \
            if "ManagerStatus" in nodeattr else {}

        self.role : str = spec["Role"]
        self.labels: dict[str, str] = {}
        if "Labels" in spec:
            self.labels = spec['Labels']
        self.availability: str = spec["Availability"]
        self.hostname: str = description["Hostname"]
        self.state: str = status["State"]
        self.address: str = status["Addr"]
        self.id = nodeattr["ID"]
        self.reachability = managerstatus["Reachability"] \
            if "Reachability" in managerstatus else "???"
        self.managementaddress: str = managerstatus["Addr"] \
            if "Addr" in managerstatus else "???"
        self.connected: bool = False
        self.client: DockerClient = None
        self.containers: list[Container] = []
        self.api_address: str = None
        if self.address != "0.0.0.0":
            self.api_address = self.address
        elif self.managementaddress != "???":
            self.api_address, _, _ = self.managementaddress.partition(":")

        verboselog(f"Node : {self.hostname} Addr: {self.address}, Id: {self.id}, state : {self.state}")
    @staticmethod
    def formatline(
        node, role, available, state, reachable,
        managementaddress, id, addr):
        #             f"{id:26s} " before addr
        return (
            f"{node:12s} "
            f"{role:8s} "
            f"{available:12s} "
            f"{state:12s} "
            f"{reachable:17s} "
            f"{managementaddress:22s} "
            f""
            f"{addr:16s}"
        )

    @staticmethod
    def underline():
        text = Node.formatline(
            "=","=","=","=","=","=","=","="
        )
        newtext = text.replace("  ","++").replace("+=", " =").replace("+", "=")
        return newtext

    @staticmethod
    def titleText():
        return Node.formatline(
            "NODE", "ROLE", "AVAILABLE",
            "STATE", "REACHABLE", "MGMT ADDRESS",
            "NODE ID", "ADDRESS"
        )

    def __repr__(self):
        # Removed self.id before address
        if self.role == "manager":
            return Node.formatline(
                self.hostname, self.role, self.availability,
                self.state, self.reachability, self.managementaddress,
                self.id,
                self.address
            )
        else:
            return Node.formatline(
                self.hostname, self.role, self.availability,
                self.state, "", "", self.id, self.address
            )

    def connect(self):
        if self.api_address is not None:
            try:
                self.client = connect(self.api_address, self.hostname)
                self.connected = True
            except Exception as e:
                errorlog(f"Node : {self.hostname} Connect Failed to {self.api_address} Reason : {e}")
        else:
            infolog(f"Node : {self.hostname} has no usable address!")
        return self.connected

    def disconnect(self):
        self.client.close()

    def getAllContainers(self):
        infolog(f"Getting All Containers for Node : {self.hostname}")
        if self.connected is False:
            self.connect()
        self.containers.clear()
        container_list = exec_with_retry(self.client.containers.list, 3, 1, [exceptions.ReadTimeout])
        if container_list is not None:
            for container in self.client.containers.list():
                dc = Container(container)
                self.containers.append(dc)
        return self.containers

    def getAllContainersFiltered(self, filters):
        containers: list[Container] = []
        for container in self.getLocalContainers():
            if filter_name(container.name, filters):
                containers.append(container)
        containers.sort(key=lambda x: x.name)
        return containers

    def getLocalContainers(self):
        # print(f"Getting Local Containers for Node : {self.hostname}")
        if self.connected is False:
            self.connect()
        self.containers.clear()
        container_list = exec_with_retry(self.client.containers.list, 3, 1, [exceptions.ReadTimeout])

        if container_list is not None:
            for container in container_list:
                dc = Container(container)
                if dc.type != "STACK":
                    self.containers.append(dc)
        return self.containers

    def getLocalContainersFiltered(self, filters):
        containers: list[Container] = []
        for container in self.getLocalContainers():
            if filter_name(container.name, filters):
                containers.append(container)
        containers.sort(key=lambda x: x.name)
        return containers

