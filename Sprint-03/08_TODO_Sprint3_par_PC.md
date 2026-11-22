# Sprint 3 – TODO complet par PC
**Projet : Clustering de serveurs – Database Cluster (Réplication PostgreSQL)**  
**Équipe de 3 – Configuration à faire chez soi**

---

## Objectif du Sprint 3

Mettre en place un **cluster de bases de données** avec :
- 1 serveur **Primary** (Master) qui accepte les écritures
- 1 ou 2 serveurs **Replica** (Slave) qui reçoivent les données en réplication
- Réplication **asynchrone** en streaming

Architecture retenue :

| PC   | Rôle base de données          | Rôle précédent     |
|------|-------------------------------|--------------------|
| PC1  | **Primary** (Master)          | HAProxy + Web1     |
| PC2  | **Replica 1**                 | Web2               |
| PC3  | **Replica 2** (optionnel)     | Web3               |

---

## TODO – PC1 (Primary / Master)

### 1. Installation de PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### 2. Créer un utilisateur et une base de démonstration
```bash
sudo -u postgres psql
```

Dans le prompt PostgreSQL :
```sql
CREATE USER cluster_user WITH PASSWORD 'motdepassefort';
CREATE DATABASE cluster_db OWNER cluster_user;
GRANT ALL PRIVILEGES ON DATABASE cluster_db TO cluster_user;
\q
```

### 3. Configuration pour autoriser la réplication

Éditer le fichier de configuration principale :
```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Modifier / décommenter ces lignes :
```conf
listen_addresses = '*'                  # écouter sur toutes les interfaces
wal_level = replica                     # niveau nécessaire pour la réplication
max_wal_senders = 10                    # nombre max de replicas
max_replication_slots = 10
hot_standby = on                        # permettre les lectures sur les replicas
```

Éditer le fichier d’accès réseau :
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Ajouter à la fin (remplacez 192.168.1.0/24 par votre vrai sous-réseau) :
```conf
# Autoriser la réplication depuis le réseau local
host    replication     cluster_user    192.168.1.0/24    md5
host    all             cluster_user    192.168.1.0/24    md5
```

### 4. Créer un utilisateur dédié à la réplication (recommandé)
```bash
sudo -u postgres psql
```
```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicatorpass';
\q
```

Puis ajouter aussi dans `pg_hba.conf` :
```conf
host    replication     replicator      192.168.1.0/24    md5
```

### 5. Redémarrer PostgreSQL
```bash
sudo systemctl restart postgresql
```

### 6. Noter les informations à communiquer demain
- IP de PC1 (Primary) : `_______________________________`
- Port : 5432 (par défaut)
- Utilisateur réplication : `replicator`
- Mot de passe : `replicatorpass`

### 7. Ouvrir le port dans le pare-feu
```bash
sudo ufw allow 5432
sudo ufw status
```

---

## TODO – PC2 (Replica 1)

### 1. Installation de PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

### 2. Arrêter PostgreSQL (on va le configurer en replica)
```bash
sudo systemctl stop postgresql
```

### 3. Vider le répertoire de données (important)
```bash
sudo rm -rf /var/lib/postgresql/*/main/*
```

### 4. Faire la copie initiale depuis le Primary (basebackup)
**Cette étape se fera demain** quand les machines seront sur le même réseau, avec la commande :

```bash
sudo -u postgres pg_basebackup -h IP_DU_PC1 -D /var/lib/postgresql/16/main -U replicator -P -v -R -X stream
```

(Le chemin exact `/var/lib/postgresql/16/main` peut varier selon la version → vérifiez avec `ls /var/lib/postgresql/`)

### 5. Préparer le fichier standby (si la version le demande)
Sur les versions récentes, l’option `-R` crée automatiquement `standby.signal`.

### 6. Ouvrir le port (même si en lecture seule)
```bash
sudo ufw allow 5432
```

### 7. Noter votre IP
`IP_PC2 = _______________________________`

---

## TODO – PC3 (Replica 2 – optionnel mais recommandé)

Exactement les **mêmes étapes** que PC2.

- [ ] Installer PostgreSQL
- [ ] Arrêter le service
- [ ] Vider le dossier de données
- [ ] Attendre demain pour faire le `pg_basebackup` depuis PC1
- [ ] Noter votre IP

---

## Ce qu’il faudra faire ensemble demain

1. Vérifier que le Primary (PC1) est bien démarré et accessible.
2. Sur PC2 (et PC3) : lancer le `pg_basebackup`.
3. Démarrer PostgreSQL sur les replicas.
4. Vérifier que la réplication fonctionne (voir le guide de tests).
5. Tester une écriture sur le Primary → elle doit apparaître sur les Replicas.
6. Tester qu’on ne peut **pas** écrire directement sur un Replica.

---

**Note :**  
Les commandes exactes de `pg_basebackup` et de vérification seront dans le fichier `10_Guide_Tests_Sprint3.md`.
