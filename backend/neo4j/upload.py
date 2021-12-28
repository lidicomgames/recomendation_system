from os import close
from py2neo import Graph
from py2neo.bulk import create_nodes
import json
import sys, getopt


def show_help():
    print("\n       Usage: upload.py <filename> <label>\n")


def exit_and_help():
    show_help()
    sys.exit()


def main(argv):
    filename = "products.json"
    label = "Product"

    try:
        opts, args = getopt.getopt(argv, 'h')
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    if len(opts) > 0 or len(args) != 2:
        exit_and_help()

    filename = args[0]
    label = args[1]

    upload(filename, label)


def upload(filename, label):
    credentials = json.load(open("credentials.json"))
    graph = Graph(
        credentials["url"],
        auth=(credentials["username"], credentials["password"]),
    )

    data = json.load(open(filename))

    print("[0/1] Deleting " + label)
    graph.run("MATCH (n:" + label + ") DETACH DELETE n")

    print("[1/1] Adding " + label)
    create_nodes(graph.auto(), data, labels={label})

    print("Complete!")


if (__name__ == "__main__"):
    main(sys.argv[1:])