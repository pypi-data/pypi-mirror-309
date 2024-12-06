# Start cache using
# docker run --name redis-cache -p 6379:6379 --privileged redis

from llamarch.patterns.layered_caching import LayeredCaching
from llamarch.common.llm import LLM

# Initialize LLMs
large_llm = LLM(model_category="huggingface",
                model_name="distilbert/distilgpt2")
small_llm = LLM(model_category="huggingface",
                model_name="distilbert/distilgpt2")

# Initialize LayeredCaching
layered_caching = LayeredCaching(large_llm, small_llm)

# Define a query for the system
query = "What are the potential impacts of AI?"

# Generate output
output = layered_caching.handle_query(query)
print(output)
