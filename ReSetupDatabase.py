import sqlite3
import tkinter as tk
from tkinter import messagebox as msg


# !!!!!!!!!!!!!!!!!!!!!!!!
# If you have Movies.db, do not run this code.
# The original Movies.db has some film datas.
# This code is for resetting the database.
# !!!!!!!!!!!!!!!!!!!!!!!!



def get_db_connection():
    return sqlite3.connect("movies.db")


def create_db_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS User (
                uid   INTEGER PRIMARY KEY AUTOINCREMENT,
                userName TEXT,
                userPassword TEXT

            );
            """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Directors (
            d_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            d_name TEXT   
        );""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Films(
            film_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            tr_title TEXT,
            en_title TEXT,
            tr_desc TEXT,
            en_desc TEXT,
            image BLOB,
            imdb NUMERIC,
            d_ID INTEGER,
            year INTEGER

        );""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Actors(
            actor_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_name TEXT

        );""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS FilmActor(
            actor_ID  INTEGER,
            film_ID  INTEGER

        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Categories(
            c_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            c_trName TEXT,
            c_enName TEXT

        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS FilmCategory (
            c_ID  INTEGER,
            film_ID  INTEGER

        );""")
        '''
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Directors(
            d_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            d_name TEXT   
        );

        CREATE TABLE IF NOT EXISTS Films (
            film_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            tr_title TEXT,
            en_title TEXT,
            tr_desc TEXT,
            en_desc TEXT,
            image BLOB,
            imdb NUMERIC,
            d_ID INTEGER

        );
        CREATE TABLE IF NOT EXISTS Actors (
            actor_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_name TEXT

        );

        CREATE TABLE IF NOT EXISTS FilmActor(
            actor_ID  INTEGER ,
            film_ID  INTEGER

        );

        CREATE TABLE IF NOT EXISTS Categories(
            c_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
            c_trName TEXT,
            c_enName TEXT

        );

        CREATE TABLE IF NOT EXISTS FilmCategory (
            c_ID  INTEGER,
            film_ID  INTEGER

        );

        """)
        '''
        conn.commit()
        conn.close()
        msg.showinfo("Setup Database", "Database table created.")
    except Exception as exc:
        msg.showerror("Error", "Error: " + str(exc))


create_db_table()


def insert_category_table(tr, en):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Categories (c_trName, c_enName) VALUES (:ctr,:cen)",
                    {"ctr": tr,
                     "cen": en})
        conn.commit()
        conn.close()
        # msg.showinfo("Done", "Insert successful")

    except Exception as exc:
        msg.showerror("Error", "Error: " + str(exc))


insert_category_table("Aksiyon", "Action")
insert_category_table("Animasyon", "Animation")
insert_category_table("Korku", "Horror")
insert_category_table("Komedi", "Comedy")
insert_category_table("Suç", "Crime")
insert_category_table("Dram", "Drama")
insert_category_table("Macera", "Adventure")
insert_category_table("Bilim-Kurgu", "Sci-Fi")
insert_category_table("Gizem", "Mystery")
insert_category_table("Romantik", "Romance")
insert_category_table("Fantastik", "Fantasy")
insert_category_table("Süper Kahraman", "Superhero")
