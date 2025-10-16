## Avant de lancer les démonstrations

> Téléchargez les scripts *SQL*, depuis le S3, d'insertion de données des vendeurs et des produits.  
> Copiez ces scripts entre les 2 démonstrations.

```bash
wget -P elastic_apm/requirements/postgres/initdb.d https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/postgres/01-insert_into_vendors.sql
cp elastic_apm/requirements/postgres/initdb.d/01-insert_into_vendors.sql prometheus_grafana/requirements/postgres/initdb.d
wget -P elastic_apm/requirements/postgres/initdb.d https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/postgres/02-insert_into_products.sql
cp elastic_apm/requirements/postgres/initdb.d/02-insert_into_products.sql prometheus_grafana/requirements/postgres/initdb.d
```

## Définitions des dossiers

- **client** :  Programmes Python générant des requêtes synchrones ou asynchrones vers FastAPI.

- **prometheus_grafana** : Démonstration.

- **elastic_apm** : Démonstration.

## Points communs entre les démonstrations

### Postgres

Nous créons une base de données nommée *suppliers* ainsi que 3 tables via le script `initdb.d/00-create_suppliers_database.sql`.  

Les 3 tables sont :

- **vendors** :
    - *id* : clé primaire ;
    - *qualification* : grade de qualification.

- **products** :
    - *id* : clé primaire ;
    - *name* : nom du produit ;
    - *price* : prix du produit ;
    - *quantity* : quantité restante du produit ;
    - *required_qualification* : grade de qualification requise pour vendre le produit.

- **transactions** : transaction par produit
    - *id* : référence de la transaction ;
    - *product_id* : référence du produit ;
    - *vendor_id* : référence du vendeur ;
    - *action* : 'withdrawal' (retrait) ou 'addition' (ajout) ;
    - *quantity* : quantité du produit ;
    - *transaction_date* : date de la transaction, date courante par défaut.
La clé primaire est la pair *id* et *product_id*.

### FastAPI

Plusieurs routes ont été définies :

#### login

Cette route gère la connection et l'authentification des utilisateurs.

Chaque utilisateur possède les attributs suivants :

- *username* : le nom de l'utilisateur ;
- *password* : le mot de passe de l'utilisateur ;
- *id* : l'id de vendeur de l'utilisateur.

**Connection** : L'utilisateur se connecte en renseignant son nom et son mot de passe. Si la connection est un succès, les informations de l'utilisateur sont enregistrées dans Redis. L'objet *LoginManager* se charge d'enregistrer le nom de l'utilisateur et le token qui lui est associé.

**Authentification** : Lors de l'exécution d'une requête nécessitant l'authentification de l'utilisateur, la fonction `load_user(username)` se charge de renvoyer les informations de l'utilisateur s'il est trouvé.

#### products

**GET /** : Renvoie la liste des produits stockés dans Postgres.

**PUT /quantity** : Sélectionne tous les produits dont la quantité restante est strictement inférieur à 50. Puis, ajoute 50 à la quantité de chacun des produits.

#### transaction

**GET /** : Renvoie toutes les transactions stockées dans Postgres.

**POST /** : Crée une transaction d'un produit par un vendeur. Vérifie si il y a assez de produit, si oui, la quantité du produit est mise à jour et la transaction est créée.

#### main

Imprime seulement "Hello World!"


Les requêtes vers Postgres s'effectuent de 2 manières :

- `postgres.py` : À chaque requête, une nouvelle connection est créée.

- `postgres_2.py` : Une *pool* de connections est créée avec entre 10 et 20 connections. Les requêtes n'ont plus besoin de créer leur connection mais utilise celles déjà instanciées. Cette méthode n'a été utilisée que dans le fichier `transactions.py`.

### Redis

La configuration du fichier `redis_7.2.conf` permet d'accepter les connexions des clients depuis n'importe quelles adresses IP et ne demande aucun mot de passe ou identifiant.
