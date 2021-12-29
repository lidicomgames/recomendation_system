import json
import random
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships

credentials = json.load(open('credentials.json'))
graph = Graph(
    credentials["url"],
    auth=(credentials["username"], credentials["password"]),
)

products = json.load(open("products.json"))
users = json.load(open("users.json"))

print("[0/3] Deleting Order and realitionships")
graph.run("MATCH p=()-[b]->(o)-[w]->() DELETE b, o, w")

orders = []
user_order_relation = []
order_product_relation = []
order_code = 0

print("[1/3] Creating Orders")
for userIndex in range(len(users)):
    username = users[userIndex]["username"]

    for _ in range(random.randrange(1, 11)):
        orders.append({"code": order_code})
        user_order_relation.append((username, {}, order_code))

        for _ in range(random.randrange(1, 11)):
            product_code = products[random.randrange(0, len(products))]["code"]
            order_product_relation.append((order_code, {}, product_code))
        
        order_code += 1


create_nodes(graph.auto(), orders, labels={"Order"})

print("[2/3] Creating Relationship User -> Order")
create_relationships(
    graph.auto(),
    user_order_relation,
    "BUY",
    start_node_key=("User", "username"),
    end_node_key=("Order", "code"),
)

print("[3/3] Creating Relationship Order -> Products")
create_relationships(
    graph.auto(),
    order_product_relation,
    "WITH_ITEM",
    start_node_key=("Order", "code"),
    end_node_key=("Product", "code"),
)