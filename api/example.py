from api import chat

session_id = chat.create_session()

url = "https://en.wikipedia.org/wiki/Brazil"

chat.index("https://en.wikipedia.org/wiki/Brazil")

print(chat.ask(url, "What is the population of Brazil?", session_id))

print(chat.ask(url, "when was the Treaty of Tordesillas?", session_id))


# chatweb.update("https://lilianweng.github.io/posts/2023-06-23-agent/")

# print(chatweb.ask("What is Task Decomposition?"))

# print(chatweb.ask("What are common ways of doing it?"))

# print(chatweb.ask("How many world cups brazil have in soccer?"))

# chatweb.update("https://neofeed.com.br/negocios/kruglensky-diz-que-fica/")

# print(chatweb.ask("o que diz essa notícia?"))

# chatweb

url