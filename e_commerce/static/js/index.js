
let home = document.getElementById("homes");
let cloth = document.getElementById("cloths");
let review = document.getElementById("reviews");
let blog = document.getElementById("blogs");
let contact = document.getElementById("contacts");
let login = document.getElementById("login");
let button = document.getElementById("btn");

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





cloth.addEventListener("click", function(){
    home.style.color="black";
    cloth.style.color="red";
    review.style.color="black";
    blog.style.color="black";
    contact.style.color="black";


})


review.addEventListener("click", function(){
    home.style.color="black";
    cloth.style.color="black";
    review.style.color="red";
    blog.style.color="black";
    contact.style.color="black";


})


blog.addEventListener("click", function(){
    home.style.color="black";
    cloth.style.color="black";
    review.style.color="black";
    blog.style.color="red";
    contact.style.color="black";


})


contact.addEventListener("click", function(){
    home.style.color="black";
    cloth.style.color="black";
    review.style.color="black";
    blog.style.color="black";
    contact.style.color="red";


})

login.addEventListener("click", function(){
    document.getElementById("log").style.display="block"
})

button.addEventListener("click", function(){
    let logName = document.getElementById("logName")
    if(logName.value == ""){
        alert("please Enter Email & Password")
    }else{
    alert("You Logged In");
    document.getElementById("log").style.display="none";
    }


})
function submit(){

    let name = document.getElementById("name");
    if(name.value == ""){
        alert("Please Enter Detail")
    }else{
    alert("Thanks for joining "+" : " + name.value);
    name.value=""
    
    }
}
function tryOnProduct() {
    const canvas = document.getElementById("tryOnCanvas");
    const ctx = canvas.getContext("2d");
    const input = document.getElementById("uploadImage");

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                // Overlay a sample saree design
                const overlay = new Image();
                overlay.src = "https://via.placeholder.com/400"; // Replace with an actual saree image
                overlay.onload = function () {
                    ctx.globalAlpha = 0.7;
                    ctx.drawImage(overlay, 0, 0, canvas.width, canvas.height);
                };
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        alert("Please upload an image first.");
    }
}

