import random
import threading
import time
import queue

class Main:
    def producent(queue):
        print("Producent komponent začal")

        komponenty = ["C1", "C2", "C3"]

        while True:
            for komponent in komponenty:
                queue.put(komponent)
                print(f"Dodani komponentu: {komponent}")
                time.sleep(0.3)

    def konzument(queue):
        vyrobeno = 0

        while True:
            komponent = queue.get()

            if komponent is None:
                break

            print(f"Prijeto komponentu: {komponent}")
            time.sleep(0.7)  # simulace výroby

            zarizeni = f"Device-{komponent}"
            vyrobeno += 1

            print(f"Vyrobeno zarizeni: {zarizeni} (celkem kusu: {vyrobeno})")

            # Po vyrobení 10 zařízení ukončíme proces
            if vyrobeno >= 10:
                queue.put(None)
                break

        print("Konec vyroby")

    if __name__ == "__main__":
        queue = queue.Queue()

        t_producent = threading.Thread(target=producent, args=(queue,))
        t_konzument = threading.Thread(target=konzument, args=(queue,))

        t_konzument.start()
        t_producent.start()

        t_konzument.join()