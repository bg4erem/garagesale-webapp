/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function render_photos_carousel(photos_array) {
    const carouselInner = document.getElementById("carousel-inner");

    for (let i=0; i < photos_array.length; i++) {
        let carouselItem = document.createElement("div");
        if (i ===0 ) {
            carouselItem.className = "carousel-item active";
        } else {
            carouselItem.className = "carousel-item";
        }
        carouselItem.innerHTML = `<img src="${photos_array[i]}" class="d-block w-100">`;

        carouselInner.appendChild(carouselItem);
    }
}

async function render_details() {
    let item_id = window.location.href.split("/").at(-1);

    let item = await fetch(`/api/v1/items?id=${item_id}`, {credentials: "same-origin"}).then(resp => {return resp.json()});
    document.getElementById("page-title").textContent = item.title
    
    const productSection = document.getElementById("product-section");
    let itemPriceHTML = `<span>${item.price} ${item.price_curr}</span>`;
    if (item.full_price) { 
        itemPriceHTML = `
            <span class="text-decoration-line-through">${item.full_price} ${item.price_curr}</span>
            <span>${item.price} ${item.price_curr}</span>
        `;
    }
    productSection.innerHTML = `
        <div class="container px-4 px-lg-5 my-5">
            <div class="row gx-4 gx-lg-5 align-items-center">
                <div class="col-md-6">
                    <div id="carouselExample" class="carousel slide">
                        <div class="carousel-inner" id="carousel-inner">
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="small mb-1">ID: ${item['_id']}</div>
                    <div class="small mb-1">Просмотров: ${item.views_all}</div>
                    <h1 class="display-5 fw-bolder">${item.title}</h1>
                    <div class="fs-5 mb-5">
                        ${itemPriceHTML}
                    </div>
                    <p class="lead">${item.description}</p>
                    <div class="d-flex">
                        <a class="btn btn-outline-dark flex-shrink-0" type="button" target="_blank" href="tg://resolve?domain=${TELEGRAM_USERNAME}">
                            <i class="bi bi-telegram"></i>
                            Telegram
                        </a>
                    </div>
                    <div class="d-flex">
                        <a class="btn btn-outline-dark flex-shrink-0" type="button" target="_blank" href="https://wa.me/${WHATSAPP_NUMBER}?text=${window.location.href}">
                            <i class="bi bi-whatsapp"></i>
                            Whatsapp
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;

    render_photos_carousel(item.photos);

    const carousel = new bootstrap.Carousel('#carouselExample');
}

render_details()