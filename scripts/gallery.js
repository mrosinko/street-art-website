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
            <img src="${cover.thumb}" alt="${cover.title}">
            <h3>${cover.title}</h3>
            <p>${cover.short_description}</p>
        `;

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
                    <img src="${cover.thumb}" alt="${cover.title}">
                    <p>${cover.title}</p>
                `;

                grid.appendChild(card);
            });

            browseSection.appendChild(grid);
        }
    }
}