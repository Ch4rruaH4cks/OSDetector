# Importamos las bibliotecas necesarias
import subprocess  # Para ejecutar comandos del sistema
import re  # Para trabajar con expresiones regulares
import os  # Para interactuar con el sistema operativo
import sys  # Para obtener argumentos pasados al script desde la línea de comandos

# Definimos una función para limpiar la pantalla, dependiendo del sistema operativo
limpiar_pantalla = lambda: (os.system("cls") if os.name == "nt" else os.system("clear"))

# Función para obtener el valor TTL de un dispositivo dado su dirección IP
def obtener_ttl(direccion_ip):
    try:
        # Definimos el parámetro para el comando de ping según el sistema operativo
        parametro = "-n" if os.name == "nt" else "-c"

        # Ejecutamos el comando de ping y obtenemos el resultado
        resultado = subprocess.check_output(['ping', parametro, '1', direccion_ip], universal_newlines=True)
        
        # Buscamos el valor TTL en el resultado utilizando una expresión regular
        ttl_match = re.search(r'ttl=(\d+)', resultado, re.IGNORECASE)
        if ttl_match:
            # Si encontramos un valor TTL válido, lo convertimos a entero y lo retornamos
            ttl = int(ttl_match.group(1))
            return ttl
    except subprocess.CalledProcessError as e:
        # En caso de error al ejecutar el comando de ping, mostramos el mensaje de error
        print(f"Error al ejecutar el comando ping: {e}")
    except ValueError:
        # Si hay un error al procesar el TTL, mostramos un mensaje de error
        print("Error al procesar el TTL.")
    
    return None


def determinar_so(ip, ttl):
    print("Identificadores de dispositivos\n")
    ttl = int(ttl)
    print(f"[!] {ip}")
    if(ttl <= 64):
        # Si el TTL es menor o igual a 64, sugerimos que el sistema operativo es Linux
        print(f"[*] TTL({ttl})")
        print("[*] OS: Linux")
    elif(ttl <= 128):
        # Si el TTL es mayor o igual a 128, sugerimos que el sistema operativo es Windows
        print(f"[*] TTL({ttl})")
        print("[*] OS: Windows")
    else:
        # En otro caso, sugerimos que el sistema operativo es Solaris/Aix
        print(f"[*] TTL({ttl})")
        print("[*] OS: Solaris/Aix")


if __name__ == "__main__":
    # Verificamos si se proporcionó una dirección IP como argumento al ejecutar el script
    if len(sys.argv) != 2:
        print("[?] Uso: python script.py <direccion_ip>")
        sys.exit(1)
    
    # Obtenemos la dirección IP desde los argumentos pasados al script
    direccion_ip = sys.argv[1]
    
    # Obtenemos el valor TTL del dispositivo con la dirección IP proporcionada
    ttl = obtener_ttl(direccion_ip)

    if ttl is not None:
        # Si se obtiene un valor válido de TTL, limpiamos la pantalla y determinamos el sistema operativo
        limpiar_pantalla()
        determinar_so(direccion_ip, ttl)
    else:
        # Si no se puede obtener el TTL, mostramos un mensaje de error
        print("No se pudo obtener el TTL.")
