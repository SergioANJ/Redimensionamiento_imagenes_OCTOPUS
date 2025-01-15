from PIL import Image
#import cv2
#import numpy as np


from PIL import Image,ImageDraw,ImageFilter
import os

from PIL import Image, ImageDraw, ImageFilter

def resize_and_crop(image_path, target_size):
    # Abre la imagen
    img = Image.open(image_path)
    
    # Calcula la relación de aspecto
    img_ratio = img.width / img.height
    target_ratio = target_size[0] / target_size[1]

    # Redimensiona la imagen manteniendo la proporción
    if img_ratio > target_ratio:
        # La imagen es más ancha que el objetivo
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)
    else:
        # La imagen es más alta que el objetivo
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)

    # Redimensiona la imagen
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Recorta la imagen al tamaño objetivo
    left = (new_width - target_size[0]) / 2
    top = (new_height - target_size[1]) / 2
    right = (new_width + target_size[0]) / 2
    bottom = (new_height + target_size[1]) / 2

    img = img.crop((left, top, right, bottom))

    return img

def round_corners(image, radius):
    """
    Redondea las esquinas de una imagen.
    :param image: La imagen a la que se le aplicará el redondeo.
    :param radius: El radio de redondeo.
    :return: La imagen con esquinas redondeadas.
    """
    # Crea una máscara con las esquinas redondeadas
    rounded_mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    
    # Aplica la máscara a la imagen
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), rounded_mask)
    
    return rounded_image

# Ejemplo de uso
if __name__ == "__main__":
    # Solicitar al usuario el tamaño deseado
    try:
        width = int(input("Ingrese el ancho deseado (por ejemplo, 1080): "))
        height = int(input("Ingrese la altura deseada (por ejemplo, 960): "))
        target_size = (width, height)

        # Cargar la imagen
        image_path = 'C:/Users/sergio.jimenez/Downloads/img5.png'  # Ruta de la imagen
        resized_image = resize_and_crop(image_path, target_size)

        # Aplicar redondeo de esquinas
        rounded_image = round_corners(resized_image, radius=80)  # Cambia el radio según lo desees

        # Aplicar un filtro de desenfoque
        #blurred_image = rounded_image.filter(ImageFilter.GaussianBlur(2))  # Cambia el valor para más o menos desenfoque

        # Mostrar la imagen estilizada
        rounded_image.show()  # Muestra la imagen redimensionada y estilizada

        # Guardar la imagen estilizada en la misma carpeta de descargas con numeración
        base_save_path = 'C:/Users/sergio.jimenez/Documents/Redimensionamiento_imagenes_OCTOPUS/imagenes_rdm/imagen'
        file_extension = '.png'
        counter = 1
        save_path = f"{base_save_path}_{counter}{file_extension}"

        # Aumentar el contador hasta encontrar un nombre de archivo disponible
        while os.path.exists(save_path):
            counter += 1
            save_path = f"{base_save_path}_{counter}{file_extension}"

        rounded_image.save(save_path)  # Guarda la imagen redimensionada
        print(f"Imagen guardada como: {save_path}")

    except ValueError:
        print("Por favor, ingrese un número válido para el ancho y la altura.")
    except FileNotFoundError:
        print("La ruta de la imagen no es válida. Asegúrese de que la imagen existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")