# Projet Clustering de serveurs – Documents complets

## Sprint 1 – Web Server Cluster (HAProxy + 3 serveurs web)

| Fichier                        | Contenu                                      |
|--------------------------------|----------------------------------------------|
| `01_TODO_par_PC.md`            | TODO complet par ordinateur                  |
| `02_Documentation_Concepts.md` | Concepts à comprendre (Load Balancing, HA…)  |
| `03_Guide_Tests_Demain.md`     | Procédure de tests                           |

## Sprint 2 – Dynamic Cluster (ajout / retrait à chaud)

| Fichier                              | Contenu                                              |
|--------------------------------------|------------------------------------------------------|
| `04_TODO_Sprint2_par_PC.md`          | TODO complet par ordinateur                          |
| `05_Documentation_Concepts_Sprint2.md`| Concepts (Runtime API, élasticité, orchestration)   |
| `06_Guide_Tests_Sprint2.md`          | Procédure de tests                                   |
| `07_manager.py`                      | **Script Python prêt à l’emploi** pour gérer les serveurs |

## Sprint 3 – Database Cluster (Réplication PostgreSQL)

| Fichier                              | Contenu                                              |
|--------------------------------------|------------------------------------------------------|
| `08_TODO_Sprint3_par_PC.md`          | TODO complet par ordinateur (Primary + Replicas)     |
| `09_Documentation_Concepts_Sprint3.md`| Concepts (Primary/Replica, WAL, Streaming…)         |
| `10_Guide_Tests_Sprint3.md`          | Procédure complète de mise en place et de tests      |

---

### Résumé des rôles finaux

| PC  | Web (Sprint 1 & 2)      | Base de données (Sprint 3) |
|-----|-------------------------|----------------------------|
| PC1 | HAProxy + Web1 + manager.py | **Primary** (Master)      |
| PC2 | Web2                    | **Replica 1**              |
| PC3 | Web3                    | **Replica 2** (optionnel)  |

---

### Ordre recommandé demain

1. Vérifier que le Sprint 1 fonctionne encore
2. Tester rapidement le Sprint 2 (add/remove)
3. Mettre en place le Sprint 3 (Primary → Replicas)
4. Faire les tests de réplication

Bon courage pour la soutenance !
