document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reclamationForm');
    const invoiceInput = document.getElementById('invoice_number');
    const productsSelect = document.getElementById('selected_products');

    // Événement pour vérifier le numéro de facture et charger les produits associés
    invoiceInput.addEventListener('change', function() {
        const invoiceNumber = invoiceInput.value;
        if (invoiceNumber) {
            // Requête AJAX pour récupérer les produits liés à la facture
            fetch(`/get_invoice_products?invoice_number=${invoiceNumber}`)
                .then(response => response.json())
                .then(data => {
                    // Effacer les options actuelles
                    productsSelect.innerHTML = '';
                    // Ajouter les nouveaux produits
                    data.products.forEach(product => {
                        const option = document.createElement('option');
                        option.value = product.id;
                        option.textContent = product.name;
                        productsSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Erreur lors de la récupération des produits:', error));
        }
    });

    // Gestion de la soumission du formulaire via AJAX
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Empêcher l'envoi classique du formulaire
        const formData = new FormData(form);

        // Requête AJAX pour soumettre le formulaire
        fetch('/submit/reclamation', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Erreur lors de la soumission de la réclamation.');
        })
        .then(data => {
            // Redirection ou message de succès
            document.body.innerHTML = data;  // Remplacer la page par la page de confirmation
        })
        .catch(error => console.error('Erreur:', error));
    });
});
