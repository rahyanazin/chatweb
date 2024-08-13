# Talk to your website

This is the project of a Chatbot that allows one to ask questions about the content of a given url.

The project is for demonstration purposes, and it was created to be tested locally.

The repository contains the implementation of two services.

An API that provides endpoints that allows one to chat with the content of a given website,

And an APP that provides a user-friendly interface for interacting with the API.

The API has three endpoints:

- **POST /create-session** : This creates a session and returns its `id`, which can be used in other endpoints, so the API can be aware of the chat history of a session

- **POST /index(url)** - Stores the content of a given `url`

- **POST /ask(url, query, session_id)** - Answers a question (`query`) about the content of a given `url`. If `session_id` is provided, the chat history of the session is considered. Also, it stores the content of the given `url` if it wasn't previously stored.

## Initialization

To initialize both services run the following command

```docker
docker-compose up --build
```

## Usage

Both API and APP ports are exposed to host machine.

After itiniatilizion, the API will be running on http://localhost:8000/docs#, and it is illustraded as bellow:

![image](https://github.com/user-attachments/assets/3ff2008d-33fe-4b8a-887c-efb9873b9f50)

The APP will be running on http://localhost:8501, and bellow there is an animation demonstrating its usage:

![chatweb](https://github.com/user-attachments/assets/a91e575d-b9ac-487c-9f89-5d1b911d4a3e)


