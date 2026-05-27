fetch("data/covers.json")
    .then(response => response.json())
    .then(covers => {
        console.log(covers);

        renderFeatured(covers);
        renderBrowseCollection(covers);
    });


function renderFeatured(covers) {

    const featuredSection = document.getElementById("featured");

    const featuredCovers = covers.filter(
        cover => cover.tags.includes("featured")
    );

    featuredCovers.forEach(cover => {

        const card = document.createElement("div");

        card.innerHTML = `
            <img
                src="${cover.thumb}"
                alt="${cover.short_description}"
                class="gallery-thumbnail"
            >
            <h3>${cover.title}</h3>
            <p>${cover.city}, ${cover.country}</p>
        `;
         card.addEventListener("click", () => {
            openImageModal(cover);
         });

        featuredSection.appendChild(card);
    });
}
function renderBrowseCollection(covers) {

    const browseSection = document.getElementById("browse");

    const grouped = {};

    covers.forEach(cover => {

        if (!grouped[cover.country]) {
            grouped[cover.country] = {};
        }

        if (!grouped[cover.country][cover.city]) {
            grouped[cover.country][cover.city] = [];
        }

        grouped[cover.country][cover.city].push(cover);
    });

    for (const country in grouped) {

        const countryHeading = document.createElement("h3");
        countryHeading.textContent = country;
        browseSection.appendChild(countryHeading);

        const cities = grouped[country];

        for (const city in cities) {

            const cityHeading = document.createElement("h4");
            cityHeading.textContent = city;
            browseSection.appendChild(cityHeading);

            const grid = document.createElement("div");
            grid.className = "thumbnail-grid";

            cities[city].forEach(cover => {

                const card = document.createElement("div");

                card.innerHTML = `
                    <img
                        src="${cover.thumb}"
                        alt="${cover.short_description}"
                        class="gallery-thumbnail"
                    >
                    <h3>${cover.title}</h3>
                    <p>${cover.city}, ${cover.country}</p>
                `;

                card.addEventListener("click", () => {
                    openImageModal(cover);
                });

                grid.appendChild(card);
            });

            browseSection.appendChild(grid);
        }
    }
}

function openImageModal(cover) {
    const modal = document.getElementById("image-modal");
    const modalImg = document.getElementById("image-modal-img");
    const modalTitle = document.getElementById("image-modal-title");
    const modalLocation = document.getElementById("image-modal-location");
    const modalDescription = document.getElementById("image-modal-description");

    modalImg.src = cover.large;
    modalImg.alt = cover.title;

    modalTitle.textContent = cover.title;
    modalLocation.textContent = `${cover.city}, ${cover.country}`;
    modalDescription.textContent = cover.description || "";

    modal.classList.remove("hidden");
}

const modal = document.getElementById("image-modal");
const closeButton = document.getElementById("image-modal-close");

closeButton.addEventListener("click", (event) => {
    event.stopPropagation();
    modal.classList.add("hidden");
});

modal.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.classList.add("hidden");
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        modal.classList.add("hidden");
    }
});