from os import close
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships, merge_nodes
import json

credentials = json.load(open("credentials.json"))
g = Graph(
    credentials["url"],
    auth=(credentials["username"], credentials["password"]),
)

print("[0/3] Deleting Products and Tags")
g.run(
    "MATCH (a:TAG)-[ab]->(b:Product) DETACH DELETE a, ab, b"
)

original_products = json.load(open("products_games.json", encoding="utf8"))

products = []
tags_key = ["name"]
tags_data = []
tags_relation_product = []

for product in original_products:
    products.append({
        "product_code": product["uniq_id"],
        "title": product["title"],
        "url": product["url"],
        "brand": product["brand"],
        "brand": product["brand"],
        "images": product["images"],
        "category": product["category"],
        "sub_cateory": product["sub_cateory"],
        "description": product["description"],
        "product_complete_description": product["product_complete_description"]
    })

    tags_data.append({"name": product["brand"]})
    tags_data.append({"name": product["category"]})
    tags_data.append({"name": product["sub_cateory"]})

    tags_relation_product.append((product["brand"], {}, product["uniq_id"]))
    tags_relation_product.append((product["category"], {}, product["uniq_id"]))
    tags_relation_product.append((product["sub_cateory"], {}, product["uniq_id"]))

print("[1/3] Creating Products")
create_nodes(g.auto(), products, labels={"Product"})
print("[2/3] Creating Tags")
merge_nodes(g.auto(), tags_data, ("Tag", "name"))
print("[3/3] Creating Relationship Tag -> Product")
create_relationships(
    g.auto(),
    tags_relation_product,
    "TAG_ITEM",
    start_node_key=("Tag", "name"),
    end_node_key=("Product", "product_code"),
)
