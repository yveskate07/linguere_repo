# À faire:

## 1. Section Boutique: Integrer Channels pour du temps reel avec notification de succes ou echec de la commande, temps reels aussi pour les filtres etc
- Lister les articles pour chaque categories principales selectionnées ✅
- Lister les articles pour chaque sous categorie selectionnée ✅
- Filtrer les articles affichés par prix croissants/décroissants ✅
- Filtrer les articles par le prix selectionné ✅
- Filtrer les articles par disponibilité ✅
- Pour chaque article, fonctionnalité pour afficher un aperçu rapide ✅
- Pour chaque article, fonctionnalité pour ajouter l'article dans le panier ✅
- Pagination: Afficher l'ensemble des article par page ✅
- Creer les models necessaires (articles, commandes etc.) ✅
- changeCartItemQuantity ✅
- removeFromCart ✅
- Tri de produits par ordre croissant decroissant ( s'assurer que tous les produits ont des urls d'images valides) ✅
- Filtre de produits par Categories et Disponibilité ✅
- Changer le filtre de prix ✅
- Adapter les badges de stock en fonction du stock disponible ✅
- Categoriser les types de filtres a cause des min max de prix ✅
- fonction js qui a chaque fois que l'on clique sur le panier pour l'afficher, met en place tous les elements qu'il contient ✅
- Generer des produits de toutes categories pour des tests ✅
- inclure la categorie de produits dans les donnees envoyees par ws au back-end ✅
- Tester l'ajout, suppression des items dans le panier ✅
- Ne pas ajouter deux fois le meme item dans le panier ✅
- au demarrage chaque produit html a l'id de son item ✅
- demander si les frais des services doivent etre payés sur la plateforme ou non.✅
- si le user connecté est un superadmin, la section user doit conduire a django admin
- creer un model order pour regrouper toutes les infos de la commande ✅
- informer Fablab et le client par mail que la commande a été acceptée et est en cours de livraison. ✅
- Changer le path dans Shop.routings.py pour que le consummer accepte aussi uuid='anonymous' ✅
- Verifiez pourquoi le badge stock de certains articles ne s'affiche pas correctement ✅
- penser a la conversion des devises ( le prix total doit etre multiple de 5 et en Francs XOF )✅
- creer un notify url pour le paiement ✅
- Gerer la pagination pour les filtres et tri. ✅
- integrer API de paiement (recuperer SITE_ID et API_KEY) ✅
- les liens des images des produits ne s'affichent pas entierement ( url relatifs et non absolu ) ✅
- Il faut integrer sweet alert pour confirmer les paiements ✅
- pour le panier, au premier rechargement il ne s'actualise pas. ✅ pb de connexion
- Faire tous les tests ajouter supprimer augmenter diminuer ✅
- Faire tous les tests ajouter supprimer augmenter diminuer mais pour les autres templates. ✅
- Trouver un moyen d'identifier les user anonyme. ✅
- Faire les tests d'envoi de mail ✅
- Il faut que le modal du panier soit accessible partout dans n'importe quelle page. ✅
- Pour les mails, la liste des articles ne s'affiche pas ✅
- Il faut que le modal du paiement soit accessible partout, dans n'importe quelle page. ✅
- Personnaliser l'interface admin ✅
- La vue utilisateur doit conduire vers django admin si user.is_admin = True ✅
- La fonctionnalité de paiement ne doit etre accessible que pour un utilisateur de fablab. ✅
- Facture de son paiement ✅
- Visualiser (imaginer) le trajet ustilisateur des qu'il arrive dans la boutique. BE FE ✅
- Le panier doit etre relié soit à un client ou une session au cas où le client n'est pas encore connecté. ✅
- Revoir tout le process incluant CartItem ✅
- Plus tard, mettre a jour le panier pour la premiere fois sans ws ✅
- panier disponible partout et sa logique aussi ✅
- revoir la logique que Chagpt a donné pour les req à cinetpay ✅
- Tout preparer pour les prochains push ✅
- Plus besoin de renseigner Nom et prenom pour finaliser commande s'il (client) est connecte (Alphonse) ✅
- Pour la vue rapide, les fonctions dans handlequantity doivent envoyer des requetes ws ✅
- Faire un test de toutes les fonctionnalités du panier ✅
- Enlever les autres fichiers js dans tous les autres templates ✅
- Enlever l'action qui s'execute apres confirmation de paiement dans cart/index ✅
- Enlever toutes les anciennes fonctions du ws qui ne sont plus utiles ✅
- Faire un test de la vue rapide ✅
- Utiliser un base.html pour les shop temp ✅
- Important revenir sur l'aspect de paginator ✅
  ------------------------------------ A FAIRE --------------------------------------------------------

1. proceder au paiement (simulation: besoin de API_KEY et autres param.) (Anta)
      - si les parametres sont fournis, voir dans ws_receive et decommenter processpayment dans process_payment

2. Faire un test complet de AntaBackEnd
   - Shop:
      - Quand l'utilisateur va dans les pages de Shop, l'on cree automatiquement une commande qui est associee au client actuel et qui a complete = False. C'est cette commande qui sera plus tard mise a jour au fur et a mesure pour aboutir a une commande complete
      - 
    - Activities:
        - il manque des activites, photos et infos
        - il faudrait demander connexion/inscription que pour la finalisation de commandes ou inscription a une formation

    - inclure une vue/fonctionnalité de recuperation de mot de passe avec lien et tout
    - inclure une vue/fonctionnalité de changement de mot de passe avec lien et tout
    - Difficultés que je rencontre:
        - les toasts doivent s'afficher sur toutes les pages
        - problemes d'authentification 535 de google
            - le problemes est dû au mot de passe d'application

    - integrer redis et celeris pour les taches en arriere plan
    - revoir les vues de connexions
    - pour ce qui est envoie de mails ou taches qui ne doit pas bloquer le site internet, utiliser celeris et redis
    - verifier les relations entre les tables, voir si aucune relation n'implique la suppression involontaire et inattendue des donnees
    - pour un utilisateur anonyme, pour le retrouver dans la bd, utiliser le champ email.
    - Inserer vue d'activation pour les nouveaux comptes  
    - voir la section temoignages sur Accueil
    - Ajouter des images aux formations sur Accueil
    - regler la section Expertise technique sur Accueil
    - regler la section Creativité sans limites sur Accueil
    - regler la section INNOVATION & FABRICATION NUMÉRIQUE sur Accueil
    - regler la section Nouveautes sur Accueil dans le header
        
    - bien ajuster les couleurs du admin
    - revoir paginator


# Comment lancer le serveur en local/developpement:

## 1. Lancer le runserver:
- Ouvrez un terminal puis executer : ```python manage.py runserver 127.0.0.1:8001```
- Ouvrez un second terminal puis executer : ```DJANGO_SETTINGS_MODULE=AntaBackEnd.settings daphne AntaBackEnd.asgi:application```
- Ouvrez un troisieme terminal puis executer : ```docker run --rm -p 6379:6379 redis:7``` avec docker déjà ouvert.

## 2. Aller à l'adresse 127.0.0.1:0:8001

## 3 Quelques commandes celery:
celery -A AntaBackEnd worker -l info

user vient dans boutique > views.py retourne paginator > produits affiches dans template index.html >
sur la page des produits, le user peut:
- filtrer les produits 
- trier les produits
- afficher la vue rapide d'un produit
    - et ajouter ce produit
- ajouter un produit
    - clic sur 'ajouter au panier' > addToCart  in FE fired with product_id as parameter > add_to_cart in the consumer fired > item added in db > item_id and product_id sent to the FE > these datas are stored in cart variable > updateDisplay fired.
- supprimer un produit
    - clic sur poubelle > removeFromCart in FE fired with item_id as parameter > remove_item_from_cart in the consumer fired > item removed in db > updateDisplay fired.

- augmenter/diminuer un produit
    - clic sur '+' > changeCartItemQuantity in FE fired with item_id as parameter > change_item_qtty in the consumer fired > quantity changed in db > quantity and product_id sent to the FE > these datas are stored in cart variable > updateDisplay fired.

- payer la commande:
    - une fois le panier plein, clic sur 'passer la commande' > getTotalPriceAndDisplayPaymentModal in payment.js fired > in the BE, get or create an order related to his articles > order sent to the FE > payment modal opened > user filling the payment-form for the payment > clic sur 'payer' > datas gathered and sent to cinetpay > if payment successfull, order marked as complete > invoice created > mail sent > items in the card deleted > done

    - traiter le cas ou le paiement echoue
    