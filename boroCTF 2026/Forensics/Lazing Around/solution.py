import zipfile
import re
import sys
import struct

# superblock
def get_block_size(img):
    log_block_size = struct.unpack_from("<I", img, 1024 + 0x18)[0]
    return 1024 << log_block_size # block size = 1024 * 2^log_block_size

def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <raw_image> <mnt.zip>")
        sys.exit(1)

    img_path = sys.argv[1]
    zip_path = sys.argv[2]

    img = open(img_path, "rb").read()
    block_size = get_block_size(img)

    print(f"[+] block size = {block_size}")

    frags = []

    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if not re.search(r"(entry|exit)_log_\d+\.txt$", name):
                continue

            content = z.read(name)

            pos = img.find(content)
            if pos == -1:
                continue
            
            # align to the end of the block
            end = ((pos + len(content) + block_size - 1) // block_size) * block_size

            # data after the content until the end of the block
            slack = img[pos + len(content):end]
            slack = slack.rstrip(b"\x00")

            if slack:
                frags.append((pos, name, slack))

    frags.sort()

    flag = b""

    for pos, name, slack in frags:
        print(f"[+] offset={pos:<8} {name:<20} slack={slack!r}")
        flag += slack

    print()
    print("[+] flag =", flag.decode())


if __name__ == "__main__":
    main()