import psycopg2

from sc import secret


def select_item(article):
    article = str(article)
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

    article = str(article)
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    if not check_contains(article):
        item = select_item(article)
        cur.execute("UPDATE vosvrati SET count=%s WHERE article=%s;", (item[6] + 1, article))
    else:
        cur.execute("INSERT INTO vosvrati VALUES (%s, %s, %s, %s, %s, %s, %s);", (name, article, image, stellash, polka, section, 1))
    conn.commit()
    conn.close()


def check_contains(article):

    article = str(article)
    item = select_item(article)
    if item:
        return False
    return True


def delete_item(article):

    article = str(article)
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    item = select_item(article)
    print(item)
    if item[6] > 1:
        cur.execute("UPDATE vosvrati SET count=%s WHERE article=%s", (item[6] - 1, article))
    else:
        cur.execute("DELETE FROM vosvrati WHERE article=%s);", (article))
    conn.commit()
    conn.close()
