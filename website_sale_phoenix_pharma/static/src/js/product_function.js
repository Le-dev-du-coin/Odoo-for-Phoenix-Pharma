//odoo.define('website_sale_phoenix_pharma.product_functions', function (require) {
//    "use strict";

    function increaseQuantity(productId) {
        const qtyInput = document.getElementById(`qty_${productId}`);
        qtyInput.value = parseInt(qtyInput.value) + 1;
    }

    function decreaseQuantity(productId) {
        const qtyInput = document.getElementById(`qty_${productId}`);
        if (qtyInput.value > 1) {
            qtyInput.value = parseInt(qtyInput.value) - 1;
        }
    }

    async function addToCart(productId) {
        const quantity = document.getElementById('qty_' + productId).value;
        const csrfToken = document.getElementById('csrf_token').value;

        try {
            const response = await fetch('/shop/cart/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'product_id': productId,
                    'add_qty': quantity,
                    'csrf_token': csrfToken
                })
            });

            if (response.ok) {
                location.reload();
            } else {
                alert('Erreur lors de l\'ajout au panier.');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'ajout au panier.');
        }
    }

    window.increaseQuantity = increaseQuantity;
    window.decreaseQuantity = decreaseQuantity;
    window.addToCart = addToCart;
//});
function displaySuggestions(products) {
    const suggestionsContainer = document.getElementById('suggestions');
    suggestionsContainer.innerHTML = '';

    if (products.length === 0) {
        suggestionsContainer.innerHTML = '<p class="list-group-item">Aucun produit trouvé</p>';
        return;
    }

    products.forEach(function(product) {
        const suggestion = document.createElement('a');
        suggestion.href = `/shop/product/${product.id}`;
        suggestion.className = 'list-group-item list-group-item-action';
        suggestion.innerHTML = `${product.name} - ${product.price} ${product.currency}`;
        suggestionsContainer.appendChild(suggestion);
    });
}

async function fetchProductSuggestions() {
    const query = document.getElementById('product_search').value;

    if (query.length >= 3) {
        try {
            const response = await fetch('/tous-les-produits/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'search_term': query})
            });

            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des suggestions de produits.');
            }

            const data = await response.json();
            const products = data.result; // Accéder au tableau des produits à partir de "result"

            displaySuggestions(products);
        } catch (error) {
            console.error('Error fetching product suggestions:', error);
        }
    } else {
        document.getElementById('suggestions').innerHTML = ''; // Vider les suggestions si moins de 3 caractères
    }
}

document.getElementById('product_search').addEventListener('input', fetchProductSuggestions);
