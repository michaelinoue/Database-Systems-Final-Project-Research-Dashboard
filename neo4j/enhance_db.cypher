// Copy this code into the neo4j Browser. Ensure database is configured per MP1.

// Delete existing clusters
MATCH (c:CLUSTER)
DETACH DELETE c;

// Initialize new clusters
MATCH (k:KEYWORD)
CREATE (c:CLUSTER)
MERGE (c)-[:CONTAINS]->(k)
