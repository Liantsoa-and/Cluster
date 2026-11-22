# Documentation – Concepts à comprendre (Sprint 3)
**Cluster de bases de données – Réplication Primary / Replica (PostgreSQL)**

---

## 1. Pourquoi un cluster de bases de données ?

Dans les Sprints 1 et 2 on a rendu les **serveurs web** hautement disponibles.  
Mais si la **base de données** tombe, toute l’application tombe aussi.

Objectifs du Sprint 3 :
- Répartir la charge de **lecture**
- Avoir une copie de secours en cas de panne du Primary
- Comprendre la réplication de données

---

## 2. Primary vs Replica (Master / Slave)

| Rôle       | Ancien nom | Peut écrire ? | Peut lire ? | Rôle principal                  |
|------------|------------|---------------|-------------|---------------------------------|
| **Primary**    | Master     | Oui           | Oui         | Reçoit toutes les écritures     |
| **Replica**    | Slave      | Non           | Oui         | Reçoit une copie des données    |

- Toutes les **écritures** (INSERT, UPDATE, DELETE) vont uniquement sur le Primary.
- Les **lectures** (SELECT) peuvent aller sur le Primary **ou** sur les Replicas (pour répartir la charge).

---

## 3. Comment fonctionne la réplication PostgreSQL (Streaming Replication)

1. Le Primary écrit toutes les modifications dans des fichiers appelés **WAL** (Write-Ahead Log).
2. Les Replicas se connectent au Primary et reçoivent ces fichiers WAL en continu (**streaming**).
3. Chaque Replica rejoue les mêmes modifications chez lui → il devient une copie quasi temps réel.

C’est de la **réplication asynchrone** par défaut :
- Le Primary n’attend pas que le Replica ait bien reçu les données avant de confirmer l’écriture au client.
- Avantage : très performant
- Inconvénient : en cas de crash très brutal du Primary, il peut y avoir une toute petite perte de données (quelques secondes max).

---

## 4. Vocabulaire important

| Terme                  | Signification |
|------------------------|---------------|
| **WAL**                | Write-Ahead Log – journal des modifications |
| **Streaming Replication** | Réplication en continu via le réseau |
| **pg_basebackup**      | Outil qui fait la copie initiale complète d’une base |
| **standby.signal**     | Fichier qui dit à PostgreSQL « tu es un Replica » |
| **Hot Standby**        | Replica qui accepte les requêtes de lecture |
| **Replication Slot**   | Mécanisme qui empêche le Primary d’effacer des WAL encore nécessaires aux Replicas |
| **Synchronous vs Asynchronous** | Sync = le Primary attend le Replica (plus sûr mais plus lent) |

---

## 5. Architecture du Sprint 3

```
                      ┌──────────────────────┐
                      │   Applications /     │
                      │   Serveurs Web       │
                      └──────────┬───────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
             ┌────────────┐ ┌─────────┐ ┌─────────┐
             │   PC1      │ │  PC2    │ │  PC3    │
             │  Primary   │ │ Replica │ │ Replica │
             │ (écriture) │ │ (lecture)│ │(lecture)│
             └────────────┘ └─────────┘ └─────────┘
                    │              ▲           ▲
                    │              │           │
                    └──────────────┴───────────┘
                         Réplication streaming
                              (WAL)
```

---

## 6. Ce qu’on peut faire / ne pas faire

**Sur le Primary (PC1) :**
- CREATE, INSERT, UPDATE, DELETE → OK
- SELECT → OK

**Sur un Replica (PC2 / PC3) :**
- SELECT → OK
- INSERT / UPDATE / DELETE → **ERREUR** (c’est normal et voulu)

---

## 7. Avantages et limites de notre solution

**Avantages :**
- Haute disponibilité en lecture
- Copie de secours prête
- Très utilisé en production (beaucoup d’entreprises font exactement ça)

**Limites (normales pour un Sprint étudiant) :**
- Pas de bascule automatique (failover) si le Primary tombe → il faudrait Patroni, repmgr ou un outil similaire
- Réplication asynchrone → très légère possibilité de perte de données en cas de crash
- Les applications doivent savoir écrire uniquement sur le Primary

---

## 8. Différence avec MySQL

On aurait pu choisir MySQL/MariaDB (réplication basée sur les binlogs).  
PostgreSQL a été choisi parce que :
- La streaming replication est plus moderne et plus simple à comprendre
- Les outils (`pg_basebackup`, slots…) sont très clairs pédagogiquement

Les concepts restent les mêmes (Primary/Replica, journal de transaction, etc.).

---

## 9. Ce qu’on attend de vous demain

- Savoir expliquer la différence Primary / Replica
- Savoir montrer qu’une donnée écrite sur le Primary apparaît bien sur les Replicas
- Savoir montrer qu’on ne peut pas écrire sur un Replica
- Comprendre à quoi servent les WAL et le streaming

Bonne lecture !
