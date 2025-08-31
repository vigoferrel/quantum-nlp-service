# Dockerfile para crear el entorno de SWE-bench
# Imagen base de Python sobre Debian "Bookworm" para parches de seguridad recientes.
FROM python:3.9-slim-bookworm

# Actualizar todos los paquetes del SO para mitigar vulnerabilidades conocidas.
RUN apt-get update && apt-get upgrade -y

# Instalar herramientas esenciales del sistema
RUN apt-get install -y git curl

# Instalar Miniconda para gestionar los entornos de Python
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH="/opt/conda/bin:$PATH"

# Aceptar los Términos de Servicio de Conda usando las URL completas
RUN /opt/conda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN /opt/conda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Configurar conda para modo no interactivo y actualizar
RUN conda config --set always_yes yes --set changeps1 no && \
    conda update -n base -c defaults conda && \
    conda config --append channels conda-forge

# Instalar pytest globalmente en el entorno base
RUN conda install -y pytest

# Crear un directorio de trabajo
WORKDIR /workspace

# El punto de entrada por defecto puede ser un shell
CMD ["/bin/bash"]
