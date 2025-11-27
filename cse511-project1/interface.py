from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, end_node):
        with self._driver.session() as session:
            # Drop existing graph if it exists
            try:
                session.run("CALL gds.graph.drop('bfsGraph', false)")
            except:
                pass

            # Project the graph
            session.run("""
                CALL gds.graph.project(
                    'bfsGraph',
                    'Location',
                    'TRIP'
                )
            """)

            # Run BFS
            query = """
                MATCH (src:Location {name: $start})
                MATCH (dst:Location {name: $end})
                CALL gds.bfs.stream('bfsGraph', {
                    sourceNode: src,
                    targetNodes: [dst]
                })
                YIELD path
                RETURN [n IN nodes(path) | {name: n.name}] AS path
                LIMIT 1
            """
            result = session.run(query, start=start_node, end=end_node)
            record = result.single()
            paths = []

            if record and record['path']:
                paths.append({'path': record['path']})

            # Clean up
            try:
                session.run("CALL gds.graph.drop('bfsGraph')")
            except:
                pass

            return paths

    def pagerank(self, max_iterations, rel_weight):
        with self._driver.session() as session:
            # Drop existing graph if it exists
            try:
                session.run("CALL gds.graph.drop('pageRankGraph', false)")
            except:
                pass

            # Project the graph
            session.run("""
                CALL gds.graph.project(
                    'pageRankGraph',
                    'Location',
                    'TRIP',
                    {relationshipProperties: $weightProp}
                )
            """, weightProp=rel_weight)

            # Compute PageRank
            query = """
                CALL gds.pageRank.stream('pageRankGraph', {
                    maxIterations: $iters,
                    relationshipWeightProperty: $weightProp
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS location, score
                ORDER BY score DESC
            """
            result = session.run(query, iters=max_iterations, weightProp=rel_weight)
            pagerank_list = list(result)

            top_node = {'name': pagerank_list[0]['location'], 'score': pagerank_list[0]['score']}
            bottom_node = {'name': pagerank_list[-1]['location'], 'score': pagerank_list[-1]['score']}

            # Clean up
            try:
                session.run("CALL gds.graph.drop('pageRankGraph')")
            except:
                pass

            return (top_node, bottom_node)