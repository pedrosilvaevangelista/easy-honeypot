import socket
import datetime
import requests
import threading
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HOST = '0.0.0.0'
PORT = 2222
API_URL = 'http://backend:8000/attempts/'

def wait_for_backend():
    """Aguardar o backend ficar disponível"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get('http://backend:8000/', timeout=5)
            if response.status_code == 200:
                logger.info("Backend is ready!")
                return True
        except requests.exceptions.RequestException as e:
            logger.info(f"Waiting for backend... ({retry_count + 1}/{max_retries})")
            time.sleep(2)
            retry_count += 1
    
    logger.error("Backend not available after maximum retries")
    return False

def log_and_send(ip, data):
    """Log e enviar dados para o backend"""
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp} - {ip} - {data}"
    logger.info(log_entry)

    payload = {
        "ip": ip,
        "data": data
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 201:
            logger.info(f"Successfully sent data to API for IP: {ip}")
        else:
            logger.warning(f"API returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending to API: {e}")

def handle_connection(conn, addr):
    """Lidar com uma conexão individual"""
    ip = addr[0]
    try:
        # Simular banner SSH
        ssh_banner = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
        conn.send(ssh_banner)
        
        # Aguardar dados do cliente
        conn.settimeout(30)
        data = conn.recv(4096).decode('utf-8', errors='ignore').strip()
        
        if data:
            log_and_send(ip, data)
        else:
            log_and_send(ip, "empty_connection")
            
    except socket.timeout:
        log_and_send(ip, "connection_timeout")
    except Exception as e:
        log_and_send(ip, f"connection_error: {str(e)}")
    finally:
        try:
            conn.close()
        except:
            pass

def run_honeypot():
    """Executar o honeypot SSH"""
    # Aguardar backend estar disponível
    if not wait_for_backend():
        logger.error("Cannot start honeypot - backend not available")
        return

    # Configurar socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(100)
        logger.info(f"Honeypot listening on {HOST}:{PORT}")

        while True:
            try:
                conn, addr = s.accept()
                logger.info(f"New connection from {addr[0]}:{addr[1]}")
                
                # Processar conexão em thread separada
                thread = threading.Thread(
                    target=handle_connection, 
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()
                
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")
                
    except Exception as e:
        logger.error(f"Error setting up honeypot: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_honeypot()
