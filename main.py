import os

def emptyFileFinder(path, removeFolder):
    empty = []
    for root, dirs, files in os.walk(path, topdown=False):
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
    removeFolder = False

    if not os.path.isdir(path):
        print("To neni platna cesta")
    else:
        findEmpty = emptyFileFinder(path, removeFolder)

        print("\nPrazdne slozky:")
        for slozka in findEmpty:
            print(slozka)

        print("\nKonec.")
