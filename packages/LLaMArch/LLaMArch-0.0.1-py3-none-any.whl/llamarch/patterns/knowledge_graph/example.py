# Start basic neo4j server using
# docker run --name neo4j -p 7474:7474 -p 7687:7687 -d \
#   -e NEO4J_AUTH=neo4j/testpassword neo4j:latest

from llamarch.common.llm import LLM
from llamarch.common.graph_db import GraphDB
from llamarch.patterns.knowledge_graph import KnowledgeLLM

kg = GraphDB("bolt://localhost:7687", "neo4j", "testpassword")
llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

sample_text = """
Piazza San Marco, or St. Mark’s Square, is the heart of Venice and a masterpiece of European architecture. Dominated by the magnificent St. Mark’s Basilica, the square is a striking blend of Byzantine and Gothic styles, reflecting Venice’s rich history as a crossroads of Eastern and Western influences. The basilica’s ornate facade shimmers with mosaics and golden domes, while its famous bronze horses gaze out over the piazza, evoking the grandeur of Venice's past.

Flanking the square are the elegant Procuratie buildings, with their long arcades and Renaissance facades, where cafes and shops create a lively atmosphere. The iconic Campanile, or bell tower, rises nearby, offering panoramic views over Venice’s canals and rooftops. Together, these architectural wonders create a timeless scene, making Piazza San Marco a symbol of Venice's beauty and cultural heritage.
"""

knowledge_llm = KnowledgeLLM(kg, llm)
ontology = knowledge_llm.generate_ontology(sample_text)
response = knowledge_llm.respond_to_query(
    "What are the main architectural features of Piazza San Marco?")
kg.close()
