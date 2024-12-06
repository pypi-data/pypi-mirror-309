
from app.conn_wizard.src.connection_utility import (
    load_connections,
    choose_connection
)

from sqlalchemy import create_engine
import pandas as pd

def main():
    connections = load_connections() 
    conn = choose_connection(connections) 

    engine = create_engine(conn)
    query = input("Input your query: ")
    df = pd.read_sql_query(query, engine)
    print(df)
     

if __name__ == "__main__":
    main() 


