#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <time.h>
#include <sys/time.h>

// Pointer fungsi asli
static int (*real_open)(const char *pathname, int flags, ...);
static FILE *(*real_fopen)(const char *pathname, const char *mode);
static ssize_t (*real_getrandom)(void *buf, size_t buflen, unsigned int flags);

// ==========================================
// 1. TIME FREEZE (Perbaikan Signature)
// ==========================================

time_t time(time_t *tloc) {
    if (tloc) *tloc = 1337;
    return 1337;
}

// FIX: Parameter kedua harus 'void *' bukan 'struct timezone *'
int gettimeofday(struct timeval *tv, void *tz) {
    if (tv) {
        tv->tv_sec = 1337;
        tv->tv_usec = 0;
    }
    return 0;
}

int clock_gettime(clockid_t clk_id, struct timespec *tp) {
    if (tp) {
        tp->tv_sec = 1337;
        tp->tv_nsec = 0;
    }
    return 0;
}

// ==========================================
// 2. ENTROPY CONTROL (Rust Specific)
// ==========================================

// Hook Open (Method 1: File read)
int open(const char *pathname, int flags, ...) {
    if (!real_open) real_open = dlsym(RTLD_NEXT, "open");
    if (strstr(pathname, "/dev/urandom") != NULL) {
        return real_open("./my_entropy", flags);
    }
    return real_open(pathname, flags);
}

// Hook getrandom (Method 2: Syscall wrapper - PENTING untuk Rust!)
ssize_t getrandom(void *buf, size_t buflen, unsigned int flags) {
    // Kita paksa baca dari file my_entropy juga agar konsisten dengan Python
    FILE *f = fopen("./my_entropy", "rb");
    if (f) {
        fread(buf, 1, buflen, f);
        fclose(f);
        return buflen; // Sukses baca file kita
    }
    // Fallback jika file tidak ada: isi dengan nol
    memset(buf, 0, buflen);
    return buflen;
}

// ==========================================
// 3. PROCESS IDENTITY
// ==========================================

pid_t getpid(void) { return 1337; }
pid_t getppid(void) { return 1337; }
uid_t getuid(void) { return 0; }
uid_t geteuid(void) { return 0; }

long ptrace(int request, pid_t pid, void *addr, void *data) {
    return 0; 
}

// ==========================================
// 4. ANTI-DEBUG STATUS
// ==========================================

FILE *fopen(const char *pathname, const char *mode) {
    if (!real_fopen) real_fopen = dlsym(RTLD_NEXT, "fopen");
    
    if (strstr(pathname, "/dev/urandom") != NULL) {
         return real_fopen("./my_entropy", "rb");
    }
    if (strstr(pathname, "/proc/self/status") != NULL) {
        return real_fopen("./fake_status", mode);
    }
    return real_fopen(pathname, mode);
}