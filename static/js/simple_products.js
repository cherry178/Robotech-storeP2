console.log('Simple products loaded');

document.addEventListener('DOMContentLoaded', function() {
    loadAllProducts();
});

function loadAllProducts() {
    fetch('http://127.0.0.1:8888/api/products?limit=50')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.products) {
                displayProducts(data.products);
            }
        });
}

function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card fade-in';

        const colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502'];
        const colorIndex = product.category ? product.category.length % colors.length : 0;
        const bgColor = colors[colorIndex];

        const hasSale = product.original_price && product.original_price > product.price;

        let html = '<div class="product-image" style="background: linear-gradient(135deg, ' + bgColor + ' 0%, ' + adjustColor(bgColor, -20) + ' 100%)">';

        if (product.image_url) {
            html += '<img src="' + product.image_url + '" alt="' + product.name + '" loading="lazy" class="product-image-element" onload="this.nextElementSibling.style.display=\'none\';" onerror="this.style.opacity=\'0.3\';" data-has-image="true">';
        }

        html += '<i class="fas fa-' + getCategoryIcon(product.category) + '" style="color: white; font-size: 3rem; opacity: 0.8;"></i>';

        if (product.is_featured) {
            html += '<div class="product-badge">Sale</div>';
        }
        html += '</div>';

        html += '<div class="product-content">';
        html += '<h3 class="product-title">' + product.name + '</h3>';
        html += '<p class="product-description">' + (product.description || 'High-quality electronics component') + '</p>';

        if (hasSale) {
            html += '<div class="product-price">';
            html += '<span class="original-price">Rs ' + product.original_price + '</span>';
            html += 'Rs ' + product.price;
            html += '<span class="gst-note">(Exc. GST)</span>';
            html += '</div>';
        } else {
            html += '<div class="product-price">Rs ' + product.price + '<span class="gst-note">(Exc. GST)</span></div>';
        }

        html += '<div class="product-actions">';
        html += '<button class="btn btn-primary btn-small" onclick="addToCart(' + product.id + ')">';
        html += '<i class="fas fa-cart-plus"></i> Add to cart';
        html += '</button>';
        html += '</div>';
        html += '</div>';

        card.innerHTML = html;
        grid.appendChild(card);
    });
    
    grid.style.display = 'grid';
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
