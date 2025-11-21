#!/usr/bin/env bash
set -e

echo "=== Ajout des fichiers et création du commit ==="
git add .
git commit -m "pushing to both linguere_repo and L_Fablab" || true

echo ""
echo "=== Sur quel repo es-tu actuellement connecté en local ? ==="
echo "1) Repo équipe L_Fablab (yvesBranch)"
echo "2) Repo Render linguere_repo (main)"
read -p "Choisis 1 ou 2 : " choix

# Définition des URLs
REPO_EQUIPE="https://github.com/desire427/L_Fablab.git"
BRANCH_EQUIPE="yvesBranch"

REPO_RENDER="https://github.com/yveskate07/linguere_repo.git"
BRANCH_RENDER="main"

# Fonction générique pour push
push_repo () {
    local url="$1"
    local branch="$2"

    echo ""
    echo "👉 Suppression de l'ancien origin (si existe)..."
    git remote remove origin 2>/dev/null || true

    echo "👉 Ajout du nouveau origin : $url"
    git remote add origin "$url"

    echo "👉 Push sur la branche $branch..."
    git push -u origin "$branch"
}

# Gestion de la logique
if [[ "$choix" == "1" ]]; then
    echo ""
    echo "=== 📌 Tu as indiqué que tu es sur le repo L_Fablab ==="
    echo "➡️ Push sur $BRANCH_EQUIPE"
    push_repo "$REPO_EQUIPE" "$BRANCH_EQUIPE"

    echo ""
    echo "=== Changement de repo pour Render ==="
    push_repo "$REPO_RENDER" "$BRANCH_RENDER"

elif [[ "$choix" == "2" ]]; then
    echo ""
    echo "=== 📌 Tu as indiqué que tu es sur le repo linguere_repo ==="
    echo "➡️ Push sur $BRANCH_RENDER"
    push_repo "$REPO_RENDER" "$BRANCH_RENDER"

    echo ""
    echo "=== Changement de repo pour l'équipe ==="
    push_repo "$REPO_EQUIPE" "$BRANCH_EQUIPE"

else
    echo "❌ Choix invalide. Relance le script."
    exit 1
fi

echo ""
echo "=== ✅ Tous les push ont été effectués correctement ! ==="
