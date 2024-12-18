from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Configuração inicial do app Flask
app = Flask(__name__)

# Configuração do banco de dados
def setup_database():
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lista_id INTEGER NOT NULL,
        produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,
        concluido INTEGER DEFAULT 0,
        FOREIGN KEY (lista_id) REFERENCES listas (id)
    )""")
    conn.commit()
    return conn

# Página inicial para exibir listas
@app.route("/")
def index():
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM listas")
    listas = cursor.fetchall()
    conn.close()
    return render_template("index.html", listas=listas)

# Criar uma nova lista
@app.route("/criar_lista", methods=["POST"])
def criar_lista():
    nome = request.form["nome"]
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO listas (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Exibir itens de uma lista
@app.route("/lista/<int:lista_id>")
def visualizar_lista(lista_id):
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM listas WHERE id = ?", (lista_id,))
    lista = cursor.fetchone()
    cursor.execute("SELECT * FROM itens WHERE lista_id = ?", (lista_id,))
    itens = cursor.fetchall()
    conn.close()
    return render_template("lista.html", lista=lista, itens=itens)

# Adicionar item a uma lista
@app.route("/adicionar_item/<int:lista_id>", methods=["POST"])
def adicionar_item(lista_id):
    produto = request.form["produto"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO itens (lista_id, produto, quantidade, preco) 
    VALUES (?, ?, ?, ?)""", (lista_id, produto, int(quantidade), float(preco)))
    conn.commit()
    conn.close()
    return redirect(url_for("visualizar_lista", lista_id=lista_id))

# Marcar item como concluído
@app.route("/concluir_item/<int:item_id>/<int:lista_id>")
def concluir_item(item_id, lista_id):
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE itens SET concluido = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("visualizar_lista", lista_id=lista_id))

# Excluir item
@app.route("/excluir_item/<int:item_id>/<int:lista_id>")
def excluir_item(item_id, lista_id):
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("visualizar_lista", lista_id=lista_id))

# Excluir lista
@app.route("/excluir_lista/<int:lista_id>")
def excluir_lista(lista_id):
    conn = sqlite3.connect("lista_compras.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itens WHERE lista_id = ?", (lista_id,))
    cursor.execute("DELETE FROM listas WHERE id = ?", (lista_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    setup_database()
    app.run(debug=True, port=8000)
