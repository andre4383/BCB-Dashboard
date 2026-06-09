from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sqlalchemy import create_engine
import uvicorn

app = FastAPI(title="BCB Dashboard API")

# Configure CORS to allow our React app to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins to prevent CORS issues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DB_URL = "postgresql://postgres:postgres@localhost:5432/bcb_dashboard"
engine = create_engine(DB_URL)

@app.get("/api/dados")
def get_dados():
    try:
        # Ler a tabela inteira
        df = pd.read_sql('SELECT * FROM silver_meios_pagamento', engine)
        
        # Converter todas as colunas de data para string e tratar NaNs
        # Isso garante que o JSON fique perfeitamente formatado para o React
        if 'datatrimestre' in df.columns:
            df['datatrimestre'] = df['datatrimestre'].dt.strftime('%Y-%m-%d')
        
        df = df.fillna(0) # Substituir NaNs por 0
        
        # Retornar como lista de dicionários
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
