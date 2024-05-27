/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
async function load_and_render_items() {
    const itemsContainer = document.getElementById("items-container");
    let items = await fetch("/api/v1/items", {credentials: "same-origin"}).then( resp => { return resp.json() })

    items.forEach(item => {
        if (!item.sold) {
            let itemCard = document.createElement("div");

            let itemPictureSrc = "https://dummyimage.com/450x300/dee2e6/6c757d.jpg";
            if (item.photos.length > 0) { itemPictureSrc = item.photos[0] }

            itemCard.className = "col mb-5";
            let itemPriceHTML = `${item.price} ${item.price_curr}`;
            if (item.full_price) { 
                itemPriceHTML = `
                    <span class="text-muted text-decoration-line-through">${item.full_price} ${item.price_curr}</span>
                    ${item.price} ${item.price_curr}
                ` 
            }

            let itemCardSaleBadge = "";
            if (item.full_price) {
                let discount = Math.ceil(100 - (item.price / item.full_price * 100))
                itemCardSaleBadge = `
                    <div class="badge bg-danger text-white position-absolute" style="top: 0.5rem; right: 0.5rem">- ${discount}%</div>
                `;
            }

            itemCard.innerHTML = `
                <div class="card h-100">
                    <!-- Sale badge-->
                    ${itemCardSaleBadge}
                    <!-- Product image-->
                    <img class="card-img-top" src="${itemPictureSrc}" alt="..." />
                    <!-- Product details-->
                    <div class="card-body p-4">
                        <div class="text-center">
                            <!-- Product name-->
                            <h5 class="fw-bolder">
                                <a href="/details/${item['_id']}" style="text-decoration: none; color: black;">${item.title}</a></h5>
                            <!-- Product price-->
                            ${itemPriceHTML}
                        </div>
                    </div>
                    <!-- Product actions-->
                    <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                        <div class="text-center"><a class="btn btn-outline-dark mt-auto" href="/details/${item['_id']}">Подробнее</a></div>
                    </div>
                </div>
            `;

            itemsContainer.appendChild(itemCard);
        }
    });

    // const progressBarContainer = document.getElementById("soldProgressBar");
    // let itemsSoldPercent = Math.ceil((items.filter( item => item.sold ).length) / (items.length) * 100) ;
    // progressBarContainer.innerHTML = `
    //     <div class="progress" role="progressbar" aria-valuenow="${itemsSoldPercent}" aria-valuemin="0" aria-valuemax="100">
    //         <div class="progress-bar progress-bar-striped progress-bar-animated overflow-visible text-dark" style="width: ${itemsSoldPercent}%">${itemsSoldPercent}%</div>
    //     </div>
    // `;
}

load_and_render_items();