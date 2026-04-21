set -o errexit

echo "updating system packages and installing wkhtmltopdf..."
apt-get update && apt-get install -y wkhtmltopdf

echo "setting up python environment by installing requirements..."
pip install -r requirements.txt

echo "collecting static files..."
python manage.py collectstatic --no-input

echo "applying database migrations..."

python manage.py makemigrations

python manage.py migrate

echo "Kindly create a superuser for the Django admin interface if you haven't already."

# python create_superuser.py

# Make sure the script is executable before adding it to version control:
# chmod a+x build.sh
