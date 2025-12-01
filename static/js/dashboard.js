// 🔥 LIVE SocketIO Dashboard - Real-time IDS updates!

let socket = io();  // same origin: http://127.0.0.1:5000

// ----- Connection status -----


let attacksChart = null;
let chartLabels = [];        // times
let chartSql = [];
let chartXss = [];
let chartDir = [];


function setStatus(online) {
    const dot = document.getElementById('status-dot');
    const text = document.getElementById('status-text');
    if (!dot || !text) return;

    if (online) {
        dot.classList.remove('offline');
        dot.classList.add('online');
        text.textContent = 'Connected to IDS';
    } else {
        dot.classList.remove('online');
        dot.classList.add('offline');
        text.textContent = 'Disconnected from IDS';
    }
}



socket.on('connect', function () {
    console.log('🔗 Connected to IDS server!');
    setStatus(true);
});

socket.on('disconnect', function () {
    console.log('🔌 Disconnected from IDS server');
    setStatus(false);
});

// ----- Handlers for events from server -----

socket.on('attack_detected', function (data) {
    console.log('🚨 Attack detected:', data);

    // Update main stats
    if (data.stats) {
        updateStat('sql-count', data.stats.sql ?? 0);
        updateStat('xss-count', data.stats.xss ?? 0);
        updateStat('dir_traversal-count', data.stats.dir_traversal ?? 0);
        updateStat('total_packets', data.stats.total_packets ?? 0);
    }

    // Add latest attack to table
    if (data.recent && data.recent.length > 0) {
        addAttackToTable(data.recent[data.recent.length - 1]);
    }

    // Optional: sound alert
    playAlertSound();
});

socket.on('stats_update', function (stats) {
    console.log('📊 Initial stats:', stats);
    updateStat('sql-count', stats.sql ?? 0);
    updateStat('xss-count', stats.xss ?? 0);
    updateStat('dir_traversal-count', stats.dir_traversal ?? 0);
    updateStat('total_packets', stats.total_packets ?? 0);
});

// ----- UI update helpers -----

function updateStat(id, value) {
    const element = document.getElementById(id);
    if (!element) return;

    element.textContent = value;

    // Pulse animation on change
    element.classList.add('pulse');
    setTimeout(() => element.classList.remove('pulse'), 400);
}

function addAttackToTable(attack) {
    if (!attack) return;

    const tbody = document.querySelector('#attacks-table tbody');
    if (!tbody) return;

    let badgeClass = 'badge-secondary';
    const typeText = (attack.type || '').toString();

    if (typeText.includes('SQL')) {
        badgeClass = 'badge-attack-sql';
    } else if (typeText.includes('XSS') || typeText.toLowerCase().includes('xss')) {
        badgeClass = 'badge-attack-xss';
    } else if (typeText.toLowerCase().includes('directory')) {
        badgeClass = 'badge-attack-dir';
    }

    const row = document.createElement('tr');
    row.className = 'attack-row';
    row.innerHTML = `
        <td>${attack.time || ''}</td>
        <td><span class="badge ${badgeClass}">${typeText}</span></td>
        <td>${attack.ip || ''}</td>
    `;

    tbody.insertBefore(row, tbody.firstChild);

    // keep only last 10 rows
    while (tbody.children.length > 10) {
        tbody.removeChild(tbody.lastChild);
    }
}

// ----- Simple beep on each alert (optional) -----

function playAlertSound() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;

        const audioContext = new AudioContext();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 750;
        oscillator.type = 'square';

        gainNode.gain.setValueAtTime(0.25, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.4);
    } catch (e) {
        console.warn('Audio not supported or blocked:', e);
    }
}

// ----- Page load -----

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 IDS Dashboard JS loaded');
});

function initAttacksChart() {
    const ctx = document.getElementById('attacks-chart');
    if (!ctx) return;

    attacksChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: 'SQL',
                    data: chartSql,
                    borderColor: '#f87171',
                    backgroundColor: 'rgba(248,113,113,0.15)',
                    tension: 0.3,
                    fill: true,
                },
                {
                    label: 'XSS',
                    data: chartXss,
                    borderColor: '#facc15',
                    backgroundColor: 'rgba(250,204,21,0.15)',
                    tension: 0.3,
                    fill: true,
                },
                {
                    label: 'Dir Traversal',
                    data: chartDir,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56,189,248,0.15)',
                    tension: 0.3,
                    fill: true,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#e5e7eb' } }
            },
            scales: {
                x: {
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(148,163,184,0.2)' }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(148,163,184,0.2)' }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 IDS Dashboard JS loaded');
    initAttacksChart();
});

socket.on('attack_detected', function (data) {
    console.log('🚨 Attack detected:', data);

    if (data.stats) {
        updateStat('sql-count', data.stats.sql ?? 0);
        updateStat('xss-count', data.stats.xss ?? 0);
        updateStat('dir_traversal-count', data.stats.dir_traversal ?? 0);
        updateStat('total_packets', data.stats.total_packets ?? 0);
    }

    if (data.recent && data.recent.length > 0) {
        const latest = data.recent[data.recent.length - 1];
        addAttackToTable(latest);

        // chart point: time on X, cumulative counts on Y
        const label = latest.time || new Date().toLocaleTimeString();
        chartLabels.push(label);
        chartSql.push(data.stats?.sql ?? 0);
        chartXss.push(data.stats?.xss ?? 0);
        chartDir.push(data.stats?.dir_traversal ?? 0);

        // keep last 20 points
        const maxPoints = 20;
        if (chartLabels.length > maxPoints) {
            chartLabels.shift();
            chartSql.shift();
            chartXss.shift();
            chartDir.shift();
        }

        if (attacksChart) {
            attacksChart.update('none'); // fast update, no animation
        }
    }

    playAlertSound();
});
