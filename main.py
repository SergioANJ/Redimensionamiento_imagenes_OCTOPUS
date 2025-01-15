from PIL import Image
"""

def redimensionar_imagen_automaticamente(ruta_imagen,nuevo_ancho):
    try:
        #Abrir
        imagen = Image.open(ruta_imagen)
        #Dimensiones originales de la imagen
        ancho_original, alto_imagen = imagen.size
        #Calcular la nueva altura manteniendo la proporiconalidad
        # Imprimir las dimensiones originales
        print(f'Dimensiones originales: {ancho_original}x{alto_imagen}')
        proporcion = alto_imagen / ancho_original
        nuevo_alto = int(nuevo_ancho * proporcion)
        #Redimensionar la imagen
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
        #Guardar la imagen redimensionada
        imagen_redimensionada.save('imagen_redimensionada.png')
        print(f'Imagen redimensionada a: {nuevo_ancho}x{nuevo_alto}')
    
    except Exception as e:
        print(f"Error al procesar la iamgen", {e})

#Ejemplo de uso:

direccion_imag = 'C:/Users/sergio.jimenez/Downloads/imagen_generada.png'
redimensionar_imagen_automaticamente(direccion_imag, 1000)
"""

import cv2
import numpy as np
"""
def redimensionar_y_recortar(imagen, nuevo_ancho, nuevo_alto):
    # Leer la imagen
    img = cv2.imread(imagen)

    # Redimensionar manteniendo la proporción
    ancho_original, alto_original = img.shape[:2]
    ratio = min(nuevo_ancho/ancho_original, nuevo_alto/alto_original)
    dim = (int(ancho_original * ratio), int(alto_original * ratio))
    img_redimensionada = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Calcular el desplazamiento para centrar la imagen
    x_offset = (nuevo_ancho - dim[0]) // 2
    y_offset = (nuevo_alto - dim[1]) // 2

    # Crear una imagen en blanco del tamaño deseado
    img_final = np.zeros((nuevo_alto, nuevo_ancho, 3), dtype=np.uint8)

    # Copiar la imagen redimensionada en el centro de la nueva imagen
    img_final[y_offset:y_offset+dim[1], x_offset:x_offset+dim[0]] = img_redimensionada

    return img_final

# Ejemplo de uso
imagen_entrada = "C:/Users/sergio.jimenez/Downloads/imagen_generada.png"
nuevo_ancho, nuevo_alto = 1080, 566
imagen_salida = redimensionar_y_recortar(imagen_entrada, nuevo_ancho, nuevo_alto)
cv2.imwrite("imagen_salida.jpg", imagen_salida)
"""

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