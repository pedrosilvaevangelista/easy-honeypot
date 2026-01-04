# 🍯 Easy Honeypot

A simple and effective SSH honeypot to detect connection attempts and network scanning. Complete system with a web interface for real-time monitoring.

## 📋 Description

This honeypot simulates an SSH server on port 2222 and automatically logs all connection attempts, allowing you to identify potential attackers, bots, or network scanners. Ideal for detecting suspicious activity on your network.

## 🏗️ Architecture

The system is composed of 3 Docker containers that communicate with each other:

* **🐍 Backend (FastAPI)**: REST API to store and query connection attempts
* **⚛️ Frontend (React)**: Modern web interface for data visualization
* **🍯 Honeypot (Python)**: Fake SSH server that captures connection attempts

## ✨ Features

* ✅ Automatic capture of SSH connection attempts
* 📊 Real-time web dashboard
* 📈 Attack statistics (total attempts and unique IPs)
* 🔄 Automatic data refresh
* 📱 Responsive interface
* 🐳 Easy deployment with Docker

## 🚀 Installation and Usage

### Prerequisites

* Docker
* Docker Compose
* git

### Steps to run

1. **Clone the repository**:

```bash
git clone https://github.com/pedrosilvaevangelista/easy-honeypot.git
cd easy-honeypot
```

2. **Run the startup script**:

```bash
./start.sh
```

The script will:

* Automatically detect the machine IP
* Initialize the Docker containers
* Display the access URLs

### Accessing the system

After startup, you can access:

* **🌐 Web Interface**: `http://<machine-ip>:3000`
* **🔧 API**: `http://<machine-ip>:8000`
* **🍯 SSH Honeypot**: `<machine-ip>:2222`

## 🧪 Testing the Honeypot

To verify that the system is working, perform a test SSH connection:

### On Windows (CMD/PowerShell):

```cmd
ssh -p 2222 user@machine-ip
```

### On Linux/macOS:

```bash
ssh -p 2222 user@machine-ip
# or
telnet machine-ip 2222
# or using netcat
nc machine-ip 2222
```

### Simulation example:

```bash
# Test simulating a scanner
nmap -p 2222 <machine-ip>
```

After running any of these commands, you should see the attempt registered in the web interface.

## 📊 Web Interface

The dashboard provides:

* **📈 General statistics**: Total attempts and unique IPs
* **📋 Attempt list**: Detailed history with IP, connection data, and timestamp
* **🔄 Automatic refresh**: Data updated every 10 seconds
* **🎯 Real-time status**: System health indicator

## 🔧 Advanced Configuration

### Customizing the honeypot port

To change the default port (2222), edit the file `honeypot/honeypot_ssh.py`:

```python
PORT = 2222  # Change to the desired port
```

### Logging configuration

Logs are automatically saved and can be viewed with:

```bash
# View honeypot logs
docker-compose logs honeypot

# View backend logs
docker-compose logs backend

# View all logs
docker-compose logs -f
```

## 🛡️ Security

⚠️ **Important warnings**:

* This honeypot is for **detection and monitoring only**
* It does not provide active protection against attacks
* Run only in controlled environments
* Regularly monitor logs for suspicious activity
* Consider implementing rate limiting to avoid DoS

## 🐛 Troubleshooting

### Container does not start

```bash
# Check detailed logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
```

### Frontend does not load data

```bash
# Check if backend is accessible
curl http://localhost:8000/health

# Check network configuration
docker-compose ps
```

### Attempts do not appear on the dashboard

```bash
# Check honeypot logs
docker-compose logs honeypot

# Test honeypot connectivity
telnet localhost 2222
```

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**📧 Support**: For questions or issues, open an issue in the repository.

**⭐ Star**: If this project was useful to you, consider giving it a star.
