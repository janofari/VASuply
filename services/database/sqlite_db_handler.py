import os
import sqlite3

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

USER_DB_PATH = r"/home/ricardoml95/Documents/GitProjects/VASuply/services/database/users_sqlite.db"


def connect_db():
    try:
        if not os.path.exists(USER_DB_PATH):
            connection = sqlite3.connect(USER_DB_PATH, check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_info
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT UNIQUE NOT NULL,
                                psw TEXT NOT NULL,
                                email TEXT NOT NULL,
                                role TEXT NOT NULL)"""
            )
            # Crear tabla afectados si no existe
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS afectados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        afectado TEXT NOT NULL,
                        ubi TEXT,
                        necesidad TEXT,
                        dni TEXT,
                        tlf INT,
                        dia_alta TEXT,
                        direccion_afectada TEXT,
                        poblacion TEXT,
                        situacion_personal TEXT,
                        dia_visita TEXT
                    )"""
            )
            # Crear tabla enseres si no existe
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS enseres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        enser TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        medidas TEXT,
                        estado TEXT,
                        donante TEXT,
                        agraciado TEXT,
                        tipo TEXT
                    )"""
            )
            connection.commit()
            connection.close()
        connection = sqlite3.connect(USER_DB_PATH, check_same_thread=False)
        return connection
    except Exception as e:
        print(f"Error connecting to SQLite database: {e}")
        return None


def insert_users(collection: str, data: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {collection} (usuario, psw, role, email) VALUES (?, ?, ?, ?)",
        (
            data["usuario"],
            generate_password_hash(data["psw"]),
            data["role"],
            data["email"],
        ),
    )
    connection.commit()
    connection.close()


def select_db(collection: str, query: dict):
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {collection} WHERE usuario = ?", (query["usuario"],))
    result = cursor.fetchall()
    connection.close()
    return result


def update_db(collection: str, data: dict, condition: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE {collection} SET role = ?, email = ? WHERE usuario = ?",
        (data["role"], data["email"], condition["usuario"]),
    )
    connection.commit()
    connection.close()


def delete_db(collection: str, condition: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute(
        f"DELETE FROM {collection} WHERE usuario = ?", (condition["usuario"],)
    )
    connection.commit()
    connection.close()


def validate_user(username: str, psw: str) -> bool:
    connection = connect_db()
    if connection is None:
        return False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_info WHERE usuario = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    if user and check_password_hash(user[2], psw):
        session["logged_in_user"] = username
        session["user_group"] = user[4]
        return True
    return False


def fetch_users():
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT usuario, email, role FROM user_info")
    users = cursor.fetchall()
    connection.close()
    return [{"nombre": user[0], "email": user[1], "rol": user[2]} for user in users]


def insert_afectado(data: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()

    dni = data.get("dni")
    encrypted_dni = generate_password_hash(dni) if dni else None

    cursor.execute(
        "INSERT INTO afectados (afectado, ubi, necesidad, dni, tlf, dia_alta, direccion_afectada, poblacion, situacion_personal, dia_visita) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            data["afectado"],
            data["ubi"],
            data["necesidad"],
            encrypted_dni,
            data["tlf"],
            data.get("dia_alta"),
            data.get("direccion_afectada"),
            data.get("poblacion"),
            data.get("situacion_personal"),
            data.get("dia_visita"),
        ),
    )
    connection.commit()
    connection.close()


def fetch_afectados():
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM afectados")
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "id": row[0],
            "afectado": row[1],
            "ubi": row[2],
            "necesidad": row[3],
            "dni": "****",
            "tlf": row[5],
            "dia_alta": row[6],
            "direccion_afectada": row[7],
            "poblacion": row[8],
            "situacion_personal": row[9],
            "dia_visita": row[10],
        }
        for row in rows
    ]


def search_afectados(name=None, dni=None, tlf=None):
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM afectados WHERE 1=1"
    params = []
    if name:
        query += " AND afectado = ?"
        params.append(name)
    if dni:
        query += " AND dni IS NOT NULL"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        # Filtrar en Python porque el hash no se puede buscar directamente
        rows = [row for row in rows if check_password_hash(row[4], dni)]
    else:
        if tlf:
            query += " AND tlf = ?"
            params.append(tlf)
        cursor.execute(query, params)
        rows = cursor.fetchall()
    connection.close()
    return [
        {
            "id": row[0],
            "afectado": row[1],
            "ubi": row[2],
            "necesidad": row[3],
            "dni": "****",
            "tlf": row[5],
            "dia_alta": row[6],
            "direccion_afectada": row[7],
            "poblacion": row[8],
            "situacion_personal": row[9],
            "dia_visita": row[10],
        }
        for row in rows
    ]


def update_afectado(id, data: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    encrypted_dni = generate_password_hash(data["dni"])
    cursor.execute(
        "UPDATE afectados SET afectado=?, ubi=?, necesidad=?, dni=?, tlf=?, dia_alta=?, direccion_afectada=?, poblacion=?, situacion_personal=?, dia_visita=? WHERE id=?",
        (
            data["afectado"],
            data["ubi"],
            data["necesidad"],
            encrypted_dni,
            data["tlf"],
            data.get("dia_alta"),
            data.get("direccion_afectada"),
            data.get("poblacion"),
            data.get("situacion_personal"),
            data.get("dia_visita"),
            id,
        ),
    )
    connection.commit()
    connection.close()


def delete_afectado(id):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute("DELETE FROM afectados WHERE id=?", (id,))
    connection.commit()
    connection.close()


def insert_enser(data: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO enseres (enser, cantidad, medidas, estado, donante, agraciado, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            data["enser"],
            data["cantidad"],
            data["medidas"],
            data["estado"],
            data["donante"],
            data["agraciado"],
            data.get("tipo"),
        ),
    )
    connection.commit()
    connection.close()


def fetch_enseres():
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM enseres")
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "id": row[0],
            "enser": row[1],
            "cantidad": row[2],
            "medidas": row[3],
            "estado": row[4],
            "donante": row[5],
            "agraciado": row[6],
            "tipo": row[7],
        }
        for row in rows
    ]


def search_enseres(
    enser=None,
    cantidad=None,
    medidas=None,
    estado=None,
    donante=None,
    agraciado=None,
    tipo=None,
):
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM enseres WHERE 1=1"
    params = []
    if enser:
        query += " AND enser = ?"
        params.append(enser)
    if cantidad:
        query += " AND cantidad = ?"
        params.append(cantidad)
    if medidas:
        query += " AND medidas = ?"
        params.append(medidas)
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    if donante:
        query += " AND donante = ?"
        params.append(donante)
    if agraciado:
        query += " AND agraciado = ?"
        params.append(agraciado)
    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "id": row[0],
            "enser": row[1],
            "cantidad": row[2],
            "medidas": row[3],
            "estado": row[4],
            "donante": row[5],
            "agraciado": row[6],
            "tipo": row[7],
        }
        for row in rows
    ]


def update_enser(id, data: dict):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE enseres SET enser=?, cantidad=?, medidas=?, estado=?, donante=?, agraciado=?, tipo=? WHERE id=?",
        (
            data["enser"],
            data["cantidad"],
            data["medidas"],
            data["estado"],
            data["donante"],
            data["agraciado"],
            data.get("tipo"),
            id,
        ),
    )
    connection.commit()
    connection.close()


def delete_enser(id):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute("DELETE FROM enseres WHERE id=?", (id,))
    connection.commit()
    connection.close()
