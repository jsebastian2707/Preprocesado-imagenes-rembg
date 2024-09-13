import os
from PIL import Image
from rembg import remove

def crop_images_in_folder(folder_path, output_size=(224, 224)):
    """
    Itera a través de las imágenes en una carpeta y las recorta al tamaño especificado.
    Guarda las imágenes recortadas en un subdirectorio llamado 'cropped_images'.
    
    Args:
    folder_path (str): Ruta a la carpeta que contiene las imágenes
    output_size (tuple): Tamaño de salida deseado (ancho, alto)
    """
    output_folder = os.path.join(folder_path, "cropped_images")
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

