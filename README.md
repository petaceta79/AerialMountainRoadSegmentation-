# 🚁 AerialMountainRoadSegmentation  

Algoritmo de visión por computadora que diferencia carreteras de zonas montañosas en imágenes aéreas. Incluye el proceso paso a paso con ejemplos visuales.  

---

## 🎯 Objetivo  
Extraer automáticamente el camino de una imagen aérea de carreteras en entornos montañosos.  

---

## 🔍 Proceso  

### 📌 Primera prueba: Detección de bordes  
- Implementé una modificación del algoritmo **Sobel** ([archivo](ruta/sobel_modificado.py)) optimizado con:  
  - **Vectorización** para acelerar cálculos.  
  - **Integral de imagen** para reducir operaciones redundantes.  
- **Problema detectado**:  
  - Excesivo ruido por las copas de los árboles (bordes irrelevantes).  
  - Costo computacional alto para filtrar falsos positivos.  

### 📊 Análisis: Canal RGB  
- Experimenté con la separación de canales de color:  
  ![RGB Channels](imagenes/rgb_channels.png)  
  - **Hallazgo clave**: El canal **azul** destaca mejor las carreteras (las copas de los árboles casi no contienen azul).  

### ⚙️ Solución implementada  
1. **Umbralizado del canal azul**:  
   - Filtro para conservar solo píxeles con valores altos en azul.  
2. **Postprocesamiento**:  
   - Algoritmo recursivo para eliminar **puntos pequeños aislados** (ruido residual).  

---

## 📌 Resultados  
### 🖼️ Ejemplo visual  
| Original | Resultado Final |  
|----------|-----------------|  
| ![Original](ejemplos/foto1.jpg) | ![Resultado](ejemplos/foto1_edit.jpg) |  

