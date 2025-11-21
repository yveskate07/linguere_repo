from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 Mo
    if value.size > max_size:
        raise ValidationError("La taille maximale autorisée est de 10 Mo.")

validate_file_extension1 = FileExtensionValidator(
    allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'dst'],
    message="Seuls les fichiers PNG, JPG, JPEG, SVG et DST sont autorisés."
)

validate_file_extension2 = FileExtensionValidator(
    allowed_extensions=['stl', 'dxf', 'ai'],
    message="Seuls les fichiers STL, DXF, AI sont autorisés."
)

validate_file_extension3 = FileExtensionValidator(
    allowed_extensions=['svg', 'dxf', 'ai'],
    message="Seuls les fichiers SVG, DXF, AI sont autorisés."
)

validate_file_extension4 = FileExtensionValidator(
    allowed_extensions=['stl', 'obj'],
    message="Seuls les fichiers STL, OBJ sont autorisés."
)

