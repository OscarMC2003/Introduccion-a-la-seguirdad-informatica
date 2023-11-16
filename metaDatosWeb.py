import whois
import sys
import dns.resolver
import subprocess
import nmap

def get_domain_info(domain):
    print("Informacion sobre el dominio:")
    try:
        domain_info = whois.whois(domain)

        # Imprime la información del dominio
        print(f"Nombre de dominio: {domain}")
        print(f"Registrante: {domain_info.registrar}")
        print(f"Fecha de registro: {domain_info.creation_date}")
        print(f"Fecha de vencimiento: {domain_info.expiration_date}")
        print(f"Servidores de nombres (DNS): {domain_info.name_servers}")
        print(f"Correos encontrados: {domain_info.registrant_email}")

    except Exception as e:
        print("Error al obtener información del dominio:", e)


def get_mx_and_ns_servers(domain):
    print("servidores MX y NS")
    try:
        # Obtener los registros MX
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f"Servers MX para {domain}:")
        for mx in mx_records:
            print(f"{mx.exchange} (prioridad {mx.preference})")

        # Obtener los registros NS
        ns_records = dns.resolver.resolve(domain, 'NS')
        print(f"Servers NS para {domain}:")
        for ns in ns_records:
            print(ns.target)

    except Exception as e:
        print(f"Error al obtener información de servidores MX y NS para {domain}: {e}")


def scan_top_ports(target):
    print("Top 10 puertos de la pagina web")
    try:
        # Ejecuta nmap con la función top-ports para los 10 primeros puertos
        cmd = ["nmap", "-T4", "--top-ports", "10", target]
        result = subprocess.check_output(cmd, universal_newlines=True)

        # Imprime la salida
        print(result)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar nmap:", e)

def scan_open_ports(url):
    print("Escaneo de puertos abiertos (puede tardar un rato)")
    try:
        # Ejecuta nmap para escanear los puertos abiertos de la URL
        proceso = subprocess.Popen(['nmap', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida, error = proceso.communicate()

        if proceso.returncode == 0:
            print(f'Puertos abiertos en la página web {url}:\n{salida}')
        else:
            print(f'Error al escanear puertos: {error}')
    except Exception as e:
        print(f'Error al ejecutar nmap: {str(e)}')


def verificar_pagina_web(url):
    print("Verificacion de si el dominio esta vivo o muerto")
    try:
        # Ejecuta el comando ping a la URL
        proceso = subprocess.Popen(['ping', '-c', '4', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida, error = proceso.communicate()

        if proceso.returncode == 0:
            print(f'La página web {url} está viva.')
        else:
            print(f'La página web {url} está inactiva. Mensaje de error: {error}')
    except Exception as e:
        print(f'Error al realizar el ping a la página web {url}: {str(e)}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Introduzca los datos necesarios")
    else:
        domain = sys.argv[1]
        get_domain_info(domain)
        print("-------------------------------------------")
        get_mx_and_ns_servers(domain)
        print("-------------------------------------------")
        scan_top_ports(domain)
        print("-------------------------------------------")
        scan_open_ports(domain)
        print("-------------------------------------------")
        verificar_pagina_web(domain)
