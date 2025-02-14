#!/usr/bin/env python3
import requests
import socket
import subprocess
import sys
import warnings
from colorama import Fore, Style, init

# Suprimir warnings de urllib3
warnings.filterwarnings("ignore", category=Warning)

# Inicializar colorama
init(autoreset=True)

def check_url(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def check_curl_status(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        result = subprocess.run(['curl', '-I', '-s', '-L', '-k', url], 
                              capture_output=True, text=True, timeout=5)
        
        status_codes = []
        for line in result.stdout.splitlines():
            if line.startswith('HTTP/'):
                status_codes.append(line.split()[1])
        
        if status_codes:
            return ' -> '.join(status_codes)
        return "No HTTP status"
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return f"Error: {str(e)}"

def get_application_gateway(url):
    host = url.split("//")[-1].split("/")[0] if "//" in url else url.split("/")[0]
    try:
        # Ejecutar nslookup para obtener el nombre del Application Gateway
        result = subprocess.run(['nslookup', host], capture_output=True, text=True)
        ip_address = socket.gethostbyname(host)  # Obtener la dirección IP

        # Buscar el nombre canónico (CNAME) en la respuesta de nslookup
        agw_name = None
        for line in result.stdout.splitlines():
            if "canonical name =" in line.lower():
                agw_name = line.split("=")[-1].strip()
                break
            elif "name =" in line.lower() and not agw_name:
                agw_name = line.split("=")[-1].strip()

        # Si no se encuentra un nombre específico, mostrar "No AGW"
        return agw_name or "No AGW", ip_address
    except Exception as e:
        return "Error en resolución DNS", "IP no disponible"

def main():
    # Verificar si se proporcionaron URLs como argumentos
    if len(sys.argv) < 2:
        print("Uso: urlcheck <url1> [url2] [url3] ...")
        sys.exit(1)
    
    urls = sys.argv[1:]  # Tomar todas las URLs proporcionadas como argumentos
    max_url_length = max(len(url) for url in urls)

    for url in urls:
        is_working = check_url(url)
        if is_working:
            gateway, ip_address = get_application_gateway(url)
            curl_status = check_curl_status(url)
            output = f"{url:<{max_url_length}} | HTTP Status: {Fore.GREEN}{curl_status}{Style.RESET_ALL} | Application Gateway: {Fore.YELLOW}{gateway}{Style.RESET_ALL} (IP: {ip_address})"
            print(output)
        else:
            output = f"{Fore.RED}{url:<{max_url_length}} | no está funcionando.{Style.RESET_ALL}"
            print(output)
        print("-----")

if __name__ == "__main__":
    main() 