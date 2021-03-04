from collections import defaultdict, abc
import numbers
from pyintergraph.infer import infer_type, get_c_type
from pyintergraph.exceptions import PyIntergraphCompatibilityException
import pyintergraph


class FixedInterGraph(pyintergraph.InterGraph):
    """This defines a interchangeable format that can be read in by the 'from_'-classmethods
        and convert the interchangeable format the package formats with the 'to_'-methods
    """

    def __init__(self, nodes, node_labels, node_attributes, edges, edge_attributes, is_directed):
        self.nodes = nodes
        self.node_labels = node_labels
        self.node_attributes = node_attributes

        self.edges = edges
        self.edge_attributes = edge_attributes

        self.is_directed = is_directed
        self.use_labels = True

    def to_graph_tool(self, labelname=None):
        """Converts Graph object to graph-tool Graph.

        :params:
            labelname: name for vertex_attribute None, defaults to None.
                if node labels should be kept as vertex attribute,
                the name for the vertex attribute can be specified this way.
        """
        import graph_tool.all as gt

        gtG = gt.Graph(directed=self.is_directed)

        if len(self.nodes) == 0:
            return gtG

        attrs = {}
        node_type = infer_type(self.node_labels.values(), as_vector=False)

        if labelname:
            attrs[labelname] = gtG.new_vertex_property(node_type)

        nodes = {}
        node_property_type_assertion = defaultdict(set)

        for nx_node, data in zip(self.nodes, self.node_attributes):

            v = gtG.add_vertex()
            if labelname:
                attrs[labelname][v] = self.node_labels[nx_node]
            nodes[nx_node] = v

            for key, val in data.items():

                # Single Type assertion
                node_property_type_assertion[key].add(type(val))
                if len(node_property_type_assertion[key]) > 1:
                    raise Exception(f"Type not equal for all nodes on Node-Attribute {key}, \
                        types found: {node_property_type_assertion[key]}")

                if key not in attrs:
                    as_vector = isinstance(
                        val, abc.Iterable) and not isinstance(val, str)
                    attrs[key] = gtG.new_vertex_property(
                        infer_type(val, as_vector=as_vector))

                attrs[key][v] = val

        for attr_name, attr_val in attrs.items():
            gtG.vertex_properties[attr_name] = attr_val

        attrs = {}
        edge_property_assertion = defaultdict(set)
        for e, data in zip(self.edges, self.edge_attributes):
            u, v = e
            edge = gtG.add_edge(nodes[u], nodes[v])
            for key, val in data.items():

                # Single Type assertion
                edge_property_assertion[key].add(type(val))
                if len(edge_property_assertion[key]) > 1:
                    raise Exception(f"Type not equal for all edges on Edge-Attribute {key}, \
                        types found: {edge_property_assertion[key]}")

                if key not in attrs:
                    as_vector = isinstance(
                        val, abc.Iterable) and not isinstance(val, str)
                    attrs[key] = gtG.new_edge_property(
                        infer_type(val, as_vector=as_vector))

                attrs[key][edge] = val

        for attr_key, attr_val in attrs.items():
            gtG.edge_properties[attr_key] = attr_val

        return gtG
