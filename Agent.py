import os
import psycopg2
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import date, timedelta
from langchain.chains import LLMChain
from langchain_core.pydantic_v1 import BaseModel, Field





# Set up the database connection
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres1",
    password="postgres",
    host="localhost",
    port="5432"
)

# Set up the LLM
os.environ["TOGETHER_API_KEY"] = "Your API KEY"
llm = ChatOpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.environ["TOGETHER_API_KEY"],
    #model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
)
memory = ConversationBufferMemory()

# Tool to get data between date ranges
def get_diet_data(date_range: str) -> str:
    start_date, end_date = date_range.split(',')
    cur = conn.cursor()
    query = "SELECT * FROM diet WHERE time BETWEEN %s AND %s;"
    cur.execute(query, (start_date.strip(), end_date.strip()))
    results = cur.fetchall()
    cur.close()
    return str(results)

def freedom_sql(query):
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return str(results)
def get_day(x):
    return str(date.today() + timedelta(days=int(x)))

def do_nothing(x):
    return "answer the question user asked."

tools = [
    Tool(
        name="DietDataRetrieval",
        func=get_diet_data,
        description="Useful for getting diet data between two unique dates. Input should be two dates in the format 'YYYY-MM-DD HH:MI,YYYY-MM-DD HH:MI'."
    ),
    Tool(
        name="getDate",
        func=get_day,
        description="Will tell you what today's date is. Input an integer, if input = 0, it will return today's date, -1 will return yesterdays date, it is timedelta for days"
    ),
    Tool(
        name ='''query from diet table
''',
        func=freedom_sql,
        description='''Send the entire SQL query string to retreive required information from diet table., The schema of diet table is,
                Table diet
                id :integer                    
                food : character varying(255)    
                time  : timestamp without time zone
                type   :character varying(10) 
        
        '''


    ),
    
]

# Set up the prompt template
template = """
The user logs all his diet in diet table. The schema of diet table is,
Table diet
 Column |            Type             | Collation | Nullable |             Default              
--------+-----------------------------+-----------+----------+----------------------------------
 id     | integer                     |           | not null | nextval('diet_id_seq'::regclass)
 food   | character varying(255)      |           |          | 
 time   | timestamp without time zone |           |          | 
 type   | character varying(10)       |           |          | 


Answer the following questions as best you can.You have access to the following tools:


{tools}

Use the following format:

Question: the input question you must answer.
Thought: Always think about what information you have, what information you need, take action based on that
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate(
    template=template,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
)

# Set up the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

class Classify(BaseModel):
    requires_database: str = Field(...,description="Is the question related to diet? Just answer Yes or No? ", enum=["Yes", "No"])
# Function to process user requests
def process_request(user_input: str):
    return agent.run(user_input)
    # Check if the request requires historical data
    # requires_db = llm.with_structured_output(Classify).invoke(user_input).requires_database
    # if requires_db == 'Yes':
    #     return agent.run(user_input)
    # chain = LLMChain(llm=llm,prompt=PromptTemplate(template=user_input,input=[]), memory=memory)
    # return chain.invoke({"input":user_input})
    

# Main loop
if __name__ == "__main__":
    while True:
        user_input = input("Ask about your diet (or type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        response = process_request(user_input)
        print(response)
        print(memory)

# Close the database connection
conn.close()
