import os

import logging

def emptyFileFinder(path, removeFolder):
    empty = []
    for root, dirs, files in os.walk(path, topdown=True):
        if not dirs and not files:
            empty.append(root)

            logging.info(f"Found empty file: {root}")

            if removeFolder is True:
                try:
                    os.rmdir(root)
                    logging.info(f"Erased file: {root}")
                except Exception as e:
                    logging.error(f"Not able to delete {root}: {e}")
                    print('Nelze smazat')
    return empty

logging.basicConfig(filename="log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

if __name__ == "__main__":
    path = input('Zadej cestu pro hledani prazdnych slozek: ').strip()

    removeFolder = input(f"Chceš smazat prázdré složky z {path} (ano/ne)? ").strip().lower()

    isRemoveFolder = removeFolder in ("true", "yes", "ano", "y")

    if not os.path.isdir(path):
        print("Neplatna cesta.")
        logging.error(f"User's incorrect path: {path}")
    else:
        logging.info(f"Starting searching paths: {path}")
        logging.info(f"Erasing: {isRemoveFolder}")

        findEmpty = emptyFileFinder(path, removeFolder)

        print("\nPrazdne slozky:")
        for slozka in findEmpty:
            print(slozka)

        print("\nKonec.")
        logging.info("End\n")
