AI Agent for diet management.

Created a simple node express js server and linked it with postgresql database to track the diet of users.

INSTRUCTIONS TO RUN:
Start express js server using command : node index.js 
Start postgresql database server using command : node database.js 
index.js runs on localhost:3000 this is where you can access the UI
(you need to setup database and create a table, according to the schema in database.js file)

go to localhost:3000

you can see the following UI:

<img width="684" alt="image" src="https://github.com/user-attachments/assets/fa77a7fc-dcc1-4400-bd28-814eb8cac965">


Here populate the database, track your meals.

Agent.py has the logic for running the AI agent using LangChain.
edit Agent.py file and paste your LLM api key.

Run the Agent.py file.

The agent prompts you about the diet in terminal.
Here are the results of test run:

<img width="1180" alt="image" src="https://github.com/user-attachments/assets/51a47a00-91d8-47b1-a676-1a27a0c859d2">


I will add more tools to the AI agent so that it can take more complex actions to assist the user better.

