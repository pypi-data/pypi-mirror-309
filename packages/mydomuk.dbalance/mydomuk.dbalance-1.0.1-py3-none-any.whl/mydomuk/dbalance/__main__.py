
#!/bin/python
import argparse
import os
from time import sleep
from dotenv import load_dotenv
from .mydocker.swarm import Swarm
from .mydocker.node import Node
from .mydocker.service import Service
from .mydocker.container import Container
from .mydocker.utils import filter_name
from .logger import initlog, infolog, debuglog, errorlog, LOGLEVEL, set_new_logging_level

initlog()
load_dotenv(override=False, verbose=False, encoding="UTF-8")
REBALANCE_LABEL = os.environ.get("REBALANCE_LABEL")

def print_labels(labels: dict[str, str]) -> None:
    header: bool = False
    for label, value in labels.items():
        if label.startswith("com.docker"):
            continue
        if header is False:
            infolog("Labels")
            header = True
        infolog(f"{' '*8} {label} = {value}")


def print_placements(placements: list[str]) -> None:
    if placements is None or len(placements) == 0:
        return
    infolog("Placements")
    for placement in placements:
        constraint, _, value = placement.partition("==")
        infolog(f"{' '*8} {constraint} = {value}")


def print_label(name: str, value: any):
    if isinstance(value, list):
        infolog(f"  Label : {name}")
        for i, v in enumerate(value):
            infolog(f"  - {i:3d} = {v}")
    elif isinstance(value, dict):
        infolog(f"  Label : {name}")
        for k, v in value.items():
            infolog(f"  - {k} = {v}")
    elif isinstance(value, str):
        infolog(f"  Label : {name} = {value}")

def discover_and_report_services(swarm: Swarm, filter: list[str], labels: list[str], detail: bool):
   # Print the Service List

    nodenames = swarm.getNodeNames()
    nodecount = [0 for _ in nodenames]
    services, groupings = swarm.getServiceFiltered(REBALANCE_LABEL, filter)

    if len(groupings) > 0:
        infolog("Service Options : G/R - Global or Replicated, B - Balance, # number for placement restrictions")
        infolog("")
        for idx, group in enumerate(groupings):
            infolog(f"Placement Group : {idx + 1} : {group}")
    else:
        infolog(f"Service Options : G/R - Global or Replicated, B - Balance\n")
        infolog("")

    infolog(Service.titleText(nodenames))
    infolog(Service.underline)

    for service in services:
        infolog(service)
        for i, count in enumerate(service.nodecount):
            nodecount[i] += count
        if detail:
            print_labels(service.labels)
            print_placements(service.placement_constraints)
            infolog("*"*100)
            for task in service.running_tasks:
                infolog(f"  Node : {task.nodename}, Task Id : {task.id}")
                if len(service.running_tasks) > 0:
                    infolog("-"*120)

        if labels is not None:
            for label, value in service.labels.items():
                if filter_name(label, labels):
                    print_label(label, value)

    infolog(Service.underline)
    infolog(Service.formatTotals(nodecount))

def main():
    detail: bool = False
    debug: bool = False
    verbose: bool = False

    parser = argparse.ArgumentParser()
    # parser.add_argument("-c", dest="config", help="Configuration file")
    parser.add_argument("-d", dest="detail", action="count", default=0, help="Detail output, use multiple times to increase level")
    parser.add_argument("-s", dest="swarm", help="IP address or Hostname of swarm node")
    parser.add_argument("-n", dest="nodes", nargs="*", help="List of Addresses of Nodes, will use Swarm list by default")
    parser.add_argument("-l", dest="labels", nargs="*", help="List of labels")
    parser.add_argument("-b", dest="balance", nargs="*", help="List of Node Names to balance, use all for all nodes")
    parser.add_argument("-ba", dest="balanceall", action="store_true", help="Balance All Nodes, will ignore the REBALANCE_LABEL environment variable")
    parser.add_argument("-q", dest="quiet", action="store_true", help="Quiet Mode")
    parser.add_argument("-f", dest="filter", nargs="*", help="List of filters")
    parser.add_argument("-dr", dest="dryrun", action="store_true", help="Show workings but do not perform rebalance")
    parser.add_argument("-bw", dest="balance_waittime", type=int, default=15, help="Number of seconds to wait after rebalancing to view results, default is 15s")
    args = parser.parse_args()

    if args.detail > 0:
        detail = True
        if args.detail == 2:
            debug = True
            set_new_logging_level(LOGLEVEL.LEVEL_DEBUG)
        elif args.detail > 2:
            verbose = True
            set_new_logging_level(LOGLEVEL.LEVEL_VERBOSE)
       
    if args.quiet is False:
        infolog(f"Rebalance Label : {REBALANCE_LABEL}")

    swarmclient = args.swarm
    if args.swarm is None and args.nodes is not None:
        swarmclient = args.nodes[0]

    swarm = Swarm(swarmclient, args.quiet)

    if args.quiet is False:

        # Print the Node List

        infolog(Node.titleText())
        infolog(Node.underline())
        for node in swarm.getNodes(sorted=True):
            infolog(node)
            debuglog(f"Node : {node.hostname} Labels : {node.labels}")

        # print("") 

        # Print the individual node containers

        for node in swarm.getNodes(sorted=True):    # role="manager", 
            if node.reachability == "unreachable":
                infolog(f"Getting Local Containers for Node : {node.hostname} - Skipped Unreachable!")
                continue
            if node.connect():
                # infolog("")
                infolog(f"Getting Local Containers for Node : {node.hostname}")

                header_done: bool = False
                for container in node.getLocalContainersFiltered(args.filter):
                    if header_done is False:
                        infolog(Container.titleText())
                        infolog(Container.underline())
                        header_done = True
                    infolog(container)
                    if detail:
                        infolog(container.dockercontainer.attrs)
                    if args.labels is not None:
                        for label, value in container.labels.items():
                            if filter_name(label, args.labels):
                                print_label(label, value)
                if header_done is False:
                    infolog(f"{' '*8} - No containers found")
                node.disconnect()
            else:
                errorlog(f"Not connected to : {node.hostname}")

        if args.labels is not None:
            infolog(args.labels)

        infolog("")
        discover_and_report_services(swarm, args.filter, args.labels, detail)


    if args.balance:
        infolog(f"Performing Rebalance")
        balance_services: list[Service] = []
        if REBALANCE_LABEL is None:
            args.balanceall = True
        services, _ = swarm.getServiceFiltered(REBALANCE_LABEL, args.filter)
        for service in services:
            if args.balanceall is False and service.rebalance_enabled is False:
                if args.quiet is False:
                    debuglog(f"Skipping Service : {service.name} as excluded by label")
                continue
            for nodename in args.balance:
                if nodename in ["*", "all"] or (nodename in service.nodenames and service.nodemap[nodename] > 0):
                    if service.replicas > 0:
                        balance_services.append(service)
                    else:
                        debuglog(f"Skipping Service : {service.name} has 0 replicas")
                    break
            else:
                if args.quiet is False:
                    debuglog(f"Skipping Service : {service.name} not active on any chosen nodes")
        for service in balance_services:
            if args.dryrun:
                infolog(f"DRYRUN - Balancing Service {service.name:32} - Nodes : {', '.join(service.restricted_hostnames)}")
            else:
                infolog(f"Balancing Service {service.name:32} - Nodes : {', '.join(service.restricted_hostnames)}")
                # service.scale_service(service.replicas, args.quiet)
                service.force_update(args.quiet)
                sleep(1)

        if args.quiet is False and args.dryrun is False:
            sleep(args.balance_waittime)
            discover_and_report_services(swarm, args.filter, args.labels, detail)

    swarm.disconnect()

if __name__ == "__main__":
  main()
