from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def comprimirImagen(imagen):
    imagenTemporal = Image.open(imagen).convert('RGBA')
    fondo = Image.new('RGBA', imagenTemporal.size, (255, 255, 255))
    outputIoStream = BytesIO()
    imagenTemporalModificada = imagenTemporal.resize((500, 500))
    imagenTemporal = Image.alpha_composite(fondo, imagenTemporal)
    imagenTemporal = imagenTemporal.convert('RGB')
    imagenTemporal.save(
        outputIoStream,
        format='JPEG',
        quality=85
    )
    outputIoStream.seek(0)
    imagen = InMemoryUploadedFile(
        outputIoStream,
        'ImageField',
        "%s.jpg" % imagen.name.split('.')[0],
        'image/jpeg',
        sys.getsizeof(outputIoStream),
        None
    )
    return imagen
