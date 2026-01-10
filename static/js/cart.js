// Cart page JavaScript for Robotech Store
console.log('🛒 Cart.js loaded and ready');

document.addEventListener('DOMContentLoaded', function() {
    initializeCartPage();
});

function initializeCartPage() {
    loadCartItems();
    setupCartEventListeners();
}

function setupCartEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.querySelector('.search-btn');

    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }

    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => performSearch(searchInput.value));
    }
}

function loadCartItems() {
    console.log('🛒 loadCartItems called');

    // Don't run on cart page - it has its own cart loading logic
    if (window.location.pathname.includes('cart') || document.querySelector('#cartContent')) {
        console.log('🛒 Skipping cart.js loadCartItems - cart page has its own logic');
        return;
    }

    // Since login is mandatory, all users accessing cart will be authenticated
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    const loggedIn = sessionStorage.getItem('logged_in') || localStorage.getItem('logged_in');
    console.log('Loading cart for authenticated user:', userId, 'loggedIn:', loggedIn);

    if (userId && loggedIn === 'true') {
        console.log('✅ User is logged in, loading cart for user:', userId);
        loadAuthenticatedCartItems(userId);
    } else {
        console.error('❌ No valid user session found - userId:', userId, 'loggedIn:', loggedIn);
        showEmptyCart();
    }
}

function loadAuthenticatedCartItems(userId) {
    console.log('Loading authenticated cart for user:', userId, 'via backend API');

    // Use backend API to get cart items with product details
    fetch(`http://127.0.0.1:8888/api/cart?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            console.log('Cart API response:', data);

            if (data.success && data.cart) {
                const cartItems = data.cart;
                console.log('Loaded cart items from backend:', cartItems);

                if (cartItems.length > 0) {
                    displayCartItems(cartItems);
                    updateCartSummary(cartItems);
                    showCartContent();
                } else {
                    showEmptyCart();
                }
            } else {
                console.error('Failed to load cart from backend:', data);
                showEmptyCart();
            }
        })
        .catch(error => {
            console.error('Error loading cart from backend:', error);
            showEmptyCart();
        });
}

function showCartContent() {
    const cartItems = document.getElementById('cartItems');
    const cartSummary = document.getElementById('cartSummary');
    const emptyCart = document.getElementById('emptyCart');

    cartItems.style.display = 'block';
    cartSummary.style.display = 'block';
    emptyCart.style.display = 'none';
}

function displayCartItems(cartItems) {
    const cartContainer = document.getElementById('cartItems');
    if (!cartContainer) {
        console.error('cartContainer not found!');
        return;
    }

    cartContainer.innerHTML = '';

    cartItems.forEach(item => {
        const cartItem = createCartItem(item);
        cartContainer.appendChild(cartItem);
    });
}

function createCartItem(item) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'cart-item';

    // Generate a color based on category
    const colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502'];
    const colorIndex = item.category ? item.category.length % colors.length : 0;
    const bgColor = colors[colorIndex];

    const imageHtml = item.image_url
        ? `<img src="${item.image_url}" alt="${item.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" data-has-image="true">`
        : '';

    const iconHtml = item.image_url
        ? `<i class="fas fa-${getCategoryIcon(item.category)}" style="display: none;"></i>`
        : `<i class="fas fa-${getCategoryIcon(item.category)}"></i>`;

    // Check if product has sale pricing
    const hasSale = item.original_price && item.original_price > item.price;
    const itemTotal = item.price * item.quantity;

    itemDiv.innerHTML = `
        <div class="cart-item-content">
            <div class="cart-item-image" style="background: linear-gradient(135deg, ${bgColor} 0%, ${adjustColor(bgColor, -20)} 100%)">
                ${imageHtml}
                ${iconHtml}
            </div>
            <div class="cart-item-details">
                <h3 class="cart-item-title">${item.name}</h3>
                <p class="cart-item-description">${item.description || 'High-quality electronics component'}</p>
                <div class="cart-item-price">
                    ${hasSale ? `<span class="original-price">₹${item.original_price}</span>` : ''}
                    ₹${item.price}
                    <span class="gst-note">(Exc. GST)</span>
                </div>
            </div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" onclick="updateQuantity(${item.product_id}, ${item.quantity - 1})">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="quantity-btn" onclick="updateQuantity(${item.product_id}, ${item.quantity + 1})">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <div class="cart-item-total">
                ₹${itemTotal.toFixed(2)}
            </div>
            <div class="cart-item-remove">
                <button class="remove-btn" onclick="removeFromCart(${item.product_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;

    return itemDiv;
}

function updateQuantity(productId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(productId);
        return;
    }

    // Use backend API to update cart
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    console.log('Updating quantity via backend API for user:', userId, 'product:', productId, 'quantity:', newQuantity);

    if (userId) {
        fetch('http://127.0.0.1:8888/api/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                product_id: productId,
                quantity: newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Quantity updated!', 'success');
                loadCartItems(); // Reload cart from backend
                updateCartCount(); // Update cart count in header
            } else {
                showNotification('Failed to update quantity', 'error');
            }
        })
        .catch(error => {
            console.error('Error updating quantity:', error);
            showNotification('Network error - please try again', 'error');
        });
    } else {
        console.error('No user ID found for quantity update');
        showNotification('Please login to update cart', 'error');
    }
}

function removeFromCart(productId) {
    // Use backend API to remove item from cart
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    console.log('Removing item from cart via backend API for user:', userId, 'product:', productId);

    if (userId) {
        fetch('http://127.0.0.1:8888/api/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                product_id: productId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Item removed from cart!', 'success');
                loadCartItems(); // Reload cart from backend
                updateCartCount(); // Update cart count in header
            } else {
                showNotification('Failed to remove item', 'error');
            }
        })
        .catch(error => {
            console.error('Error removing item:', error);
            showNotification('Network error - please try again', 'error');
        });
    } else {
        console.error('No user ID found for cart removal');
        showNotification('Please login to modify cart', 'error');
    }
}

function updateCartSummary(cartItems) {
    let subtotal = 0;

    cartItems.forEach(item => {
        subtotal += item.price * item.quantity;
    });

    const gst = subtotal * 0.18; // 18% GST
    const total = subtotal + gst;

    document.getElementById('subtotal').textContent = `₹${subtotal.toFixed(2)}`;
    document.getElementById('gst').textContent = `₹${gst.toFixed(2)}`;
    document.getElementById('total').textContent = `₹${total.toFixed(2)}`;
}

function showEmptyCart() {
    const cartItems = document.getElementById('cartItems');
    const emptyCart = document.getElementById('emptyCart');
    const cartSummary = document.getElementById('cartSummary');

    cartItems.style.display = 'none';
    cartSummary.style.display = 'none';
    emptyCart.style.display = 'block';
}

async function proceedToCheckout() {
    // Check if user is logged in by checking storage
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    const isLoggedIn = (sessionStorage.getItem('logged_in') === 'true') ||
                      (localStorage.getItem('logged_in') === 'true') ||
                      (userId && parseInt(userId) > 0);

    console.log('Checkout check - userId:', userId, 'isLoggedIn:', isLoggedIn);

    // User must be logged in to checkout
    if (!userId || !isLoggedIn) {
        showNotification('Please login to proceed to checkout', 'error');
        // Redirect to home page for login flow
        window.location.href = '/';
        return;
    }

    // Check if cart has items from the backend API
    try {
        const response = await fetch(`http://127.0.0.1:8888/api/cart?user_id=${userId}`);
        const data = await response.json();
        
        if (!data.success || !data.cart || data.cart.length === 0) {
            showNotification('Your cart is empty. Add some items first.', 'warning');
            return;
        }
        
        // Cart has items, proceed to payment
        window.location.href = '/payment';
    } catch (error) {
        console.error('Error checking cart:', error);
        // If API fails, try to proceed anyway
        window.location.href = '/payment';
    }
}

function buyNowFromCart() {
    console.log('Buy Now from cart clicked');

    // Check if user is logged in by checking storage
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    const isLoggedIn = (sessionStorage.getItem('logged_in') === 'true') ||
                      (localStorage.getItem('logged_in') === 'true');

    console.log('Buy Now check - userId:', userId, 'isLoggedIn:', isLoggedIn);

    if (!isLoggedIn || !userId) {
        showNotification('Please login to purchase items', 'error');
        // Redirect to home page for login flow
        window.location.href = 'index.html';
        return;
    }

    // Check if cart has items
    const cartData = localStorage.getItem('demo_cart_' + userId);

    if (!cartData || JSON.parse(cartData).length === 0) {
        showNotification('Your cart is empty. Add some items first.', 'warning');
        return;
    }

    // Show success message and redirect to payment
    showNotification('Processing your order...', 'success');
    setTimeout(() => {
        window.location.href = 'payment.html';
    }, 1000);
}

function performSearch(query) {
    if (!query.trim()) {
        showNotification('Please enter a search term', 'warning');
        return;
    }

    window.location.href = `/products?search=${encodeURIComponent(query.trim())}`;
}

function getCategoryIcon(category) {
    const icons = {
        'Sensors': 'eye',
        'Microcontrollers': 'microchip',
        'Actuators': 'cogs',
        'Communication': 'wifi',
        'Power Supply': 'bolt',
        'Displays': 'tv',
        'Tools & Accessories': 'tools'
    };
    return icons[category] || 'cube';
}

function adjustColor(color, amount) {
    // Simple color adjustment function
    const usePound = color[0] === '#';
    const col = usePound ? color.slice(1) : color;

    const num = parseInt(col, 16);
    let r = (num >> 16) + amount;
    let g = (num >> 8 & 0x00FF) + amount;
    let b = (num & 0x0000FF) + amount;

    r = r > 255 ? 255 : r < 0 ? 0 : r;
    g = g > 255 ? 255 : g < 0 ? 0 : g;
    b = b > 255 ? 255 : g < 0 ? 0 : b;

    return (usePound ? '#' : '') + (r << 16 | g << 8 | b).toString(16);
}

// Add CSS for cart page
const cartStyle = document.createElement('style');
cartStyle.textContent = `
    .cart-section {
        padding: 4rem 0;
        min-height: 60vh;
    }

    .cart-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .cart-content {
        display: grid;
        grid-template-columns: 1fr 350px;
        gap: 2rem;
        align-items: start;
    }

    .cart-items {
        background: white;
        border-radius: var(--border-radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }

    .cart-item {
        border-bottom: 1px solid #e2e8f0;
    }

    .cart-item:last-child {
        border-bottom: none;
    }

    .cart-item-content {
        display: grid;
        grid-template-columns: 100px 1fr auto auto auto;
        gap: 1rem;
        padding: 1.5rem;
        align-items: center;
    }

    .cart-item-image {
        width: 80px;
        height: 80px;
        border-radius: var(--border-radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .cart-item-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: var(--border-radius-md);
    }

    .cart-item-details {
        flex: 1;
    }

    .cart-item-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .cart-item-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .cart-item-price {
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary-color);
    }

    .cart-item-quantity {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .quantity-btn {
        width: 30px;
        height: 30px;
        border: 1px solid #e2e8f0;
        background: white;
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .quantity-btn:hover {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    .quantity-value {
        font-weight: 600;
        min-width: 30px;
        text-align: center;
    }

    .cart-item-total {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-primary);
        min-width: 80px;
        text-align: right;
    }

    .cart-item-remove {
        min-width: 40px;
    }

    .remove-btn {
        width: 35px;
        height: 35px;
        border: none;
        background: #fee2e2;
        color: #dc2626;
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .remove-btn:hover {
        background: #dc2626;
        color: white;
    }

    .empty-cart {
        grid-column: 1 / -1;
        text-align: center;
        padding: 4rem 2rem;
    }

    .empty-cart-content {
        max-width: 400px;
        margin: 0 auto;
    }

    .empty-cart i {
        font-size: 4rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }

    .empty-cart h3 {
        font-size: 1.5rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .empty-cart p {
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }

    .cart-summary {
        background: white;
        border-radius: var(--border-radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        position: sticky;
        top: 2rem;
    }

    .summary-card h3 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
    }

    .summary-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        font-size: 1rem;
    }

    .summary-row.total {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 1rem 0;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }

    .summary-row span:first-child {
        color: var(--text-secondary);
    }

    .summary-row span:last-child {
        font-weight: 600;
    }

    .btn-large {
        width: 100%;
        padding: 1rem;
        font-size: 1.125rem;
        margin-bottom: 1rem;
    }

    @media (max-width: 1024px) {
        .cart-content {
            grid-template-columns: 1fr;
            gap: 2rem;
        }

        .cart-summary {
            position: static;
            order: -1;
        }
    }

    @media (max-width: 768px) {
        .cart-item-content {
            grid-template-columns: 80px 1fr;
            gap: 1rem;
        }

        .cart-item-quantity,
        .cart-item-total,
        .cart-item-remove {
            grid-column: span 1;
            justify-self: center;
        }

        .cart-item-quantity {
            order: 1;
        }

        .cart-item-total {
            order: 2;
        }

        .cart-item-remove {
            order: 3;
        }
    }
`;
// Guest cart helper functions
function updateAuthenticatedCartItem(userId, productId, quantity) {
    const productIdNum = parseInt(productId, 10);
    console.log('Updating authenticated cart for user:', userId, 'item:', productIdNum, 'to quantity:', quantity);

    try {
        const cartData = localStorage.getItem('demo_cart_' + userId);
        let cart = cartData ? JSON.parse(cartData) : [];
        const itemIndex = cart.findIndex(item => item.product_id === productIdNum);

        if (itemIndex !== -1) {
            if (quantity <= 0) {
                cart.splice(itemIndex, 1);
                console.log('Removed item from authenticated cart');
            } else {
                cart[itemIndex].quantity = quantity;
                console.log('Updated item quantity in authenticated cart');
            }
            localStorage.setItem('demo_cart_' + userId, JSON.stringify(cart));
            console.log('Updated authenticated cart:', cart);
        }
    } catch (error) {
        console.error('Error updating authenticated cart:', error);
    }
}

function updateAuthenticatedCartItem(userId, productId, quantity) {
    const productIdNum = parseInt(productId, 10);
    console.log('Updating authenticated cart for user:', userId, 'item:', productIdNum, 'to quantity:', quantity);

    try {
        const cartData = localStorage.getItem('demo_cart_' + userId);
        let cart = cartData ? JSON.parse(cartData) : [];
        const itemIndex = cart.findIndex(item => item.product_id === productIdNum);

        if (itemIndex !== -1) {
            if (quantity <= 0) {
                cart.splice(itemIndex, 1);
                console.log('Removed item from authenticated cart');
            } else {
                cart[itemIndex].quantity = quantity;
                console.log('Updated item quantity in authenticated cart');
            }
            localStorage.setItem('demo_cart_' + userId, JSON.stringify(cart));
            console.log('Updated authenticated cart:', cart);
        }
    } catch (error) {
        console.error('Error updating authenticated cart:', error);
    }
}

// Function to refresh cart display (call this when cart page loads)
function refreshCartDisplay() {
    console.log('🔄 Refreshing cart display');
    loadCartItems();
}


document.head.appendChild(cartStyle);
