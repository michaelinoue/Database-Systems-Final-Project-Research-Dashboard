from neo4j import  GraphDatabase

# neo4j constants 
NEO_URL = 'bolt://localhost:7687'
NEO_DB = 'academicworld'
NEO_PW = 'password'
NEO_UN = 'neo4j'


driver = GraphDatabase.driver(NEO_URL, auth=(NEO_UN, NEO_PW))

query = """USE academicworld MATCH (k:KEYWORD) RETURN k.name as name LIMIT 10"""

# neo4j queries
GET_CLUSTERS = """USE academicworld
MATCH (c:CLUSTER)-[:CONTAINS]->(k)
WITH c, COUNT(k) as keyCount
WHERE keyCount > 1
MATCH (c)-[:CONTAINS]->(k)
WITH c, apoc.text.join(collect(k.name), ', ') as Cluster, keyCount as Keywords
RETURN Cluster, Keywords
ORDER BY Keywords DESC
LIMIT 25"""

GET_SIMILAR_KEYWORDS = """USE academicworld
MATCH (k:KEYWORD {{name:'{name}'}})<-[:LABEL_BY]-(p:PUBLICATION)-[:LABEL_BY]->(:KEYWORD)<-[:CONTAINS]-(c:CLUSTER)
WITH k, count(DISTINCT p) as publication_count, c
MATCH (c)-[:CONTAINS]->(k2)
WITH c, apoc.text.join(collect(k2.name), ', ') as cluster, publication_count
RETURN cluster, publication_count
ORDER BY publication_count DESC
LIMIT 10"""
       

MERGE_CLUSTERS = """USE academicworld
MATCH (k1:KEYWORD{{name:'{name1}'}})<-[:CONTAINS]-(c1:CLUSTER)
MATCH (k2:KEYWORD{{name:'{name2}'}})<-[:CONTAINS]-(c2:CLUSTER)
WITH c1, c2
MATCH (c2)-[:CONTAINS]-(k)
MERGE (c1)-[:CONTAINS]-(k)
DETACH DELETE c2
"""

def try_connect(query):
    try: 
        with driver.session() as session:
            out = list(session.run(query))
    except:
        print('Unable to fetch neo data')
        out = None
    return out


def get_similar_clusters(keyword):
    if not keyword:
        return
    keyword = keyword.strip()
    if not keyword:
        return 
    
    query = GET_SIMILAR_KEYWORDS.format(name=keyword)
    
    return try_connect(query)

def get_largest_clusters():
    return try_connect(GET_CLUSTERS)

def cluster_keywords(keyword_string):
    keywords = list(word.strip() for word in keyword_string.split(','))
    keywords = list(word for word in keywords if word)
    
    #sanitize by removing single quote
    keywords = list(word for word in keywords if not "'" in word)
    if len(keywords) < 2:
        return
    else:
        for i in range(len(keywords)):
            if i == 0:
                continue
            else:
                query = MERGE_CLUSTERS.format(name1=keywords[i-1], name2=keywords[i])
                try_connect(query)
            
    