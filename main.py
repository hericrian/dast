import sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()


def init_db():
    conn = sqlite3.connect("universidade.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS alunos (id INTEGER, nome TEXT, nota REAL, segredo TEXT)"
    )
    cursor.execute("DELETE FROM alunos")
    cursor.execute("INSERT INTO alunos VALUES (1, 'Ana', 9.5, 'SenhaAdmin123')")
    cursor.execute("INSERT INTO alunos VALUES (2, 'Carlos', 7.0, 'SenhaUser456')")
    conn.commit()
    conn.close()


init_db()


@app.get("/", response_class=HTMLResponse)
def index(busca: str = Query(default="")):
    html_content = f"""
    <html>
        <body>
            <h1>Portal de Notas</h1>
            <p>Você buscou por: <b>{busca}</b></p>
            <form method="GET" action="/buscar">
                <input type="text" name="aluno" placeholder="Nome do aluno">
                <button type="submit">Buscar Notas</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/buscar")
def buscar_aluno(aluno: str):
    conn = sqlite3.connect("universidade.db")
    cursor = conn.cursor()

    query = f"SELECT nome, nota FROM alunos WHERE nome = '{aluno}'"

    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        return {"resultados": resultados, "query_executada": query}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
