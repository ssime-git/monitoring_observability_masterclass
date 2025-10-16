## Contexte

Déploiement de 5 services :

- Postgres : base de données principale
- FastAPI : intermédiaire entre l'utilisateur et la base de données ; instancie un instrumentateur Prometheus afin de générer des métriques
- Redis : mémoire cache
- Prometheus : base de données secondaire ; intermédiaire entre l'instrumentateur de FastAPI et Grafana
- Grafana : interface utilisateur connectée à Postgres et Prometheus

La démonstration a pour but d'introduire l'utilisation de Prometheus et Grafana.
Un instrumentateur est implémenté dans le code de FastAPI.
Celui-ci envoie les données des métriques à la base de données Prometheus qui se charge de stocker les données avant de les envoyer à Grafana.

## Déploiement

> Remplissez le fichier `.env` avec la commande suivante :

```bash
echo "USER_ID=$(id -u)" > .env
```

> Créez le dossier `data` dans le dossier `requirements/prometheus`.

```bash
mkdir requirements/prometheus/data
```

> [!IMPORTANT]
> Ces étapes sont nécessaires pour éviter les problèmes de droits des volumes de Prometheus et de Grafana.

> Lancez le déploiement des services à l'aide du fichier `Makefile`.

```bash
make
```

> [!IMPORTANT]
> Déploie les conteneurs depuis le fichier `docker-compose.yml`.  
> Lance les *exporters Prometheus* respectifs de Redis et Postgres.

> [!WARNING]
> N'oubliez pas de charger les scripts *SQL*  à l'aide du [README](https://github.com/DataScientest/dst_masterclass/tree/feature/issue-17/demo-prometheus_grafana-elasticapm/Monitoring_Observability/demo) du dossier `demo`.

## Utilisation

Rendez-vous à l'adresse <VM_IP_address|localhost>:5000/docs.  
Requêtez la route */hello*.

> [!TIP]
> Utilisez les programmes du dossier `client` pour générer des requêtes aléatoires.

## Visualisation

Rendez-vous à l'adresse <VM_IP_address|localhost>:3000.  
Entrez les identifiants suivants : admin et admin_password123.  
Naviguez dans l'onglet *Dashboards*.  
Cliquez sur le dashboard *Demo*.
