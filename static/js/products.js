// Products page script
console.log('Products.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    initializeProductsPage();
});

let currentPage = 1;
let currentCategory = '';
let currentSearch = '';
let totalPages = 1;

function initializeProductsPage() {
    const urlParams = new URLSearchParams(window.location.search);
    currentCategory = urlParams.get('category') || '';
    currentSearch = urlParams.get('search') || '';

    loadProducts();
    setupProductEventListeners();
    updateActiveFilter();
}

function setupProductEventListeners() {
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

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            var category = this.textContent.toLowerCase().replace('all', '').trim();
            filterByCategory(category);
        });
    });

    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', loadProducts);
    }
}

function loadProducts() {
    const productsGrid = document.getElementById('productsGrid');
    const loadingContainer = document.getElementById('loadingContainer');
    const noResults = document.getElementById('noResults');

    if (!productsGrid) return;

    if (loadingContainer) loadingContainer.style.display = 'block';
    productsGrid.style.display = 'none';
    noResults.style.display = 'none';

    let apiUrl = 'http://127.0.0.1:8888/api/products?page=' + currentPage + '&limit=12';

    if (currentCategory) apiUrl += '&category=' + encodeURIComponent(currentCategory);
    if (currentSearch) apiUrl += '&search=' + encodeURIComponent(currentSearch);

    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect && sortSelect.value) apiUrl += '&sort=' + sortSelect.value;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log('🔍 RAW API RESPONSE:', JSON.stringify(data, null, 2));
            
            if (data.products && data.products.length > 0) {
                console.log('🔍 FIRST PRODUCT DETAILS:', JSON.stringify(data.products[0], null, 2));
                console.log('🔍 ALL PRODUCT IDs:', data.products.map(p => ({id: p.id, name: p.name})));
            }

            if (loadingContainer) loadingContainer.style.display = 'none';

            if (data.success && data.products && data.products.length > 0) {
                displayProducts(data.products);
                productsGrid.style.display = 'grid';

                const resultsCount = document.getElementById('resultsCount');
                if (resultsCount) resultsCount.textContent = data.products.length;

                if (data.total) {
                    totalPages = Math.ceil(data.total / 12);
                    console.log('Total products:', data.total, 'Total pages:', totalPages, 'Current page:', currentPage);
                    updatePagination();
                }

                // Force show pagination multiple times
                const showPagination = () => {
                    const pagination = document.getElementById('pagination');
                    if (pagination) {
                        pagination.style.display = 'flex';
                        pagination.style.visibility = 'visible';
                        pagination.style.opacity = '1';
                        pagination.style.position = 'relative';
                        pagination.style.border = '2px solid blue';
                        console.log('Forced pagination to show');
                    }
                };

                setTimeout(() => {
                    showPagination();
                    // Add a big visible indicator
                    const indicator = document.createElement('div');
                    indicator.id = 'pagination-indicator';
                    indicator.style.cssText = 'position: fixed; bottom: 20px; left: 20px; background: red; color: white; padding: 10px; border-radius: 5px; font-size: 16px; font-weight: bold; z-index: 9999;';
                    indicator.textContent = '🔍 LOOK FOR PAGINATION BELOW!';
                    document.body.appendChild(indicator);
                    setTimeout(() => document.body.removeChild(indicator), 5000);
                }, 500);
                setTimeout(showPagination, 1000);
                setTimeout(showPagination, 2000);
            } else {
                noResults.style.display = 'block';
            }
        })
        .catch(() => {
            if (loadingContainer) loadingContainer.style.display = 'none';
            noResults.style.display = 'block';
        });
}

function displayProducts(products) {
    console.log('displayProducts called with', products.length, 'products');
    alert('Loading ' + products.length + ' products. First product: ID ' + products[0].id + ' - ' + products[0].name);
    const productsGrid = document.getElementById('productsGrid');
    if (!productsGrid) {
        console.error('productsGrid not found!');
        return;
    }

    productsGrid.innerHTML = '';
    console.log('Cleared products grid');

    console.log('🔍 FULL PRODUCTS ARRAY RECEIVED:', products);
    products.forEach((product, index) => {
        console.log(`📦 Card ${index + 1}: ID=${product.id} Name="${product.name}"`);
        const card = createProductCard(product);
        productsGrid.appendChild(card);
    });

    console.log('Added', products.length, 'product cards to grid');
    console.log('Grid children count:', productsGrid.children.length);

    // Force visibility
    productsGrid.style.display = 'grid';
    productsGrid.style.visibility = 'visible';
    productsGrid.style.opacity = '1';
}

function createProductCard(product) {
    console.log('🎴 createProductCard called with:', JSON.stringify(product, null, 2));
    console.log('🎴 Product ID:', product.id, 'Type:', typeof product.id);
    console.log('🎴 Product Name:', product.name);
    
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
    html += '<div style="background: red; color: white; padding: 2px 5px; font-size: 10px; display: inline-block; margin-bottom: 5px;">ID: ' + product.id + '</div>';
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
    // Store product ID in data attribute for debugging
    html += '<button class="btn btn-primary btn-small" data-product-id="' + product.id + '" data-product-name="' + product.name.replace(/'/g, "\\'") + '" onclick="var btn = this; var productId = parseInt(btn.getAttribute(\'data-product-id\')); var productName = btn.getAttribute(\'data-product-name\'); console.log(\'🛒 BUTTON CLICKED: data-product-id=\' + productId + \', data-product-name=\' + productName); alert(\'Adding to cart: ID \' + productId + \' - \' + productName); addToCart(productId)">';
    html += '<i class="fas fa-cart-plus"></i> Add to cart';
    html += '</button>';
    html += '</div>';
    html += '</div>';

    console.log('🎴 Generated HTML button onclick will use product.id =', product.id);
    card.innerHTML = html;
    
    // Verify the button after creation
    const button = card.querySelector('button');
    if (button) {
        const dataId = button.getAttribute('data-product-id');
        console.log('🎴 Button created with data-product-id:', dataId);
    }
    
    return card;
}function getCategoryIcon(category) {
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
    currentPage = 1;
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
    updateActiveFilter();
}

function performSearch(query) {
    if (!query.trim()) return;

    currentSearch = query.trim();
    currentCategory = '';
    currentPage = 1;

    const url = new URL(window.location);
    url.searchParams.set('search', currentSearch);
    url.searchParams.delete('category');
    window.history.pushState({}, '', url);

    loadProducts();
}

function updateActiveFilter() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    const activeBtn = document.querySelector('.filter-btn:first-child');
    if (activeBtn) activeBtn.classList.add('active');
}

function updatePagination() {
    console.log('updatePagination called, totalPages:', totalPages, 'currentPage:', currentPage);
    const pagination = document.getElementById('pagination');
    const pageNumbers = document.getElementById('pageNumbers');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    console.log('Pagination elements found:', { pagination: !!pagination, pageNumbers: !!pageNumbers, prevBtn: !!prevBtn, nextBtn: !!nextBtn });

    // Always show pagination since we have 6 pages
    if (pagination) {
        pagination.style.display = 'flex';
        pagination.style.visibility = 'visible';
        console.log('Pagination made visible');
    }

    if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
        console.log('Prev button disabled:', prevBtn.disabled);
    }
    if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
        console.log('Next button disabled:', nextBtn.disabled);
    }

    if (pageNumbers) {
        pageNumbers.innerHTML = '';

        // Show all pages for simplicity: 1, 2, 3, 4, 5, 6
        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = 'page-btn' + (i === currentPage ? ' active' : '');
            pageBtn.textContent = i;
            pageBtn.onclick = () => changePage(i);
            pageNumbers.appendChild(pageBtn);
        }

        console.log('Created', totalPages, 'page buttons');
    }

    if (prevBtn) prevBtn.disabled = currentPage <= 1;
    if (nextBtn) nextBtn.disabled = currentPage >= totalPages;

    if (pageNumbers) {
        pageNumbers.innerHTML = '';

        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = 'page-btn ' + (i === currentPage ? 'active' : '');
            pageBtn.textContent = i;
            pageBtn.onclick = () => changePage(i);
            pageNumbers.appendChild(pageBtn);
        }
    }
}

function changePage(page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    loadProducts();
    document.querySelector('.products-page').scrollIntoView({ behavior: 'smooth' });
}


