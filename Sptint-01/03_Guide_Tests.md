# Guide de Tests –   (Sprint 1)
**À faire une fois les 3 PC branchés sur le même réseau**

---

## 1. Préparation collective (10-15 minutes)

### Étape 1 – Réseau
- [ ] Brancher les 3 ordinateurs sur le **même réseau** (même box Wi-Fi ou même switch)
- [ ] Vérifier que tout le monde a une IP dans le même sous-réseau  
  Exemple : 192.168.1.xx

### Étape 2 – Échange des IP
Noter ici les adresses IP réelles :

| Machine | Rôle              | Adresse IP          |
|---------|-------------------|---------------------|
| PC1     | HAProxy + Web1    | __________________  |
| PC2     | Web2              | __________________  |
| PC3     | Web3              | __________________  |

### Étape 3 – Mise à jour de HAProxy (sur PC1 uniquement)
1. Ouvrir la configuration :
   ```bash
   sudo nano /etc/haproxy/haproxy.cfg
   ```
2. Décommenter et remplir les lignes des serveurs web2 et web3 :
   ```haproxy
   server web1 127.0.0.1:80 check
   server web2 192.168.x.x:80 check     # ← IP réelle de PC2
   server web3 192.168.x.x:80 check     # ← IP réelle de PC3
   ```
3. Vérifier la config :
   ```bash
   sudo haproxy -c -f /etc/haproxy/haproxy.cfg
   ```
4. Recharger HAProxy :
   ```bash
   sudo systemctl restart haproxy
   ```

---

## 2. Tests de base (à faire dans l’ordre)

### Test 1 – Accès simple via HAProxy
Depuis **n’importe quel PC** (ou même un téléphone sur le même Wi-Fi) :

```bash
curl http://IP_DE_PC1/a.html
```

ou dans le navigateur : `http://IP_DE_PC1/a.html`

**Résultat attendu :**  
Vous devez voir apparaître « Ceci est le serveur numéro X » (1, 2 ou 3).

---

### Test 2 – Vérifier la répartition de charge (Round-robin)
Lancer plusieurs requêtes d’affilée :

```bash
for i in {1..12}; do curl -s http://IP_DE_PC1/a.html; echo; done
```

**Résultat attendu :**  
Les réponses doivent alterner entre les 3 serveurs (pas forcément parfaitement dans l’ordre, mais les 3 doivent apparaître).

---

### Test 3 – Page de statistiques HAProxy (très utile)
Dans un navigateur, aller sur :

```
http://IP_DE_PC1/haproxy?stats
```

Vous verrez :
- L’état de chaque serveur (UP / DOWN)
- Le nombre de requêtes reçues par chaque serveur
- Les sessions actives
- Les erreurs éventuelles

C’est l’outil le plus important pour comprendre ce qui se passe.

---

## 3. Test de High Availability (le plus important)

### Scénario : un serveur tombe

1. Sur **PC2**, arrêter Nginx :
   ```bash
   sudo systemctl stop nginx
   ```

2. Relancer des requêtes depuis un autre PC :
   ```bash
   for i in {1..10}; do curl -s http://IP_DE_PC1/a.html; echo; done
   ```

**Résultat attendu :**
- Plus aucune réponse « serveur numéro 2 »
- Uniquement serveur 1 et serveur 3
- Dans la page stats (`/haproxy?stats`), le serveur web2 doit apparaître en **rouge / DOWN**

3. Remettre PC2 en service :
   ```bash
   sudo systemctl start nginx
   ```

4. Attendre 5-10 secondes puis relancer les requêtes.  
   → Le serveur 2 doit revenir automatiquement dans la rotation.

**C’est exactement le principe de la High Availability.**

---

## 4. Simuler plusieurs clients en même temps

Installer Apache Bench (sur PC1 ou un autre PC) :

```bash
sudo apt install apache2-utils -y
```

Lancer un test de charge :

```bash
ab -n 200 -c 20 http://IP_DE_PC1/a.html
```

Explications :
- `-n 200` : 200 requêtes au total
- `-c 20`  : 20 clients simultanés

Regarder ensuite la page de stats HAProxy pour voir comment le trafic a été réparti.

---

## 5. Checklist finale de validation du Sprint 1

| Test                              | Réussi ? | Commentaire |
|-----------------------------------|----------|-----------|
| Les 3 serveurs répondent via HAProxy | ☐       |           |
| La répartition round-robin fonctionne | ☐     |           |
| La page de stats est accessible      | ☐       |           |
| Un serveur down est bien retiré      | ☐       |           |
| Le serveur revient automatiquement   | ☐       |           |
| Test avec plusieurs clients simultanés | ☐     |           |

---

## 6. En cas de problème  

| Problème                        | Vérification rapide                              |
|--------------------------------|--------------------------------------------------|
| `curl` ne répond pas           | `ping IP_DE_PC1` + vérifier `sudo systemctl status haproxy` |
| Un serveur n’apparaît jamais   | Vérifier l’IP dans haproxy.cfg + `curl http://IP_DU_SERVEUR/a.html` depuis PC1 |
| Tous les serveurs en DOWN      | Firewall (`sudo ufw status`) ou Nginx arrêté     |
| Page stats inaccessible        | Vérifier que la section `stats` est bien dans le frontend |

---

**Bon courage pour   !**  
Une fois ces tests validés, le Sprint 1 est terminé et on pourra passer au Sprint 2 (ajout/retrait dynamique).
