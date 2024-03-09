import psycopg2
from openai import AzureOpenAI
import sys
from pgvector.psycopg2 import register_vector
import numpy as np
import os



# Setup your AzureOpenAI environment
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

# Register the vector type with your connection cursor
register_vector(conn)

# Create a cursor object to execute SQL queries
cur = conn.cursor()
text = ""

while text != "q":
    # Promp user to enter text to lookup
    text = input("Enter text to lookup (q to quit): ")
    if text == "q":
        break
      
    # Embed the text using Azure OpenAI and extract the vector from the results
    response = client.embeddings.create(
      input = text,
      model= "UPDATE_YOUR_EMBEDDING_MODEL_NAME"
    ).data[0].embedding
    
    # Convert the response to a numpy array
    vector = np.array(response)

    # select text and vector distance from vectoritems table using vector array
    cur.execute('SELECT text, (embedding <-> %s) FROM vector.vectoritems ORDER BY embedding <-> %s LIMIT 10', (vector, vector))
    # Fetch the results
    results = cur.fetchall()
    # Print the results
    for row in results:
        print(row[0], " ", row[1])


# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
