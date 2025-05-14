from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 Mo
    if value.size > max_size:
        raise ValidationError("La taille maximale autorisée est de 10 Mo.")

validate_file_extension = FileExtensionValidator(
    allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'dst'],
    message="Seuls les fichiers PNG, JPG, JPEG, SVG et DST sont autorisés."
)
