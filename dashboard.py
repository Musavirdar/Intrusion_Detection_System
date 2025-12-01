# this is for test case
'''from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ids-secret-key-2025'
socketio =SocketIO(app)

attack_stats = {
    'sql' : 0,
    'xss' : 0,
    'dir_traversal' : 0,
    'sql_injection' : 0,
    'total_packets': 0
    
}

recent_attacks =[]

def simulate_attacks():
    attacks = [
        ('SQL injection detected', 'sql'),
        ('XSS attack detected', 'xss'),
        ('Directory traversal detected', 'dir_traversal'),
        ('SQL injection attempt', 'sql_injection')
    ]
    while True:
        time.sleep(3)
        attack_name, attack_type = attacks[int(time.time())% len(attacks)]
        
        #updaee stats
        attack_stats[attack_type] +=1
        attack_stats['total_packets'] += 10
        
        #recent attacks
        recent_attacks.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': attack_name,
            'ip': f'127.0.0.{int(time.time())% 255}'
        })
        recent_attacks[:] = recent_attacks[-10:] # it will keep last 10
        
        socketio.emit('attack_detected',{
            'type': attack_type,
            'stats': attack_stats,
            'recent': recent_attacks
        })


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('client connected!!')
    emit('stats_update', attack_stats)
    
@socketio.on('disconnect')
def handle_disconnect():
    print('🔌 Client disconnected!')
    
    
def push_attack_event(attack_type_key, attack_label, src_ip):
    """
    Used by IDS code to push a real attack to the dashboard.
    attack_type_key: 'sql', 'xss', 'dir_traversal', 'sql_injection'
    attack_label: human readable text, e.g. 'SQL injection detected'
    src_ip: '127.0.0.1' or any string IP
    """
    attack_stats[attack_type_key] += 1
    attack_stats['total_packets'] += 1

    recent_attacks.append({
        'time': datetime.now().strftime('%H:%M:%S'),
        'type': attack_label,
        'ip': src_ip
    })
    recent_attacks[:] = recent_attacks[-10:]

    socketio.emit('attack_detected', {
        'type': attack_type_key,
        'stats': attack_stats,
        'recent': recent_attacks
    })

    

if __name__ == '__main__':
    simulator_thread = threading.Thread(target=simulate_attacks, daemon=True)
    simulator_thread.start()
    
    print("🚀 Dashboard running on http://127.0.0.1:5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)'''

# real 
# dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading
import time



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ids-secret-key-2025'
socketio = SocketIO(app)


attack_stats = {
    'sql': 0,
    'xss': 0,
    'dir_traversal': 0,
    'sql_injection': 0,
    'total_packets': 0,
}

recent_attacks = []


def push_attack_event(attack_type_key: str, attack_label: str, src_ip: str):
    print("PUSH_ATTACK_EVENT CALLED:", attack_type_key, attack_label, src_ip)

    if attack_type_key not in attack_stats:
        print("UNKNOWN ATTACK TYPE KEY:", attack_type_key)
        return

    attack_stats[attack_type_key] += 1
    attack_stats['total_packets'] += 1

    recent_attacks.append({
        'time': datetime.now().strftime('%H:%M:%S'),
        'type': attack_label,
        'ip': src_ip,
    })
    del recent_attacks[:-10]

    socketio.emit('attack_detected', {
        'type': attack_type_key,
        'stats': attack_stats,
        'recent': recent_attacks,
    })


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')        # ✅ different URL
def test():
    socketio.emit('attack_detected', {
        'type': 'sql',
        'stats': {
            'sql': 1,
            'xss': 0,
            'dir_traversal': 0,
            'sql_injection': 0,
            'total_packets': 10
        },
        'recent': [{
            'time': 'NOW',
            'type': 'SQL test',
            'ip': '127.0.0.1'
        }],
    })
    return "emitted"


@socketio.on('connect')
def handle_connect():
    print('🔗 client connected')
    emit('stats_update', attack_stats)


def simulate_attacks():
    attacks = [
        ('sql', 'SQL injection detected'),
        ('xss', 'XSS attack detected'),
        ('dir_traversal', 'Directory traversal detected'),
        ('sql_injection', 'SQL injection attempt'),
    ]
    while True:
        time.sleep(5)
        key, label = attacks[int(time.time()) % len(attacks)]
        push_attack_event(key, label, '127.0.0.1')


if __name__ == '__main__':
    # threading.Thread(target=simulate_attacks, daemon=True).start()
    print('🚀 Dashboard running at http://127.0.0.1:5000')
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
