# WiSpy-Deauth

# ⚠️ Wi-Fi Deauthentication Tool

> **Author**: CHINNAPAREDDY VENKATA KARTHIK REDDY  
> **For Educational and Ethical Research Purposes Only**

This tool automates Wi-Fi network scanning and sends **ARP spoofing packets** to deauthenticate all devices except the router and the attacker's device. It scans the local subnets, detects connected devices, and launches **continuous deauthentication attacks** using the Scapy library.

---

## 📌 Features

- 🔍 Automatically detects all local `/24` subnets
- 🛜 Scans for active hosts (devices) in each subnet
- 📡 Identifies the router IP in each subnet
- 🚫 Sends continuous ARP spoofing packets to disconnect devices from the router
- 🔄 Monitors the network every 5 seconds for new devices and attacks them
- 🧠 Skips self-IP and router to avoid self-disruption
- 🔐 Thread-safe device tracking with graceful shutdown via `Ctrl+C`

---

## ⚙️ Requirements

- Python 3.x
- `scapy`
- `psutil`

Install dependencies:

```bash
pip install scapy psutil
```

> ✅ Must be run with **root/admin privileges** to allow raw packet sending.

---

## 🚀 Usage

```bash
sudo python3 main.py
```

### Output Example

```
[+] Found subnets: ['192.168.1.0/24']
[+] Router detected: 192.168.1.1
[+] Launching initial attack on 192.168.1.10
[+] Starting deauth on 192.168.1.10
[~] Scanning for new devices in 192.168.1.0/24...
[+] New device detected: 192.168.1.15 - Launching deauth
```

---

## 📄 File Description

| File             | Description                                         |
|------------------|-----------------------------------------------------|
| `main.py` | Main script that performs scanning and attacks     |
| `README.md`      | Documentation (you're reading it)                  |

---

## ⚠️ Disclaimer

This tool is intended **ONLY for testing and ethical research in your own network** (e.g., cybersecurity labs, test setups).  
**Do NOT use** this tool on networks you do not own or have explicit permission to test.  
Unauthorized use is **illegal** and violates most jurisdictions' cybercrime laws.

---

## 🧠 How It Works

1. Finds all `/24` local subnets (ignores `127.0.0.1` and APIPA)
2. Scans devices in each subnet via ARP
3. Identifies the router IP (based on who replies)
4. Starts deauth attacks (ARP spoofing) against all devices
5. Monitors subnet continuously to attack new devices

---

## 📬 Contact

For queries or ethical collaboration:

- 📧 Email: [22bq1a4720@gmail.com](mailto:22bq1a4720@gmail.com)
- 🌐 GitHub: [@CEHCVKR](https://github.com/CEHCVKR)
- 💼 LinkedIn: [@cvkr](https://linkedin.com/in/cvkr)

---

## 🔐 License

This project is for **educational purposes only**. Use responsibly.
