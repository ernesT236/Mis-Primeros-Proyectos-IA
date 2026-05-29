import os
import shutil

# =========================================================================
# ⚠️ CONFIGURACIÓN DE TU CARPETA REAL
# Reemplaza el texto de abajo por la ruta de la carpeta que creaste en el Paso 1.
# Ejemplo en Windows: "C:/Users/TuUsuario/Desktop/PruebaOrdenadoReal"
# Nota: Usa barras normales (/) en lugar de barras invertidas (\) para evitar errores.
# =========================================================================
carpeta_a_organizar = "C:/PruebaOrdenadoReal"

# El plan de organización completo que ya creamos
PLAN_ORGANIZACION = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documentos": [
        ".pdf",
        ".docx",
        ".txt",
        ".xlsx",
        ".pptx",
        ".csv",
        ".odt",
        ".ods",
    ],
    "Programas_y_Comprimidos": [
        ".exe",
        ".zip",
        ".rar",
        ".msi",
        ".7z",
        ".tar",
        ".gz",
    ],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"],
    "Musica_y_Audio": [".mp3", ".wav", ".wma", ".flac", ".m4a", ".ogg"],
    "Libros_y_Epub": [".epub", ".mobi", ".azw3"],
    "Codigo_y_Desarrollo": [
        ".py",
        ".html",
        ".css",
        ".js",
        ".json",
        ".ipynb",
        ".cpp",
    ],
}


def organizar_carpeta_real():
    """Lee tu carpeta real, detecta las extensiones y mueve tus archivos."""
    # Seguridad: Verificamos si la ruta que pusiste existe de verdad
    if not os.path.exists(carpeta_a_organizar):
        print(
            f"❌ Error: La ruta '{carpeta_a_organizar}' no existe. Por favor, revísala."
        )
        return

    print(f"\n🚀 Iniciando limpieza en: {carpeta_a_organizar}")
    archivos_movidos = 0

    for nombre_archivo in os.listdir(carpeta_a_organizar):
        ruta_completa = os.path.join(carpeta_a_organizar, nombre_archivo)

        if os.path.isfile(ruta_completa):
            _, extension = os.path.splitext(nombre_archivo)
            extension = extension.lower()

            se_organizo = False

            for nombre_carpeta, extensiones_validas in PLAN_ORGANIZACION.items():
                if extension in extensiones_validas:
                    ruta_destino_carpeta = os.path.join(
                        carpeta_a_organizar,
                        "C:/PruebaOrdenadoReal",
                    )
                    if not os.path.exists(ruta_destino_carpeta):
                        os.makedirs(ruta_destino_carpeta)

                    ruta_destino_archivo = os.path.join(
                        ruta_destino_carpeta, nombre_archivo
                    )
                    shutil.move(ruta_completa, ruta_destino_archivo)
                    print(
                        f"🚚 Movido de verdad: '{nombre_archivo}' -> [{nombre_carpeta}]"
                    )
                    se_organizo = True
                    archivos_movidos += 1
                    break

            if not se_organizo:
                print(f"⚠️ Archivo ignorado (sin categoría): '{nombre_archivo}'")

    print(
        f"\n🎉 ¡Limpieza terminada! Se organizaron {archivos_movidos} archivos reales."
    )


# --- EJECUCIÓN ---
organizar_carpeta_real()
