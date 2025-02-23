// Fonction pour voter
function voter(missId) {
    const csrfToken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;

    fetch(`/vote/${missId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mettre à jour le pourcentage de votes affiché
            const votePercentage = document.getElementById(`votes-${missId}`);
            votePercentage.textContent = data.vote_percentage + '%';
            // Ajouter une animation
            votePercentage.style.transform = 'scale(1.2)';
            setTimeout(() => {
                votePercentage.style.transform = 'scale(1)';
            }, 300);
            showNotification(data.message, 'success');
            updateChartData(); // Mettre à jour le graphique
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => console.error('Erreur :', error));
}


// Fonction pour filtrer les candidates
function filterCandidates() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const cards = document.querySelectorAll('.miss-card');

    cards.forEach(card => {
        const name = card.querySelector('h2').textContent.toLowerCase();
        if (name.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Fonction pour trier les candidates
function sortCandidates() {
    const sortBy = document.getElementById('sort').value;
    window.location.href = `?sort=${sortBy}`;
}

// Fonction pour activer/désactiver le mode sombre
function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    const isDarkMode = body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode); // Sauvegarder le choix dans localStorage
    document.getElementById('theme-toggle').textContent = isDarkMode ? 'Mode clair' : 'Mode sombre';
}

// Charger le mode sombre au démarrage
function loadDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        document.getElementById('theme-toggle').textContent = 'Mode clair';
    } else {
        document.body.classList.remove('dark-mode');
        document.getElementById('theme-toggle').textContent = 'Mode sombre';
    }
}

// Appliquer le mode sombre au chargement de la page
loadDarkMode();

// Écouter le clic sur le bouton de mode sombre
document.getElementById('theme-toggle').addEventListener('click', toggleDarkMode);

// Fonction pour afficher des notifications
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Fonction pour mettre à jour le graphique des résultats
const ctx = document.getElementById('resultsChart').getContext('2d');
const resultsChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [], // Noms des candidates
        datasets: [{
            label: 'Pourcentage de votes',
            data: [], // Pourcentage de votes
            backgroundColor: '#6200ea',
        }]
    },
    options: {
        responsive: true, // Activer la réactivité
        maintainAspectRatio: false, // Désactiver le maintien du ratio pour une meilleure adaptation
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value) {
                        return value + '%'; // Ajouter le symbole % aux valeurs de l'axe Y
                    }
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.raw + '%'; // Ajouter le symbole % aux tooltips
                    }
                }
            }
        }
    }
});

function updateChartData() {
    fetch('/get_results/')
        .then(response => response.json())
        .then(data => {
            resultsChart.data.labels = data.labels;
            resultsChart.data.datasets[0].data = data.votes;
            resultsChart.update();
        });
}

// Charger les données initiales du graphique
updateChartData();