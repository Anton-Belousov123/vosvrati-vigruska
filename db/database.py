import psycopg2

from sc import secret


def select_item(article):
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM vosvrati WHERE article=%s;", (article,))
    el = cur.fetchone()
    conn.close()
    return el


def connect_item(name, article, image, stellash, polka, section):
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO vosvrati VALUES (%s, %s, %s, %s, %s, %s);", (name, article, image, stellash, polka, section))
    conn.commit()
    conn.close()


def check_contains(article):
    item = select_item(article)
    if item:
        return True
    return False


def delete_item(article):
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM vosvrati WHERE article=%s LIMIT 1;", (article))
    conn.commit()
    conn.close()
