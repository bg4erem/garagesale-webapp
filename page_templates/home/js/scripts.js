/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
async function load_and_render_items() {
    const itemsContainer = document.getElementById("items-container");
    let items = await fetch("/api/v1/items").then( resp => { return resp.json() })

    items.forEach(item => {
        let itemCard = document.createElement("div");
        let itemPictureSrc = "https://dummyimage.com/450x300/dee2e6/6c757d.jpg";
        if (item.photos.length > 0) { itemPictureSrc = item.photos[0] }
        itemCard.className = "col mb-5";
        itemCard.innerHTML = `
            <div class="card h-100">
                <!-- Sale badge-->
                <div class="badge bg-dark text-white position-absolute" style="top: 0.5rem; right: 0.5rem">Sale</div>
                <!-- Product image-->
                <img class="card-img-top" src="${itemPictureSrc}" alt="..." />
                <!-- Product details-->
                <div class="card-body p-4">
                    <div class="text-center">
                        <!-- Product name-->
                        <h5 class="fw-bolder">${item.title}</h5>
                        <!-- Product price-->
                        ${item.price} ${item.price_curr}
                    </div>
                </div>
                <!-- Product actions-->
                <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                    <div class="text-center"><a class="btn btn-outline-dark mt-auto" href="/details/${item['_id']}">Подробнее</a></div>
                </div>
            </div>
        `;

        itemsContainer.appendChild(itemCard);
    })
}

load_and_render_items();