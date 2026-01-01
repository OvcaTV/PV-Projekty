
if __name__ == "__main__":
    from config import get_connection
    try:
        conn = get_connection()
        print("Připojení k databázi úspěšné")
        conn.close()
    except Exception as e:
        print("Chyba připojení:", e)

    from dao import ProductDAO
    from dao import ProductionOrderDAO

    product_dao = ProductDAO()
    order_dao = ProductionOrderDAO()

    product_dao.insert("Copper Sheet", 8.4)

    orders = order_dao.get_all()
    for o in orders:
        print(o)

    product_dao.close()
    order_dao.close()