import random
import threading
import time
import queue


def dodavatel(queue_komponent):
    print("Producent komponent začal")

    komponenty = ["K1", "K2", "K3"]

    #kontrola plnosti skladu
    while True:
        for komponent in komponenty:
            if queue_komponent.full():
                while queue_komponent.full():
                    time.sleep(0.2)

            queue_komponent.put(komponent)
            print(f"Dodani komponentu: {komponent}")
            time.sleep(0.2) #Vyroba

def vyroba(queue_komponent, queue_finished):
    while True:
        komponent = queue_komponent.get()
        print(f"Prijat komponent: {komponent}")

        time.sleep(1)

        product = f"Device-{komponent}"

        if queue_finished.full():
            print('Sklad na hotove vyrobky plny')
            while queue_finished.full():
                time.sleep(0.2)

        queue_finished.put(product)

def shop(queue_products, shop_capacity):
    sold = 0
    sklad = []

    while True:
        product = queue_products.get()

        if len(sklad) >= shop_capacity:
            while len(sklad) >= shop_capacity:
                time.sleep(0.2)

        sklad.append(product)
        time.sleep(2)
        print(f'\nProdan produkt: {product}\n')
        sklad.pop()
        sold += 1

        queue_products.task_done()
        if sold >= 10:
            print('Dosazena denni kapacita obchodu')
            break



if __name__ == "__main__":
    komponent = queue.Queue(maxsize=1)
    finished_product = queue.Queue(maxsize=1)
    shop_capacity = 1

    vyrobce_komponent = threading.Thread(target=dodavatel, args=(komponent,))
    produkce_Vyrobku = threading.Thread(target=vyroba, args=(komponent, finished_product,))
    obchod = threading.Thread(target=shop, args=(finished_product, shop_capacity,))

    vyrobce_komponent.start()
    produkce_Vyrobku.start()
    obchod.start()

    obchod.join()