
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

