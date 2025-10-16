## Contexte

Déploiement de 6 services :

- Postgres : base de données principale
- FastAPI : intermédiaire entre l'utilisateur et la base de données ; instancie un agent APM pour collecter et envoyer des données de performances
- Redis : mémoire cache
- Elasticsearch : base de données secondaire
- Serveur APM : intermédiaire entre l'agent APM et Elasticsearch
- Kibana : interface utilisateur connectée à Elasticsearch

La démonstration a pour but d'introduire la solution Elasticsearch APM
Un agent APM est implémenté dans le code de l'application FastAPI.
Celui-ci envoie des données de performance au Serveur APM qui se charge de valider, processer et transformer les données avant de les envoyer à Elasticsearch.

## Déploiement

> Lancez le déploiement des services à l'aide du fichier `Makefile`.

```bash
make
```

> [!IMPORTANT]
> Déploie les conteneurs depuis le fichier `docker-compose.yml`.

> [!WARNING]
> N'oubliez pas de charger les scripts *SQL*  à l'aide du [README](https://github.com/DataScientest/dst_masterclass/tree/feature/issue-17/demo-prometheus_grafana-elasticapm/Monitoring_Observability/demo) du dossier `demo`.

## Utilisation

Rendez-vous à l'adresse <VM_IP_address|localhost>:5000/docs.  
Requêtez la route */hello*.

> [!TIP]
> Utilisez les programmes du dossier `client` pour générer des requêtes aléatoires.

## Visualisation

Rendez-vous à l'adresse <VM_IP_address|localhost>:5601.  
Naviguez dans l'onglet *Observability / APM*.  
Cliquez sur le service *fastapi*.  
Vous trouvez plusieurs panels en lien avec la performance de l'application.  
En bas de la page, vous trouverez les traces et les spans qui la composent s'il y en a.
