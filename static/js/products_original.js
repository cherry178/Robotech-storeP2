// Simple products page script
console.log('Products loaded');

document.addEventListener('DOMContentLoaded', function() {
    initializeProductsPage();
});

let currentPage = 1;
let currentCategory = '';
let currentSearch = '';
let totalPages = 1;

function initializeProductsPage() {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    currentCategory = urlParams.get('category') || '';
    currentSearch = urlParams.get('search') || '';


    // Load products
    loadProducts();

    // Setup event listeners
    setupProductEventListeners();

    // Update active filter button
    updateActiveFilter();
}

function setupProductEventListeners() {
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

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            // Simple category extraction
            var category = this.textContent.toLowerCase().replace('all', '');
            if (category === '') {
                filterByCategory('');
            } else {
                filterByCategory(category);
            }
        });
    });

    // Sort select
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            loadProducts(); // Reload with new sorting
        });
    }

    // Pagination
    document.getElementById('prevBtn')?.addEventListener('click', () => changePage(currentPage - 1));
    document.getElementById('nextBtn')?.addEventListener('click', () => changePage(currentPage + 1));
}

function loadProducts() {
    const loadingContainer = document.getElementById('loadingContainer');
    const productsGrid = document.getElementById('productsGrid');
    const noResults = document.getElementById('noResults');

    if (!productsGrid) {
        console.error('Products grid element not found!');
        return;
    }

    // Show loading
    if (loadingContainer) {
        loadingContainer.style.display = 'block';
    }

    // Hide products grid initially
    productsGrid.style.display = 'none';
    noResults.style.display = 'none';

    // Build API URL
    let apiUrl = `/api/products?page=${currentPage}&limit=20`;

    if (currentCategory) {
        apiUrl += `&category=${encodeURIComponent(currentCategory)}`;
    }

    if (currentSearch) {
        apiUrl += `&search=${encodeURIComponent(currentSearch)}`;
    }

    // Add sorting
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect && sortSelect.value) {
        apiUrl += `&sort=${sortSelect.value}`;
    }

    console.log('🌐 Fetching products from:', apiUrl);

    fetch(apiUrl)
        .then(response => {
            console.log('📡 API response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('API data received:', {
                success: data.success,
                productsCount: data.products ? data.products.length : 0
            });

            // Hide loading
            if (loadingContainer) {
                loadingContainer.style.display = 'none';
                console.log('Loading container hidden');
            }

            if (data.success) {
                if (data.products && data.products.length > 0) {
                    displayProducts(data.products);

                    // Force visibility
                    productsGrid.style.display = 'grid';
                    productsGrid.style.visibility = 'visible';
                    productsGrid.style.opacity = '1';
                    console.log('✅ Products grid made visible');

                    // Update results count
                    const resultsCount = document.getElementById('resultsCount');
                    if (resultsCount) {
                        resultsCount.textContent = data.products.length;
                    }

                    // Setup pagination
                    if (data.total) {
                        totalPages = Math.ceil(data.total / 20);
                        updatePagination();
                    }
                } else {
                    console.log('⚠️ No products in API response');
                    noResults.style.display = 'block';
                }
            } else {
                console.error('❌ API returned error:', data.message);
                noResults.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('❌ Network error:', error);
            if (loadingContainer) {
                loadingContainer.style.display = 'none';
            }
            noResults.style.display = 'block';
        })
        .catch(error => {
            console.error('Fetch failed:', error);
            loadingContainer.style.display = 'none';
            noResults.style.display = 'block';
        });
}

function displayProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    const loadingContainer = document.getElementById('loadingContainer');

    if (!productsGrid) {
        return;
    }

    productsGrid.innerHTML = '';

    products.forEach((product, index) => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });

    // Force visibility with maximum CSS specificity
    productsGrid.style.cssText = 'display: grid !important; visibility: visible !important; opacity: 1 !important;';

    // Add a specific CSS rule to ensure visibility
    const style = document.createElement('style');
    style.textContent = `
        #productsGrid {
            display: grid !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        #productsGrid .product-card {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
    `;
    document.head.appendChild(style);

    console.log('✅ Products grid made visible with maximum CSS specificity');

}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in';

    let productImageHtml = '<div class="product-image" style="background: linear-gradient(135deg, ' + bgColor + ' 0%, ' + adjustColor(bgColor, -20) + ' 100%)">';

    productImageHtml += '<img src="' + (product.image_url || 'https://via.placeholder.com/200x150?text=No+Image') + '" alt="' + product.name + '" loading="lazy" class="product-image-element" onload="this.nextElementSibling.style.display=\'none\';" onerror="this.style.opacity=\'0.3\';" data-has-image="true">';

    productImageHtml += '<i class="fas fa-' + getCategoryIcon(product.category) + '" style="color: white; font-size: 3rem; opacity: 0.8;"></i>';

    // Generate a color based on category
    const colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502'];
    const colorIndex = product.category ? product.category.length % colors.length : 0;
    const bgColor = colors[colorIndex];

    // Check if product has sale pricing
    const hasSale = product.original_price && product.original_price > product.price;

    // Generate star rating HTML
    const ratingHtml = product.rating ? generateStarRating(product.rating, product.review_count) : '';

    let productImageHtml = '<div class="product-image" style="background: linear-gradient(135deg, ' + bgColor + ' 0%, ' + adjustColor(bgColor, -20) + ' 100%)">';

    // FORCE image creation for testing
    console.log('🔧 FORCE CREATING IMAGE for:', product.name, 'with URL:', product.image_url);
    productImageHtml += `<img src="${product.image_url || 'https://via.placeholder.com/200x150?text=No+Image'}" alt="${product.name}" loading="lazy" class="product-image-element" onload="console.log('✅ ${product.name} image loaded'); this.nextElementSibling.style.display='none';" onerror="console.log('❌ ${product.name} image failed'); this.style.opacity='0.3';" data-has-image="true">`;

    productImageHtml += `<i class="fas fa-${getCategoryIcon(product.category)}" style="color: white; font-size: 3rem; opacity: 0.8;"></i>`;

    if (product.is_featured) {
        productImageHtml += '<div class="product-badge">Sale</div>';
    }
    productImageHtml += '</div>';


    let fullCardHtml = productImageHtml;
    fullCardHtml += `
        <div class="product-content">
            <h3 class="product-title">${product.name}</h3>
            <p class="product-description">${product.description || 'High-quality electronics component'}</p>
            ${ratingHtml}
            <div class="product-price">
                ${hasSale ? `<span class="original-price">₹${product.original_price}</span>` : ''}
                ₹${product.price}
                <span class="gst-note">(Exc. GST)</span>
            </div>
            <div class="product-actions">
                <button class="btn btn-primary btn-small" onclick="addToCart(${product.id})">
                    <i class="fas fa-cart-plus"></i> Add to cart
                </button>
            </div>
        </div>
    `;

    card.innerHTML = fullCardHtml;

    return card;
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

function generateStarRating(rating, reviewCount) {
    if (!rating || rating < 0) return '';

    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    let starsHtml = '<div class="product-rating"><div class="stars">';

    // Full stars
    for (let i = 0; i < fullStars; i++) {
        starsHtml += '<i class="fas fa-star"></i>';
    }

    // Half star
    if (hasHalfStar) {
        starsHtml += '<i class="fas fa-star-half-alt"></i>';
    }

    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        starsHtml += '<i class="far fa-star"></i>';
    }

    starsHtml += '</div>';
    if (reviewCount && reviewCount > 0) {
        starsHtml += `<span class="rating-count">(${reviewCount})</span>`;
    }
    starsHtml += '</div>';

    return starsHtml;
}

function filterByCategory(category) {
    currentCategory = category;
    currentPage = 1;
    currentSearch = ''; // Clear search when filtering by category

    // Update URL
    const url = new URL(window.location);
    if (category) {
        url.searchParams.set('category', category);
        url.searchParams.delete('search');
    } else {
        url.searchParams.delete('category');
        url.searchParams.delete('search');
    }
    window.history.pushState({}, '', url);

    // Reload products
    loadProducts();

    // Update active filter button
    updateActiveFilter();
}

function performSearch(query) {
    if (!query.trim()) {
        showNotification('Please enter a search term', 'warning');
        return;
    }

    currentSearch = query.trim();
    currentCategory = ''; // Clear category when searching
    currentPage = 1;

    // Update URL
    const url = new URL(window.location);
    url.searchParams.set('search', currentSearch);
    url.searchParams.delete('category');
    window.history.pushState({}, '', url);

    // Reload products
    loadProducts();
}

function updateActiveFilter() {
    // Remove active class from all filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to current filter
    const activeBtn = document.querySelector(`.filter-btn[onclick*="'${currentCategory}'"]`) ||
                     document.querySelector('.filter-btn:first-child');
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

function changePage(page) {
    if (page < 1 || page > totalPages) return;

    currentPage = page;
    loadProducts();

    // Scroll to top of products
    document.querySelector('.products-page').scrollIntoView({ behavior: 'smooth' });
}

function updatePagination() {
    const pagination = document.getElementById('pagination');
    const pageNumbers = document.getElementById('pageNumbers');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (totalPages <= 1) {
        pagination.style.display = 'none';
        return;
    }

    pagination.style.display = 'flex';

    // Update prev/next buttons
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= totalPages;

    // Generate page numbers
    pageNumbers.innerHTML = '';

    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.className = `page-btn ${i === currentPage ? 'active' : ''}`;
        pageBtn.textContent = i;
        pageBtn.onclick = () => changePage(i);
        pageNumbers.appendChild(pageBtn);
    }
}

// Add CSS for products page
const productStyle = document.createElement('style');
productStyle.textContent = `
    .breadcrumb {
        margin-bottom: 2rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }

    .breadcrumb a {
        color: var(--primary-color);
        text-decoration: none;
    }

    .breadcrumb a:hover {
        text-decoration: underline;
    }

    .page-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .page-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
    }

    .products-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: var(--bg-gray);
        border-radius: var(--border-radius-md);
    }

    .filter-buttons {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .filter-btn {
        padding: 0.5rem 1rem;
        border: 1px solid #e2e8f0;
        background: white;
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }

    .filter-btn:hover,
    .filter-btn.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    .sort-select {
        padding: 0.5rem 1rem;
        border: 1px solid #e2e8f0;
        border-radius: var(--border-radius-sm);
        background: white;
        font-size: 0.875rem;
        cursor: pointer;
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        text-align: center;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #e2e8f0;
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .no-results {
        text-align: center;
        padding: 4rem 2rem;
    }

    .no-results i {
        font-size: 4rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }

    .no-results h3 {
        font-size: 1.5rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .no-results p {
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-top: 3rem;
        padding: 2rem 0;
    }

    .page-btn {
        padding: 0.75rem 1rem;
        border: 1px solid #e2e8f0;
        background: white;
        color: var(--text-primary);
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .page-btn:hover:not(:disabled) {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    .page-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .page-btn.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    .page-numbers {
        display: flex;
        gap: 0.5rem;
    }

    .product-rating {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }

    .stars {
        display: flex;
        gap: 0.125rem;
    }

    .stars i {
        color: #ffc107;
        font-size: 0.875rem;
    }

    .stars .far {
        color: #e0e0e0;
    }

    .rating-count {
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .product-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: var(--border-radius-md);
    }

    @media (max-width: 768px) {
        .products-controls {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
        }

        .filter-buttons {
            justify-content: center;
        }

        .page-title {
            font-size: 2rem;
        }

        .pagination {
            flex-wrap: wrap;
        }
    }
`;
document.head.appendChild(productStyle);

