//odoo.define('test_fetch.test_function', function(require) {
//    'use strict';
console.log('JS charge');

async function chargerNom(nom) {
    const response = await fetch ('/test/api', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    if (!response.ok){
        console.log('Erreur, mauvaise response')
        alert('Mauvaise response')
    }
}
function onclikCharger() {
    const nom = document.getElementById('nom');
    console.log(nom)

    if(!nom){
        alert('Veuillez remplir le chanps')
    }
    chargerNom()
};
//});