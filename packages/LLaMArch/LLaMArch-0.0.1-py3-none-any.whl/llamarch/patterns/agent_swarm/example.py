import os
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding

from llamarch.common.base_agent import GenerativeAIAgent
from llamarch.patterns.agent_swarm import AgentSwarm

llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

embedding = LLMEmbedding(model_category="huggingface",
                         embedding_model_name="distilbert-base-uncased")

NUM_AGENTS = 3

# Initialize Generative AI Agents with different model names
agent_list = [GenerativeAIAgent(agent_id=i, llm=llm, embedding=embedding)
              for i in range(NUM_AGENTS)]

# Define a query for the system
query = "What are the potential impacts of AI on the job market over the next decade?"

# Create agent swarm
agent_swarm = AgentSwarm(agent_list)

# Generate output
output = agent_swarm.run_iteration(query)
print(output)
