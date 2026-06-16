import zipfile
import sys

def find_flag(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        for i in range(1, 101):
            for j in range(1, 101):
                for k in range(1, 11):
                    filename = f"dir_{i}/sub_{j}/data_{k}.txt"

                    try:
                        data = z.read(filename)
                        if data != b'System nominal. Sector clear.':
                            print(data)
                    except KeyError:
                        continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} challenge.zip")
        sys.exit(1)

    find_flag(sys.argv[1])