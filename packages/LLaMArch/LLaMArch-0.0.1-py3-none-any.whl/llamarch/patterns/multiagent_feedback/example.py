from copy import deepcopy
from llamarch.common.base_agent import AgentResponse, GenerativeAIAgent
from llamarch.common.llm import LLM
from llamarch.patterns.multiagent_feedback import MultiAgentModel

NUM_AGENTS = 3

# Create agents
llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")
# Initialize Generative AI Agents with different model names
agent_list = [GenerativeAIAgent(agent_id=i, llm=llm)
              for i in range(NUM_AGENTS)]

# Initialize the multi-agent model
multiagent_model = MultiAgentModel(agent_list)

# Process a query
query = "What is the best way to train a model for natural language processing?"
output = multiagent_model.process_query(query)
print(output)
