"""
Detector Automático de Círculos Blancos para Zonas de Free Fire
Versión Local - Reemplaza el script de Google Colab

Uso:
    python detectarCirculoBlanco.py                          # Procesa todos los mapas en imagenesRecortadas/
    python detectarCirculoBlanco.py --input mapa20           # Procesa solo mapa20
    python detectarCirculoBlanco.py --preview                # Muestra vista previa de cada detección
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import json
import argparse
from pathlib import Path


class CircleDetector:
    def __init__(self):
        # Radios FIJOS por zona (basados en datos históricos)
        self.fixed_radius = {
            1: 376,  # Zona inicial grande
            2: 206,  # Zona media
            3: 103,  # Zona pequeña
            4: 53    # Zona final
        }
        
        # Configuración de radios para DETECCIÓN del centro (rango de búsqueda)
        self.radius_config = {
            1: {'minRadius': 350, 'maxRadius': 400},
            2: {'minRadius': 180, 'maxRadius': 230},
            3: {'minRadius': 80, 'maxRadius': 120},
            4: {'minRadius': 40, 'maxRadius': 70}
        }
        
        # Directorio base
        self.base_dir = Path(__file__).parent
        self.input_dir = self.base_dir / "imagenesRecortadas"
        self.output_dir = self.base_dir / "datos" / "resultados"
        
        # Resultados
        self.results = {}
        self.failed_detections = []
    
    def detect_circle(self, img, radius_params, attempts=3):
        """
        Detecta círculo blanco en la imagen con múltiples intentos
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Diferentes configuraciones de detección
        configs = [
            {'blur': (9, 9), 'param1': 50, 'param2': 30},
            {'blur': (5, 5), 'param1': 40, 'param2': 25},
            {'blur': (11, 11), 'param1': 60, 'param2': 35},
            {'blur': (7, 7), 'param1': 45, 'param2': 20},
        ]
        
        best_circle = None
        
        for config in configs[:attempts]:
            blurred = cv2.GaussianBlur(gray, config['blur'], 2)
            
            circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=50,
                param1=config['param1'],
                param2=config['param2'],
                minRadius=radius_params['minRadius'],
                maxRadius=radius_params['maxRadius']
            )
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                # Tomar el círculo más brillante (probablemente el blanco)
                best_brightness = 0
                for circle in circles[0]:
                    x, y, r = circle
                    # Verificar que está dentro de la imagen
                    if x >= r and y >= r and x + r < img.shape[1] and y + r < img.shape[0]:
                        # Calcular brillo promedio en el borde del círculo
                        mask = np.zeros(gray.shape, dtype=np.uint8)
                        cv2.circle(mask, (x, y), r, 255, 2)
                        brightness = cv2.mean(gray, mask)[0]
                        
                        if brightness > best_brightness:
                            best_brightness = brightness
                            best_circle = (int(x), int(y), int(r))
                
                if best_circle:
                    return best_circle
        
        return None
    
    def process_map(self, map_folder, preview=False):
        """
        Procesa todas las imágenes de un mapa
        """
        map_name = map_folder.name
        map_results = {}
        
        print(f"\n📂 Procesando {map_name}...")
        
        for img_num in range(1, 5):
            img_path = map_folder / f"{img_num}.jpg"
            
            if not img_path.exists():
                print(f"  ⚠️ Imagen {img_num}.jpg no encontrada")
                continue
            
            img = cv2.imread(str(img_path))
            if img is None:
                print(f"  ❌ Error leyendo {img_num}.jpg")
                continue
            
            radius_params = self.radius_config[img_num]
            circle = self.detect_circle(img, radius_params)
            
            if circle:
                center_x, center_y, _ = circle  # Ignoramos el radio detectado
                fixed_r = self.fixed_radius[img_num]  # Usamos radio fijo
                map_results[f"imagen_{img_num}"] = {
                    "centro_x": center_x,
                    "centro_y": center_y,
                    "radio": fixed_r
                }
                print(f"  ✅ Zona {img_num}: Centro ({center_x}, {center_y}), Radio {fixed_r} (fijo)")
                
                if preview:
                    self.show_preview(img, (center_x, center_y, fixed_r), f"{map_name} - Zona {img_num}")
            else:
                self.failed_detections.append(f"{map_name}/imagen_{img_num}")
                print(f"  ❌ Zona {img_num}: No se detectó círculo")
        
        return map_results
    
    def show_preview(self, img, circle, title):
        """
        Muestra vista previa de la detección
        """
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(img_rgb)
        
        # Dibujar círculo detectado
        center_x, center_y, radius = circle
        circle_patch = patches.Circle(
            (center_x, center_y), radius,
            linewidth=3, edgecolor='red', facecolor='none'
        )
        ax.add_patch(circle_patch)
        ax.plot(center_x, center_y, 'g+', markersize=15, markeredgewidth=3)
        
        ax.set_title(f"{title}\nCentro: ({center_x}, {center_y}), Radio: {radius}")
        ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def process_all(self, specific_map=None, preview=False):
        """
        Procesa todos los mapas o uno específico
        """
        if specific_map:
            map_folders = [self.input_dir / specific_map]
            if not map_folders[0].exists():
                print(f"❌ Carpeta '{specific_map}' no encontrada en {self.input_dir}")
                return False
        else:
            map_folders = sorted([
                f for f in self.input_dir.iterdir() 
                if f.is_dir() and f.name.startswith("mapa")
            ])
        
        if not map_folders:
            print(f"❌ No se encontraron carpetas de mapas en {self.input_dir}")
            return False
        
        print(f"🎯 Detectando círculos blancos en {len(map_folders)} mapa(s)")
        print("=" * 50)
        
        for map_folder in map_folders:
            map_results = self.process_map(map_folder, preview)
            if map_results:
                self.results[map_folder.name] = map_results
        
        return True
    
    def save_results(self, output_file=None):
        """
        Guarda resultados en JSON
        """
        if not self.results:
            print("⚠️ No hay resultados para guardar")
            return None
        
        # Crear directorio de salida si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_file is None:
            output_file = self.output_dir / "circulos_detectados.json"
        else:
            output_file = Path(output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        return output_file
    
    def print_summary(self):
        """
        Imprime resumen de la detección
        """
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE DETECCIÓN")
        print("=" * 50)
        
        total_images = sum(len(m) for m in self.results.values())
        total_maps = len(self.results)
        
        print(f"✅ Mapas procesados: {total_maps}")
        print(f"✅ Círculos detectados: {total_images}")
        
        if self.failed_detections:
            print(f"\n⚠️ Detecciones fallidas ({len(self.failed_detections)}):")
            for failed in self.failed_detections:
                print(f"   - {failed}")
        
        # Mostrar formato Python para copiar
        if self.results:
            print("\n📋 Formato Python (para copiar):")
            print("circulos = {")
            for map_name, zones in self.results.items():
                print(f"    '{map_name}': {{")
                for zone_name, data in zones.items():
                    print(f"        '{zone_name}': {{'centro_x': {data['centro_x']}, 'centro_y': {data['centro_y']}, 'radio': {data['radio']}}},")
                print("    },")
            print("}")


def main():
    parser = argparse.ArgumentParser(
        description="Detector automático de círculos blancos para zonas de Free Fire"
    )
    parser.add_argument(
        '--input', '-i',
        help="Nombre de carpeta específica (ej: mapa20). Si no se especifica, procesa todos."
    )
    parser.add_argument(
        '--preview', '-p',
        action='store_true',
        help="Mostrar vista previa de cada detección"
    )
    parser.add_argument(
        '--output', '-o',
        help="Archivo de salida JSON (por defecto: datos/resultados/circulos_detectados.json)"
    )
    
    args = parser.parse_args()
    
    print("🎨 Detector de Círculos Blancos - Free Fire Zona")
    print("=" * 50)
    
    detector = CircleDetector()
    
    if detector.process_all(specific_map=args.input, preview=args.preview):
        detector.save_results(args.output)
        detector.print_summary()
    else:
        print("❌ Error en el procesamiento")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())