function redirectToSelectedPage() {
    // Get the selected option
    var selectedOption = document.getElementById("Category").value;

    // Define the mapping of options to page URLs
    var pageURLs = {
        "Shantiniketan Leather": "WB GI Tag Items/1. Shantiniketan Leather Goods/ShantiniketanLeatherGoods.html",
        "Madur Kathi": "WB GI Tag Items/2. Madur Kathi/MadurKathi.html",
        "Baluchuri": "WB GI Tag Items/3. Baluchari Saree/BaluchariSaree.html",
        "Nakshi Katha": "WB GI Tag Items/4. Nakshi Katha/NakshiKatha.html",
        "Purulia Chhau Mask": "WB GI Tag Items/5. Purulia Chhau Mask/ChhauMask.html",
        "Santipur Saree": "WB GI Tag Items/6. Santipuri Saree/SantipuriSaree.html",
        "Bankura Terracotta Horse": "bankWB GI Tag Items/7. Bankura Terracotta Horse/BankuraTerracotta.htmlura_terracotta_horse.html",
        "Dhokra Craft": "WB GI Tag Items/8. Dhokra Craft/DhokraCraft.html",
        "Garad Saree": "WB GI Tag Items/9. Garad Saree/GaradSaree.html",
        "SitaBhog": "WB GI Tag Items/10. Burdwan's Sitabhog/GaradSaree.html"
    };

    // Get the corresponding URL for the selected option
    var selectedPageURL = pageURLs[selectedOption];

    // Redirect to the selected page
    if (selectedPageURL) {
        window.location.href = selectedPageURL;
    }
}
let compareList = [];

// document.querySelector('#addToCompareBtn').addEventListener('click', () => {
//     console.log("Add to compare clicked");
// });

// function addToCompare(productId) {
//     console.log("Item added to compare");
//     if (!compareList.includes(productId)) {
//         compareList.push(productId);
//         alert(`Product ${productId} added to comparison!`);
//     } else {
//         alert(`Product ${productId} is already in comparison.`);
//     }

//     if (compareList.length === 2) {
//         // Redirect to the comparison page or show the comparison modal
//         window.location.href = `/compare/${compareList[0]}/${compareList[1]}`;
//     }
// }
// document.addEventListener('DOMContentLoaded', () => {
//     const button = document.querySelector('#addToCompareBtn');
//     if (button) {
//         button.addEventListener('click', () => {
//             const productId = button.getAttribute('data-product-id');
//             console.log(`Product ID: ${productId}`);
//             addToCompare(productId);
//         });
//     }
// });

// function addToCompare(productId) {
//     console.log(`Product ID: ${productId}`);
//     // Add your logic here
// }


