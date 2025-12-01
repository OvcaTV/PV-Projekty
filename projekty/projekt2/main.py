import os

def emptyFileFinder(path, removeFolder):
    empty = []
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty.append(root)

            if removeFolder is True:
                try:
                    os.rmdir(root)
                except Exception as e:
                    print('Nelze smazat')
    return empty



if __name__ == "__main__":
    path = input('Zadej cestu pro hledani prazdnych slozek: ').strip()

    removeFolder = input(f"Chceš smazat prázdré složky z {path}? ").strip().lower()

    isRemoveFolder = removeFolder in ("true", "yes", "ano", "y")

    if not os.path.isdir(path):
        print("Neplatna cesta.")
    else:
        findEmpty = emptyFileFinder(path, isRemoveFolder)

        print("\nPrazdne slozky:")
        for slozka in findEmpty:
            print(slozka)

        print("\nKonec.")
