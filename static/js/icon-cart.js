let iconCart = document.querySelector('.icon-cart');
let iconCartSpan = document.querySelector('.icon-cart span');
let closeCart = document.querySelector('.close');
let body = document.querySelector('body');

iconCart.addEventListener('click', function () {
    body.classList.add('showCart');
})

closeCart.addEventListener('click', function () {
    body.classList.toggle('showCart');
})