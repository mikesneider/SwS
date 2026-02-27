import os
import hashlib
from cryptography.fernet import Fernet

# 1. Configuración de Seguridad
# En la prueba local generamos la llave manualmente. 
# En Azure, esta llave vendría del Key Vault.
LLAVE_LOCAL = Fernet.generate_key()
cifrador = Fernet(LLAVE_LOCAL)

def calcular_hash(ruta_archivo):
    """Calcula el hash SHA-256 para validar integridad."""
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def simular_flujo_seguro(nombre_imagen):
    ruta_origen = f"imagenes_originales/{nombre_imagen}"
    ruta_destino = f"servidor_simulado/{nombre_imagen}.enc"
    
    print(f"--- Iniciando prueba para: {nombre_imagen} ---")
    hash_original = calcular_hash(ruta_origen)
    
    # PASO A: Cifrado y "Subida"
    with open(ruta_origen, "rb") as f:
        datos_encriptados = cifrador.encrypt(f.read())
    
    with open(ruta_destino, "wb") as f:
        f.write(datos_encriptados)
    print(f"[OK] Imagen cifrada y guardada en el servidor simulado.")

    # PASO B: Descifrado (Lo que haría el Compute Instance en Azure)
    with open(ruta_destino, "rb") as f:
        datos_leidos = f.read()
        datos_desencriptados = cifrador.decrypt(datos_leidos)
    
    ruta_final = f"servidor_simulado/recuperada_{nombre_imagen}"
    with open(ruta_final, "wb") as f:
        f.write(datos_desencriptados)
    
    # PASO C: Validación de Integridad
    hash_final = calcular_hash(ruta_final)
    
    if hash_original == hash_final:
        print(f"✅ ÉXITO: Los hashes coinciden. La imagen es idéntica tras el proceso.")
    else:
        print(f"❌ ERROR: La integridad de la imagen se perdió.")

# Ejecutar la prueba
# Asegúrate de tener una imagen llamada 'test.jpg' en la carpeta 'imagenes_originales'
if __name__ == "__main__":
    if os.path.exists("imagenes_originales/test.jpg"):
        simular_flujo_seguro("test.jpg")
    else:
        print("Por favor, coloca una imagen llamada 'test.jpg' en 'imagenes_originales/'")