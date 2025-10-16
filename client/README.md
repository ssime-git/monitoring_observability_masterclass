## Avant de commencer

> Téléchargez les données au format *csv* des vendeurs et des produits :

```bash
wget -P data https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/data/products.csv
wget -P data https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/data/vendors.csv
```

> Lancez l'application composée de FastAPI, Postgres et Redis depuis les dossiers `prometheus_grafana` ou `elastic_apm`.

## Présentations des programmes

Points communs entre les programmes :

- Connecte quelques utilisateurs à FastAPI afin de récupérer leur token respectif pour requêter.
- Déclare un client asynchrone et lance des requêtes selon un interval de temps à partir d'un utilisateur choisi aléatoirement.

Les programmes :

- **00-post_transactions_low.py** : Les requêtes sont envoyées toutes les 0 à 3 secondes. Les requêtes sont des demandes d'enregistrements de transactions.

- **01-wrong_vendor_id.py** : Les requêtes sont envoyées toutes les 4 à 6 secondes. Les requêtes sont des demandes d'enregistrements de transactions mais l'id du vendeur n'est pas définit dans la table `vendors` pour lever une exception.

- **02-post_transactions_high.py** : Identique au script `00` mais les requêtes sont envoyées toutes les 20 micro secondes.

- **03-resupply_products.py** : Les requêtes sont envoyées toutes les 30 secondes. La requête ajoute 50 à la quantité de chaque produit dont la quantité est inférieur à 50.

## Lancer des scripts

Les scripts précédent se lancent à l'aide de la commande suivante :

```bash
python3 <script.py> $(docker inspect fastapi | grep -o '"IPAddress": "[^"]*' | tail -1 | awk -F'"' '{print $4}'\n)
```

> [!TIP]
> L'instruction qui suit le nom du script permet de récupérer l'adresse IP du conteneur Docker où FastAPI tourne. Nos programmes communiquent avec FastAPI et ont donc besoin de l'adresse IP de ce dernier pour lui envoyer des requêtes.
