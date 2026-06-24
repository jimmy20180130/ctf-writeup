from pwn import *

context.log_level = "info"

HOST, PORT = "162.243.83.113", 9000

DIRS = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]


def parse_grid(data):
    lines = [line.strip() for line in data.decode(errors="ignore").splitlines() if line.strip()]

    i = next(i for i, line in enumerate(lines) if line.startswith("GRID"))
    n = int(lines[i].split()[1])

    return [
        list(map(int, lines[i + 1 + r].split()))
        for r in range(n)
    ]


def solve(grid):
    n = len(grid)
    m = n * n
    mat = []

    for r in range(n):
        for c in range(n):
            mask = 0

            for dr, dc in DIRS:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    mask ^= 1 << (rr * n + cc)

            mat.append(mask | (grid[r][c] << m))

    where = [-1] * m
    row = 0

    for col in range(m):
        pivot = next(
            (i for i in range(row, m) if (mat[i] >> col) & 1),
            None
        )

        if pivot is None:
            continue

        mat[row], mat[pivot] = mat[pivot], mat[row]
        where[col] = row

        for i in range(m):
            if i != row and ((mat[i] >> col) & 1):
                mat[i] ^= mat[row]

        row += 1

    presses = []

    for cell in range(m):
        if where[cell] != -1:
            value = (mat[where[cell]] >> m) & 1
            if value:
                presses.append((cell // n, cell % n))

    return presses


io = remote(HOST, PORT)

for _ in range(20):
    data = io.recvuntil(b"AWAITING SOLUTION", timeout=10)
    grid = parse_grid(data)
    io.info(f"Solving chamber {_+1} (size={len(grid)}x{len(grid)})")
    presses = solve(grid)

    io.sendline(f"PRESSES {len(presses)}".encode())

    for r, c in presses:
        io.sendline(f"{r} {c}".encode())

io.interactive()