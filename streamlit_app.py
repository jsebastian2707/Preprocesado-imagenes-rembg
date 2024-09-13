import streamlit as st
import os
from app import crop_images_in_folder, remove_background

def main():
    st.title("Procesamiento de Imágenes")

    base_folder = st.text_input("Ruta de la carpeta de imágenes:", "C:/Users/dmedina/Documents/Daniel/Ucc/10mo/Electiva 3/Prueba/Accipiter sp")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Recortar Imágenes"):
            crop_images_in_folder(base_folder)
            st.success("Imágenes recortadas con éxito!")

    with col2:
        if st.button("Remover Fondo"):
            no_bg_folder = os.path.join(base_folder, "no_background")
            remove_background(base_folder, no_bg_folder)
            st.success("Fondo removido de las imágenes con éxito!")

if __name__ == "__main__":
    main()