document.addEventListener("DOMContentLoaded", function () {
    const generateImageForm = document.getElementById("logoForm");
    let imageCounter = 0;

    generateImageForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(generateImageForm);
        fetch("/generate_image", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const generatedImageElement = document.getElementById("generatedImage");
            if (imageCounter < 3) {
                const imgElement = document.createElement("img");
                imgElement.src = data.image_url;
                imgElement.alt = "Generated Image";
                generatedImageElement.appendChild(imgElement);
                imageCounter++;
            } else {
                // Replace the oldest image with the new one
                const images = generatedImageElement.getElementsByTagName("img");
                images[0].src = data.image_url;
            }
        });
    });
});