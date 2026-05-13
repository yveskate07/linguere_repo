#!/bin/bash

# Aller à l'emplacement du script
cd "$(dirname "$0")"

# Définir les dossiers à exclure (ton environnement virtuel)
EXCLUDE_DIR=".venv"

echo "🔍 Nettoyage des migrations Django (en ignorant $EXCLUDE_DIR)..."

# Supprimer les migrations en excluant le dossier .venv
find . -path "./$EXCLUDE_DIR" -prune -o -path "*/migrations/*.py" ! -name "__init__.py" -delete
find . -path "./$EXCLUDE_DIR" -prune -o -path "*/migrations/*.pyc" -delete

echo "🧹 Migrations supprimées."

echo ""
echo "❓ Voulez-vous également supprimer tous les dossiers __pycache__ ? (oui/non)"
read -r answer

answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

if [ "$answer" = "oui" ]; then
    echo "🔍 Suppression des dossiers __pycache__ (en ignorant $EXCLUDE_DIR)..."
    # Supprimer les pycache en excluant le dossier .venv
    find . -path "./$EXCLUDE_DIR" -prune -o -type d -name "__pycache__" -exec rm -rf {} +
    echo "🧹 Tous les __pycache__ ont été supprimés."
else
    echo "⏭️ Suppression des __pycache__ ignorée."
fi

echo ""
echo "⚠️ Pensez à recréer les migrations avec :"
echo "python manage.py makemigrations && python manage.py migrate"
