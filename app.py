
import os
import psycopg
from flask import Flask, render_template

app = Flask(__name__)

def consultar_banco():
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_database(),
                    current_user,
                    current_timestamp
            """)
            return cur.fetchone()

@app.route("/")
def index():
    try:
        dados = consultar_banco()
        return render_template(
            "index.html",
            conectado=True,
            banco=dados[0],
            usuario=dados[1],
            horario=dados[2],
            erro=None
        )
    except Exception as e:
        return render_template(
            "index.html",
            conectado=False,
            banco=None,
            usuario=None,
            horario=None,
            erro=str(e)
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
