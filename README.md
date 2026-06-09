# Honeypot Security System
A Flask-based honeypot project that simulates an admin portal, logs attacker activity, and displays results on a dashboard.  
This project was developed in a controlled lab environment for educational purposes.

---

## 📌 Project Overview
- Fake admin login page to attract attackers
- Logs attacker activities in JSON format
- Dashboard to visualize attack statistics
- Ethical testing only (no real systems targeted)

---

## 🛠 Tools & Technologies
- VirtualBox (Lab setup)
- Kali Linux (Attacker machine)
- Python (Core development)
- Flask (Web framework & dashboard)
- JSON (Log storage)
- VS Code (Coding environment)

---

## 📂 Project Structure
---

## 🔄 Methodology
1. Lab setup in VirtualBox  
2. Honeypot development in Python  
3. Dashboard creation with Flask  
4. Fake login page deployment  
5. Attack simulation using Kali Linux  
6. Analysis & reporting of logs  

---

## ▶️ How to Run

1. Clone this repository:
```bash
git clone https://github.com/asbah4311-wq/Honeypot_Security_Project.git

cd Honeypot_security_Project
```

2. Install required library:
```bash
pip install flask
```

3. Run the honeypot:
```bash
python honeypot.py
```

4. In a new terminal, run the login trap:
```bash
python login_trap.py
```

5. In another terminal, open the dashboard:
```bash
python dashboard1.py
```

6. Open your browser and go to:
- http://localhost:5000 → fake login page
- http://localhost:8080 → attack dashboard

---

## 📁 Project Files
- `honeypot.py` — core honeypot logic
- `login_trap.py` — fake admin login page
- `dashboard1.py` — Flask dashboard to view attack logs
- `honeypot_logs.json` — stores all captured attack logs

---

## 👁 What You'll See
- A fake admin login page on http://localhost:5000
- Every login attempt gets logged with IP, username, password, timestamp
- Dashboard on http://localhost:8080 shows all attack logs

---

## 📸 Screenshots
<img width="1920" height="1080" alt="Screenshot (249)" src="https://github.com/user-attachments/assets/7d805e4f-f2e3-4e6c-8eee-87fa92cb2b3c" />
<img width="1920" height="1080" alt="Screenshot (248)" src="https://github.com/user-attachments/assets/a1da23be-74af-4e34-9c00-b1142a4c04e6" />
<img width="1920" height="1080" alt="Screenshot (252)" src="https://github.com/user-attachments/assets/11f4e6b7-61ae-4196-a87d-5624fc2fbf7d" />

---

## ⚠️ Disclaimer
This project is for educational purposes only.  
Built in an isolated lab environment. Do not deploy on real networks.
