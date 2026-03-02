# Shadow without showing - SwS

Este proyecto implementa una prueba de concepto para el flujo seguro de imágenes médicas, aplicando cifrado de extremo a extremo sin exponer la imagen original durante el almacenamiento o transmisión. Está diseñado específicamente para integrarse como mecanismo de seguridad en arquitecturas de **Federated Learning utilizando NVFLARE sobre Azure**.

## 🛡️ Arquitectura de Seguridad Propuesta

El proceso simula la subida de imágenes desde un entorno local (por ejemplo, un hospital) hacia la nube, garantizando confidencialidad mediante los siguientes servicios de Azure:

| Componente | Servicio Azure | Función |
|------------|----------------|---------|
| Gestión de Llaves | **Azure Key Vault** | Almacenamiento seguro de llaves maestras sin exponerlas al código. |
| Almacenamiento | **Azure Blob Storage** | Almacena los archivos binarios cifrados en reposo (.enc). |
| Procesamiento | **ML Compute Instance** | Nodo trabajador donde la imagen se descifra para extraer las características o entrenar el modelo local. |
| Validación | **Hash SHA-256** | Control de integridad estricto. |

## 🚀 Flujo Criptográfico Implementado

El flujo consta de tres fases críticas desarrolladas en el notebook principal (`cifrado_imagenes_azure_documentado.ipynb`):

### 1. Fase de origen (Hospital Local)
- Se obtiene la imagen en crudo.
- Se genera un hash **SHA-256** a partir de los bytes originales como firma digital.
- Se aplica cifrado simétrico mediante **Fernet (AES-128 en modo CBC)**.
- El archivo viaja totalmente encriptado hacia Azure (`nombre.enc`).

### 2. Fase de destino temporal en nube (Azure Compute)
- El clúster o Compute Instance lee la imagen cifrada.
- Solicita la llave de cifrado de forma segura directamente desde *Azure Key Vault*.
- Procede con el descifrado en memoria / bloque de disco local aislado.

### 3. Validación y Rechazo Criptográfico
- Se toma la imagen descifrada y se recalcula su huella hash SHA-256.
- Se **compara** con el hash digital en origen. 
- Si difieren, la imagen se rechaza automáticamente mitigando fallas de binarios o ataques *Man-in-the-Middle*.

## 🔑 Consideraciones hacia Producción
La arquitectura final para Federated Learning debe contemplar:

* **Zero Trust:** Uso estricto de **Private Endpoints (Azure Private Link)** para todos los servicios (Blob y KeyVault) aislando la carga de la red pública.
* **Autenticación sin secretos:** Empleo de **Managed Identities** para todos los flujos de lectura/escritura (ningún *connection string* viaja en el código).
* **Cumplimiento:** Cifrado doble activado por defecto tanto en Azure Blob Storage (Service-managed plus CMK) como el cifrado de la capa de aplicación (Fernet) propuesto aquí.

