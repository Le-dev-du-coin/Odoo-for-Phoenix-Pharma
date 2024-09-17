//odoo.define('phoenix_pharma_claim.claim_functions', function (require) {
//    "use strict";

const baseUrl = window.location.pathname;

// Fonction pour récupérer les produits associés à une facture
async function fetchInvoiceProducts(invoiceNumber) {
  let url =`/get_invoice_products?invoice_number=${invoiceNumber}`;
  console.log("URL:", url);
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Vérifiez si la réponse est correcte
    if (!response.ok) {
      throw new Error("Erreur lors de la récupération des produits.");
    }

    // Récupérer les données JSON
    const data = await response.json();

    // Appeler la fonction pour afficher les produits
    displayProducts(data.products);
  } catch (error) {
    console.error("Erreur lors de la récupération sdes produits:", error);
    alert("Erreur lors de la récupération des produits.");
  }
}

// Fonction pour afficher les produits récupérés
function displayProducts(products) {
  const productsDiv = document.getElementById("products_div");
  const productsSelect = document.getElementById("selected_products");

  productsSelect.innerHTML = ""; // Vider la liste existante

  if (products.length === 0) {
    productsDiv.style.display = "none";
    alert("Aucun produit trouvé pour cette facture.");
    return;
  }

  // Afficher les produits trouvés
  productsDiv.style.display = "block";
  products.forEach(function (product) {
    const option = document.createElement("option");
    option.value = product.id;
    option.textContent = product.name;
    productsSelect.appendChild(option);
  });

  // Afficher également le champ de message et le bouton de soumission
  document.getElementById("message_field").style.display = "block";
  document.getElementById("submit_btn").style.display = "block";
}

// Fonction pour soumettre le formulaire via AJAX
async function submitClaimForm() {
  const form = document.getElementById("reclamationForm");
  const formData = new FormData(form);

  try {
    const response = await fetch("/submit/reclamation", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      document.body.innerHTML = await response.text(); // Remplacer le contenu de la page par la page de
      confirmation;
    } else {
      alert("Erreur lors de la soumission de la réclamation.");
    }
  } catch (error) {
    console.error("Erreur:", error);
    alert("Erreur lors de la soumission de la réclamation.");
  }
}

// Fonction appelée lors du clic sur le bouton "Trouver la Facture"
function onFindInvoice() {
  const invoiceNumber = document.getElementById("invoice_number").value;

  if (!invoiceNumber) {
    alert("Veuillez entrer un numéro de facture valide.");
    return;
  }

  // Récupérer et afficher les produits de la facture
  fetchInvoiceProducts(invoiceNumber);
}

// Écouteur pour la soumission du formulaire
document
  .getElementById("reclamationForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Empêcher le rechargement de la page
    submitClaimForm(); // Soumettre le formulaire via AJAX
  });
//});
