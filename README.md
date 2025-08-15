# Technical Test
Candidate: Alfonso Ardoiz  
Date: 15/08/2025

# Project Overview
A small assistant for the technical test.

The project I decided to build consists of an assistant with three functionalities: retrieving papers from arXiv, querying a couple of pages from LangChain’s documentation, and handling generic requests.

As expected, all functionalities could be improved further, and I reached the point that time allowed.

> The reason behind this project—the retrieval of papers from arXiv by querying an external API—was something I had pending as a personal project, and I decided to take the opportunity... 😎

# Flow

![Flow Image](docs/internal_flow.png)

# Components

## 1. Docker
The assistant is deployed within a Docker container that merges three services:
  - The assistant’s backend
  - A vector database (Qdrant) with three web pages from LangChain’s documentation
  - A MongoDB instance to store user interactions and manage history

For this, a small docker-compose file was used where the folder accessed by both Qdrant and Mongo is linked via a volume, and the corresponding ports are assigned.  
> Important! The local port for Mongo can be changed. In my case, port 27017 was occupied, so I had to use 27018.

## 2. API
The backend is structured into two separate folders by functionality—on one side, the assistant code (src), and on the other, all API-related code (apps).

It includes a boot file that acts as the “engine” to start the assistant’s code, and then a small API with two endpoints: the chat view and, by default, a health view.

To interact with the chat, one must send an `AssistantInput` that has two required fields: the user's "query" and the "chat_id". This object is defined in schemas/models.

Finally, the apps folder also includes the Mongo functionalities. This way, the assistant code is solely responsible for content generation.

## 3. Code
This is the core of the technical test. Initially, I organized everything within the chat, pulling out globally used components such as settings and the logger.

Regarding the code, there is an orchestrator file `core.py` and three subfolders. This file serves as the core and orchestrates the sequence of each inference.

Within the domain folder, I have defined the system’s specific classes and objects, dividing them into subfolders for each specific functionality. As a special mention, inside `domain/generation/langchain_conversor.py` there is a converter I created specifically to interchange LangChain code with pure code using the OpenAI library.

---

Within the generation folder, all functionalities related to the agents are included, as well as the specific classes I created for Azure/LangChain. In the end, I aimed to isolate the main inference method from the agent’s message handling.

Regarding the agents, I included the following:
- Reformulator: It is responsible for improving the user’s query using the previous conversation. For example, if a user asks, "Best restaurant in Madrid," and then follows up with, "And in Valencia?", what they are really asking is "Best restaurant in Valencia." This agent is a prototype I am testing, and for this technical test I thought it interesting to include.
- IR-Reformulator: A specific agent for arXiv searches. It transforms a query like "Recent papers on LLMs" into the central topic -> "LLMs," thereby improving the IR system.
- Planner: Plans which agents/flow to follow next during inference. It is provided with the assistant’s context and chooses the pathway based on the user’s query. (The downside of this agent is how I implemented the subsequent code call…)
- Assistant: A general agent for content verbalization. I structured the code such that, whichever path is selected by the planner, the assistant uses the query and context to respond to the user. If it’s a general question, there is no context; if it’s a call to the arXiv API, it will be a set of papers; and if it’s the RAG itself, it will be a document from LangChain’s documentation.

Additionally, besides the agents, I created a main class to manage calls to the OpenAI model (specifically gpt4o).

This class could have been defined as an LLM in an abstract class in another file, but to keep things simple I decided to implement it directly in two classes: `AzureClient` and `LangChainAzure`.  
Both classes include a method to generate text and another to generate embeddings (unfortunately, I did not have time to adapt the LC one for the latter).

The idea behind this separation of Agents/Client is to distribute functionalities and properly manage dependencies. If we abstract away the agents’ function, we see that all they do is prepare the message list in a certain manner, and then it is the client that calls Azure with the text generation function and the list of messages.

---

Finally, the searches folder includes the code for calling an external API and for the RAG.

- Arxiv: Makes a GET request to the public API of this scientific article repository. I hardcoded it to always use the latest papers relative to the made query, but I hope that is sufficient for this technical test.
- Qdrant: Connects to the vector database to use documents as context for RAG. It’s a bit unfortunate because there are only three documents in the DB.

---

> For both the agents and the searches, custom objects (`TextResponse` and `SearchResponse`) are returned. These will be used to construct the object returned by the API described above and to store the inference in the database.

## 4. Mongo

Used for managing user history internally as well as persisting API usage in a database.

In short, an object (document) has been defined that will be uploaded to Mongo, along with a couple of methods to insert/update the document.

Defining custom objects beforehand allows us to select exactly what we want to save from each: execution times, document references (title and score), costs of each agent, intermediate artifacts...

## 5. Library Management, Environment Variables, and Bash Commands

Library management has been handled using Poetry.

Pre-commit has been used for code cleanup.

The variables are stored in the .env file and pydantic_settings is used to access them in the code.

Additionally, a Makefile has been included with the most convenient commands for the system (Docker and API-related tasks).

# Running the Program

IMPORTANT! :boom:  
> Azure credentials must be included in the .env file

Simply by being in Docker and running the command:
----------------------------------------------------
make build
----------------------------------------------------
the project’s containers are built and launched.

# TODO

- [x] Make the API functional
- [x] Add functionalities in LangChain
- [x] Create a README with the documentation
- [x] Add a diagram of the components
---