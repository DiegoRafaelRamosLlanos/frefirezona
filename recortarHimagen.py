import os
from PIL import Image
from pathlib import Path

def procesar_imagenes_en_carpetas(directorio_origen, directorio_destino):
    """
    Recorre las carpetas de forma ascendente y procesa las imágenes
    guardándolas en una estructura idéntica en el directorio de destino
    """
    try:
        # Crear carpeta principal de destino si no existe
        Path(directorio_destino).mkdir(exist_ok=True)
        
        # Obtener lista de carpetas ordenada
        carpetas = sorted([d for d in os.listdir(directorio_origen) 
                         if os.path.isdir(os.path.join(directorio_origen, d))])
        
        for carpeta in carpetas:
            ruta_carpeta_origen = os.path.join(directorio_origen, carpeta)
            ruta_carpeta_destino = os.path.join(directorio_destino, carpeta)
            
            # Saltar si la carpeta ya existe
            if os.path.exists(ruta_carpeta_destino):
                print(f"⏭️  Saltando carpeta existente: {carpeta}")
                continue
            
            # Crear carpeta nueva
            Path(ruta_carpeta_destino).mkdir(exist_ok=True)
            print(f"✅ Creada carpeta: {carpeta}")
            
            print(f"\nProcesando carpeta: {carpeta}")
            
            # Obtener lista de imágenes ordenada
            imagenes = sorted([f for f in os.listdir(ruta_carpeta_origen) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            
            for imagen in imagenes:
                ruta_imagen_origen = os.path.join(ruta_carpeta_origen, imagen)
                print(f"Procesando imagen: {imagen}")
                
                try:
                    # Abrir y procesar imagen
                    img = Image.open(ruta_imagen_origen)
                    
                    # Usar las coordenadas de recorte (1309, -5, 2533, 1220)
                    crop_area = (1309, -5, 2533, 1220)
                    mapa = img.crop(crop_area)
                    
                    # Guardar imagen recortada en la carpeta correspondiente
                    ruta_imagen_destino = os.path.join(ruta_carpeta_destino, imagen)
                    mapa.save(ruta_imagen_destino)
                    print(f"✅ Guardada como: {ruta_imagen_destino}")
                    
                except Exception as e:
                    print(f"❌ Error procesando {imagen}: {str(e)}")
                    
    except Exception as e:
        print(f"❌ Error general: {str(e)}")

if __name__ == "__main__":
    # Directorio donde están las carpetas originales con las imágenes
    directorio_origen = "imagenesOriginales"
    
    # Directorio donde se guardarán las imágenes recortadas
    directorio_destino = "imagenesRecortadas"
    
    procesar_imagenes_en_carpetas(directorio_origen, directorio_destino)