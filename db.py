from sqlalchemy import create_engine
from dotenv import load_dotenv
import os 

load_dotenv()

def get_connection():
    try:
        # Dados da conexão
        host = os.getenv("HOST")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        db = os.getenv("DB")
        port = os.getenv("PORT")
        
        # Criar a URL de conexão
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        
        # Usando SQLAlchemy para criar a engine de conexão
        engine = create_engine(connection_string)
        connection = engine.connect()
        
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None