#!/usr/bin/env python3
import socket
import time
import platform
import getpass
import os

SERVER_IP = "192.168.5.87"
SERVER_PORT = 4444
CONNECT_TIMEOUT = 8

BANNER = (
    "[EM Shell - SIMULADO BIDIRECCIONAL]\n"
    "Modo: comandos predefinidos (sin ejecucion arbitraria)\n"
    "Escriba HELP para ver comandos.\n"
)


def sys_info() -> str:
    u = platform.uname()
    return (
        f"Time: {time.ctime()}\n"
        f"User: {getpass.getuser()}\n"
        f"PID: {os.getpid()}\n"
        f"System: {u.system} {u.release}\n"
        f"Machine: {u.machine}\n"
        f"CWD: {os.getcwd()}\n"
    )


def handle_command(cmd: str) -> str:
    c = cmd.strip().upper()

    if c in ("HELP", "?"):
        return (
            "Comandos permitidos:\n"
            "  HELP  - muestra esta ayuda\n"
            "  INFO  - info basica del sistema\n"
            "  TIME  - hora del sistema\n"
            "  USER  - usuario actual\n"
            "  PWD   - directorio actual\n"
            "  PING  - prueba de vida\n"
            "  EXIT  - cerrar sesion\n"
        )
    if c == "INFO":
        return sys_info()
    if c == "TIME":
        return time.ctime() + "\n"
    if c == "USER":
        return getpass.getuser() + "\n"
    if c == "PWD":
        return os.getcwd() + "\n"
    if c == "PING":
        return "PONG\n"
    if c == "EXIT":
        return "BYE\n"

    return "Comando no permitido. Use HELP.\n"


def recv_line(sock: socket.socket, maxlen: int = 1024):
    data = b""
    while len(data) < maxlen:
        chunk = sock.recv(1)
        if not chunk:
            return None
        data += chunk
        if chunk == b"\n":
            break
    return data.decode("utf-8", errors="replace")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(CONNECT_TIMEOUT)

    try:
        s.connect((SERVER_IP, SERVER_PORT))
        s.settimeout(None)

        s.sendall(BANNER.encode("utf-8"))
        s.sendall(("Status: OK (demo)\n" + sys_info()).encode("utf-8"))

        while True:
            s.sendall(b"> ")
            line = recv_line(s)
            if line is None:
                break

            resp = handle_command(line)
            s.sendall(resp.encode("utf-8"))

            if line.strip().upper() == "EXIT":
                break

    except Exception as e:
        print(f"[EM Shell] No se pudo conectar o fallo la sesion: {e}")
    finally:
        try:
            s.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
