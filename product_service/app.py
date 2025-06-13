from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema
from resolvers import resolvers
from database import init_db
import uvicorn

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, resolvers)

graphql_app = GraphQL(
    schema, 
    debug=True,
    introspection=True
)

app = FastAPI(title="Product Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def graphql_playground():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Service - GraphQL Playground</title>
        <style>
            body { height: 100%; margin: 0; width: 100%; overflow: hidden; }
            #graphiql { height: 100vh; }
        </style>
        <script crossorigin src="https://unpkg.com/react@17/umd/react.development.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
        <script crossorigin src="https://unpkg.com/graphiql/graphiql.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/graphiql/graphiql.min.css" />
    </head>
    <body>
        <div id="graphiql">Loading...</div>
        <script>
            function fetcher(graphQLParams) {
                return fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(graphQLParams),
                }).then(response => response.json());
            }
            
            ReactDOM.render(
                React.createElement(GraphiQL, { 
                    fetcher: fetcher,
                    defaultQuery: `query GetProducts {
  products {
    id
    name
    unit
    quantity
  }
  
  rawMaterials {
    id
    livestock_type
    quantity
    received_at
  }
}

mutation CreateProduct {
  createProduct(
    name: "Beef Steak"
    unit: "kg"
    quantity: 100
  ) {
    id
    name
    unit
    quantity
  }
}`
                }),
                document.getElementById('graphiql')
            );
        </script>
    </body>
    </html>
    """

app.mount("/graphql", graphql_app)

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Product Service - DB initialized")
    print("GraphQL Playground available at: http://localhost:8003/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)