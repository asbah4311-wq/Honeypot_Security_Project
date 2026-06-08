from flask import Flask, request, render_template_string, redirect, session
import json
import os
import datetime

app = Flask(__name__)
app.secret_key = 'honeypot_secret_key_2024'
LOG_FILE = '/home/asbah/honeypot_logs.json'

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Control Panel — Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #1a1a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        .login-box {
            background: #16213e;
            padding: 40px;
            border-radius: 10px;
            border: 1px solid #0f3460;
            width: 380px;
            box-shadow: 0 0 30px rgba(0,0,0,0.7);
        }
        .login-box h2 {
            color: #e94560;
            text-align: center;
            margin-bottom: 10px;
            font-size: 22px;
        }
        .subtitle {
            color: #555;
            text-align: center;
            font-size: 12px;
            margin-bottom: 25px;
        }
        .warning {
            color: #ff6b6b;
            font-size: 11px;
            text-align: center;
            margin-bottom: 20px;
            padding: 8px;
            border: 1px solid #ff6b6b;
            border-radius: 4px;
        }
        .error {
            color: #ff4444;
            font-size: 13px;
            text-align: center;
            margin-bottom: 15px;
            padding: 10px;
            background: rgba(255,0,0,0.1);
            border-radius: 4px;
            border-left: 3px solid #ff4444;
        }
        .form-group { margin-bottom: 15px; }
        .form-group label {
            display: block;
            color: #888;
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        input {
            width: 100%;
            padding: 12px;
            background: #0f3460;
            border: 1px solid #1a4a8a;
            border-radius: 5px;
            color: white;
            font-size: 14px;
            outline: none;
            transition: border 0.3s;
        }
        input:focus { border-color: #e94560; }
        input::placeholder { color: #444; }
        button {
            width: 100%;
            padding: 13px;
            background: linear-gradient(135deg, #e94560, #c73652);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 15px;
            cursor: pointer;
            margin-top: 10px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        button:hover { background: linear-gradient(135deg, #c73652, #a82a42); }
        .footer {
            color: #333;
            font-size: 10px;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔒 Admin Control Panel</h2>
        <div class="subtitle">System Administration Portal v3.2</div>
        <div class="warning">⚠️ Authorized Personnel Only</div>
        {% if show_error %}
        <div class="error">❌ Invalid username or password. Please try again.</div>
        {% endif %}
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter admin username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit">🔓 LOGIN</button>
        </form>
        <div class="footer">
            SecureSystem Corp © 2024 | Security Operations Center
        </div>
    </div>
</body>
</html>
'''

FAKE_ADMIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel — Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #f0f2f5; font-family: Arial, sans-serif; }
        .topbar {
            background: #2c3e50;
            color: white;
            padding: 14px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .topbar h1 { font-size: 17px; }
        .topbar-right { display: flex; align-items: center; gap: 15px; }
        .user-badge {
            background: #e74c3c;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
        }
        .logout-btn {
            background: transparent;
            border: 1px solid #e74c3c;
            color: #e74c3c;
            padding: 6px 14px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            text-decoration: none;
        }
        .logout-btn:hover { background: #e74c3c; color: white; }
        .alert-bar {
            background: #27ae60;
            color: white;
            padding: 10px 25px;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
        }
        .layout { display: flex; min-height: calc(100vh - 88px); }
        .sidebar {
            width: 230px;
            background: #2c3e50;
            padding: 15px 0;
            flex-shrink: 0;
        }
        .sidebar-section {
            padding: 12px 20px 5px;
            font-size: 10px;
            letter-spacing: 2px;
            color: #7f8c8d;
            text-transform: uppercase;
        }
        .sidebar a {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 11px 20px;
            color: #bdc3c7;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.2s;
        }
        .sidebar a:hover { background: #34495e; color: white; }
        .sidebar a.active { background: #e74c3c; color: white; }
        .main { flex: 1; padding: 25px; overflow-y: auto; }
        .page-title {
            font-size: 20px;
            color: #2c3e50;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #e74c3c;
        }
        .stat-number { font-size: 30px; font-weight: bold; color: #2c3e50; }
        .stat-label { font-size: 12px; color: #7f8c8d; margin-top: 4px; }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 12px;
            border-bottom: 1px solid #ecf0f1;
        }
        .card-title { font-size: 14px; font-weight: bold; color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; }
        th {
            text-align: left;
            font-size: 11px;
            color: #7f8c8d;
            padding: 8px 10px;
            border-bottom: 2px solid #ecf0f1;
            text-transform: uppercase;
        }
        td {
            padding: 12px 10px;
            font-size: 13px;
            color: #2c3e50;
            border-bottom: 1px solid #f5f6fa;
        }
        tr:hover td { background: #f8f9fa; }
        .btn {
            display: inline-block;
            padding: 5px 11px;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
            text-decoration: none;
            margin: 2px;
            border: none;
            font-weight: bold;
        }
        .btn-red { background: #e74c3c; color: white; }
        .btn-blue { background: #3498db; color: white; }
        .btn-green { background: #27ae60; color: white; }
        .btn-orange { background: #f39c12; color: white; }
        .btn-gray { background: #95a5a6; color: white; }
        .btn:hover { opacity: 0.85; }
        .badge { padding: 3px 9px; border-radius: 12px; font-size: 11px; font-weight: bold; }
        .badge-active { background: #d5f5e3; color: #27ae60; }
        .badge-inactive { background: #fadbd8; color: #e74c3c; }
        .badge-pending { background: #fef9e7; color: #f39c12; }
        .form-inline input, .form-inline select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            margin: 3px;
            background: white;
            color: #2c3e50;
        }
        .success-msg {
            background: #d5f5e3;
            border: 1px solid #27ae60;
            color: #27ae60;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-size: 13px;
        }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>
<div class="topbar">
    <h1>⚙️ Admin Control Panel</h1>
    <div class="topbar-right">
        <span class="user-badge">👤 {{ username }}</span>
        <span style="color:#bdc3c7; font-size:12px;">{{ current_time }}</span>
        <a href="/logout" class="logout-btn">🚪 Logout</a>
    </div>
</div>
<div class="alert-bar">
    <span>✅ Welcome back, <strong>{{ username }}</strong>!</span>
    <span>⚠️ 3 pending alerts</span>
</div>
<div class="layout">
    <div class="sidebar">
        <div class="sidebar-section">Navigation</div>
        <a href="/fake/dashboard" class="{% if current_page == 'dashboard' %}active{% endif %}">📊 Dashboard</a>
        <a href="/fake/users" class="{% if current_page == 'users' %}active{% endif %}">👥 User Management</a>
        <a href="/fake/database" class="{% if current_page == 'database' %}active{% endif %}">🗄️ Database</a>
        <a href="/fake/files" class="{% if current_page == 'files' %}active{% endif %}">📁 File Manager</a>
        <div class="sidebar-section">System</div>
        <a href="/fake/settings" class="{% if current_page == 'settings' %}active{% endif %}">⚙️ Settings</a>
        <a href="/fake/logs" class="{% if current_page == 'logs' %}active{% endif %}">📋 System Logs</a>
        <a href="/fake/network" class="{% if current_page == 'network' %}active{% endif %}">🌐 Network</a>
        <a href="/fake/backup" class="{% if current_page == 'backup' %}active{% endif %}">💾 Backup</a>
    </div>
    <div class="main">

        {% if current_page == "dashboard" %}
        <div class="page-title">📊 Dashboard Overview</div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">1,284</div><div class="stat-label">Total Users</div></div>
            <div class="stat-card"><div class="stat-number">47</div><div class="stat-label">Active Sessions</div></div>
            <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">Pending Alerts</div></div>
            <div class="stat-card"><div class="stat-number">99.8%</div><div class="stat-label">Server Uptime</div></div>
        </div>
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><div class="card-title">⚡ Recent Activity</div></div>
                <table>
                    <tr><th>Time</th><th>User</th><th>Action</th></tr>
                    <tr><td>09:42</td><td>admin</td><td>Updated permissions</td></tr>
                    <tr><td>09:31</td><td>sysadmin</td><td>DB backup created</td></tr>
                    <tr><td>09:15</td><td>admin</td><td>New user created</td></tr>
                </table>
            </div>
            <div class="card">
                <div class="card-header"><div class="card-title">🚨 Alerts</div></div>
                <table>
                    <tr><th>Level</th><th>Message</th><th>Action</th></tr>
                    <tr>
                        <td style="color:#e74c3c">🔴 High</td>
                        <td>Unauthorized attempt</td>
                        <td><a href="/fake/action/dismiss_alert" class="btn btn-gray">Dismiss</a></td>
                    </tr>
                    <tr>
                        <td style="color:#f39c12">🟡 Medium</td>
                        <td>Backup overdue</td>
                        <td><a href="/fake/action/start_backup" class="btn btn-orange">Backup</a></td>
                    </tr>
                </table>
            </div>
        </div>

        {% elif current_page == "users" %}
        <div class="page-title">👥 User Management</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Add New User</div></div>
            <form method="POST" action="/fake/users/add" class="form-inline">
                <input type="text" name="new_username" placeholder="Username" required>
                <input type="password" name="new_password" placeholder="Password" required>
                <input type="email" name="new_email" placeholder="Email">
                <select name="new_role">
                    <option>Administrator</option>
                    <option>Editor</option>
                    <option>Viewer</option>
                    <option>Super Admin</option>
                </select>
                <button type="submit" class="btn btn-green">➕ Add User</button>
            </form>
        </div>
        <div class="card">
            <div class="card-header">
                <div class="card-title">All Users</div>
                <a href="/fake/action/export_users" class="btn btn-blue">📤 Export</a>
            </div>
            <table>
                <tr><th>Username</th><th>Role</th><th>Email</th><th>Last Login</th><th>Status</th><th>Actions</th></tr>
                {% for user in fake_users %}
                <tr>
                    <td>{{ user.username }}</td><td>{{ user.role }}</td>
                    <td>{{ user.email }}</td><td>{{ user.last_login }}</td>
                    <td><span class="badge badge-{{ user.status_class }}">{{ user.status }}</span></td>
                    <td>
                        <a href="/fake/users/edit/{{ user.username }}" class="btn btn-blue">Edit</a>
                        <a href="/fake/users/delete/{{ user.username }}" class="btn btn-red">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

        {% elif current_page == "database" %}
        <div class="page-title">🗄️ Database Management</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Execute SQL Query</div></div>
            <form method="POST" action="/fake/database/query" class="form-inline">
                <select name="db_name">
                    <option>main_db</option>
                    <option>users_db</option>
                    <option>logs_db</option>
                </select>
                <input type="text" name="sql_query" placeholder="SELECT * FROM users LIMIT 10" style="width:400px">
                <button type="submit" class="btn btn-blue">▶ Execute</button>
            </form>
        </div>
        <div class="card">
            <div class="card-header"><div class="card-title">Databases</div></div>
            <table>
                <tr><th>Name</th><th>Host</th><th>Size</th><th>Status</th><th>Actions</th></tr>
                <tr>
                    <td>main_db</td><td>192.168.1.10:3306</td><td>840 MB</td>
                    <td><span class="badge badge-active">Connected</span></td>
                    <td>
                        <a href="/fake/action/browse_main_db" class="btn btn-blue">Browse</a>
                        <a href="/fake/action/export_main_db" class="btn btn-green">Export</a>
                        <a href="/fake/action/drop_main_db" class="btn btn-red">Drop</a>
                    </td>
                </tr>
                <tr>
                    <td>users_db</td><td>192.168.1.10:3306</td><td>124 MB</td>
                    <td><span class="badge badge-active">Connected</span></td>
                    <td>
                        <a href="/fake/action/browse_users_db" class="btn btn-blue">Browse</a>
                        <a href="/fake/action/export_users_db" class="btn btn-green">Export</a>
                    </td>
                </tr>
            </table>
        </div>

        {% elif current_page == "files" %}
        <div class="page-title">📁 File Manager</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Upload File</div></div>
            <form method="POST" action="/fake/files/upload" class="form-inline">
                <input type="text" name="upload_path" placeholder="/var/www/html/" value="/var/www/html/">
                <input type="file" name="upload_file">
                <button type="submit" class="btn btn-green">📤 Upload</button>
            </form>
        </div>
        <div class="card">
            <div class="card-header"><div class="card-title">📂 /var/www/html/admin/</div></div>
            <table>
                <tr><th>Name</th><th>Size</th><th>Modified</th><th>Actions</th></tr>
                <tr>
                    <td>🔑 credentials.txt</td><td>2.4 KB</td><td>Today</td>
                    <td>
                        <a href="/fake/action/view_credentials" class="btn btn-blue">View</a>
                        <a href="/fake/action/download_credentials" class="btn btn-green">Download</a>
                        <a href="/fake/action/delete_credentials" class="btn btn-red">Delete</a>
                    </td>
                </tr>
                <tr>
                    <td>📦 database_backup.zip</td><td>840 MB</td><td>Yesterday</td>
                    <td>
                        <a href="/fake/action/download_backup_zip" class="btn btn-green">Download</a>
                        <a href="/fake/action/delete_backup_zip" class="btn btn-red">Delete</a>
                    </td>
                </tr>
                <tr>
                    <td>🔐 private_keys.pem</td><td>4 KB</td><td>3 days ago</td>
                    <td><a href="/fake/action/download_private_keys" class="btn btn-red">Download</a></td>
                </tr>
            </table>
        </div>

        {% elif current_page == "settings" %}
        <div class="page-title">⚙️ System Settings</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Change Admin Password</div></div>
            <form method="POST" action="/fake/settings/password" class="form-inline">
                <input type="password" name="current_password" placeholder="Current Password">
                <input type="password" name="new_password" placeholder="New Password">
                <input type="password" name="confirm_password" placeholder="Confirm Password">
                <button type="submit" class="btn btn-red">🔑 Change Password</button>
            </form>
        </div>
        <div class="card">
            <div class="card-header"><div class="card-title">Server Configuration</div></div>
            <form method="POST" action="/fake/settings/server" class="form-inline">
                <input type="text" name="server_ip" placeholder="Server IP" value="192.168.1.10">
                <input type="number" name="server_port" placeholder="Port" value="8080">
                <select name="environment">
                    <option>Production</option>
                    <option>Staging</option>
                    <option>Development</option>
                </select>
                <button type="submit" class="btn btn-blue">💾 Save Settings</button>
            </form>
        </div>

        {% elif current_page == "logs" %}
        <div class="page-title">📋 System Logs</div>
        <div class="card">
            <div class="card-header">
                <div class="card-title">Access Logs</div>
                <a href="/fake/action/export_logs" class="btn btn-blue">📤 Export</a>
            </div>
            <table>
                <tr><th>Time</th><th>IP</th><th>User</th><th>Action</th><th>Status</th></tr>
                <tr><td>09:42</td><td>192.168.1.5</td><td>admin</td><td>User update</td><td style="color:#27ae60">Success</td></tr>
                <tr><td>09:31</td><td>192.168.1.5</td><td>sysadmin</td><td>DB backup</td><td style="color:#27ae60">Success</td></tr>
                <tr><td>08:55</td><td>192.168.1.12</td><td>unknown</td><td>Login failed</td><td style="color:#e74c3c">Failed</td></tr>
            </table>
        </div>

        {% elif current_page == "network" %}
        <div class="page-title">🌐 Network Configuration</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Network Interfaces</div></div>
            <table>
                <tr><th>Interface</th><th>IP</th><th>Status</th><th>Actions</th></tr>
                <tr>
                    <td>eth0</td><td>192.168.1.10</td>
                    <td><span class="badge badge-active">Up</span></td>
                    <td><a href="/fake/action/configure_eth0" class="btn btn-blue">Configure</a></td>
                </tr>
            </table>
        </div>
        <div class="card">
            <div class="card-header">
                <div class="card-title">Firewall Rules</div>
            </div>
            <form method="POST" action="/fake/network/firewall" class="form-inline" style="margin-bottom:15px">
                <input type="text" name="rule_ip" placeholder="IP Address">
                <select name="rule_action"><option>ALLOW</option><option>DENY</option><option>DROP</option></select>
                <select name="rule_port"><option>80</option><option>443</option><option>22</option><option>ALL</option></select>
                <button type="submit" class="btn btn-orange">Apply Rule</button>
            </form>
        </div>

        {% elif current_page == "backup" %}
        <div class="page-title">💾 Backup Management</div>
        {% if action_msg %}<div class="success-msg">✅ {{ action_msg }}</div>{% endif %}
        <div class="card">
            <div class="card-header"><div class="card-title">Create Backup</div></div>
            <form method="POST" action="/fake/backup/create" class="form-inline">
                <select name="backup_type">
                    <option>Full System Backup</option>
                    <option>Database Only</option>
                    <option>Files Only</option>
                </select>
                <input type="text" name="backup_name" placeholder="Backup name">
                <button type="submit" class="btn btn-green">💾 Start Backup</button>
            </form>
        </div>
        <div class="card">
            <div class="card-header"><div class="card-title">Existing Backups</div></div>
            <table>
                <tr><th>Name</th><th>Type</th><th>Size</th><th>Date</th><th>Actions</th></tr>
                <tr>
                    <td>backup_20240601</td><td>Full</td><td>2.4 GB</td><td>Today</td>
                    <td>
                        <a href="/fake/action/download_backup_today" class="btn btn-green">Download</a>
                        <a href="/fake/action/restore_backup_today" class="btn btn-orange">Restore</a>
                        <a href="/fake/action/delete_backup_today" class="btn btn-red">Delete</a>
                    </td>
                </tr>
            </table>
        </div>
        {% endif %}

    </div>
</div>
</body>
</html>
'''

FAKE_USERS = [
    {"username": "admin", "role": "Super Admin", "email": "admin@system.local", "last_login": "Today 09:42", "status": "Active", "status_class": "active"},
    {"username": "sysadmin", "role": "Administrator", "email": "sys@system.local", "last_login": "Today 09:31", "status": "Active", "status_class": "active"},
    {"username": "dbadmin", "role": "DB Admin", "email": "db@system.local", "last_login": "Yesterday", "status": "Inactive", "status_class": "inactive"},
    {"username": "editor01", "role": "Editor", "email": "editor@system.local", "last_login": "2 days ago", "status": "Active", "status_class": "active"},
]

def log_event(ip, service, data):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    entry = {
        "timestamp": str(datetime.datetime.now()),
        "attacker_ip": ip,
        "port_attacked": 8080,
        "service": service,
        "data_sent": data
    }
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
    print(f"[{service}] IP: {ip} | {data}")

def render_fake_admin(page, action_msg=None):
    username = session.get('username', 'admin')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template_string(
        FAKE_ADMIN,
        current_page=page,
        username=username,
        current_time=current_time,
        action_msg=action_msg,
        fake_users=FAKE_USERS
    )

def check_logged_in():
    return session.get('logged_in', False)

# ─────────────────────────────────────────────
# LOGIN ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def index():
    # Always redirect to login — never skip
    return redirect('/login-page')

@app.route('/login-page')
def login_page():
    # If not logged in show login form
    if check_logged_in():
        return redirect('/fake/dashboard')
    show_error = session.pop('show_error', False)
    return render_template_string(LOGIN_PAGE, show_error=show_error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr

    if 'attempts' not in session:
        session['attempts'] = 0

    session['attempts'] += 1
    attempt = session['attempts']

    log_event(ip, "HTTP-LOGIN", f"attempt={attempt} username={username} password={password}")

    # After 5 attempts show fake admin panel
    if attempt >= 5:
        session['logged_in'] = True
        session['username'] = username
        session['attempts'] = 0
        log_event(ip, "FAKE-ADMIN-ACCESS", f"Entered fake admin as username={username}")
        return redirect('/fake/dashboard')

    session['show_error'] = True
    return redirect('/login-page')

# ─────────────────────────────────────────────
# LOGOUT ROUTE — Fixed
# ─────────────────────────────────────────────
@app.route('/logout')
def logout():
    ip = request.remote_addr
    username = session.get('username', 'unknown')
    log_event(ip, "FAKE-ADMIN-LOGOUT", f"logged_out username={username}")
    # Clear everything completely
    session.clear()
    return redirect('/login-page')

# ─────────────────────────────────────────────
# FAKE ADMIN ROUTES — All protected
# ─────────────────────────────────────────────
@app.route('/fake/dashboard')
def fake_dashboard():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_dashboard")
    return render_fake_admin("dashboard")

@app.route('/fake/users')
def fake_users_page():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_users")
    return render_fake_admin("users")

@app.route('/fake/users/add', methods=['POST'])
def fake_add_user():
    if not check_logged_in():
        return redirect('/login-page')
    ip = request.remote_addr
    username = request.form.get('new_username', '')
    password = request.form.get('new_password', '')
    email = request.form.get('new_email', '')
    role = request.form.get('new_role', '')
    log_event(ip, "FAKE-ADMIN-ACTION", f"added_user username={username} password={password} email={email} role={role}")
    return render_fake_admin("users", action_msg=f"User '{username}' added successfully!")

@app.route('/fake/users/edit/<uname>')
def fake_edit_user(uname):
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"edited_user username={uname}")
    return render_fake_admin("users", action_msg=f"User '{uname}' updated!")

@app.route('/fake/users/delete/<uname>')
def fake_delete_user(uname):
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"deleted_user username={uname}")
    return render_fake_admin("users", action_msg=f"User '{uname}' deleted!")

@app.route('/fake/database')
def fake_database():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_database")
    return render_fake_admin("database")

@app.route('/fake/database/query', methods=['POST'])
def fake_db_query():
    if not check_logged_in():
        return redirect('/login-page')
    query = request.form.get('sql_query', '')
    db = request.form.get('db_name', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"executed_sql db={db} query={query}")
    return render_fake_admin("database", action_msg=f"Query executed: {query}")

@app.route('/fake/files')
def fake_files():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_files")
    return render_fake_admin("files")

@app.route('/fake/files/upload', methods=['POST'])
def fake_upload():
    if not check_logged_in():
        return redirect('/login-page')
    path = request.form.get('upload_path', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"file_upload_attempt path={path}")
    return render_fake_admin("files", action_msg=f"File uploaded to {path}!")

@app.route('/fake/settings')
def fake_settings():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_settings")
    return render_fake_admin("settings")

@app.route('/fake/settings/password', methods=['POST'])
def fake_change_password():
    if not check_logged_in():
        return redirect('/login-page')
    current = request.form.get('current_password', '')
    new = request.form.get('new_password', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"password_change current={current} new={new}")
    return render_fake_admin("settings", action_msg="Password changed successfully!")

@app.route('/fake/settings/server', methods=['POST'])
def fake_server_settings():
    if not check_logged_in():
        return redirect('/login-page')
    ip = request.form.get('server_ip', '')
    port = request.form.get('server_port', '')
    env = request.form.get('environment', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"server_settings ip={ip} port={port} env={env}")
    return render_fake_admin("settings", action_msg="Server settings saved!")

@app.route('/fake/logs')
def fake_logs():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_logs")
    return render_fake_admin("logs")

@app.route('/fake/network')
def fake_network():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_network")
    return render_fake_admin("network")

@app.route('/fake/network/firewall', methods=['POST'])
def fake_firewall():
    if not check_logged_in():
        return redirect('/login-page')
    rule_ip = request.form.get('rule_ip', '')
    action = request.form.get('rule_action', '')
    port = request.form.get('rule_port', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"firewall_rule ip={rule_ip} action={action} port={port}")
    return render_fake_admin("network", action_msg=f"Firewall rule added: {action} {rule_ip}:{port}")

@app.route('/fake/backup')
def fake_backup():
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN", "visited_backup")
    return render_fake_admin("backup")

@app.route('/fake/backup/create', methods=['POST'])
def fake_create_backup():
    if not check_logged_in():
        return redirect('/login-page')
    backup_type = request.form.get('backup_type', '')
    backup_name = request.form.get('backup_name', '')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"backup_created type={backup_type} name={backup_name}")
    return render_fake_admin("backup", action_msg=f"Backup '{backup_name}' created!")

@app.route('/fake/action/<action_name>')
def fake_action(action_name):
    if not check_logged_in():
        return redirect('/login-page')
    log_event(request.remote_addr, "FAKE-ADMIN-ACTION", f"clicked_{action_name}")
    return render_fake_admin("dashboard", action_msg=f"Action '{action_name}' completed!")

if __name__ == '__main__':
    print("=" * 50)
    print("  LOGIN TRAP RUNNING")
    print("  Open: http://0.0.0.0:8080")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=True)