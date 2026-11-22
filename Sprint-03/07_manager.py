#!/usr/bin/env python3
"""
Sprint 2 - Gestion dynamique des serveurs HAProxy
Usage:
    python3 manager.py list
    python3 manager.py add    <nom> <ip> [port]
    python3 manager.py remove <nom>
    python3 manager.py disable <nom>
    python3 manager.py enable  <nom>
    python3 manager.py help
"""

import subprocess
import sys
import os

# Configuration
SOCKET_PATH = "/run/haproxy/admin.sock"
BACKEND_NAME = "web_servers"          # Doit correspondre au nom dans haproxy.cfg
DEFAULT_PORT = 80


def run_haproxy_command(command: str) -> str:
    """Envoie une commande au Runtime API de HAProxy via le socket."""
    if not os.path.exists(SOCKET_PATH):
        print(f"[ERREUR] Socket introuvable : {SOCKET_PATH}")
        print("Vérifiez que HAProxy tourne et que 'stats socket' est bien configuré.")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["socat", "stdio", SOCKET_PATH],
            input=command + "\n",
            text=True,
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            return f"[ERREUR] {result.stderr.strip()}"
        return result.stdout.strip()
    except FileNotFoundError:
        print("[ERREUR] La commande 'socat' n'est pas installée.")
        print("Installez-la avec : sudo apt install socat")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        return "[ERREUR] Timeout lors de la communication avec HAProxy"


def list_servers():
    """Liste tous les serveurs du backend avec leur état."""
    print(f"\n=== Serveurs du backend '{BACKEND_NAME}' ===\n")
    output = run_haproxy_command(f"show servers state {BACKEND_NAME}")
    
    if output.startswith("[ERREUR]"):
        print(output)
        return

    # Format de sortie de "show servers state" est un peu brut, on le rend lisible
    lines = output.strip().splitlines()
    if len(lines) <= 1:
        print("Aucun serveur trouvé ou backend inexistant.")
        return

    # On ignore la première ligne (header)
    print(f"{'Nom':<15} {'IP:Port':<22} {'Statut':<10} {'Dernière vérif'}")
    print("-" * 65)
    
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 18:
            # Format approximatif de show servers state
            srv_name = parts[3]
            ip = parts[4]
            port = parts[5]
            status = parts[17] if len(parts) > 17 else "?"
            print(f"{srv_name:<15} {ip}:{port:<17} {status:<10}")
        else:
            print(line)

    print()


def add_server(name: str, ip: str, port: int = DEFAULT_PORT):
    """Ajoute un serveur au backend."""
    # On ajoute avec health check
    cmd = f"add server {BACKEND_NAME}/{name} {ip}:{port} check"
    result = run_haproxy_command(cmd)
    
    if "error" in result.lower() or result.startswith("[ERREUR]"):
        print(f"[ÉCHEC] Impossible d'ajouter {name} : {result}")
    else:
        print(f"[OK] Serveur '{name}' ({ip}:{port}) ajouté avec succès.")
        # On active immédiatement le health check
        run_haproxy_command(f"enable server {BACKEND_NAME}/{name}")


def remove_server(name: str):
    """Supprime un serveur du backend."""
    cmd = f"del server {BACKEND_NAME}/{name}"
    result = run_haproxy_command(cmd)
    
    if "error" in result.lower() or result.startswith("[ERREUR]"):
        print(f"[ÉCHEC] Impossible de supprimer {name} : {result}")
    else:
        print(f"[OK] Serveur '{name}' supprimé.")


def set_server_state(name: str, state: str):
    """Active (enable) ou désactive (disable) un serveur."""
    if state not in ("enable", "disable"):
        print("[ERREUR] État invalide. Utilisez 'enable' ou 'disable'.")
        return
    
    cmd = f"{state} server {BACKEND_NAME}/{name}"
    result = run_haproxy_command(cmd)
    
    if "error" in result.lower() or result.startswith("[ERREUR]"):
        print(f"[ÉCHEC] {result}")
    else:
        action = "activé" if state == "enable" else "désactivé"
        print(f"[OK] Serveur '{name}' {action}.")


def print_help():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command in ("help", "-h", "--help"):
        print_help()

    elif command == "list":
        list_servers()

    elif command == "add":
        if len(sys.argv) < 4:
            print("Usage : python3 manager.py add <nom> <ip> [port]")
            sys.exit(1)
        name = sys.argv[2]
        ip = sys.argv[3]
        port = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_PORT
        add_server(name, ip, port)

    elif command == "remove" or command == "rm" or command == "del":
        if len(sys.argv) < 3:
            print("Usage : python3 manager.py remove <nom>")
            sys.exit(1)
        remove_server(sys.argv[2])

    elif command == "disable":
        if len(sys.argv) < 3:
            print("Usage : python3 manager.py disable <nom>")
            sys.exit(1)
        set_server_state(sys.argv[2], "disable")

    elif command == "enable":
        if len(sys.argv) < 3:
            print("Usage : python3 manager.py enable <nom>")
            sys.exit(1)
        set_server_state(sys.argv[2], "enable")

    else:
        print(f"Commande inconnue : {command}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
