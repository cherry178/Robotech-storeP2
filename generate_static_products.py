#!/usr/bin/env python3

import json
import math

# Read the DEMO_PRODUCTS from app.py
with open('backend/app.py', 'r') as f:
    content = f.read()

# Extract DEMO_PRODUCTS
start = content.find('DEMO_PRODUCTS = [')
# Find the matching closing bracket by counting brackets
bracket_count = 0
end = start
for i, char in enumerate(content[start:], start):
    if char == '[':
        bracket_count += 1
    elif char == ']':
        bracket_count -= 1
        if bracket_count == 0:
            end = i + 1
            break

demo_products_str = content[start:end]

# Parse the products list manually since exec() can be tricky
import ast
try:
    # Try to evaluate the list
    products = ast.literal_eval(demo_products_str.split('=', 1)[1].strip())
except:
    # Fallback: extract products one by one
    products = []
    lines = demo_products_str.split('\n')
    i = 0
    while i < len(lines):
        if '{' in lines[i] and '"id"' in lines[i]:
            product = {}
            while i < len(lines) and '}' not in lines[i]:
                line = lines[i].strip().rstrip(',')
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().strip('"')
                    value = value.strip().rstrip(',')
                    if value.startswith('"') and value.endswith('"'):
                        product[key] = value.strip('"')
                    elif value.replace('.', '').replace('-', '').isdigit() or (value.startswith('-') and value[1:].replace('.', '').isdigit()):
                        product[key] = float(value) if '.' in value else int(value)
                    else:
                        product[key] = value.strip('"')
                i += 1
            if product:
                products.append(product)
        i += 1

print(f"Found {len(products)} products")

# Product icons mapping
icon_map = {
    'Microcontrollers': 'microchip',
    'Sensors': 'eye',
    'Actuators': 'cogs',
    'Displays': 'tv',
    'Power Supply': 'bolt',
    'Tools & Accessories': 'tools',
    'Audio Components': 'volume-up'
}

# Colors for product cards
colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502', '#2ed573', '#3742fa', '#ff3838']

def get_product_html(product, index):
    color_idx = index % len(colors)
    bg_color = colors[color_idx]

    icon = icon_map.get(product['category'], 'cube')

    return f'''                        <div class="product-card">
                            <div class="product-image" style="background: linear-gradient(135deg, {bg_color} 0%, #{"f7931e" if color_idx == 0 else "ff6b35"} 100%)">
                                <i class="fas fa-{icon}" style="color: white; font-size: 3rem; opacity: 0.8;"></i>
                            </div>
                            <div class="product-content">
                                <h3 class="product-title">{product['name']}</h3>
                                <p class="product-description">{product['description']}</p>
                                <div class="product-price">Rs {int(product['price'])}<span class="gst-note">(Exc. GST)</span></div>
                                <div class="product-actions">
                                    <button class="btn btn-primary btn-small" onclick="addToCart({product['id']})">
                                        <i class="fas fa-cart-plus"></i> Add to cart
                                    </button>
                                </div>
                            </div>
                        </div>'''

# Generate HTML for all pages
products_per_page = 6
total_pages = math.ceil(len(products) / products_per_page)

print(f"Creating {total_pages} pages with {products_per_page} products each")

pages_html = ""
for page_num in range(total_pages):
    start_idx = page_num * products_per_page
    end_idx = min(start_idx + products_per_page, len(products))
    page_products = products[start_idx:end_idx]

    active_class = " active" if page_num == 0 else ""

    pages_html += f'''                <!-- Page {page_num + 1} -->
                <div class="product-page{active_class}" id="page-{page_num + 1}">
                    <div class="products-grid">\n'''

    for i, product in enumerate(page_products):
        pages_html += get_product_html(product, start_idx + i) + '\n'

    pages_html += '''                    </div>
                </div>\n'''

# Generate pagination numbers
pagination_html = ""
for i in range(1, total_pages + 1):
    active_class = " active" if i == 1 else ""
    pagination_html += f'''                    <button class="page-btn{active_class}" onclick="goToPage({i})">{i}</button>\n'''

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Products - Robotech Store</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/Robotech-storeP2/static/css/style.css">
    <style>
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}

        @media (max-width: 599px) {{
            .products-grid {{
                grid-template-columns: repeat(1, 1fr);
            }}
        }}

        .product-page {{
            display: none;
        }}

        .product-page.active {{
            display: block;
        }}

        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin: 3rem 0;
        }}

        .page-btn {{
            padding: 0.5rem 1rem;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .page-btn:hover:not(:disabled) {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}

        .page-btn.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}

        .page-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <span>Robotech Store</span>
                </div>

                <!-- Mobile Menu Toggle -->
                <button class="mobile-menu-toggle" id="mobileMenuToggle" aria-label="Toggle menu">
                    <i class="fas fa-bars"></i>
                </button>

                <!-- Navigation -->
                <nav class="nav" id="mainNav">
                    <a href="/Robotech-storeP2/" class="nav-link">Home</a>
                    <div class="nav-dropdown">
                        <a href="/Robotech-storeP2/products_static.html" class="nav-link dropdown-toggle active">Products ▼</a>
                        <div class="dropdown-menu">
                            <div class="dropdown-column">
                                <h4>Components</h4>
                                <a href="#" onclick="filterByCategory('Resistors')">Resistors</a>
                                <a href="#" onclick="filterByCategory('Capacitors')">Capacitors</a>
                                <a href="#" onclick="filterByCategory('LEDs')">LEDs</a>
                                <a href="#" onclick="filterByCategory('Diodes')">Diodes</a>
                                <a href="#" onclick="filterByCategory('Transistors')">Transistors</a>
                            </div>
                            <div class="dropdown-column">
                                <h4>Development Boards</h4>
                                <a href="#" onclick="filterByCategory('Microcontrollers')">Microcontrollers</a>
                                <a href="#" onclick="filterByCategory('Arduino')">Arduino</a>
                                <a href="#" onclick="filterByCategory('Raspberry Pi')">Raspberry Pi</a>
                                <a href="#" onclick="filterByCategory('ESP')">ESP Boards</a>
                            </div>
                            <div class="dropdown-column">
                                <h4>Sensors</h4>
                                <a href="#" onclick="filterByCategory('Sensors')">All Sensors</a>
                                <a href="#" onclick="filterByCategory('Temperature Sensors')">Temperature</a>
                                <a href="#" onclick="filterByCategory('Motion Sensors')">Motion</a>
                                <a href="#" onclick="filterByCategory('Distance Sensors')">Distance</a>
                                <a href="#" onclick="filterByCategory('Light Sensors')">Light</a>
                            </div>
                        </div>
                    </div>
                    <a href="#categories" class="nav-link">Categories</a>
                    <a href="#about" class="nav-link">About</a>
                    <a href="#contact" class="nav-link">Contact</a>
                </nav>

                <!-- User Actions -->
                <div class="user-actions">
                    <div class="search-box">
                        <input type="text" id="searchInput" placeholder="Search components..." class="search-input">
                        <button class="search-btn"><i class="fas fa-search"></i></button>
                    </div>

                    <div class="action-buttons">
                        <div class="login-dropdown">
                            <button class="user-trigger">
                                <i class="fas fa-user"></i>
                                <span id="loginText">Demo User</span>
                            </button>
                        </div>

                        <button class="btn-icon cart-btn">
                            <i class="fas fa-shopping-cart"></i>
                            <span class="cart-count" id="cartCount">0</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Products Section -->
    <section class="products-page">
        <div class="container">
            <!-- Breadcrumb -->
            <div class="breadcrumb">
                <a href="/Robotech-storeP2/">Home</a> / <span>Products</span>
            </div>

            <!-- Page Header -->
            <div class="page-header">
                <h1 class="page-title">All Products</h1>
                <p class="page-subtitle">Browse our complete collection of {len(products)} electronics components</p>
            </div>

            <!-- Filters and Sorting -->
            <div class="products-controls">
                <div class="filter-buttons">
                    <button class="filter-btn active" onclick="filterByCategory('')">All</button>
                    <button class="filter-btn" onclick="filterByCategory('Microcontrollers')">Microcontrollers</button>
                    <button class="filter-btn" onclick="filterByCategory('Actuators')">Actuators</button>
                    <button class="filter-btn" onclick="filterByCategory('Sensors')">Sensors</button>
                    <button class="filter-btn" onclick="filterByCategory('Displays')">Displays</button>
                    <button class="filter-btn" onclick="filterByCategory('Power Supply')">Power Supply</button>
                    <button class="filter-btn" onclick="filterByCategory('Tools & Accessories')">Tools & Accessories</button>
                    <button class="filter-btn" onclick="filterByCategory('Audio Components')">Audio Components</button>
                    <select id="sortSelect" class="sort-select" onchange="sortProducts()">
                        <option value="name">Sort by Name</option>
                        <option value="price_low">Price: Low to High</option>
                        <option value="price_high">Price: High to Low</option>
                        <option value="newest">Newest First</option>
                    </select>
                </div>
            </div>

            <!-- Products Pages Container -->
            <div id="productsContainer">
{pages_html}
            </div>

            <!-- Pagination -->
            <div class="pagination">
                <button class="page-btn" id="prevBtn" disabled><i class="fas fa-chevron-left"></i> Previous</button>
                <div class="page-numbers">
{pagination_html}
                </div>
                <button class="page-btn" id="nextBtn" onclick="goToPage(2)"><i class="fas fa-chevron-right"></i> Next</button>
            </div>
        </div>
    </section>

    <!-- Scripts -->
    <script>
        let currentPage = 1;
        const totalPages = {total_pages};

        function goToPage(page) {{
            if (page >= 1 && page <= totalPages) {{
                // Hide current page
                document.getElementById(`page-${{currentPage}}`).classList.remove('active');

                // Show new page
                currentPage = page;
                document.getElementById(`page-${{currentPage}}`).classList.add('active');

                // Update pagination buttons
                updatePaginationButtons();

                // Scroll to top of products
                document.querySelector('.products-page').scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        function updatePaginationButtons() {{
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');

            prevBtn.disabled = currentPage <= 1;
            nextBtn.disabled = currentPage >= totalPages;

            // Update next button
            if (currentPage < totalPages) {{
                nextBtn.onclick = () => goToPage(currentPage + 1);
            }}
        }}

        function addToCart(productId) {{
            alert(`Added product ${{productId}} to cart! (Demo - not functional on static page)`);
        }}

        function filterByCategory(category) {{
            alert(`Filtering by ${{category}} (Demo - not functional on static page)`);
        }}

        function sortProducts() {{
            alert('Sorting (Demo - not functional on static page)');
        }}

        // Initialize pagination
        updatePaginationButtons();
    </script>
</body>
</html>'''

with open('products_static.html', 'w') as f:
    f.write(html_content)

print(f"✅ Generated static products page with {len(products)} products across {total_pages} pages")
print("📁 File saved as: products_static.html")