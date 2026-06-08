from flask import Flask, render_template_string, jsonify
import json
import os

app = Flask(__name__)

LOG_FILE = '/home/asbah/honeypot_logs.json'

def get_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Honeypot Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #0a0a0a; 
            color: #00ff00; 
            font-family: monospace;
            padding: 20px;
        }
        h1 { 
            text-align: center; 
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 24px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-box {
            border: 1px solid #00ff00;
            padding: 15px;
            text-align: center;
            background: #0d0d0d;
        }
        .stat-number { 
            font-size: 36px; 
            font-weight: bold;
            color: #ff0000;
        }
        .stat-label { 
            font-size: 12px;
            color: #00ff00;
            margin-top: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background: #003300;
            color: #00ff00;
            padding: 10px;
            border: 1px solid #00ff00;
        }
        td {
            padding: 8px;
            border: 1px solid #003300;
            font-size: 13px;
            word-break: break-all;
        }
        tr:nth-child(even) { background: #0d0d0d; }
        tr:hover { background: #001a00; }
        .critical { color: #ff0000; font-weight: bold; }
        .high { color: #ff6600; }
        .medium { color: #ffff00; }
        .section-title {
            color: #00ff00;
            border-bottom: 1px solid #00ff00;
            padding-bottom: 10px;
            margin: 20px 0 10px 0;
            font-size: 18px;
        }
        .refresh-btn {
            background: #003300;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 10px 20px;
            cursor: pointer;
            font-family: monospace;
            font-size: 14px;
            display: block;
            margin: 0 auto 20px auto;
        }
        .refresh-btn:hover { background: #005500; }
        .port-bar {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        .port-label { width: 100px; }
        .bar {
            height: 20px;
            background: #00ff00;
            margin-left: 10px;
            min-width: 5px;
        }
        .port-count { margin-left: 10px; }
    </style>
    <script>
        setTimeout(function(){ location.reload(); }, 5000);
    </script>
</head>
<body>
    <h1>🍯 HONEYPOT SECURITY DASHBOARD</h1>
    
    <button class="refresh-btn" onclick="location.reload()">
        [ REFRESH DATA ]
    </button>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-number critical">{{ total_attacks }}</div>
            <div class="stat-label">TOTAL ATTACKS</div>
        </div>
        <div class="stat-box">
            <div class="stat-number high">{{ unique_ips }}</div>
            <div class="stat-label">UNIQUE ATTACKERS</div>
        </div>
        <div class="stat-box">
            <div class="stat-number medium">{{ most_targeted }}</div>
            <div class="stat-label">MOST TARGETED PORT</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ last_attack }}</div>
            <div class="stat-label">LAST ATTACK</div>
        </div>
    </div>

    <div class="section-title">▶ ATTACK BREAKDOWN BY SERVICE</div>
    {% for service, count in service_counts.items() %}
    <div class="port-bar">
        <span class="port-label">{{ service }}</span>
        <div class="bar" style="width: {{ count * 20 }}px"></div>
        <span class="port-count">{{ count }} attacks</span>
    </div>
    {% endfor %}

    <div class="section-title">▶ RECENT ATTACK LOGS</div>
    <table>
        <tr>
            <th>TIMESTAMP</th>
            <th>ATTACKER IP</th>
            <th>PORT</th>
            <th>SERVICE</th>
            <th>RISK LEVEL</th>
            <th>DATA SENT</th>
        </tr>
        {% for log in logs[-20:] | reverse %}
        <tr>
            <td>{{ log.timestamp }}</td>
            <td class="critical">{{ log.attacker_ip }}</td>
            <td>{{ log.port_attacked }}</td>
            <td class="high">{{ log.service }}</td>
            <td>
                {% if log.port_attacked in [21, 23] %}
                <span class="critical">🔴 CRITICAL</span>
                {% elif log.port_attacked in [22, 3306] %}
                <span class="high">🟠 HIGH</span>
                {% else %}
                <span class="medium">🟡 MEDIUM</span>
                {% endif %}
            </td>
            <td>{{ log.data_sent[:100] if log.data_sent else 'No data' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def dashboard():
    logs = get_logs()
    total_attacks = len(logs)
    unique_ips = len(set(log['attacker_ip'] for log in logs)) if logs else 0
    service_counts = {}
    for log in logs:
        service = log['service']
        service_counts[service] = service_counts.get(service, 0) + 1
    most_targeted = max(service_counts, key=service_counts.get) if service_counts else 'None'
    last_attack = logs[-1]['timestamp'][:16] if logs else 'No attacks yet'
    return render_template_string(
        DASHBOARD_HTML,
        logs=logs,
        total_attacks=total_attacks,
        unique_ips=unique_ips,
        service_counts=service_counts,
        most_targeted=most_targeted,
        last_attack=last_attack
    )

@app.route('/api/logs')
def api_logs():
    return jsonify(get_logs())

if __name__ == '__main__':
    print("Dashboard running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)