import os
import glob
import shutil
from datetime import datetime

def mover_ultimas_imagenes():
    # 1. Identificar la carpeta de Descargas
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")
    
    # Verificar si la carpeta de descargas existe
    if not os.path.exists(downloads_dir):
        print(f"No se encontró la carpeta de Descargas en: {downloads_dir}")
        return

    # 2. Encontrar extensiones de imagen comunes
    extensiones = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"]
    archivos_imagen = []
    
    for ext in extensiones:
        # Usar glob para buscar patrones
        archivos_imagen.extend(glob.glob(os.path.join(downloads_dir, ext)))
    
    # 3. Ordenar por fecha de creación en disco (lo más reciente descargado)
    # Usamos getctime en Windows para saber cuándo se creó el archivo en esta carpeta (descarga)
    archivos_imagen.sort(key=os.path.getctime, reverse=True)
    
    # 4. Seleccionar las ultimas 4
    imagenes_a_mover = archivos_imagen[:4]
    
    if not imagenes_a_mover:
        print("No se encontraron imágenes en la carpeta de Descargas.")
        return
        
    print(f"Se encontraron {len(imagenes_a_mover)} imágenes para mover.")

    # 5. Crear estructura de carpetas destino
    # Carpeta base donde está este script: .../frefirezona/prepararHimagen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir un nivel para llegar a: .../frefirezona
    project_root = os.path.dirname(script_dir)
    # Carpeta destino solicitada: .../frefirezona/imagenesOriginales
    carpeta_principal = os.path.join(project_root, "imagenesOriginales")
    
    # Crear nombre de subcarpeta secuencial (mapaN)
    prefijo = "mapa"
    max_num = 0
    
    # Asegurarnos de que el directorio padre existe para poder listarlo
    if os.path.exists(carpeta_principal):
        for nombre in os.listdir(carpeta_principal):
            ruta_completa = os.path.join(carpeta_principal, nombre)
            if os.path.isdir(ruta_completa) and nombre.startswith(prefijo):
                parte_num = nombre[len(prefijo):]
                if parte_num.isdigit():
                    num = int(parte_num)
                    if num > max_num:
                        max_num = num
    
    # El siguiente número
    siguiente_num = max_num + 1
    nombre_subcarpeta = f"{prefijo}{siguiente_num}"
    carpeta_destino = os.path.join(carpeta_principal, nombre_subcarpeta)
    
    # Crear carpetas (makedirs crea las intermedias si no existen)
    try:
        os.makedirs(carpeta_destino, exist_ok=True)
        print(f"Carpeta destino creada: {carpeta_destino}")
    except Exception as e:
        print(f"Error al crear carpetas: {e}")
        return

    # 6. Mover las imágenes
    
    # Ordenar las 4 seleccionadas de manera ascendente por NOMBRE
    # Como los nombres son 'Screenshot_YYYY...', el orden alfabético es cronológico
    imagenes_a_mover.sort(key=os.path.basename)

    for i, ruta_imagen in enumerate(imagenes_a_mover, 1):
        # Renombrar a 1.jpg, 2.jpg, 3.jpg, 4.jpg
        # Asumimos .jpg por consistencia con carpetas anteriores, o mantenemos extensión original
        # Dado que los archivos previos eran .jpg, forzamos la extensión .jpg para 'limpiar' dobles extensiones como .jpg.jpeg
        nombre_archivo = f"{i}.jpg" 
        destino_final = os.path.join(carpeta_destino, nombre_archivo)
        
        try:
            shutil.move(ruta_imagen, destino_final)
            print(f"Movido y renombrado: {ruta_imagen} -> {nombre_archivo}")
        except Exception as e:
            print(f"Error moviendo {ruta_imagen}: {e}")

    print("Proceso completado.")

if __name__ == "__main__":
    mover_ultimas_imagenes()
