import networkx as nx
from pyvis.network import Network
import xmltodict
import json
import re
import numpy as np


# import spacy_universal_sentence_encoder


class Graphs:

    def __init__(self):
        pass

    def parse_xml(self, book_path, output_path):
        edges = []
        nodes = []

        names_data = []
        nodes_data = []
        edges_data = []

        # Load XML file
        with open(book_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())

        # Close file after reading
        xml_file.close()

        # convert xml to json data
        json_data = json.dumps(data_dict)
        xx = json.loads(json_data)

        # Grab elements of the grap
        graph_data = xx["mxfile"]["diagram"]["mxGraphModel"]["root"]["mxCell"]

        # Grab nodes and edges
        for i in range(2, len(graph_data)):
            try:
                # Grab edges
                if graph_data[i]["@edge"]:
                    edges.append(graph_data[i])
            except:
                # Grab nodes
                nodes.append(graph_data[i])

        # Grab id and values of nodes
        for n in nodes:
            id_ = n["@id"]
            val = n["@value"]
            val = self.remove_tags(val)
            nodes_data.append([id_, val])

        # Grab source and target from edges
        for e in edges:
            source = e["@source"]
            target = e["@target"]
            edges_data.append([source, target])

            # match the source and targets of all edges in nodes based on id
        for i in range(len(edges_data)):
            s = ""
            t = ""
            v = edges_data[i][0]
            z = edges_data[i][1]

            for j in range(len(nodes_data)):

                if v == nodes_data[j][0]:
                    s = {"source_id": v,
                         "source": nodes_data[j][1]}

                if z == nodes_data[j][0]:
                    t = {"target_id": z,
                         "target": nodes_data[j][1]}

            names_data.append([s, t])

        # Join all node and edge data
        all_data = {"nodes": nodes_data, "pairs": names_data}

        # Save graph json to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

    def display_graph(self, path, name, can_show):
        book_nodes = []
        book_edges = []

        # Load book json data
        f = open(path)
        data = json.load(f)

        # Fetch nodes
        for d in data["nodes"]:
            book_nodes.append(d[1])

        # Fetch book pairs
        for p in data["pairs"]:
            # source_id = p[0]["source_id"]
            source = p[0]["source"]

            # target_id = p[0]["target_id"]
            target = p[1]["target"]

            pair = (source, target)
            # print(pair)
            book_edges.append(pair)

        # Draw graphs
        G = nx.Graph()

        # Create nodes
        G.add_nodes_from(book_nodes)

        # Create edges
        G.add_edges_from(book_edges)

        # Display graph
        net = Network(notebook=True)
        net.from_nx(G)
        # net.show(name)

        return net
        # display(HTML(name))

    def remove_tags(self, text):
        clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(clean, ' ', text).strip()

    def get_book_content(self, path):
        content = ""
        f = open(path)
        data = json.load(f)

        for d in data["pairs"]:
            content += d[1]["target"] + "\n"

        return content

    def cosine(u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

