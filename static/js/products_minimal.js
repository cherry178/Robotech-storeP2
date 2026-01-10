// Products page JavaScript - Complete functionality with images
console.log('Products loaded');

document.addEventListener('DOMContentLoaded', function() {
    initializeProductsPage();
});

let currentCategory = '';
let currentSearch = '';

function initializeProductsPage() {
    const urlParams = new URLSearchParams(window.location.search);
    currentCategory = urlParams.get('category') || '';
    currentSearch = urlParams.get('search') || '';

    loadProducts();
    setupEventListeners();
}

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.querySelector('.search-btn');

    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch(this.value);
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', () => performSearch(searchInput.value));
    }

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.textContent.toLowerCase().replace('all', '').trim();
            filterByCategory(category);
        });
    });
}

function loadProducts() {
    const grid = document.getElementById('productsGrid');
    const loading = document.getElementById('loadingContainer');
    const noResults = document.getElementById('noResults');

    if (!grid) return;

    if (loading) loading.style.display = 'block';
    grid.style.display = 'none';
    if (noResults) noResults.style.display = 'none';

    let url = 'http://127.0.0.1:8888/api/products?limit=20';
    if (currentCategory) {
        url += '&category=' + encodeURIComponent(currentCategory);
    }
    if (currentSearch) {
        url += '&search=' + encodeURIComponent(currentSearch);
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (loading) loading.style.display = 'none';

            if (data.success && data.products && data.products.length > 0) {
                displayProducts(data.products);
                grid.style.display = 'grid';

                const resultsCount = document.getElementById('resultsCount');
                if (resultsCount) resultsCount.textContent = data.products.length;
            } else {
                if (noResults) noResults.style.display = 'block';
            }
        })
        .catch(() => {
            if (loading) loading.style.display = 'none';
            if (noResults) noResults.style.display = 'block';
        });
}

function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card fade-in';

        // Generate color based on category
        const colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502'];
        const colorIndex = product.category ? product.category.length % colors.length : 0;
        const bgColor = colors[colorIndex];

        const hasSale = product.original_price && product.original_price > product.price;

        let html = '<div class="product-image" style="background: linear-gradient(135deg, ' + bgColor + ' 0%, ' + adjustColor(bgColor, -20) + ' 100%)">';

        // ADD IMAGE IF AVAILABLE
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

function filterByCategory(category) {
    currentCategory = category;
    currentSearch = '';

    const url = new URL(window.location);
    if (category) {
        url.searchParams.set('category', category);
        url.searchParams.delete('search');
    } else {
        url.searchParams.delete('category');
        url.searchParams.delete('search');
    }
    window.history.pushState({}, '', url);

    loadProducts();
}

function performSearch(query) {
    if (!query.trim()) return;

    currentSearch = query.trim();
    currentCategory = '';

    const url = new URL(window.location);
    url.searchParams.set('search', currentSearch);
    url.searchParams.delete('category');
    window.history.pushState({}, '', url);

    loadProducts();
}
