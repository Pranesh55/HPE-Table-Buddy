from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


transport = AIOHTTPTransport(url="https://api.mocki.io/v2/c4d7a195/graphql", )

client = Client(transport=transport)


products_query = gql("""
  {
      users{
          name
      }
  }
""")
response = client.execute(products_query)
print(response)