import os
import shutil

# Como moviste todo al disco C:, vamos a crear una ruta de pruebas limpia y directa ahí
carpeta_origen = "C:/Prueba_Audiovisual"

# El plan para organizar los materiales de un editor de video
PLAN_EDICION = {
    "Videos_Brutos": [".mp4", ".mov", ".mkv", ".avi"],
    "Audio_y_Musica": [".mp3", ".wav", ".flac", ".m4a"],
    "Efectos_y_Fotos": [".png", ".jpg", ".jpeg", ".gif"],
    "Guiones_y_Textos": [".txt", ".docx", ".pdf"],
}


def preparar_archivos_reales_falsos():
    """Crea la carpeta en el disco C con archivos limpios para la prueba."""
    if not os.path.exists(carpeta_origen):
        os.makedirs(carpeta_origen)

    archivos = [
        "toma1.mp4",
        "entrevista.mov",
        "musica_fondo.mp3",
        "efecto_explosion.wav",
        "miniatura.png",
        "guion_final.txt",
    ]
    for nombre in archivos:
        ruta = os.path.join(carpeta_origen, nombre)
        with open(ruta, "w") as f:
            f.write("datos del archivo de video")
    print(
        f"📦 Carpeta de pruebas creada en: {carpeta_origen} con 6 archivos desordenados."
    )


def clasificar_materiales():
    print("\n🚚 Iniciando los camiones de mudanza automatizados...")

    # Leemos la carpeta del disco C
    elementos = os.listdir(carpeta_origen)
    archivos_movidos = 0

    for nombre in elementos:
        ruta_completa = os.path.join(carpeta_origen, nombre)

        # Validamos que sea un archivo suelto
        if os.path.isfile(ruta_completa):
            _, extension = os.path.splitext(nombre)
            extension = extension.lower()

            # Buscamos su categoría correspondiente
            for carpeta_destino, extensiones_validas in PLAN_EDICION.items():
                if extension in extensiones_validas:
                    # Creamos la subcarpeta dentro de C:/Prueba_Audiovisual
                    ruta_subcarpeta = os.path.join(carpeta_origen, carpeta_destino)
                    if not os.path.exists(ruta_subcarpeta):
                        os.makedirs(ruta_subcarpeta)

                    # Movemos el archivo físico
                    ruta_final_archivo = os.path.join(ruta_subcarpeta, nombre)
                    shutil.move(ruta_completa, ruta_final_archivo)
                    print(f"   -> Moviendo '{nombre}' a la carpeta [{carpeta_destino}]")
                    archivos_movidos += 1
                    break

    print(
        f"\n🎉 ¡Operación terminada! Se han clasificado {archivos_movidos} archivos con éxito."
    )


# --- EJECUCIÓN ---
preparar_archivos_reales_falsos()
clasificar_materiales()
