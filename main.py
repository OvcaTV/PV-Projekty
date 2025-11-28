import os

def emptyFileFinder(cesta, removeFolder):
    empty = []
    for root, dirs, files in os.walk(cesta, topdown=False):
        if not dirs and not files:
            empty.append(root)

            if removeFolder is True:
                try:
                    os.rmdir(root)
                except Exception as e:
                    print('Nelze smazat')
    return empty


path = "C:\\Users\\hryma\\Downloads"
removeFolder = True
findEmpty = emptyFileFinder(path, removeFolder)


print("Prazdne slozky:")
for slozka in findEmpty:
    print(slozka)

if __name__ == "__main__":
    print("")