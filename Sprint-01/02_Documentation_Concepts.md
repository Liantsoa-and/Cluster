# Documentation – Concepts à comprendre (Sprint 1)
**À lire avant   – Projet Clustering de serveurs**

Ce document explique simplement les notions importantes du Sprint 1.  
L’objectif n’est pas de tout retenir par cœur, mais de **comprendre le pourquoi** de ce qu’on fait.

---

## 1. Pourquoi fait-on un cluster de serveurs web ?

Quand un seul serveur web reçoit trop de requêtes, il ralentit ou plante.  
Solution : mettre **plusieurs serveurs identiques** derrière un répartiteur de charge.

Avantages :
- Plus de capacité (plus de clients en même temps)
- Si un serveur tombe, les autres continuent de répondre → **Haute Disponibilité**
- On peut ajouter des serveurs plus tard (élasticité)

---

## 2. Load Balancing (Répartition de charge)

C’est le fait de **distribuer les requêtes** des clients sur plusieurs serveurs.

Algorithmes courants :
| Algorithme       | Comment ça marche                          | Quand l’utiliser          |
|------------------|--------------------------------------------|---------------------------|
| **roundrobin**   | Tour à tour (1 → 2 → 3 → 1 → 2…)           | Le plus simple et courant |
| **leastconn**    | Envoie au serveur qui a le moins de connexions actives | Quand les requêtes ont des durées très différentes |
| source           | Même client → toujours le même serveur     | Quand on a besoin de sessions sticky |

Dans notre projet on utilise **roundrobin** (le plus pédagogique).

---

## 3. Reverse Proxy

Un **Reverse Proxy** se place **devant** les serveurs web.

Le client ne voit **que** le Reverse Proxy.  
Il ne sait pas qu’il y a plusieurs serveurs derrière.

Rôles du Reverse Proxy :
- Cache
- Sécurité (filtre les requêtes)
- SSL/TLS termination
- Load Balancing (dans le cas de HAProxy)

**HAProxy** est à la fois un Load Balancer **et** un Reverse Proxy.

---

## 4. HAProxy – Le cœur du Sprint 1

HAProxy = **High Availability Proxy**

C’est un logiciel très utilisé en production (beaucoup de grands sites l’utilisent).

Dans notre architecture :
```
Client  →  HAProxy (port 80)  →  Serveur Web 1, 2 ou 3
```

Avantages de HAProxy :
- Très performant
- Health checks intégrés
- Page de statistiques intégrée
- Configuration relativement simple

---

## 5. Health Checks (Contrôles de santé)

C’est ce qui apporte la **High Availability**.

HAProxy envoie régulièrement une requête (ex : `GET /a.html`) à chaque serveur.

- Si le serveur répond **200 OK** → il est considéré comme **UP**
- S’il ne répond pas ou répond une erreur → il est marqué **DOWN** et HAProxy arrête de lui envoyer du trafic

Dès que le serveur revient, HAProxy le remet automatiquement dans le pool.

C’est automatique, pas besoin d’intervenir manuellement.

---

## 6. High Availability (Haute Disponibilité)

Objectif : le service reste disponible même si un composant tombe.

Dans le Sprint 1 on a une HA **de base** :
- Si un serveur web tombe → les deux autres continuent
- HAProxy détecte automatiquement la panne grâce aux health checks

Limitation actuelle :
- Si **HAProxy lui-même** tombe, tout le service est down.  
  (On améliorera ça plus tard avec un second HAProxy + Keepalived – hors scope Sprint 1)

---

## 7. Architecture finale du Sprint 1

```
                    ┌─────────────────────┐
                    │   Clients           │
                    │ (navigateurs, curl, │
                    │  Apache Bench...)   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      PC1            │
                    │  HAProxy (:80)      │
                    │  + Nginx (Web1)     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │   PC1    │     │   PC2    │     │   PC3    │
        │  Web1    │     │  Web2    │     │  Web3    │
        │ Nginx    │     │ Nginx    │     │ Nginx    │
        └──────────┘     └──────────┘     └──────────┘
```

Le client tape uniquement l’adresse IP de **PC1**.  
Il ne parle jamais directement à PC2 ou PC3.

---

## 8. Vocabulaire important à connaître  

| Terme              | Signification simple                                      |
|--------------------|-----------------------------------------------------------|
| Frontend           | La partie de HAProxy qui reçoit les requêtes des clients  |
| Backend            | Le groupe de serveurs web derrière HAProxy                |
| Health check       | Test automatique pour savoir si un serveur est vivant     |
| Round-robin        | Répartition tour à tour                                   |
| Reverse Proxy      | Serveur qui se place devant les vrais serveurs web        |
| High Availability  | Le service reste disponible même en cas de panne          |
| Fault Tolerance    | Capacité à continuer malgré une panne                     |

---

## 9. Ce qu’on attend de vous  

- Savoir expliquer **pourquoi** on utilise HAProxy
- Savoir expliquer la différence entre Load Balancing et Reverse Proxy
- Comprendre à quoi servent les health checks
- Être capable de montrer qu’un serveur down est bien retiré automatiquement

Bonne lecture !  
Posez vos questions   si quelque chose n’est pas clair.
