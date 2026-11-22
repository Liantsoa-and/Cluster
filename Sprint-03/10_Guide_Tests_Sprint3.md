# Guide de Tests – Sprint 3 (Demain)
**Cluster PostgreSQL – Réplication Primary / Replica**

---

## 1. Préparation collective

### Informations à noter

| Machine | Rôle      | Adresse IP          | Utilisateur réplication |
|---------|-----------|---------------------|--------------------------|
| PC1     | Primary   | __________________  | replicator / replicatorpass |
| PC2     | Replica 1 | __________________  | -                        |
| PC3     | Replica 2 | __________________  | -                        |

### Vérifications sur PC1 (Primary)
```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "SHOW wal_level;"
# Doit afficher : replica
```

---

## 2. Mise en place des Replicas (PC2 et PC3)

**Sur chaque Replica (PC2 puis PC3) :**

```bash
# 1. Arrêter PostgreSQL
sudo systemctl stop postgresql

# 2. Vider le répertoire de données (ATTENTION : destructif)
sudo rm -rf /var/lib/postgresql/*/main/*

# 3. Faire la copie initiale depuis le Primary
# Remplacez IP_PC1 par la vraie adresse IP de PC1
sudo -u postgres pg_basebackup \
  -h IP_PC1 \
  -D /var/lib/postgresql/$(ls /var/lib/postgresql)/main \
  -U replicator \
  -P -v -R -X stream \
  -C -S replica_$(hostname)
```

Explications des options :
- `-R` : crée automatiquement le fichier `standby.signal` + configuration de connexion
- `-X stream` : récupère aussi les WAL en streaming pendant la copie
- `-C -S nom` : crée un replication slot (recommandé)

### Démarrer le Replica
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

---

## 3. Vérifier que la réplication fonctionne

### Depuis le Primary (PC1)
```bash
sudo -u postgres psql -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
```

**Résultat attendu :**  
Vous devez voir une ou deux lignes avec l’IP de PC2 (et PC3) et `state = streaming`.

### Depuis un Replica (PC2)
```bash
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"
```
**Résultat attendu :** `t` (true) → confirme que c’est bien un Replica.

---

## 4. Test fonctionnel complet (le plus important)

### Étape A – Écriture sur le Primary
Sur **PC1** :
```bash
sudo -u postgres psql -d cluster_db
```
```sql
CREATE TABLE IF NOT EXISTS test_replication (
    id SERIAL PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO test_replication (message) VALUES 
('Bonjour depuis le Primary - test 1'),
('Donnée importante du cluster');

SELECT * FROM test_replication;
\q
```

### Étape B – Lecture sur les Replicas
Sur **PC2** (et PC3) :
```bash
sudo -u postgres psql -d cluster_db -c "SELECT * FROM test_replication;"
```

**Résultat attendu :**  
Les mêmes lignes apparaissent (parfois avec 1 seconde de décalage max).

### Étape C – Tentative d’écriture sur un Replica (doit échouer)
Sur **PC2** :
```bash
sudo -u postgres psql -d cluster_db -c "INSERT INTO test_replication (message) VALUES ('essai écriture replica');"
```

**Résultat attendu :**  
Erreur du type :  
`ERROR: cannot execute INSERT in a read-only transaction`  
→ C’est **normal** et prouve que la protection fonctionne.

---

## 5. Checklist de validation du Sprint 3

| Test                                              | Réussi ? | Commentaire |
|---------------------------------------------------|----------|-----------|
| Primary démarré et `wal_level = replica`          | ☐        |           |
| `pg_basebackup` réussi sur PC2                    | ☐        |           |
| `pg_basebackup` réussi sur PC3 (si fait)          | ☐        |           |
| `pg_stat_replication` montre les replicas en streaming | ☐   |           |
| Donnée écrite sur Primary visible sur Replica     | ☐        |           |
| Écriture refusée sur Replica                      | ☐        |           |
| Les serveurs web du Sprint 1/2 fonctionnent encore| ☐        |           |

---

## 6. En cas de problème

| Problème                              | Solution |
|---------------------------------------|----------|
| `pg_basebackup` : authentification échoue | Vérifier `pg_hba.conf` + mot de passe + `sudo systemctl restart postgresql` sur PC1 |
| `pg_basebackup` : connection refused  | Pare-feu (`sudo ufw allow 5432`) + `listen_addresses = '*'` |
| Replica ne démarre pas                | Regarder les logs : `sudo journalctl -u postgresql -e` |
| Pas de ligne dans `pg_stat_replication` | Vérifier que le Replica a bien le fichier `standby.signal` et redémarrer |
| Données n’apparaissent pas sur Replica | Attendre 2-3 secondes + vérifier l’état de la réplication |

---

## 7. Commandes utiles de diagnostic

```bash
# État de la réplication (Primary)
sudo -u postgres psql -c "SELECT * FROM pg_stat_replication;"

# Est-ce un Replica ? (sur PC2/PC3)
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"

# Retard de réplication (en octets)
sudo -u postgres psql -c "SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) FROM pg_stat_replication;"
```

---

**Une fois ces tests validés, le Sprint 3 est terminé.**  
Félicitations, vous aurez un vrai petit cluster complet :  
Load Balancing web + gestion dynamique + base de données répliquée.
