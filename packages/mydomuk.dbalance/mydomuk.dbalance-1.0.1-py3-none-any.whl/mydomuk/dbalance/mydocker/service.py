from .task import Task
from .node import Node
from ..logger import debuglog, infolog, errorlog, verboselog, warnlog
from docker.models.services import Service as DockerService

class ServiceOptions:
    def __init__(self):
        self.rebalance: str = " "
        self.mode: str = " "
        self.group: str = " "

    def __repr__(self) -> str:
        text = self.mode + self.rebalance + self.group
        return f"{text:6}"

class Service:
    underline: str = ""
    def __init__(self, data, nodes: dict[str, Node]) -> None:
        self.id = data.id
        self.short_id = data.short_id
        self.name = data.name
        self.mode = ""
        self.dockerservice: DockerService = data
        self.tasks = data.tasks()
        self.labels = {}
        self.placement_constraints: list[str] = []
        self.replicas: int = 0
        self.rebalance_enabled: bool = True # Enabled by default
        if "Spec" in data.attrs:
            spec = data.attrs["Spec"]
            if "Labels" in spec:
                self.labels = spec["Labels"]
            if "TaskTemplate" in spec:
                templates = spec["TaskTemplate"]
                if "Placement" in templates:
                    placement = templates["Placement"]
                    if "Constraints" in placement:
                        self.placement_constraints = placement["Constraints"]
            if "Mode" in spec:
                mode = spec["Mode"]
                if "Global" in mode:
                    self.mode = "Global"
                    self.rebalance_enabled = False
                elif "Replicated" in mode:
                    self.mode = "Replicated"
                    replicas = mode['Replicated']
                    if 'Replicas' in replicas:
                        self.replicas = replicas['Replicas']

        self.nodenames: list[str] = sorted([x.hostname for x in nodes.values() if x.availability == "active"])
        self.running_tasks = [
            Task(t) for t in data.tasks({"desired-state":"running"})
            ]
        for rt in self.running_tasks:
            rt.setNodeName(nodes)

        self.nodemap: dict[str, int] = {}

        for nodename in self.nodenames:
            self.nodemap[nodename] = 0
        for rt in self.running_tasks:
            if rt.nodename in self.nodemap:
                self.nodemap[rt.nodename] += 1
        self.nodecount = list(self.nodemap.values())
        self.restricted_hostnames: list[str] = []
        for constraint in self.placement_constraints:
            placement_key, _, placement_value = constraint.partition("==")
            if placement_key == "node.hostname":
                self.restricted_hostnames = [placement_value]                
                break
            if placement_key.startswith("node.labels"):
                matched_hostnames = self.get_node_hostnames_by_label(placement_key[12:], placement_value, list(nodes.values()))
                if len(self.restricted_hostnames) == 0:
                    self.restricted_hostnames.extend(matched_hostnames)
                else:
                    remove_hostnames: list[str] = []
                    for restriction in self.restricted_hostnames:
                        if restriction not in matched_hostnames:
                            remove_hostnames.append(restriction)
                    for hostname in remove_hostnames:
                        self.restricted_hostnames.remove(hostname)
        self.restricted_hostnames.sort()
        self.restricted_group: int = -1



    def get_node_hostnames_by_label(self, labelname: str, labelvalue: str, nodes: list[Node]) -> list[str]:
        verboselog(f"Finding Nodes for Service : {self.name} with LABEL : {labelname} and VALUE : {labelvalue}")
        matched_hostnames: list[str] = []
        for node in nodes:
            for nodelabelname, nodelabelvalue in node.labels.items():
                # print(f"Checking Node : {node.hostname} Label : {nodelabelname} Value : {nodelabelvalue}")
                if nodelabelname == labelname and nodelabelvalue == labelvalue:
                    # print(f"Matched Node : {node.hostname}")
                    matched_hostnames.append(node.hostname)
        verboselog(f"Matched Nodes : {matched_hostnames}")
        return matched_hostnames

    @staticmethod
    def formatline(
        servicename, serviceid, nodenames
        ):
        text = f"{servicename:32s} {serviceid:12s} "
        Service.underline = "="*32 + " " + "="*12
        for nodename in nodenames:
            text += f"{nodename:12} "
            Service.underline += " " + "="*12
        Service.underline += " " + "=" * 8 + " " + "=" * 8

        return text

    @staticmethod
    def formatTotals(nodecounts):
        return Service.formatline("Total","", nodecounts)

    @staticmethod
    def titleText(*nodenames):
        return Service.formatline(
            "SERVICE NAME", "SERVICE ID", map(lambda x: x.upper(), *nodenames)
        ) + "Options  Replicas"

    def __repr__(self) -> str:
        text = Service.formatline(
                    self.name, self.short_id,
                    self.nodecount
               )
        opts = ServiceOptions()
        if self.mode == "Global":
            opts.mode = "G"
        elif self.mode == "Replicated":
            opts.mode = "R"
        if len(self.restricted_hostnames) != 1:
            if self.rebalance_enabled:
                opts.rebalance = "B"
        if self.restricted_group != -1:
            opts.group = str(self.restricted_group)
        return f"{text}[{opts}] ({self.replicas})"
        # return text + " [" + str(opts) + "] "

    def force_update(self, quiet: bool):
        try:
            if self.dockerservice.force_update():
                infolog(f"Service {self.name} - updated")
            else:
                warnlog(f"Service {self.name} - update failed, no reason!")
        except Exception as e:
            errorlog(f"Service {self.name} scale failed - {e}")

    def scale_service(self, count: int, quiet: bool):
        try:
            result = self.dockerservice.scale(count)
            if quiet is False:
                if result == {"Warnings": None}:
                    warnlog(f"Service {self.name} scaled to {count}")
                else:
                    infolog(f"Service {self.name} scaled to {count} - {result}")
        except Exception as e:
            errorlog(f"Service {self.name} scale failed - {e}")
