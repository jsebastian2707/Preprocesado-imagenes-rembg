import os
from PIL import Image
from rembg import remove

# Constantes
CONST_MAKE_REESCALE = True # True para redimensionar y recortar, False para solo recortar
CONST_OUTPUT_WIDTH = 224
CONST_FILLBG_COLOR = (186, 202, 227, 255)
CONST_NOBG_FOLDER = "no_background"
CONST_FILLBG_FOLDER = "fill_background"
CONST_RESIZE_FOLDER = "resize_images"

# +---------------------+      +---------------------+      +---------------------+
# |resize or crop images| -- > |  remove background  | -- > |  fill background    |
# +---------------------+      +---------------------+      +---------------------+

def getfolders(folder_path):
    # Verifica si el folder_path es válido
    if not os.path.exists(folder_path):
        return []  # Retorna una lista vacía si la ruta no existe
    
    # Lista únicamente los directorios en la carpeta especificada
    return [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]

def resize_images_in_folder(folder_path):
    if CONST_MAKE_REESCALE:
        escale_images_in_folder(folder_path)
    else:
        crop_images_in_folder(folder_path)

def crop_images_in_folder(folder_path):
    """
    Itera a través de las imágenes en una carpeta y las recorta al tamaño especificado.
    Guarda las imágenes recortadas en un subdirectorio llamado "resize_images".
    
    Args:
    folder_path (str): Ruta a la carpeta que contiene las imágenes
    output_size (tuple): Tamaño de salida deseado (ancho, alto)
    """
    output_folder = os.path.join(folder_path, CONST_RESIZE_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                left = (width - CONST_OUTPUT_WIDTH) // 2
                top = (height - CONST_OUTPUT_WIDTH) // 2
                right = left + CONST_OUTPUT_WIDTH
                bottom = top + CONST_OUTPUT_WIDTH

                cropped_img = img.crop((left, top, right, bottom))
                
                output_filename = f"cropped_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                cropped_img.save(output_path)

    print(f"Todas las imagenes han sido cortadas. Estan guardadas en: {output_folder}")

def escale_images_in_folder(folder_path, output_size=(224, 224)):
    # Crear carpetas de salida
    output_folder = os.path.join(folder_path, CONST_RESIZE_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

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
                resize_img = cropped_img.resize(output_size)
                
                # Guardar la imagen recortada
                output_filename = f"escale_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                resize_img.save(output_path)
    

    print(f"Todas las imágenes han sido recortadas y redimensionadas. Las imágenes recortadas están en: {output_folder}, y las redimensionadas en: ")

def remove_background(folder_path):
    input_folder = os.path.join(folder_path, CONST_RESIZE_FOLDER)
    output_folder = os.path.join(folder_path, CONST_NOBG_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"nobg_{os.path.splitext(filename)[0]}.png")

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path, format='PNG')

    print(f"Fondo removido. Imagenes procesadas estan guardadas en: {output_folder}")


def fillbgimages_in_folder(folder_path):
    input_folder = os.path.join(folder_path, CONST_NOBG_FOLDER)
    output_folder = os.path.join(folder_path, CONST_FILLBG_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(input_folder, filename)
            with Image.open(file_path).convert("RGBA") as img:
                # Create a new image with a green background
               # Create a new image with a sky blue background
                sky_blue_background = Image.new("RGBA", (CONST_OUTPUT_WIDTH, CONST_OUTPUT_WIDTH), CONST_FILLBG_COLOR)
                
                # Paste the original image on top of the sky blue background
                sky_blue_background.paste(img, (0, 0), img)
                
                # Convert to RGB mode to remove alpha channel (transparency)
                green_image = sky_blue_background.convert("RGB")
                # Save the result
                output_filename = f"fillbg{filename}"
                output_path = os.path.join(output_folder, output_filename)
                green_image.save(output_path)

    print(f"Todas las imagenes han sido rellenadas. Estan guardadas en: {output_folder}")

