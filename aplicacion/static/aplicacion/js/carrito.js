let cartItems = [];

function toggleCart() {
    const cart = document.getElementById("shoppingCart");
    cart.classList.toggle("open");
}

function addToCart(image, name, artist, price) {
    const existingItem = cartItems.find((item) => item.name === name);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cartItems.push({
            image,
            name,
            artist,
            price,
            quantity: 1,
        });
    }

    updateCartDisplay();
    toggleCart(); // Mostrar el carrito cuando se agrega un producto
}

function updateCartDisplay() {
    const cartBody = document.getElementById("cartBody");
    cartBody.innerHTML = ""; // Limpiar el contenido anterior

    cartItems.forEach((item) => {
        const cartItem = document.createElement("div");
        cartItem.className = "cart-item";

        cartItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" style="width: 120px; height: 120px; object-fit: cover; margin-right: 10px;">
            <div>
                <button class="btn btn-sm btn-outline-secondary" onclick="decreaseQuantity('${item.name}')">-</button>
                <span>${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="increaseQuantity('${item.name}')">+</button>
                <button class="btn btn-danger btn-sm" onclick="removeFromCart('${item.name}')">Eliminar</button>
            </div>
            <div>
                <p>$${item.price.toFixed(2)}</p>
            </div>
        `;

        cartBody.appendChild(cartItem);
    });

    updateCartTotal(); // Actualizar el total después de cada cambio
}

function updateCartTotal() {
    const cartTotalElement = document.getElementById("cartTotal").querySelector("p:last-child");
    const total = cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);
    cartTotalElement.textContent = `$${total.toFixed(2)}`;
}

function increaseQuantity(name) {
    const item = cartItems.find((i) => i.name === name);
    if (item) {
        item.quantity++;
        updateCartDisplay();
    }
}

function decreaseQuantity(name) {
    const item = cartItems.find((i) => i.name === name);
    if (item && item.quantity > 1) {
        item.quantity--;
        updateCartDisplay();
    } else if (item && item.quantity === 1) {
        removeFromCart(name);
    }
}

function removeFromCart(name) {
    cartItems = cartItems.filter((item) => item.name !== name);
    updateCartDisplay();
}

function checkout() {
    if (cartItems.length > 0) { // Comprobar si el carrito no está vacío
        window.location.href = "/usuario/checkout/"; // Redirige al usuario a la página de pago
    } else {
        // Puedes mostrar un mensaje de advertencia o indicar que el carrito está vacío
        alert("El carrito está vacío. Por favor, añade elementos antes de realizar la compra.");
    }
}
