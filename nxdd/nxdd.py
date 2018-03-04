#!/usr/bin/env python3
import networkx as nx
import itertools


_b2to1 = [
    [0,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,0,1,1],
    [0,1,0,0],
    [0,1,0,1],
    [0,1,1,0],
    [0,1,1,1],
    [1,0,0,0],
    [1,0,0,1],
    [1,0,1,0],
    [1,0,1,1],
    [1,1,0,0],
    [1,1,0,1],
    [1,1,1,0],
    [1,1,1,1],
]
b2to1 = []
for i in _b2to1:
    b2to1.append([bool(x) for x in i])

def make_bool2_to_bool1():
    dd = nxdd()
    funcs = []
    for func in b2to1:
        # In theory, this should create a list of the invoked subgraphs
        # from each function...
        funcs.append(nx.bfs_tree(dd.graph, dd.func_from_tt(func)))
    return dd, funcs

class nxdd(object):
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(False)
        self.graph.add_node(True)
        self._uid_counter = itertools.count(2)

    def next_uid(self):
        return next(self._uid_counter)

    def run(self, node, v):
        v_iter = iter(v)
        while node is not True and node is not False:
            node = self.eval(node, next(v_iter))
        return node

    def eval(self, node, v):
        if v:
            return self.get_hi(node)
        else:
            return self.get_lo(node)

    def mk_node(self, lo, hi):
        if lo not in self.graph:
            raise KeyError(lo)
        if hi not in self.graph:
            raise KeyError(hi)
        lo_parents = self.get_parents(lo, 'lo')
        hi_parents = self.get_parents(hi, 'hi')
        shared_parents = lo_parents.intersection(hi_parents)
        if len(shared_parents) > 0:
            return shared_parents.pop()
        else:
            newnode_uid = self.next_uid()
            # print(newnode_uid, lo, hi)
            self.graph.add_node(newnode_uid)
            self.graph.add_edge(newnode_uid, lo, key='lo')
            self.graph.add_edge(newnode_uid, hi, key='hi')
            # print(self.graph[newnode_uid])
            return newnode_uid

    def func_from_tt(self, truthtable):
        while(len(truthtable) > 1):
            tt_iter = iter(truthtable)
            newnodes = []
            while(True):
                try:
                    lo = next(tt_iter)
                    hi = next(tt_iter)
                except StopIteration:
                    break
                newnodes.append(self.mk_node(lo, hi))
            truthtable = newnodes
        return truthtable[0]

    def ite(self, hi, lo):
        return self.mk_node(lo, hi)

    def get_hi(self, node):
        for child, attr in self.graph[node].items():
            if 'hi' in attr:
                return child
        raise KeyError("No 'hi' edge could be found for node {}".format(node))

    def get_lo(self, node):
        for child, attr in self.graph[node].items():
            if 'lo' in attr:
                return child
        raise KeyError("No 'lo' edge could be found for node {}".format(node))

    def get_parents(self, node, attr=None):
        if attr is None:
            return self.graph._pred[node]
        else:
            return set({k:v for k,v in self.graph.pred[node].items() if attr in v}.keys())

    def get_subgraph(self, node):
        ddnodes = nx.bfs_tree(self.graph, node)
        ddgraph = self.graph.subgraph(list(ddnodes.nodes) + [node])
        return ddgraph

    def __call__(self, node, v):
        return self.run(node, v)

    def draw_graph(self, path, rootnode=None):
        from pygraphviz import AGraph
        if rootnode is None:
            # rootnode = max(self.graph.nodes.keys())
            ddgraph = self.graph
        # ddnodes = nx.bfs_tree(self.graph, rootnode)
        else:
            ddgraph = self.get_subgraph(rootnode)
        g = AGraph(directed=True, strict=False)
        # ranks = {}
        node_hash = {}
        for e, node in enumerate(ddgraph.nodes.keys()):
            nodename = 'n{}'.format(e)
            node_hash[node] = nodename
            # if node.level not in ranks:
            #     ranks[node.level] = []
            # ranks[node.level].append(nodename)
        for node in ddgraph.nodes.keys():
            if node is True or node is False:
                g.add_node(node_hash[node], shape='box', label={False: 'False', True: 'True'}[node])
            else:
                g.add_node(node_hash[node], label=str(node))

        for node in ddgraph.nodes.keys():
            if node is not True and node is not False:
                g.add_edge(node_hash[node], node_hash[self.get_hi(node)], 'hi', color='blue')
                g.add_edge(node_hash[node], node_hash[self.get_lo(node)], 'lo', color='red', style='dashed')
        # for level, nodes in ranks.items():
        #     g.add_subgraph(nodes, rank='same')
        g.draw(path=path, prog='dot')
