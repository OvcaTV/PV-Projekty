
if __name__ == "__main__":
    from config import get_connection
    try:
        conn = get_connection()
        print("Připojení k databázi úspěšné")
        conn.close()
    except Exception as e:
        print("Chyba připojení:", e)
