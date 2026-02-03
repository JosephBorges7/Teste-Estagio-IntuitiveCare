from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI(title="API IntuitiveCare - Etapa 4")

# Configuração do CORS (Permite que o seu HTML acesse a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sua conexão, conforme sua senha local
DB_URL = "postgresql://postgres:SUASENHA@localhost:5432/intuitive_db"
engine = create_engine(DB_URL)

@app.get("/")
def home():
    return {"status": "API Online", "docs": "/docs"}

@app.get("/api/agregados")
def listar_agregados():
    """Retorna os dados da tabela de despesas agregadas da Etapa 3"""
    try:
        query = "SELECT * FROM despesas_agregadas"
        df = pd.read_sql(query, engine)
        # Converte o DataFrame para uma lista de dicionários (JSON)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Erro ao acessar o banco: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)