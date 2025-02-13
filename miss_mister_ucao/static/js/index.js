// Récupérer le CSRF token depuis le formulaire caché
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function voter(missId) {
    fetch(`/vote/${missId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            let voteCount = document.getElementById(`votes-${missId}`);
            if (voteCount) {
                voteCount.textContent = data.votes; // Nouveau nombre de votes
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erreur:', error));
}