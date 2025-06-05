from ariadne import gql, QueryType, make_executable_schema
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        ping: String!
    }
""")

query = QueryType()

@query.field("ping")
def resolve_ping(_, info):
    return "pong"

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
