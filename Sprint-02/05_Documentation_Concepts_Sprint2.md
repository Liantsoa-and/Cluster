# Documentation – Concepts à comprendre (Sprint 2)
**Ajout et retrait dynamique de serveurs (Dynamic Cluster)**

---

## 1. Pourquoi le Sprint 2 existe-t-il ?

Au Sprint 1, on a un cluster **statique** :
- Les 3 serveurs sont écrits en dur dans `haproxy.cfg`
- Pour ajouter ou enlever un serveur, il faut modifier le fichier à la main et recharger HAProxy

C’est pénible et risqué en production.  
Le Sprint 2 apporte l’**élasticité** : on peut ajouter ou retirer des serveurs **à chaud**, sans interruption de service.

---

## 2. Les deux façons de rendre HAProxy dynamique

### Méthode 1 : Réécriture du fichier de configuration + reload
- On modifie `haproxy.cfg` avec un script
- On fait `systemctl reload haproxy` (reload gracieux)
- Avantage : simple à comprendre
- Inconvénient : un peu plus lourd, et il faut gérer le fichier proprement

### Méthode 2 : Runtime API (recommandée) ← celle qu’on utilise
HAProxy possède un **socket d’administration** qui permet d’envoyer des commandes en direct :

```bash
echo "add server web_servers/web4 192.168.1.50:80 check" | socat stdio /run/haproxy/admin.sock
echo "del server web_servers/web4" | socat stdio /run/haproxy/admin.sock
echo "show servers state" | socat stdio /run/haproxy/admin.sock
```

Avantages :
- Très rapide
- Pas besoin de toucher au fichier de config pour les opérations courantes
- Les changements sont immédiats

Inconvénient :
- Les serveurs ajoutés via Runtime API **disparaissent** si on redémarre HAProxy (il faut les re-ajouter ou les mettre aussi dans le fichier de config pour la persistance).

Dans un vrai projet on combine les deux : Runtime API pour l’opérationnel + mise à jour du fichier pour la persistance.

---

## 3. Ce que doit faire notre outil Python

L’outil (`manager.py`) est un **petit chef d’orchestre** qui parle au socket HAProxy.

Fonctionnalités minimales attendues :

| Commande                  | Action                                      |
|---------------------------|---------------------------------------------|
| `list`                    | Affiche tous les serveurs du backend + leur état (UP/DOWN) |
| `add <nom> <ip>`          | Ajoute un serveur au backend avec health check |
| `remove <nom>`            | Supprime un serveur du backend              |
| `enable <nom>` / `disable`| Active ou désactive temporairement un serveur |
| `help`                    | Affiche l’aide                              |

Exemple d’utilisation demain :
```bash
python3 manager.py list
python3 manager.py remove web3
python3 manager.py add web3 192.168.1.12
python3 manager.py list
```

---

## 4. Notions importantes à bien comprendre

### Élasticité (Elasticity)
Capacité d’un système à **grandir ou rétrécir** facilement selon la charge.  
C’est l’objectif principal du Sprint 2.

### Orchestration légère
On n’utilise pas Kubernetes ou Docker Swarm.  
On fait une orchestration **très simple** avec un script Python + HAProxy.  
C’est pédagogique et ça suffit pour comprendre les principes.

### Service Discovery (découverte de services)
Dans les gros systèmes, les serveurs s’enregistrent tout seuls (Consul, etcd, Kubernetes…).  
Ici on fait du **Service Discovery manuel** : c’est l’administrateur (toi) qui dit « ajoute ce serveur ».

### Différence entre disable et remove
- `disable` : le serveur reste dans la config mais ne reçoit plus de trafic (utile pour maintenance)
- `remove` / `del server` : le serveur est complètement enlevé du backend

---

## 5. Architecture mise à jour (Sprint 2)

```
                    ┌─────────────────────────────┐
                    │         Clients             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │           PC1               │
                    │  HAProxy + Runtime API      │
                    │  + manager.py (Python)      │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
        ┌──────────┐         ┌──────────┐         ┌──────────┐
        │   PC1    │         │   PC2    │         │   PC3    │
        │  Web1    │         │  Web2    │         │  Web3    │
        └──────────┘         └──────────┘         └──────────┘
                                      ▲
                                      │
                          On peut ajouter / retirer
                          n’importe lequel à chaud
```

---

## 6. Vocabulaire Sprint 2

| Terme              | Explication simple |
|--------------------|--------------------|
| Runtime API        | Interface en direct de HAProxy (via socket) |
| Socket admin       | Fichier spécial (`/run/haproxy/admin.sock`) qui reçoit les commandes |
| add server         | Commande pour ajouter un serveur à chaud |
| del server         | Commande pour supprimer un serveur à chaud |
| show servers state | Affiche l’état de tous les serveurs |
| Élasticité         | Pouvoir grandir/réduire le cluster facilement |
| Orchestration      | Automatisation de la gestion des serveurs |

---

## 7. Limites de notre solution (à connaître)

- Les serveurs ajoutés via Runtime API ne survivent pas à un redémarrage de HAProxy (sauf si on les ajoute aussi dans le fichier `.cfg`).
- Pas encore de véritable interface web (on reste en ligne de commande pour rester simple).
- Pas de vérification automatique que le serveur est bien joignable avant de l’ajouter (on peut l’ajouter plus tard).

Ces limites sont normales pour un Sprint 2 étudiant. L’important est de comprendre le principe.

---

## 8. Ce qu’on attend de vous demain

- Savoir expliquer la différence entre configuration statique (Sprint 1) et dynamique (Sprint 2)
- Savoir utiliser les commandes `list`, `add` et `remove`
- Montrer qu’on peut retirer un serveur et qu’il disparaît bien du load balancing
- Montrer qu’on peut le remettre ensuite

Bonne lecture !
