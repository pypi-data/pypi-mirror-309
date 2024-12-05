from typing import List, Dict
from defigraph.Vertex import Vertex
from defigraph.Edge import Edge
from defigraph.Pool import Pool


class Graph:
    def __init__(self, edges: List[Edge]) -> None:
        self.vertices: List[Vertex] = []
        self.adjascency_list: Dict[Vertex, List[Edge]] = {}

        for edge in edges:
            # Create adjacency list
            if edge.pool.token0 not in self.adjascency_list:
                self.adjascency_list[edge.pool.token0] = [edge]
            else:
                if edge not in self.adjascency_list[edge.pool.token0]:
                    self.adjascency_list[edge.pool.token0].append(edge)
            # Create vertices list
            if edge.pool.token0 not in self.vertices:
                self.vertices.append(edge.pool.token0)
            if edge.pool.token1 not in self.vertices:
                self.vertices.append(edge.pool.token1)

    def __repr__(self) -> str:
        return f"{self.adjascency_list}"

    def __getitem__(self, vertex: str) -> List[Edge]:
        return self.adjascency_list[vertex]

    def __setitem__(self, vertex: str, edges: List[Vertex]) -> None:
        if vertex not in self.adjascency_list:
            self.adjascency_list[vertex] = edges
        else:
            for edge in edges:
                if edge not in self.adjascency_list[vertex]:
                    self.adjascency_list[vertex].append(edge)

    def __len__(self):
        return len(self.vertices)

    def add_edge(self, pool: Pool, directed=False) -> None:
        edge = Edge(pool=pool)

        if edge.pool.token0 not in self.adjascency_list:
            self.adjascency_list[edge.pool.token0] = [edge]
        else:
            if edge not in self.adjascency_list[edge.pool.token0]:
                self.adjascency_list[edge.pool.token0].append(edge)

        # add the undirected edge
        if not directed:
            token0 = edge.pool.token0
            token1 = edge.pool.token1
            pool_address = edge.pool.address
            fee = edge.pool.fee
            token0price = edge.pool.token0_price
            token1price = edge.pool.token1_price
            reverse_pool_direction = Pool(
                token0=token1,
                token1=token0,
                pool_address=pool_address,
                fee=fee,
                token0_price=token1price,
                token1_price=token0price,
            )
            edge = Edge(pool=reverse_pool_direction)

            if edge.pool.token0 not in self.adjascency_list:
                self.adjascency_list[edge.pool.token0] = [edge]
            else:
                if edge not in self.adjascency_list[edge.pool.token0]:
                    self.adjascency_list[edge.pool.token0].append(edge)

        # Update vertices list
        if edge.pool.token0 not in self.vertices:
            self.vertices.append(edge.pool.token0)
        if edge.pool.token1 not in self.vertices:
            self.vertices.append(edge.pool.token1)

    def get_edge_count(self) -> int:
        count = 0
        for vertex in self.adjascency_list:
            count += len(self.adjascency_list[vertex])
        return count

    def get_vertices(self) -> List[Vertex]:
        return self.vertices

    def get_edges(self) -> List[Edge]:
        edges = []
        for vertex in self.adjascency_list:
            edges.extend(self.adjascency_list[vertex])
        return edges
