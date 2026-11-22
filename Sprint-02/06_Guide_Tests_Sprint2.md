# Guide de Tests – Sprint 2 (Demain)
**Ajout et retrait dynamique des serveurs**

---

## 1. Préparation (5-10 minutes)

### Vérifications préalables
- [ ] Le Sprint 1 fonctionne encore (les 3 serveurs répondent bien via HAProxy)
- [ ] Sur PC1, le socket admin existe :
  ```bash
  ls -l /run/haproxy/admin.sock
  ```
- [ ] L’outil `manager.py` est présent et exécutable

### Rappel des IP (à remplir)

| Machine | Nom dans HAProxy | Adresse IP          |
|---------|------------------|---------------------|
| PC1     | web1             | __________________  |
| PC2     | web2             | __________________  |
| PC3     | web3             | __________________  |

---

## 2. Tests de base de l’outil

### Test 1 – Lister les serveurs actuels
```bash
cd ~/cluster-manager
python3 manager.py list
```

**Résultat attendu :**  
Tu dois voir web1, web2 et web3 avec leur état (UP).

---

### Test 2 – Retirer un serveur (PC3 par exemple)
```bash
python3 manager.py remove web3
```

Puis vérifier :
```bash
python3 manager.py list
```

Et tester le load balancing :
```bash
for i in {1..9}; do curl -s http://IP_PC1/a.html; echo; done
```

**Résultat attendu :**
- Plus aucune réponse « serveur numéro 3 »
- Uniquement serveur 1 et 2
- Dans la page stats (`http://IP_PC1/haproxy?stats`) → web3 est absent ou DOWN

---

### Test 3 – Remettre le serveur
```bash
python3 manager.py add web3 IP_DE_PC3
```

Vérifier :
```bash
python3 manager.py list
for i in {1..9}; do curl -s http://IP_PC1/a.html; echo; done
```

**Résultat attendu :**  
Le serveur 3 revient dans la rotation.

---

### Test 4 – Désactiver temporairement (bonus)
Si ton script le gère :
```bash
python3 manager.py disable web2
# → plus de trafic vers web2
python3 manager.py enable web2
# → web2 revient
```

---

## 3. Scénario complet de démonstration (recommandé pour la soutenance)

1. Montrer la page de stats HAProxy avec les 3 serveurs UP
2. Lister avec `manager.py list`
3. Retirer PC2 → montrer que les requêtes n’y vont plus
4. Remettre PC2 → montrer qu’il revient
5. (Optionnel) Ajouter un 4ᵉ serveur s’il y en a un de disponible
6. Expliquer la différence avec le Sprint 1 (plus besoin de toucher au fichier de config à la main)

---

## 4. Checklist de validation du Sprint 2

| Test                                      | Réussi ? | Commentaire |
|-------------------------------------------|----------|-----------|
| `manager.py list` fonctionne              | ☐        |           |
| On peut retirer un serveur à chaud        | ☐        |           |
| Les requêtes n’organisent plus vers le serveur retiré | ☐ |           |
| On peut remettre le serveur               | ☐        |           |
| Le serveur revient bien dans le load balancing | ☐   |           |
| La page de stats reflète les changements  | ☐        |           |

---

## 5. En cas de problème

| Problème                          | Solution rapide |
|-----------------------------------|-----------------|
| `Permission denied` sur le socket | `sudo chmod 660 /run/haproxy/admin.sock` puis ajouter ton utilisateur au groupe haproxy ou utiliser `sudo` |
| `No such file` (socket)           | Vérifier que la ligne `stats socket` est bien dans `haproxy.cfg` et que HAProxy a été redémarré |
| Serveur ajouté mais reste DOWN    | Vérifier que Nginx tourne sur la machine cible + `curl http://IP:80/a.html` depuis PC1 |
| Les changements disparaissent après reboot | Normal avec Runtime API pure → il faudra aussi mettre à jour le fichier `.cfg` pour la persistance (amélioration possible) |

---

## 6. Améliorations possibles (si vous avez le temps)

- Ajouter une vraie petite interface web (Flask ou FastAPI)
- Faire en sorte que `add` vérifie d’abord que le serveur répond avant de l’ajouter
- Sauvegarder automatiquement les serveurs ajoutés dans le fichier `haproxy.cfg`
- Afficher des couleurs dans le terminal (vert = UP, rouge = DOWN)

---

**Une fois ces tests validés, le Sprint 2 est terminé.**  
On pourra ensuite attaquer le Sprint 3 (cluster de bases de données avec réplication).
