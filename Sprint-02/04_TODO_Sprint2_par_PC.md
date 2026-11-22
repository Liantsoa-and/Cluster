# Sprint 2 – TODO complet par PC
**Projet : Clustering de serveurs – Ajout / Retrait dynamique**  
**Équipe de 3 – Configuration à faire chez soi**

---

## Objectif du Sprint 2

Pouvoir **ajouter et retirer des serveurs web à chaud** (sans redémarrer tout le cluster) grâce à une interface Python qui dialogue avec HAProxy.

---

## Attribution des rôles (même que Sprint 1)

| PC   | Rôle principal                          | Responsable     |
|------|-----------------------------------------|-----------------|
| PC1  | HAProxy + Outil Python de gestion       | Chef de groupe  |
| PC2  | Serveur Web 2 (prêt à être ajouté/retiré) | Membre 2      |
| PC3  | Serveur Web 3 (prêt à être ajouté/retiré) | Membre 3      |

---

## TODO – PC1 (Chef de groupe) – Gestion dynamique

### 1. Prérequis (si pas déjà fait au Sprint 1)
- [ ] Nginx installé et page `/var/www/html/a.html` présente
- [ ] HAProxy installé et fonctionnel
- [ ] Page de stats accessible : `http://IP_PC1/haproxy?stats`

### 2. Activer le Runtime API de HAProxy (très important)
On va utiliser le **socket d’administration** de HAProxy pour ajouter/supprimer des serveurs sans réécrire tout le fichier de config à chaque fois.

- [ ] Éditer la configuration HAProxy :
  ```bash
  sudo nano /etc/haproxy/haproxy.cfg
  ```

- [ ] Dans la section `global`, ajouter (ou vérifier) ces lignes :
  ```haproxy
  global
      ...
      stats socket /run/haproxy/admin.sock mode 660 level admin
      stats timeout 30s
  ```

- [ ] Créer le dossier si besoin et donner les bons droits :
  ```bash
  sudo mkdir -p /run/haproxy
  sudo chown haproxy:haproxy /run/haproxy
  ```

- [ ] Vérifier la config puis recharger :
  ```bash
  sudo haproxy -c -f /etc/haproxy/haproxy.cfg
  sudo systemctl restart haproxy
  ```

- [ ] Vérifier que le socket existe :
  ```bash
  ls -l /run/haproxy/admin.sock
  ```

### 3. Installer les outils Python nécessaires
- [ ] Installer les paquets :
  ```bash
  sudo apt install python3 python3-pip socat -y
  pip3 install --user requests   # au cas où on fait une petite API plus tard
  ```

### 4. Créer l’outil de gestion dynamique
- [ ] Créer le dossier du projet :
  ```bash
  mkdir -p ~/cluster-manager
  cd ~/cluster-manager
  ```

- [ ] Créer le script principal `manager.py` (le contenu complet te sera fourni dans le fichier de documentation ou tu peux le copier depuis le guide).

  Le script devra permettre au minimum :
  - `python3 manager.py list`          → lister les serveurs actuels
  - `python3 manager.py add <nom> <ip>` → ajouter un serveur
  - `python3 manager.py remove <nom>`   → retirer un serveur
  - `python3 manager.py help`

- [ ] Rendre le script exécutable :
  ```bash
  chmod +x manager.py
  ```

### 5. Test local chez soi (PC1 seul)
- [ ] Lister les serveurs :
  ```bash
  python3 manager.py list
  ```
- [ ] Ajouter un serveur fictif puis le retirer (pour vérifier que les commandes fonctionnent).

---

## TODO – PC2 (Serveur Web 2)

### Objectif
Ton serveur doit rester simple et prêt à être ajouté ou retiré dynamiquement par PC1.

- [ ] Vérifier que Nginx tourne :
  ```bash
  sudo systemctl status nginx
  ```
- [ ] Vérifier que la page d’identification est bien présente :
  ```bash
  curl http://localhost/a.html
  ```
  → Doit afficher « Ceci est le serveur numéro 2 (PC2) »

- [ ] S’assurer que le port 80 est ouvert :
  ```bash
  sudo ufw allow 80
  sudo ufw status
  ```

- [ ] Noter ton adresse IP (tu la donneras demain à PC1) :
  `IP_PC2 = _______________________________`

**Rien d’autre à installer.** Ton rôle est d’être un « nœud » que l’on peut ajouter/retirer à chaud.

---

## TODO – PC3 (Serveur Web 3)

Exactement le même travail que PC2 :

- [ ] Nginx démarré et page `a.html` correcte (« serveur numéro 3 »)
- [ ] Port 80 ouvert
- [ ] Noter ton IP : `IP_PC3 = _______________________________`

---

## Ce qu’il faudra faire ensemble demain

1. Vérifier que le Sprint 1 fonctionne encore (les 3 serveurs répondent via HAProxy).
2. Sur PC1, utiliser l’outil Python pour :
   - Lister les serveurs
   - Retirer PC3 par exemple
   - Vérifier que les requêtes n’y vont plus
   - Remettre PC3
   - Ajouter éventuellement un 4ᵉ serveur (si quelqu’un a un 4ᵉ PC ou une VM)
3. Suivre le guide de tests Sprint 2.

---

**Note importante pour PC1 :**  
Le script `manager.py` complet te sera donné dans le prochain fichier ou tu peux me demander de te le générer séparément si tu veux le copier-coller directement.
