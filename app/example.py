from app.chat import ChatWebClient

chatweb = ChatWebClient()

chatweb.update("https://en.wikipedia.org/wiki/Brazil")

print(chatweb.ask("What is the population of Brazil?"))

print(chatweb.ask("when was the Treaty of Tordesillas?"))

chatweb.update("https://lilianweng.github.io/posts/2023-06-23-agent/")

print(chatweb.ask("What is Task Decomposition?"))

print(chatweb.ask("What are common ways of doing it?"))

print(chatweb.ask("How many world cups brazil have in soccer?"))

chatweb.update("https://neofeed.com.br/negocios/kruglensky-diz-que-fica/")

print(chatweb.ask("o que diz essa notícia?"))

chatweb
