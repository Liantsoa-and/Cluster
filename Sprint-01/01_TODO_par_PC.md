# Sprint 1 – TODO complet par PC
**Projet : Clustering de serveurs Web avec HAProxy**  
**Équipe de 3 – Configuration à faire chez soi**

---

## Règles générales (pour tout le monde)

- Chaque personne configure **son propre PC** chez elle.
- On se retrouve   pour brancher les machines ensemble et tester.
- Notez bien **votre adresse IP** (commande : `ip a` ou `hostname -I`).
- Utilisez Ubuntu (ou une distribution Debian-like).
- Communiquez vos IP   dès le début (idéalement sur un groupe WhatsApp/Discord).

**Attribution des rôles :**
| PC   | Rôle principal              | Responsable     |
|------|-----------------------------|-----------------|
| PC1  | HAProxy + Serveur Web 1     | Membre 1        |
| PC2  | Serveur Web 2               | Membre 2        |
| PC3  | Serveur Web 3               | Membre 3        |

---

## TODO – PC1 (Membre 1) – HAProxy + Web1

### 1. Préparation système
- [ ] Mettre à jour le système  
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Noter votre adresse IP : `_______________________________`
- [ ] Vérifier que le pare-feu n’bloque pas le port 80 (temporairement)  
  ```bash
  sudo ufw allow 80
  sudo ufw allow 8404   # pour la page de stats HAProxy (optionnel)
  ```

### 2. Installation Nginx (Serveur Web 1)
- [ ] Installer Nginx  
  ```bash
  sudo apt install nginx -y
  ```
- [ ] Créer la page d’identification  
  ```bash
  echo "<h1>Ceci est le serveur numéro 1 (PC1)</h1>" | sudo tee /var/www/html/a.html
  ```
- [ ] Tester localement  
  ```bash
  curl http://localhost/a.html
  ```
  → Doit afficher : `Ceci est le serveur numéro 1 (PC1)`

### 3. Installation HAProxy
- [ ] Installer HAProxy  
  ```bash
  sudo apt install haproxy -y
  ```
- [ ] Sauvegarder la config d’origine  
  ```bash
  sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup
  ```

### 4. Configuration HAProxy (à préparer chez soi)
- [ ] Ouvrir le fichier de configuration  
  ```bash
  sudo nano /etc/haproxy/haproxy.cfg
  ```
- [ ] Remplacer tout le contenu par la configuration ci-dessous  
  (laissez les IP de PC2 et PC3 en commentaire pour le moment)

```haproxy
global
    log /dev/log    local0
    log /dev/log    local1 notice
    maxconn 4096
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms
    retries 3

# Frontend : ce que les clients voient
frontend http_front
    bind *:80
    default_backend web_servers

    # Page de statistiques (très utile  )
    stats enable
    stats uri /haproxy?stats
    stats refresh 5s
    stats admin if TRUE

# Backend : les 3 serveurs web
backend web_servers
    balance roundrobin
    option httpchk GET /a.html
    http-check expect status 200

    # Remplacez les IP   dès que vous les avez
    server web1 127.0.0.1:80 check          # PC1 (local)
    # server web2 IP_PC2:80 check           # ← à décommenter et remplir  
    # server web3 IP_PC3:80 check           # ← à décommenter et remplir  
```

- [ ] Vérifier la syntaxe de la configuration  
  ```bash
  sudo haproxy -c -f /etc/haproxy/haproxy.cfg
  ```
- [ ] Redémarrer HAProxy  
  ```bash
  sudo systemctl restart haproxy
  sudo systemctl enable haproxy
  ```

### 5. Test chez soi (PC1 seul)
- [ ] Tester que HAProxy répond  
  ```bash
  curl http://localhost/a.html
  ```
- [ ] Accéder à la page de stats (dans le navigateur) :  
  `http://localhost/haproxy?stats`

---

## TODO – PC2 (Serveur Web 2)

### 1. Préparation
- [ ] Mettre à jour le système  
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Noter votre adresse IP : `_______________________________`
- [ ] Autoriser le port 80  
  ```bash
  sudo ufw allow 80
  ```

### 2. Installation et configuration Nginx
- [ ] Installer Nginx  
  ```bash
  sudo apt install nginx -y
  ```
- [ ] Créer la page d’identification  
  ```bash
  echo "<h1>Ceci est le serveur numéro 2 (PC2)</h1>" | sudo tee /var/www/html/a.html
  ```
- [ ] Vérifier les permissions  
  ```bash
  sudo chown www-data:www-data /var/www/html/a.html
  ```
- [ ] Tester localement  
  ```bash
  curl http://localhost/a.html
  ```
  → Doit afficher : `Ceci est le serveur numéro 2 (PC2)`

### 3. Vérifications finales
- [ ] S’assurer que Nginx démarre automatiquement  
  ```bash
  sudo systemctl enable nginx
  sudo systemctl status nginx
  ```
- [ ] Noter votre IP et la communiquer au Membre 1   matin.

---

## TODO – PC3 (Serveur Web 3)

### 1. Préparation
- [ ] Mettre à jour le système  
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Noter votre adresse IP : `_______________________________`
- [ ] Autoriser le port 80  
  ```bash
  sudo ufw allow 80
  ```

### 2. Installation et configuration Nginx
- [ ] Installer Nginx  
  ```bash
  sudo apt install nginx -y
  ```
- [ ] Créer la page d’identification  
  ```bash
  echo "<h1>Ceci est le serveur numéro 3 (PC3)</h1>" | sudo tee /var/www/html/a.html
  ```
- [ ] Vérifier les permissions  
  ```bash
  sudo chown www-data:www-data /var/www/html/a.html
  ```
- [ ] Tester localement  
  ```bash
  curl http://localhost/a.html
  ```
  → Doit afficher : `Ceci est le serveur numéro 3 (PC3)`

### 3. Vérifications finales
- [ ] S’assurer que Nginx démarre automatiquement  
  ```bash
  sudo systemctl enable nginx
  sudo systemctl status nginx
  ```
- [ ] Noter votre IP et la communiquer au Membre 1   matin.

---

## Ce qu’il faudra faire   matin (tous ensemble)

1. Brancher les 3 PC sur le même réseau (même box / même switch).
2. Échanger les adresses IP.
3. Sur PC1 : décommenter et remplir les lignes `server web2` et `server web3` dans HAProxy, puis relancer :
   ```bash
   sudo systemctl restart haproxy
   ```
4. Lancer les tests (voir le fichier `03_Guide_Tests_ .md`).
