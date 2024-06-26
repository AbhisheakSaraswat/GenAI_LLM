import os
import sqlite3
from dotenv import load_dotenv
from anthropic import Anthropic
import chainlit as cl
load_dotenv()

# Setup the API Client
client = Anthropic(api_key=os.getenv('api_key'))
MODEL_NAME = 'claude-3-5-sonnet-20240620'

# Define a function to send a wuery to claude and get the response
def ask_claude(query, schema):
    prompt = f"""Here is the schema for database:
    {schema}
    Could you provide a SQL query based on this schema to address the inquiry? Please limit the response to the SQL Query only.
    Question : {query}
    """
    response = client.messages.create(
        model = MODEL_NAME,
        max_tokens=2000,
        messages=[{'role':'user', 'content':prompt}]
    )
    return response.content[0].text

# Function get the database schema
def get_db_schema(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    tables = cursor.fetchall()
    schema_str = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f'PRAGMA table_info({table_name});')
        table_info = cursor.fetchall()
        schema_str += f"CREATE TABLE {table_name} (\n" 
        schema_str += ",\n".join([f"{col[1]} {col[2]}" for col in table_info])
        schema_str += "\n)\n"    
    conn.close()
    return schema_str


# Chainlit UI
@cl.on_message
async def main(message: cl.Message):
    db_path = 'student.db'
    schema_str = get_db_schema('example.db')
    sql_query = ask_claude(message.content, schema_str)
    await cl.Message(
        content=f"**Generated SQL Query:**\n```sql\n{sql_query}\n```"
    ).send()

