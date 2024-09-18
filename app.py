import os
from PIL import Image
from rembg import remove
import cv2

def getfolders(folder_path):
    return os.listdir(folder_path)

def crop_images_in_folder(folder_path, output_size=(224, 224)):
    """
    Itera a través de las imágenes en una carpeta y las recorta al tamaño especificado.
    Guarda las imágenes recortadas en un subdirectorio llamado 'result'.
    
    Args:
    folder_path (str): Ruta a la carpeta que contiene las imágenes
    output_size (tuple): Tamaño de salida deseado (ancho, alto)
    """
    output_folder = os.path.join(folder_path, "result")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                left = (width - output_size[0]) // 2
                top = (height - output_size[1]) // 2
                right = left + output_size[0]
                bottom = top + output_size[1]

                cropped_img = img.crop((left, top, right, bottom))
                
                output_filename = f"cropped_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                cropped_img.save(output_path)

    print(f"Todas las imagenes han sido cortadas. Estan guardadas en: {output_folder}")


def resize_images_in_folder(folder_path, output_size=(224, 224)):
    # Crear carpetas de salida
    output_folder = os.path.join(folder_path, "cropped_images_square")
    output_folder2 = os.path.join(folder_path, "result")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_folder2, exist_ok=True)

    # Parte 1: Recortar las imágenes para hacerlas cuadradas
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Definir el área de recorte para hacer la imagen cuadrada
                if width > height:
                    new_width = height
                    left = (width - new_width) // 2
                    upper = 0
                    right = left + new_width
                    lower = height
                else:
                    new_height = width
                    left = 0
                    upper = (height - new_height) // 2
                    right = width
                    lower = upper + new_height

                # Recortar la imagen
                cropped_img = img.crop((left, upper, right, lower))
                
                # Guardar la imagen recortada
                output_filename = f"cropped_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                cropped_img.save(output_path)

    # Parte 2: Redimensionar las imágenes recortadas
    for filename in os.listdir(output_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(output_folder, filename)
            
            # Leer la imagen recortada con OpenCV
            image = cv2.imread(file_path)
            
            if image is not None:  # Verificar si la imagen se cargó correctamente
                # Redimensionar la imagen al tamaño deseado
                resized_image = cv2.resize(image, output_size)
                
                # Generar nombre de archivo de salida
                output_filename = f"resize_{filename}"
                output_path = os.path.join(output_folder2, output_filename)
                
                # Guardar la imagen redimensionada
                cv2.imwrite(output_path, resized_image)

    print(f"Todas las imágenes han sido recortadas y redimensionadas. Las imágenes recortadas están en: {output_folder}, y las redimensionadas en: {output_folder2}")

def remove_background(input_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"nobg_{os.path.splitext(filename)[0]}.png")

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path, format='PNG')

    print(f"Fondo removido. Iamgenes procesadas estan guardadas en: {output_folder}")

