# Projet Clustering de serveurs – Documents

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

---

### Comment utiliser le script du Sprint 2 (PC1)

1. Copier `07_manager.py` sur PC1 dans `~/cluster-manager/manager.py`
2. Le rendre exécutable : `chmod +x manager.py`
3. Utilisation :
   ```bash
   python3 manager.py list
   python3 manager.py add    web4 192.168.1.50
   python3 manager.py remove web3
   python3 manager.py disable web2
   python3 manager.py enable  web2
   ```

---

**Prochain sprint :** Sprint 3 – Database Cluster (réplication PostgreSQL Master/Replica)
