import os
from cryptography.fernet import Fernet

# SIMULACIÓN: Generamos una llave local (en lugar de pedirla al Key Vault aún)
key = Fernet.generate_key()
fernet = Fernet(key)

def prueba_local_cifrado(ruta_imagen):
    # 1. Leer imagen original
    with open(ruta_imagen, "rb") as f:
        data_original = f.read()
    
    # 2. Cifrar
    data_cifrada = fernet.encrypt(data_original)
    
    # 3. Guardar como si fuera el servidor (Simulamos la subida)
    ruta_servidor_simulado = "servidor_local/imagen_cifrada.enc"
    os.makedirs("servidor_local", exist_ok=True)
    
    with open(ruta_servidor_simulado, "wb") as f:
        f.write(data_cifrada)
    
    print(f"ÉXITO: Imagen enviada al 'servidor' local.")
    return ruta_servidor_simulado

# Ejecutar prueba
archivo_en_nube = prueba_local_cifrado("imagenpueba.JPG")