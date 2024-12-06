# Import memory and Qdrant components
from .short_term_memory import ShortTermMemory
from .long_term_memory import LongTermMemory
from .summarizer import Summarizer  # Summarizer component
from .memory_decay import MemoryDecay  # Memory evaluation and decay component
# Your VectorDB class that supports Qdrant
from llamarch.common.vector_db import VectorDB
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding  # Embedding class
from llamarch.patterns.memory_cognition import MemoryCognition

# Initialize the embedding model
embedding = LLMEmbedding(
    model_category="huggingface", embedding_model_name="distilbert-base-uncased"
)

# Initialize the LLM class
llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

# Initialize Qdrant clients for Short-Term Memory and Long-Term Memory
stm_client = VectorDB(
    db_type="qdrant", environment="http://localhost:6333", index_name="short_term_memory", embedding_model=embedding.embedding_model
)
ltm_client = VectorDB(
    db_type="qdrant", environment="http://localhost:6333", index_name="long_term_memory", embedding_model=embedding.embedding_model
)

# Initialize memory modules
short_term_memory = ShortTermMemory(stm_client)
long_term_memory = LongTermMemory(ltm_client)
summarizer = Summarizer(llm)  # Summarizer component
memory_decay = MemoryDecay()  # Memory evaluation and decay component


# Example data
query = "Example query text"
query_vector = embedding.get_embeddings(query)

# Create a MemoryCognition object
memory_cognitive = MemoryCognition(
    llm=llm,
    embedding=embedding,
    short_term_memory=short_term_memory,
    long_term_memory=long_term_memory,
    summarizer=summarizer,
    memory_decay=memory_decay
)

# Step 1: Store query in Short-Term Memory
memory_cognitive.store_information(query, query_vector)

# Step 2: Retrieve similar items from Short-Term Memory
similar_items_stm = memory_cognitive.fetch_similar(query_vector)

# Step 3: Summarize similar items from STM
summary = memory_cognitive.summarize(similar_items_stm)

# Step 4: Evaluate if the summarized information should be stored in Long-Term Memory
if memory_cognitive.evaluate(summary):
    # Step 5: If evaluation passes, flush summarized information to Long-Term Memory
    memory_cognitive.flush_to_long_term(long_term_memory)

# Step 6: Fetch similar items from Long-Term Memory for future queries
long_term_results = memory_cognitive.fetch_similar_from_long_term(query_vector)
