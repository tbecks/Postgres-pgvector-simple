import psycopg2
from openai import AzureOpenAI
import sys
import os

# Setup your OpenAI environment
client = AzureOpenAI(
    api_key = os.getenv("UPDATE_AZURE_OPENAI_API_KEY")
    # example: api_key="baba43ad7df1djejdu928737553bfc24aa",
    azure_endpoint="UPDATE_AZURE_OPENAI_ENDPOINT",
    # example: azure_endpoint="https://beckeropenai.openai.azure.com/",
    api_version="2023-07-01-preview"
)



# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
  host="UPDATE_YOUR_POSTGRES_HOST",
  # example: host="beckerflex.postgres.database.azure.com",
  database="UPDATE_YOUR_POSTGRES_DATABASE",
  user="UPDATE_YOUR_POSTGRES_USER",
  password=os.environ['VECTOR_PG_PASSWORD'] 
  # example: export VECTOR_PG_PASSWORD=yourpassword or in windows set VECTOR_PG_PASSWORD=yourpassword
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()
text = ""

# Loop through until user quits
while text != "q":
    # Promp user to enter text to embed
    text = input("Enter text to embed (q to quit): ")
    if text == "q":
        break
    # Embed the text using Azure OpenAI
    response = client.embeddings.create(
      input = text,
      model= "BeckerEmbedding"
    ).data[0].embedding

    # Insert the text and its embedding into the vector table
    cur.execute("""
      INSERT INTO vector.vectoritems (text, embedding)
      VALUES (%s, %s) ON CONFLICT (text) DO UPDATE SET embedding = EXCLUDED.embedding;
    """, (text, response))

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

# print("Results: Text:",text," Embedding: ",embeddings)
print("All added!")