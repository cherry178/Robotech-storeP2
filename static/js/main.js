// Main JavaScript for Robotech Store

// Global variables
let cart = [];
let currentUser = null;

// Initialize currentUser from storage on script load
initializeUserFromStorage();

function initializeUserFromStorage() {
    console.log('initializeUserFromStorage called');

    try {
        // Try sessionStorage first (persists until tab closes)
        let storedUserId = sessionStorage.getItem('user_id');
        let storedPhone = sessionStorage.getItem('phone');
        let storedLoggedIn = sessionStorage.getItem('logged_in');

        console.log('sessionStorage check - userId:', storedUserId, 'phone:', storedPhone, 'loggedIn:', storedLoggedIn);

        if (storedLoggedIn === 'true' && storedUserId && storedPhone) {
            const parsedId = parseInt(storedUserId);
            if (!isNaN(parsedId) && parsedId > 0) {
                currentUser = {
                    user_id: parsedId,
                    phone: storedPhone
                };
                console.log('Initialized currentUser from sessionStorage:', JSON.stringify(currentUser));
                console.log('currentUser global variable is now:', JSON.stringify(currentUser));
                return;
            } else {
                console.log('Invalid user ID in sessionStorage, clearing:', storedUserId);
                clearUserData();
            }
        }

        // If not in sessionStorage, try localStorage (persists longer)
        storedUserId = localStorage.getItem('user_id');
        storedPhone = localStorage.getItem('phone');
        storedLoggedIn = localStorage.getItem('logged_in');

        console.log('localStorage check - userId:', storedUserId, 'phone:', storedPhone, 'loggedIn:', storedLoggedIn);

        if (storedLoggedIn === 'true' && storedUserId && storedPhone) {
            const parsedId = parseInt(storedUserId);
            if (!isNaN(parsedId) && parsedId > 0) {
                currentUser = {
                    user_id: parsedId,
                    phone: storedPhone
                };
                console.log('Initialized currentUser from localStorage:', JSON.stringify(currentUser));
                console.log('currentUser is now set to:', JSON.stringify(currentUser));
            } else {
                console.log('Invalid user ID in localStorage, clearing:', storedUserId);
                clearUserData();
            }
            // Also sync to sessionStorage for current session (ensure it's a valid number)
            const validUserId = parseInt(storedUserId);
            if (!isNaN(validUserId) && validUserId > 0) {
                sessionStorage.setItem('user_id', validUserId.toString());
                sessionStorage.setItem('phone', storedPhone);
                sessionStorage.setItem('logged_in', storedLoggedIn);
            } else {
                console.log('Invalid user ID from localStorage, not syncing to sessionStorage');
                clearUserData();
            }
            return;
        }

        console.log('No valid user found in storage');
        currentUser = null;

    } catch (error) {
        console.error('Error accessing storage:', error);
        // In case of storage errors (like incognito mode), reset
        currentUser = null;
    }
}

// Guest cart functions
function addToGuestCart(productId) {
    console.log('addToGuestCart called with productId:', productId, typeof productId);

    // Ensure productId is a number
    const productIdNum = parseInt(productId, 10);
    console.log('Parsed productId:', productIdNum);

    // Load existing cart from localStorage
    const guestCart = getGuestCart();
    console.log('Current guest cart:', guestCart);

    // Find existing item or add new one
    const existingItem = guestCart.find(item => item.product_id === productIdNum);
    if (existingItem) {
        existingItem.quantity += 1;
        console.log('Updated existing item quantity to:', existingItem.quantity);
    } else {
        guestCart.push({
            product_id: productIdNum,
            quantity: 1
        });
        console.log('Added new item to cart');
    }

    // Save to localStorage
    localStorage.setItem('guest_cart', JSON.stringify(guestCart));
    console.log('Saved cart to localStorage:', guestCart);

    showNotification('Item added to cart!', 'success');
    updateCartCount();
}

// Authenticated cart functions
function addToAuthenticatedCart(productId) {
    console.log('🛒 addToAuthenticatedCart called with productId:', productId, typeof productId);

    // Get user ID from storage
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    const phone = sessionStorage.getItem('phone') || localStorage.getItem('phone');
    const isLoggedIn = (sessionStorage.getItem('logged_in') === 'true') ||
                      (localStorage.getItem('logged_in') === 'true');

    console.log('🛒 addToAuthenticatedCart - userId:', userId, 'phone:', phone, 'isLoggedIn:', isLoggedIn);

    if (!userId || !isLoggedIn) {
        console.error('❌ No authenticated user session for cart');
        showNotification('Please login to add items to cart', 'error');
        return;
    }

    // Ensure productId is a number
    const productIdNum = parseInt(productId, 10);
    console.log('Parsed productId:', productIdNum, 'for user:', userId, 'phone:', phone);

    // Use backend API instead of localStorage
    console.log('Calling backend API to add item to cart');

    console.log('📤 Sending cart update request:', {
        user_id: userId,
        product_id: productIdNum,
        quantity: 1,
        phone: phone
    });

    fetch('http://127.0.0.1:8888/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: userId,
            product_id: productIdNum,
            quantity: 1,
            phone: phone
        })
    })
    .then(response => {
        console.log('📥 Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('📦 Response data:', data);
        if (data.success) {
            console.log('✅ Item successfully added to cart via backend');
            showNotification('Item added to cart!', 'success');
            updateCartCount();
        } else {
            console.error('❌ Backend returned error:', data.error);
            showNotification('Failed to add item to cart: ' + (data.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('❌ Error calling cart API:', error);
        showNotification('Network error - please try again', 'error');
    });
}

function getGuestCart() {
    try {
        const cartData = localStorage.getItem('guest_cart');
        return cartData ? JSON.parse(cartData) : [];
    } catch (error) {
        console.error('Error loading guest cart:', error);
        return [];
    }
}

function updateGuestCartItem(productId, quantity) {
    const guestCart = getGuestCart();
    const itemIndex = guestCart.findIndex(item => item.product_id === productId);

    if (itemIndex !== -1) {
        if (quantity <= 0) {
            guestCart.splice(itemIndex, 1);
        } else {
            guestCart[itemIndex].quantity = quantity;
        }
        localStorage.setItem('guest_cart', JSON.stringify(guestCart));
    }
}

function removeFromGuestCart(productId) {
    const guestCart = getGuestCart();
    const updatedCart = guestCart.filter(item => item.product_id !== productId);
    localStorage.setItem('guest_cart', JSON.stringify(updatedCart));
}

// IMMEDIATE CLEANUP - Clear any invalid data on script load
(function() {
    console.log('main.js - Performing immediate cleanup of invalid data...');

    // Check and clear invalid sessionStorage data
    const sessionUserId = sessionStorage.getItem('user_id');
    if (sessionUserId && (isNaN(parseInt(sessionUserId)) || parseInt(sessionUserId) <= 0 || sessionUserId.includes('demo_') || sessionUserId.includes('_'))) {
        console.log('main.js - Clearing invalid sessionStorage user_id:', sessionUserId);
        sessionStorage.removeItem('user_id');
        sessionStorage.removeItem('phone');
        sessionStorage.removeItem('logged_in');
    }

    // Check and clear invalid localStorage data
    const localUserId = localStorage.getItem('user_id');
    if (localUserId && (isNaN(parseInt(localUserId)) || parseInt(localUserId) <= 0 || localUserId.includes('demo_') || localUserId.includes('_'))) {
        console.log('main.js - Clearing invalid localStorage user_id:', localUserId);
        localStorage.removeItem('user_id');
        localStorage.removeItem('phone');
        localStorage.removeItem('logged_in');
    }

    console.log('main.js - Immediate cleanup completed');
})();

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Landing Page Functionality
function initializeLandingPage() {
    console.log('initializeLandingPage called, currentUser:', JSON.stringify(currentUser));

    const landingOverlay = document.getElementById('landingOverlay');
    const mainContent = document.getElementById('mainContent');
    const proceedBtn = document.getElementById('proceedBtn');

    // Check if landing page elements exist (only on homepage)
    if (landingOverlay && mainContent) {
        // Check if user is already logged in
        const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
        const isLoggedIn = (sessionStorage.getItem('logged_in') === 'true') ||
                          (localStorage.getItem('logged_in') === 'true');

        console.log('Landing page check - userId:', userId, 'isLoggedIn:', isLoggedIn, 'currentUser:', JSON.stringify(currentUser));

        // Also check the currentUser global variable as a backup
        if ((isLoggedIn && userId && !isNaN(parseInt(userId)) && parseInt(userId) > 0) ||
            (currentUser && currentUser.user_id && !isNaN(currentUser.user_id) && currentUser.user_id > 0)) {
            // User is already logged in, skip landing page and show main content
            console.log('User is logged in, skipping landing page');
            landingOverlay.style.display = 'none';
            mainContent.style.display = 'block';
            mainContent.classList.add('show');
            initializeCarousel();
            setupContactForm();
            updateUserInterface();
            return;
        }

        // Check if user has already proceeded past landing page in this session
        const hasSeenLanding = sessionStorage.getItem('hasSeenLanding');

        if (hasSeenLanding === 'true') {
            // User has already seen landing page, show main content directly
            console.log('User has seen landing page, showing main content');
            landingOverlay.style.display = 'none';
            mainContent.style.display = 'block';
            mainContent.classList.add('show');
            initializeCarousel();
            return;
        }

        // Show landing page (first visit or page refresh)
        console.log('Showing landing page for first-time or non-logged-in user');
        landingOverlay.style.display = 'flex';
        mainContent.style.display = 'none';

        // Handle proceed button click
        if (proceedBtn) {
            proceedBtn.addEventListener('click', function() {
                // Hide landing page with animation
                landingOverlay.classList.add('fade-out');

                // Show login modal after animation
                setTimeout(() => {
                    landingOverlay.style.display = 'none';
                    showLandingLoginModal();
                }, 300);
            });
        }
    } else {
        // No landing page (not homepage), setup contact form and update login UI
        setupContactForm();
        updateUserInterface();
    }
}

// Product Carousel Functionality
function initializeCarousel() {
    const carousel = document.querySelector('.product-carousel');
    if (!carousel) return;

    const slides = carousel.querySelectorAll('.carousel-slide');
    const indicators = carousel.querySelectorAll('.carousel-indicator');
    let currentSlide = 0;
    const totalSlides = slides.length;

    // Function to show specific slide
    function showSlide(index) {
        // Hide all slides
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('active'));

        // Show current slide
        slides[index].classList.add('active');
        indicators[index].classList.add('active');
    }

    // Function to next slide
    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    // Auto slide every 10 seconds (10 seconds = 10000 milliseconds)
    const slideInterval = setInterval(nextSlide, 10000);

    // Click indicators to change slide
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
            // Reset the auto-slide timer
            clearInterval(slideInterval);
            setTimeout(() => {
                setInterval(nextSlide, 10000);
            }, 10000);
        });
    });

    // Start with first slide
    showSlide(0);
}

function initializeApp() {
    console.log('Initializing app...');

    // Initialize landing page
    initializeLandingPage();

    // Check if user is logged in
    console.log('Checking user login status...');
    checkUserLoginStatus();

    // Load popular products
    loadPopularProducts();

    // Load development boards
    loadDevelopmentBoards();

    // Load cart count
    updateCartCount();

    // Setup event listeners
    setupEventListeners();

    // Setup scroll animations
    setupScrollAnimations();

    // Setup search functionality
    setupSearch();

    // Setup contact form immediately (will be called again after landing page if needed)
    setupContactForm();

    // Setup mobile menu
    setupMobileMenu();

    // Update user interface one more time to ensure User ID displays
    setTimeout(() => {
        console.log('Final UI update in initializeApp');
        updateUserInterface();
    }, 100);
}

function checkUserLoginStatus() {
    console.log('Checking user login status...');

    // currentUser should already be initialized from storage
    // Just update the UI based on current state
    console.log('Current currentUser state:', JSON.stringify(currentUser));

    if (currentUser) {
        console.log('User is logged in, updating UI');
        updateUserInterface();
    } else {
        console.log('User not logged in, resetting UI');
        // Reset UI to logged out state
        updateUserInterface();
    }
}

function updateUserInterface() {
    console.log('updateUserInterface called, currentUser:', JSON.stringify(currentUser));
    console.log('Storage check - user_id:', sessionStorage.getItem('user_id') || localStorage.getItem('user_id'));
    console.log('Storage check - logged_in:', sessionStorage.getItem('logged_in') || localStorage.getItem('logged_in'));

    // Update UI elements based on login status
    const loginText = document.getElementById('loginText');

    console.log('loginText element:', loginText);

    if (loginText) {
        // Try multiple sources for user data
        let userId = null;
        let displayId = null;

        // First try currentUser global variable
        if (currentUser && currentUser.user_id && !isNaN(currentUser.user_id) && currentUser.user_id > 0) {
            displayId = Math.floor(Math.abs(currentUser.user_id));
            console.log('Using currentUser for display:', displayId);
        }

        // If not available, try storage
        if (!displayId) {
            userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
            if (userId && !isNaN(parseInt(userId)) && parseInt(userId) > 0) {
                displayId = Math.floor(Math.abs(parseInt(userId)));
                console.log('Using storage for display:', displayId);
            }
        }

        // Set the display text
        if (displayId) {
            loginText.textContent = `My User ID: ${displayId}`;
            console.log('Final login text set to:', loginText.textContent);
        } else {
            console.log('No valid user data found anywhere, showing loading state');
            loginText.textContent = 'Loading...';

            // Clear invalid user data
            if (currentUser && (!currentUser.user_id || isNaN(currentUser.user_id) || currentUser.user_id <= 0)) {
                console.log('Clearing invalid currentUser data');
                currentUser = null;
                clearUserData();
            }
        }
    }
}

// Landing Page Login Modal Functions
function showLandingLoginModal() {
    const loginModal = document.getElementById('loginModal');
    if (loginModal) {
        loginModal.style.display = 'flex';
        setupLandingLoginEventListeners();
    }
}

function hideLandingLoginModal() {
    const loginModal = document.getElementById('loginModal');
    if (loginModal) {
        loginModal.style.display = 'none';
    }
}

function setupLandingLoginEventListeners() {
    console.log('Setting up landing login event listeners');

    // Phone login form
    const phoneForm = document.getElementById('landingPhoneLoginForm');
    const sendOtpBtn = document.getElementById('landingSendOtpBtn');
    const verifyOtpBtn = document.getElementById('landingVerifyOtpBtn');

    if (sendOtpBtn) {
        sendOtpBtn.addEventListener('click', function(e) {
            e.preventDefault();
            landingSendOTP();
        });
    }

    if (verifyOtpBtn) {
        verifyOtpBtn.addEventListener('click', function(e) {
            e.preventDefault();
            landingVerifyOTP();
        });
    }

    if (phoneForm) {
        phoneForm.addEventListener('submit', function(e) {
            e.preventDefault();
            landingVerifyOTP();
        });
    }
}

function landingSendOTP() {
    const phoneInput = document.getElementById('landingPhoneNumber');
    const phone = phoneInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    // Show loading state
    const sendBtn = document.getElementById('landingSendOtpBtn');
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // Prepare OTP request
    const otpData = { phone: phone };

    // DEMO MODE: Mock send OTP API
    console.log('Demo mode: Mock landing send OTP API called for phone:', phone);

    // Simulate API delay
    setTimeout(() => {
        // Mock successful OTP send response
        const mockResponse = {
            success: true,
            otp: '123456', // Always use demo OTP
            message: 'OTP sent successfully'
        };

        console.log('Mock landing OTP send success:', mockResponse);

        showNotification('OTP sent successfully!', 'success');

        // Show OTP input
        document.getElementById('landingOtpGroup').style.display = 'block';
        document.getElementById('landingSendOtpBtn').style.display = 'none';
        document.getElementById('landingVerifyOtpBtn').style.display = 'block';

        // Start OTP timer
        startLandingOtpTimer();

        // Reset button
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';
    }, 800); // Simulate 0.8 second API delay
}

function landingVerifyOTP() {
    const phoneInput = document.getElementById('landingPhoneNumber');
    const otpInput = document.getElementById('landingOtp');
    const phone = phoneInput.value.trim();
    const otp = otpInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    if (!otp || otp.length !== 6) {
        showNotification('Please enter a valid 6-digit OTP', 'error');
        otpInput.focus();
        return;
    }

    // Show loading state
    const verifyBtn = document.getElementById('landingVerifyOtpBtn');
    verifyBtn.disabled = true;
    verifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    // Prepare login data
    const loginData = {
        phone: phone,
        otp: otp
    };

    // DEMO MODE: Mock landing login API
    console.log('Demo mode: Mock landing login API called with:', loginData);

    // Simulate API delay
    setTimeout(() => {
        if (otp === '123456') {
            // Mock successful login response
            const mockResponse = {
                success: true,
                user: {
                    id: Math.floor(Math.random() * 1000) + 100, // Random user ID
                    phone: phone
                },
                message: 'Login successful'
            };

            console.log('Mock landing login success:', mockResponse);

            // Set current user and store login data
            currentUser = {
                user_id: mockResponse.user.id,
                phone: phone
            };

            // Store in both sessionStorage and localStorage for persistence
            sessionStorage.setItem('user_id', mockResponse.user.id.toString());
            sessionStorage.setItem('phone', phone);
            sessionStorage.setItem('logged_in', 'true');

            localStorage.setItem('user_id', mockResponse.user.id.toString());
            localStorage.setItem('phone', phone);
            localStorage.setItem('logged_in', 'true');

            console.log('Landing login successful, currentUser set to:', JSON.stringify(currentUser));

            showNotification('Login successful! Welcome to Robotech Store!', 'success');

            // Hide login modal and show main content
            setTimeout(() => {
                hideLandingLoginModal();
                showMainContentAfterLogin();
            }, 1500);
        } else {
            // Mock failed login
            console.log('Mock landing login failed - invalid OTP');
            showNotification('Invalid OTP. Please try again.', 'error');
            verifyBtn.disabled = false;
            verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify OTP & Continue';
        }
    }, 1000); // Simulate 1 second API delay
}

function showMainContentAfterLogin() {
    const mainContent = document.getElementById('mainContent');
    if (mainContent) {
        // Mark that user has seen the landing page
        sessionStorage.setItem('hasSeenLanding', 'true');

        mainContent.style.display = 'block';

        // Add show class for smooth transition
        setTimeout(() => {
            mainContent.classList.add('show');
            // Initialize carousel after main content is shown
            initializeCarousel();
            // Setup contact form and login after main content is shown
            setupContactForm();
            // Update login UI after main content is shown
            updateUserInterface();
        }, 50);
    }
}

function startLandingOtpTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('landingOtpTimer');
    const resendBtn = document.getElementById('landingResendOtpBtn');

    const timer = setInterval(() => {
        timeLeft--;
        timerElement.textContent = `Resend OTP in ${timeLeft}s`;

        if (timeLeft <= 0) {
            clearInterval(timer);
            timerElement.textContent = 'OTP expired. Please resend.';
            resendBtn.disabled = false;
            resendBtn.textContent = 'Resend OTP';
        }
    }, 1000);

    // Setup resend button
    resendBtn.onclick = function() {
        clearInterval(timer);
        landingSendOTP();
    };
}

function validatePhoneNumber(phone) {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone);
}

function landingLoginWithGmail() {
    showNotification('Gmail login not implemented yet. Please use phone login.', 'info');
}

// Tab switching for landing login modal
function showLoginTab(tabName) {
    // Hide all tabs
    const allTabs = document.querySelectorAll('.login-modal .auth-tab-content');
    allTabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all tab buttons
    const allTabButtons = document.querySelectorAll('.login-modal .auth-tab');
    allTabButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const selectedTab = document.getElementById(tabName + 'LoginTab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Add active class to selected tab button
    const selectedButton = document.querySelector(`.login-modal .auth-tab[onclick*="${tabName}"]`);
    if (selectedButton) {
        selectedButton.classList.add('active');
    }
}

function loadPopularProducts() {
    // DEMO MODE: Mock popular products
    const mockProducts = [
        {
            id: 1,
            name: 'Arduino Uno R3',
            description: 'ATmega328P microcontroller board',
            price: 450,
            category: 'Microcontrollers',
            is_featured: true,
            image_url: 'https://m.media-amazon.com/images/I/51+N-57gSiL.jpg'
        },
        {
            id: 2,
            name: 'ESP32 Development Board',
            description: 'WiFi & Bluetooth enabled microcontroller',
            price: 350,
            category: 'Microcontrollers',
            is_featured: true,
            image_url: 'https://i.pinimg.com/736x/d1/66/1b/d1661bdecf277684181694a4fedbf9bf.jpg'
        },
        {
            id: 5,
            name: 'SG90 Servo Motor',
            description: '9g micro servo motor for robotics',
            price: 95,
            category: 'Actuators',
            is_featured: true,
            image_url: 'https://i.pinimg.com/1200x/c6/da/02/c6da024f4702e68756c6d466894a027c.jpg'
        }
    ];

    displayPopularProducts(mockProducts);
}

function displayPopularProducts(products) {
    const container = document.getElementById('popularProducts');
    if (!container) return;

    container.innerHTML = '';

    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

function loadDevelopmentBoards() {
    // DEMO MODE: Mock development boards
    const mockProducts = [
        {
            id: 1,
            name: 'Arduino Uno R3',
            description: 'ATmega328P microcontroller board',
            price: 450,
            category: 'Microcontrollers',
            image_url: 'https://m.media-amazon.com/images/I/51+N-57gSiL.jpg'
        },
        {
            id: 2,
            name: 'ESP32 Development Board',
            description: 'WiFi & Bluetooth enabled microcontroller',
            price: 350,
            category: 'Microcontrollers',
            image_url: 'https://i.pinimg.com/736x/d1/66/1b/d1661bdecf277684181694a4fedbf9bf.jpg'
        },
        {
            id: 36,
            name: 'Raspberry Pi Zero W',
            description: 'Compact Raspberry Pi with WiFi and Bluetooth',
            price: 1200,
            category: 'Microcontrollers',
            image_url: 'https://i.pinimg.com/1200x/f7/56/7c/f7567c73f08d270f14b0fccf8f7e18bc.jpg'
        },
        {
            id: 41,
            name: 'Adafruit Feather M0',
            description: 'Adafruit Feather M0 with ATSAMD21 microcontroller',
            price: 650,
            category: 'Microcontrollers',
            image_url: 'https://i.pinimg.com/1200x/27/42/d7/2742d764962b3debf7ec4475259071b1.jpg'
        }
    ];

    displayDevelopmentBoards(mockProducts);
}

function displayDevelopmentBoards(products) {
    const container = document.getElementById('devBoardsGrid');
    if (!container) return;

    container.innerHTML = '';

    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

function filterCategory(category) {
    // Update active filter
    document.querySelectorAll('.filter-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');

    // Filter products based on category
    let filteredProducts = [];

    if (category === 'all') {
        loadDevelopmentBoards();
        return;
    }

    // This would need backend support for sub-category filtering
    // For now, we'll just show a message
    showNotification(`Filtering by ${category} category`, 'info');
}

function filterSensorCategory(category) {
    // Update active filter in sensors section only
    const sensorsSection = document.querySelector('.sensors-section');
    sensorsSection.querySelectorAll('.filter-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');

    // Filter sensor cards
    const sensorCards = document.querySelectorAll('.sensor-card');

    if (category === 'all') {
        // Show all sensors
        sensorCards.forEach(card => {
            card.style.display = 'block';
            card.classList.add('fade-in');
        });
    } else {
        // Show only sensors matching the category
        sensorCards.forEach(card => {
            const cardCategory = card.dataset.category;
            if (cardCategory === category) {
                card.style.display = 'block';
                card.classList.add('fade-in');
            } else {
                card.style.display = 'none';
                card.classList.remove('fade-in');
            }
        });
    }
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in';

    // Generate a color based on category
    const colors = ['#ff6b35', '#f7931e', '#ff4757', '#ffa502'];
    const colorIndex = product.category ? product.category.length % colors.length : 0;
    const bgColor = colors[colorIndex];

    // Check if product has sale pricing
    const hasSale = product.original_price && product.original_price > product.price;

    card.innerHTML = `
        <div class="product-image" style="background: linear-gradient(135deg, ${bgColor} 0%, ${adjustColor(bgColor, -20)} 100%)">
            <i class="fas fa-${getCategoryIcon(product.category)}"></i>
            ${product.is_featured ? '<div class="product-badge">Sale</div>' : ''}
        </div>
        <div class="product-content">
            <h3 class="product-title">${product.name}</h3>
            <p class="product-description">${product.description || 'High-quality electronics component'}</p>
            <div class="product-price">
                ${hasSale ? `<span class="original-price">₹${product.original_price}</span>` : ''}
                ₹${product.price}
                <span class="gst-note">(Exc. GST)</span>
            </div>
            <div class="product-actions">
                <button class="btn btn-primary btn-small" onclick="console.log('🏠 Homepage: Clicking Add to Cart for: ID ${product.id} - ${product.name}'); addToCart(${product.id})">
                    <i class="fas fa-cart-plus"></i> Add to cart
                </button>
            </div>
        </div>
    `;

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
    b = b > 255 ? 255 : b < 0 ? 0 : b;

    return (usePound ? '#' : '') + (r << 16 | g << 8 | b).toString(16);
}

function addToCart(productId) {
    console.log('🛒 addToCart called with productId:', productId);
    console.log('🛒 currentUser:', currentUser);

    // Find the product name for debugging
    // This is a temporary debug addition
    console.log('🛒 DEBUG: Looking up product name for ID', productId);

    // Check if user is logged in by checking storage and currentUser
    const userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
    const isLoggedIn = (sessionStorage.getItem('logged_in') === 'true') ||
                      (localStorage.getItem('logged_in') === 'true');

    console.log('addToCart check - currentUser:', currentUser, 'userId:', userId, 'isLoggedIn:', isLoggedIn);

    if (!currentUser && (!isLoggedIn || !userId)) {
        console.log('User not logged in, redirecting to landing page');
        showNotification('Please login to add items to your cart', 'warning');
        // Redirect to home page since that's our entry point
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
        return;
    }

    // User is logged in - add to authenticated cart
    console.log('User is logged in, adding to authenticated cart');
    addToAuthenticatedCart(productId);
}

function buyNow(productId) {
    // Check if user is logged in before allowing purchase
    if (!currentUser) {
        showNotification('Please login to purchase items', 'warning');
        // Redirect to login page
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
        return;
    }

    // Add to cart
    addToAuthenticatedCart(productId);

    // Redirect to checkout after a short delay
    setTimeout(() => {
        window.location.href = '/checkout';
    }, 1000);
}

function viewProduct(productId) {
    // For now, redirect to products page with the specific product
    // In a full implementation, this would open a product detail modal or page
    window.location.href = `/products?product=${productId}`;
}

function updateCartCount() {
    if (currentUser) {
        // User is logged in - get cart count from backend API
        fetch(`http://127.0.0.1:8888/api/cart?user_id=${currentUser.user_id}`)
            .then(response => response.json())
            .then(data => {
                if (data.success && data.cart) {
                    const count = data.cart.reduce((total, item) => total + item.quantity, 0);
                    updateCartCountDisplay(count);
                } else {
                    updateCartCountDisplay(0);
                }
            })
            .catch(error => {
                console.error('Error loading cart count from backend:', error);
                updateCartCountDisplay(0);
            });
    } else {
        // Use guest cart for non-logged in users
    const guestCart = getGuestCart();
    const count = guestCart.reduce((total, item) => total + item.quantity, 0);
    updateCartCountDisplay(count);
    }
}

function updateCartCountDisplay(count) {
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        cartCountElement.style.display = count > 0 ? 'block' : 'none';
    }
}

function filterByCategory(category) {
    window.location.href = `/products?category=${encodeURIComponent(category)}`;
}

function setupEventListeners() {
    // Address selector
    const addressSelect = document.getElementById('addressSelect');
    if (addressSelect) {
        addressSelect.addEventListener('change', function() {
            if (this.value) {
                showNotification(`Delivery address set to ${this.value}`, 'success');
                // Store in localStorage for persistence
                localStorage.setItem('deliveryAddress', this.value);
            }
        });

        // Load saved address
        const savedAddress = localStorage.getItem('deliveryAddress');
        if (savedAddress) {
            addressSelect.value = savedAddress;
        }
    }

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function setupSearch() {
    const searchBtn = document.querySelector('.search-btn');
    const searchInput = document.getElementById('searchInput');

    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => {
            performSearch(searchInput.value);
        });
    }
}

function performSearch(query) {
    if (!query.trim()) {
        showNotification('Please enter a search term', 'warning');
        return;
    }

    window.location.href = `/products?search=${encodeURIComponent(query)}`;
}

function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all elements with fade-in class
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;

    const icon = type === 'success' ? 'check-circle' :
                 type === 'error' ? 'exclamation-circle' :
                 type === 'warning' ? 'exclamation-triangle' : 'info-circle';

    notification.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;

    // Add close button styles
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        opacity: 0.8;
        margin-left: auto;
    `;

    closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
    closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.8');

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }

    .notification {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
    }
`;
document.head.appendChild(style);

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(price);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function setupContactForm() {
    // Setup login functionality for header dropdown
    setupHeaderLoginForm();
}

function setupHeaderLoginForm() {
    console.log('setupHeaderLoginForm called');

    // Check if login form elements exist on this page
    const headerSendLoginOtpBtn = document.getElementById('headerSendLoginOtpBtn');
    const loginDropdown = document.getElementById('loginDropdown');

    // If login elements don't exist on this page, skip setup
    if (!headerSendLoginOtpBtn && !loginDropdown) {
        console.log('No login form elements found on this page, skipping setup');
        return;
    }

    // Login dropdown toggle - make sure it's globally available
    // Make functions globally available
    window.toggleLoginDropdown = function() {
        console.log('toggleLoginDropdown called');
        const dropdown = document.getElementById('loginDropdown');
        console.log('dropdown element:', dropdown);

        if (dropdown) {
            const isActive = dropdown.classList.contains('active');
            console.log('dropdown currently active:', isActive);

            if (isActive) {
                dropdown.classList.remove('active');
                console.log('dropdown hidden');
            } else {
                dropdown.classList.add('active');
                console.log('dropdown shown');
            }
        } else {
            console.error('loginDropdown element not found!');
        }
    };

    console.log('toggleLoginDropdown function defined globally');

    // Close dropdown when clicking outside (but not on OTP modal)
    document.addEventListener('click', function(e) {
        const dropdown = document.getElementById('loginDropdown');
        const trigger = document.querySelector('.login-trigger');
        const otpModal = document.querySelector('.otp-modal-overlay');

        // Don't close dropdown if OTP modal exists or if clicking on OTP modal
        if (otpModal) {
            return; // Keep dropdown open while OTP modal is visible
        }

        if (dropdown && trigger && !dropdown.contains(e.target) && !trigger.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });

    // Login tab switching
    window.showLoginTab = function(tabType) {
        // Update tab buttons
        document.querySelectorAll('.login-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');

        // Update tab content
        document.querySelectorAll('.login-tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabType + 'LoginTab').classList.add('active');
    };

    // Phone number input validation
    const phoneInput = document.getElementById('headerLoginPhone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Only allow numbers and limit to 10 digits
            this.value = this.value.replace(/[^0-9]/g, '').substring(0, 10);
        });
    }

    // OTP input validation
    const otpInput = document.getElementById('headerLoginOtp');
    if (otpInput) {
        otpInput.addEventListener('input', function(e) {
            // Only allow numbers
            this.value = this.value.replace(/[^0-9]/g, '');

            // Auto-submit when 6 digits entered
            if (this.value.length === 6) {
                verifyHeaderLoginOTP();
            }
        });
    }

    // Send OTP button (only if it exists on this page)
    const sendOtpBtn = document.getElementById('headerSendLoginOtpBtn');
    console.log('sendOtpBtn element:', sendOtpBtn);
    if (sendOtpBtn) {
        sendOtpBtn.addEventListener('click', sendHeaderLoginOTP);
        console.log('sendHeaderLoginOTP event listener added to sendOtpBtn');
    } else {
        console.log('sendOtpBtn not found on this page (expected on pages without login form)');
    }
}

// Global functions for login
window.showLoginTab = function(tabType) {
    // Update tab buttons
    document.querySelectorAll('.login-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update tab content
    document.querySelectorAll('.login-tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabType + 'LoginTab').classList.add('active');
};

function sendLoginOTP() {
    const phoneInput = document.getElementById('loginPhone');
    const phone = phoneInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid 10-digit phone number', 'error');
        phoneInput.focus();
        return;
    }

    // Show loading state
    const sendOtpBtn = document.getElementById('sendLoginOtpBtn');
    sendOtpBtn.disabled = true;
    sendOtpBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // Send OTP request to backend
    fetch('http://127.0.0.1:8888/api/send-otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ phone: phone })
    })
    .then(response => {
        console.log('OTP API response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('OTP API response data:', data);
        if (data.success) {
            // Show OTP input field immediately
            document.getElementById('loginOtpGroup').style.display = 'block';
            document.getElementById('sendLoginOtpBtn').style.display = 'none';
            document.getElementById('verifyLoginOtpBtn').style.display = 'block';

            // Start OTP timer
            startLoginOTPTimer();

            // Reset button
            sendOtpBtn.disabled = false;
            sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';

            // Focus on OTP input immediately
            document.getElementById('loginOtp').focus();

            // Show OTP modal immediately with the received OTP
            const otp = data.otp; // Backend sends the OTP for demo
            console.log('OTP received from backend:', otp);

            // Create a visible OTP display element on the page
            const otpDisplay = document.createElement('div');
            otpDisplay.id = 'otp-display-popup';
            otpDisplay.innerHTML = `
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    border: 4px solid #ff6b35;
                    border-radius: 15px;
                    padding: 30px;
                    z-index: 1000001;
                    text-align: center;
                    font-family: Arial, sans-serif;
                    box-shadow: 0 0 50px rgba(0,0,0,0.7);
                    max-width: 90vw;
                    min-width: 350px;
                ">
                    <h2 style="color: #ff6b35; margin: 0 0 20px 0; font-size: 28px;">🔐 DEMO OTP</h2>
                    <p style="margin: 0 0 20px 0; color: #666; font-size: 18px;">Your verification code is:</p>
                    <div style="font-size: 32px; font-weight: bold; color: #ff6b35; letter-spacing: 5px; margin: 20px 0; font-family: monospace;">
                        ${otp}
                    </div>
                    <p style="margin: 20px 0 10px 0; color: #888; font-size: 16px;">Enter this code in the login form</p>
                    <button onclick="this.parentElement.parentElement.remove()" style="
                        margin-top: 20px;
                        background: #ff6b35;
                        color: white;
                        border: none;
                        padding: 12px 25px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 16px;
                        font-weight: bold;
                    ">OK, Got it!</button>
                </div>
            `;
            document.body.appendChild(otpDisplay);
            console.log('OTP display element created and appended to body');

            // Also log to console very clearly
            console.log('========================================');
            console.log('🔐 DEMO OTP CODE:', otp);
            console.log('📱 Phone:', phone);
            console.log('⚠️  Copy this code to login');
            console.log('========================================');

            // Auto-remove after 30 seconds
            setTimeout(() => {
                if (otpDisplay.parentElement) {
                    otpDisplay.remove();
                    console.log('OTP display auto-removed');
                }
            }, 30000);

            // Also try to show the modal as backup
            setTimeout(() => {
                try {
                showDemoOTPNotification(otp);
                console.log(`📱 DEMO OTP for ${phone}: ${otp}`);
                showNotification('OTP sent successfully! Check the popup on the page for your code.', 'success');
                } catch (error) {
                    console.error('Modal creation failed:', error);
                }
            }, 500);
        } else {
            showNotification(data.message || 'Failed to send OTP', 'error');
            sendOtpBtn.disabled = false;
            sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';
        }
    })
    .catch(error => {
        console.error('OTP send error:', error);
        showNotification('Network error. Please try again.', 'error');
        sendOtpBtn.disabled = false;
        sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';
    });
}

function startLoginOTPTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('loginOtpTimer');
    const resendBtn = document.getElementById('resendLoginOtpBtn');

    const timer = setInterval(() => {
        timerElement.textContent = `Resend OTP in ${timeLeft}s`;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            timerElement.textContent = 'OTP expired';
            resendBtn.disabled = false;
            resendBtn.addEventListener('click', resendLoginOTP);
        }
    }, 1000);
}

function resendLoginOTP() {
    const phoneInput = document.getElementById('loginPhone');
    const phone = phoneInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    // Reset OTP input
    document.getElementById('loginOtp').value = '';

    // Disable resend button
    const resendBtn = document.getElementById('resendLoginOtpBtn');
    resendBtn.disabled = true;

    // Send new OTP
    sendLoginOTP();
}

function verifyLoginOTP() {
    const phoneInput = document.getElementById('loginPhone');
    const otpInput = document.getElementById('loginOtp');
    const phone = phoneInput.value.trim();
    const otp = otpInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    if (!otp || otp.length !== 6) {
        showNotification('Please enter a valid 6-digit OTP', 'error');
        otpInput.focus();
        return;
    }

    // Show loading state
    const verifyBtn = document.getElementById('verifyLoginOtpBtn');
    verifyBtn.disabled = true;
    verifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    // Prepare login data
    const loginData = {
        phone: phone,
        otp: otp
    };

    // Send login request
    fetch('http://127.0.0.1:8888/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        // Reset button state
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify OTP & Login';

        if (data.success) {
            console.log('Login page login successful, user data:', data.user);
            showNotification('Login successful! Welcome to Robotech Store.', 'success');

            // Store user data in both sessionStorage and localStorage for persistence
            const userData = {
                user_id: data.user.user_id,
                phone: data.user.phone,
                logged_in: 'true'
            };

            sessionStorage.setItem('user_id', userData.user_id);
            sessionStorage.setItem('phone', userData.phone);
            sessionStorage.setItem('logged_in', userData.logged_in);

            localStorage.setItem('user_id', userData.user_id);
            localStorage.setItem('phone', userData.phone);
            localStorage.setItem('logged_in', userData.logged_in);

            console.log('Stored user data in both storages:', userData);

            // Update current user
            currentUser = data.user;

            // Update login button in header
            updateLoginStatus();

            // Ensure storage is complete before redirect
            console.log('Login successful, preparing redirect...');
            setTimeout(() => {
                console.log('Redirecting to products page...');
                // Double-check storage before redirect
                console.log('Final storage check before redirect:', JSON.stringify({
                    session_user_id: sessionStorage.getItem('user_id'),
                    session_phone: sessionStorage.getItem('phone'),
                    session_logged_in: sessionStorage.getItem('logged_in'),
                    local_user_id: localStorage.getItem('user_id'),
                    local_phone: localStorage.getItem('phone'),
                    local_logged_in: localStorage.getItem('logged_in')
                }));
                window.location.href = '/products';
            }, 2000);

            // Reset form
            document.getElementById('loginOtp').value = '';
            document.getElementById('loginOtpGroup').style.display = 'none';
            document.getElementById('sendLoginOtpBtn').style.display = 'block';
            document.getElementById('verifyLoginOtpBtn').style.display = 'none';

            // Close OTP modal if open
            const otpModal = document.querySelector('.otp-modal-overlay');
            if (otpModal) {
                otpModal.remove();
            }

        } else {
            showNotification(data.message || 'Login failed. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showNotification('Network error. Please try again.', 'error');
        // Reset button
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify OTP & Login';
    });
}

function loginWithGmail() {
    // Show loading state
    const gmailBtn = document.querySelector('.btn-gmail');
    gmailBtn.disabled = true;
    gmailBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';

    // Simulate Gmail login
    setTimeout(() => {
        showNotification('Gmail authentication not implemented yet. Use phone login instead.', 'warning');
        gmailBtn.disabled = false;
        gmailBtn.innerHTML = '<i class="fab fa-google"></i> Continue with Google';
    }, 2000);
}

function validatePhoneNumber(phone) {
    // For demo purposes, accept any 10-digit number
    const phoneRegex = /^\d{10}$/;
    return phoneRegex.test(phone);
}

function showDemoOTPNotification(otp) {
    console.log('Creating simple OTP display with OTP:', otp);

    // Create a simple, guaranteed-to-work display
    const otpDiv = document.createElement('div');
    otpDiv.id = 'demo-otp-display';
    otpDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border: 3px solid #ff6b35;
        border-radius: 15px;
        padding: 30px;
        z-index: 1000000;
        box-shadow: 0 0 50px rgba(0,0,0,0.5);
        text-align: center;
        font-family: Arial, sans-serif;
        max-width: 90vw;
        min-width: 300px;
    `;

    const otpString = String(otp);
    otpDiv.innerHTML = `
        <h2 style="color: #ff6b35; margin: 0 0 20px 0; font-size: 24px;">🔐 DEMO OTP</h2>
        <p style="margin: 0 0 20px 0; color: #666; font-size: 16px;">Your verification code is:</p>
        <div style="display: flex; justify-content: center; gap: 10px; margin: 20px 0;">
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[0] || ''}</div>
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[1] || ''}</div>
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[2] || ''}</div>
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[3] || ''}</div>
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[4] || ''}</div>
            <div style="width: 40px; height: 50px; background: #ff6b35; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">${otpString[5] || ''}</div>
        </div>
        <p style="margin: 20px 0 0 0; color: #888; font-size: 14px;">Enter this code in the login form below</p>
        <button onclick="this.parentElement.remove()" style="
            margin-top: 20px;
            background: #ff6b35;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        ">OK, Got it!</button>
    `;

    document.body.appendChild(otpDiv);
    console.log('Simple OTP display created and appended');

    // Auto-remove after 30 seconds
    setTimeout(() => {
        if (otpDiv.parentElement) {
            otpDiv.remove();
            console.log('OTP display auto-removed');
        }
    }, 30000);
}

function closeOTPModal() {
    console.log('Closing OTP modal');
    const otpModal = document.querySelector('.otp-modal-overlay');
    if (otpModal) {
        otpModal.remove();
        console.log('OTP modal removed');
    } else {
        console.log('OTP modal not found for removal');
    }
}

function generateDemoOTP() {
    // Generate a random 6-digit OTP for demo purposes
    return Math.floor(100000 + Math.random() * 900000).toString();
}

function sendHeaderLoginOTP() {
    console.log('sendHeaderLoginOTP called');
    const phoneInput = document.getElementById('headerLoginPhone');
    console.log('phoneInput element:', phoneInput);
    let phone = phoneInput.value.trim();
    // Remove any non-digit characters and ensure it's 10 digits
    phone = phone.replace(/\D/g, '').slice(-10);
    console.log('cleaned phone value to send:', phone, 'length:', phone.length);

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid 10-digit phone number', 'error');
        phoneInput.focus();
        return;
    }

    // Show loading state
    const sendOtpBtn = document.getElementById('headerSendLoginOtpBtn');
    sendOtpBtn.disabled = true;
    sendOtpBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // DEMO MODE: Generate OTP locally
    console.log('Using demo mode for OTP generation');
    setTimeout(() => {
        const otp = '123456'; // Demo OTP
        console.log(`Demo OTP generated: ${otp} for phone: ${phone}`);

        // Show OTP input field
            document.getElementById('headerLoginOtpGroup').style.display = 'block';
            document.getElementById('headerSendLoginOtpBtn').style.display = 'none';
            document.getElementById('headerVerifyLoginOtpBtn').style.display = 'block';

            // Start OTP timer
            startHeaderLoginOTPTimer();

            // Reset button
            sendOtpBtn.disabled = false;
            sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';

        // Focus on OTP input
            document.getElementById('headerLoginOtp').focus();

        // Show demo OTP notification
            showDemoOTPNotification(otp);

        console.log(`📱 DEMO OTP: ${otp}`);
        showNotification('Demo OTP sent! Check the popup for your code.', 'success');
    }, 1000);
}

function startHeaderLoginOTPTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('headerLoginOtpTimer');
    const resendBtn = document.getElementById('headerResendLoginOtpBtn');

    const timer = setInterval(() => {
        timerElement.textContent = `Resend OTP in ${timeLeft}s`;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            timerElement.textContent = 'OTP expired';
            resendBtn.disabled = false;
            resendBtn.addEventListener('click', resendHeaderLoginOTP);
        }
    }, 1000);
}

function resendHeaderLoginOTP() {
    const phoneInput = document.getElementById('headerLoginPhone');
    const phone = phoneInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    // Reset OTP input
    document.getElementById('headerLoginOtp').value = '';

    // Disable resend button
    const resendBtn = document.getElementById('headerResendLoginOtpBtn');
    resendBtn.disabled = true;

    // Send new OTP
    sendHeaderLoginOTP();
}

function verifyHeaderLoginOTP() {
    const phoneInput = document.getElementById('headerLoginPhone');
    const otpInput = document.getElementById('headerLoginOtp');
    let phone = phoneInput.value.trim();
    let otp = otpInput.value.trim();

    // Clean phone number
    phone = phone.replace(/\D/g, '').slice(-10);
    // Clean OTP
    otp = otp.replace(/\D/g, '');

    console.log('verifyHeaderLoginOTP called');
    console.log('cleaned phone:', phone, 'cleaned otp:', otp);

    if (!validatePhoneNumber(phone)) {
        console.log('Phone validation failed for:', phone);
        showNotification('Please enter a valid 10-digit phone number', 'error');
        return;
    }

    if (!otp || otp.length !== 6) {
        console.log('OTP validation failed, otp:', otp, 'length:', otp.length);
        showNotification('Please enter a valid 6-digit OTP', 'error');
        otpInput.focus();
        return;
    }

    console.log('Validation passed, sending login request...');

    // Show loading state
    const verifyBtn = document.getElementById('headerVerifyLoginOtpBtn');
    verifyBtn.disabled = true;
    verifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    // Prepare login data
    const loginData = {
        phone: phone,
        otp: otp
    };

    console.log('verifyHeaderLoginOTP - Sending login request to /api/login with data:', loginData);

    // DEMO MODE: Mock login response since server can't run
    console.log('verifyHeaderLoginOTP - Using demo mode (server not available)');

    // Simulate network delay
    setTimeout(() => {
        console.log('Demo login successful for phone:', phone);

        // Create mock user data with proper numeric ID
        const mockUser = {
            user_id: 1000 + Math.floor(Math.random() * 9000), // Always 1000-9999
            phone: phone
        };

        // Store user data in both sessionStorage and localStorage for persistence
        const userData = {
            user_id: mockUser.user_id,
            phone: mockUser.phone,
            logged_in: 'true'
        };

        sessionStorage.setItem('user_id', userData.user_id);
        sessionStorage.setItem('phone', userData.phone);
        sessionStorage.setItem('logged_in', userData.logged_in);

        localStorage.setItem('user_id', userData.user_id);
        localStorage.setItem('phone', userData.phone);
        localStorage.setItem('logged_in', userData.logged_in);

        console.log('Stored demo user data:', userData);

            // Update current user
        currentUser = mockUser;
        console.log('Set currentUser to:', JSON.stringify(currentUser));

        // Reset button state
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify & Login';

            // Update login button in header
            updateLoginStatus();

            // Reset form
            document.getElementById('headerLoginOtp').value = '';
            document.getElementById('headerLoginOtpGroup').style.display = 'none';
            document.getElementById('headerSendLoginOtpBtn').style.display = 'block';
            document.getElementById('headerVerifyLoginOtpBtn').style.display = 'none';

            // Close OTP modal if open
            const otpModal = document.querySelector('.otp-modal-overlay');
            if (otpModal) {
                otpModal.remove();
            }

        // Show success message
        showNotification('Demo login successful! Welcome to Robotech Store.', 'success');

    }, 1000); // 1 second delay to simulate network request
}

function updateLoginStatus() {
    console.log('updateLoginStatus called');
    // Update the login button in header to show user is logged in
    const loginText = document.getElementById('loginText');
    const loginTrigger = document.querySelector('.login-trigger');

    console.log('updateLoginStatus - loginText:', loginText, 'loginTrigger:', loginTrigger);

    if (loginText && loginTrigger) {
        // Get and validate user ID
        const storedUserId = sessionStorage.getItem('user_id');
        const parsedUserId = storedUserId ? parseInt(storedUserId) : null;

        if (parsedUserId && !isNaN(parsedUserId) && parsedUserId > 0) {
            // Valid user ID - show it
            loginText.textContent = `User ${parsedUserId}`;
            console.log('updateLoginStatus - Set text to:', loginText.textContent);
            // Only set onclick if not already set (to avoid overriding home page custom handler)
            if (!loginTrigger.onclick || loginTrigger.onclick.toString().indexOf('toggleAccountMenuHome') === -1) {
                loginTrigger.onclick = () => toggleAccountMenu();
            }
        } else {
            // Invalid or no user ID - show login
            loginText.textContent = 'Login';
            console.log('updateLoginStatus - Invalid user ID, set to Login');
            loginTrigger.onclick = () => toggleLoginDropdown();

            // Clear any invalid data
            if (storedUserId && (isNaN(parsedUserId) || parsedUserId <= 0 || storedUserId.includes('demo_'))) {
                console.log('updateLoginStatus - Clearing invalid user data');
                clearUserData();
            }
        }

        // Close dropdown if open
        const dropdown = document.getElementById('loginDropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }

        // Show success notification with user details
        const phone = sessionStorage.getItem('phone') || 'Unknown';
        showNotification(`Welcome! Logged in as User ID: ${userId} (${phone})`, 'success');
    }
}

// Make toggleAccountMenu globally available
window.toggleAccountMenu = function() {
    console.log('toggleAccountMenu called - toggling account menu');

    // Close any existing login dropdown first
    const loginDropdown = document.getElementById('loginDropdown');
    if (loginDropdown) {
        loginDropdown.classList.remove('active');
        console.log('Closed existing login dropdown');
    }

    // Toggle the existing account dropdown menu
    let accountMenu = document.getElementById('accountMenu');

    if (!accountMenu) {
        console.log('Creating new account menu');
        accountMenu = document.createElement('div');
        accountMenu.id = 'accountMenu';
        accountMenu.className = 'account-menu';
        accountMenu.style.cssText = `
            position: absolute;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            min-width: 180px;
            z-index: 10001;
            overflow: hidden;
            opacity: 1;
            visibility: visible;
        `;

        console.log('Account menu styled and ready');

        // Create menu items without inline onclick handlers
        const ordersItem = document.createElement('div');
        ordersItem.style.cssText = 'padding: 15px 20px; cursor: pointer; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 10px; background: white; transition: background 0.2s;';
        ordersItem.innerHTML = '<i class="fas fa-shopping-bag" style="color: #007bff; font-size: 16px;"></i><span style="font-weight: 500;">My Orders</span>';
        ordersItem.onclick = () => window.location.href = '/Robotech-storeP2/orders';

        const logoutItem = document.createElement('div');
        logoutItem.style.cssText = 'padding: 15px 20px; cursor: pointer; display: flex; align-items: center; gap: 10px; background: white; transition: background 0.2s;';
        logoutItem.innerHTML = '<i class="fas fa-sign-out-alt" style="color: #dc3545; font-size: 16px;"></i><span style="font-weight: 500;">Logout</span>';
        logoutItem.onclick = () => logout();

        // Add hover effects
        [ordersItem, logoutItem].forEach(item => {
            item.onmouseover = () => item.style.background = '#f8f9fa';
            item.onmouseout = () => item.style.background = 'white';
        });

        // Append items to menu
        accountMenu.appendChild(ordersItem);
        accountMenu.appendChild(logoutItem);

        console.log('Account menu HTML set:', accountMenu.innerHTML);

        document.body.appendChild(accountMenu);
        console.log('Account menu created and added to body');

        // Position the menu below the login trigger
        const trigger = document.querySelector('.login-trigger');
        if (trigger) {
        const rect = trigger.getBoundingClientRect();
            accountMenu.style.position = 'fixed';
            accountMenu.style.top = (rect.bottom + window.scrollY + 5) + 'px';
            accountMenu.style.left = (rect.left + window.scrollX) + 'px';
            accountMenu.style.display = 'block';
            accountMenu.style.visibility = 'visible';
            console.log('Account menu positioned at:', accountMenu.style.top, accountMenu.style.left);
        } else {
            console.error('Login trigger not found for positioning');
            // Fallback positioning
            accountMenu.style.position = 'fixed';
            accountMenu.style.top = '60px';
            accountMenu.style.right = '20px';
            accountMenu.style.display = 'block';
            accountMenu.style.visibility = 'visible';
        }

        // Add click outside handler
        const closeMenu = (e) => {
            // Only close if click is outside both menu and trigger
            if (accountMenu && !accountMenu.contains(e.target) && trigger && !trigger.contains(e.target)) {
                console.log('Click outside account menu, removing menu');
                if (accountMenu.parentNode) {
                    accountMenu.parentNode.removeChild(accountMenu);
                }
                document.removeEventListener('click', closeMenu);
            }
        };

        // Add handler after a short delay to prevent immediate closing
        setTimeout(() => {
            document.addEventListener('click', closeMenu);
            console.log('Click outside handler added for account menu');
        }, 10);

    } else {
        console.log('Toggling existing account menu');
        // Toggle visibility of existing menu
        if (accountMenu.style.display === 'none' || accountMenu.style.display === '') {
            accountMenu.style.display = 'block';
            accountMenu.style.visibility = 'visible';

            // Position the menu below the login trigger
            const trigger = document.querySelector('.login-trigger') || document.querySelector('.user-trigger');
            if (trigger) {
                const rect = trigger.getBoundingClientRect();
                accountMenu.style.position = 'fixed';
                accountMenu.style.top = (rect.bottom + window.scrollY + 5) + 'px';
                accountMenu.style.left = (rect.left + window.scrollX) + 'px';
                console.log('Account menu positioned at:', accountMenu.style.top, accountMenu.style.left);
            }

            // Add click outside handler
            const closeMenu = (e) => {
                if (accountMenu && !accountMenu.contains(e.target) && trigger && !trigger.contains(e.target)) {
                    console.log('Click outside account menu, hiding menu');
                    accountMenu.style.display = 'none';
                    document.removeEventListener('click', closeMenu);
                }
            };

            // Add handler after a short delay to prevent immediate closing
            setTimeout(() => {
                document.addEventListener('click', closeMenu);
                console.log('Click outside handler added for account menu');
            }, 10);
        } else {
            accountMenu.style.display = 'none';
        }
    }
}


// Make logout globally available
window.logout = function() {
    // DEMO MODE: Mock logout
    console.log('Demo logout for user:', JSON.stringify(currentUser));

    // Simulate successful logout
    // Clear both sessionStorage and localStorage
            sessionStorage.removeItem('user_id');
            sessionStorage.removeItem('phone');
            sessionStorage.removeItem('logged_in');

    localStorage.removeItem('user_id');
    localStorage.removeItem('phone');
    localStorage.removeItem('logged_in');

    // Clear demo cart
    if (currentUser) {
        localStorage.removeItem('demo_cart_' + currentUser.user_id);
    }

            // Reset current user
            currentUser = null;

            // Reset login button
            const loginText = document.getElementById('loginText');
            if (loginText) {
                loginText.textContent = 'Login';
            }

            const loginTrigger = document.querySelector('.login-trigger');
            if (loginTrigger) {
                loginTrigger.onclick = () => toggleLoginDropdown();
            }

            // Close account menu if open
            const accountMenu = document.getElementById('accountMenu');
            if (accountMenu) {
                accountMenu.remove();
            }

            // Update cart count
            updateCartCount();

            showNotification('Logged out successfully', 'success');
}

// Mobile Menu Functionality
function setupMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mainNav = document.getElementById('mainNav');
    
    if (!mobileMenuToggle || !mainNav) return;
    
    // Create mobile menu overlay and navigation
    const mobileMenuOverlay = document.createElement('div');
    mobileMenuOverlay.className = 'mobile-menu-overlay';
    mobileMenuOverlay.id = 'mobileMenuOverlay';
    
    const mobileNav = document.createElement('nav');
    mobileNav.className = 'mobile-nav';
    mobileNav.id = 'mobileNav';
    
    // Build mobile nav HTML manually for better control
    let mobileNavHTML = `
        <div class="mobile-nav-header">
            <div class="logo">
                <i class="fas fa-robot"></i>
                <span>Robotech Store</span>
            </div>
            <button class="mobile-nav-close" id="mobileNavClose" aria-label="Close menu">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="mobile-nav-content">
            <a href="/" class="mobile-nav-link active" onclick="closeMobileMenu()">Home</a>
            <div class="mobile-nav-dropdown">
                <div class="mobile-nav-dropdown-toggle">
                    <span>Products</span>
                    <i class="fas fa-chevron-down"></i>
                </div>
                <div class="mobile-nav-dropdown-menu">
                    <div style="padding: 0.5rem 0;">
                        <h4 style="padding: 0.75rem 1.5rem 0.5rem; font-size: 0.9rem; color: var(--primary-color); font-weight: 600;">Components</h4>
                        <a href="/products?category=Crystal%20Oscillators" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Crystal Oscillators</a>
                        <a href="/products?category=Resistors" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Resistors</a>
                        <a href="/products?category=Capacitors" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Capacitors</a>
                        <a href="/products?category=Inductors" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Inductors</a>
                        <a href="/products?category=LEDs" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">LEDs</a>
                        <a href="/products?category=Diodes" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Diodes</a>
                        <a href="/products?category=Transistors" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Transistors</a>
                    </div>
                    <div style="padding: 0.5rem 0;">
                        <h4 style="padding: 0.75rem 1.5rem 0.5rem; font-size: 0.9rem; color: var(--primary-color); font-weight: 600;">Development Boards</h4>
                        <a href="/products?category=Arduino" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Arduino Compatible</a>
                        <a href="/products?category=Raspberry%20Pi" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Raspberry Pi</a>
                        <a href="/products?category=ESP" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">NodeMCU/ESP</a>
                        <a href="/products?category=STM" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">STM</a>
                        <a href="/products?category=PIC" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">PIC/ATMEL</a>
                        <a href="/products?category=Programmers" class="mobile-nav-dropdown-link" onclick="closeMobileMenu()">Programmers</a>
                    </div>
                </div>
            </div>
            <a href="#categories" class="mobile-nav-link" onclick="scrollToSection('categories'); closeMobileMenu(); return false;">Categories</a>
            <a href="#about" class="mobile-nav-link" onclick="scrollToSection('about'); closeMobileMenu(); return false;">About</a>
            <a href="#contact" class="mobile-nav-link" onclick="scrollToSection('contact'); closeMobileMenu(); return false;">Contact</a>
        </div>
    `;
    
    mobileNav.innerHTML = mobileNavHTML;
    
    document.body.appendChild(mobileMenuOverlay);
    document.body.appendChild(mobileNav);
    
    // Close mobile menu function
    window.closeMobileMenu = function() {
        mobileMenuOverlay.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
    };
    
    // Toggle mobile menu
    mobileMenuToggle.addEventListener('click', function() {
        mobileMenuOverlay.classList.add('active');
        mobileNav.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    // Close mobile menu
    const mobileNavClose = document.getElementById('mobileNavClose');
    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', closeMobileMenu);
    }
    
    mobileMenuOverlay.addEventListener('click', closeMobileMenu);
    
    // Handle mobile dropdowns
    const mobileDropdownToggles = mobileNav.querySelectorAll('.mobile-nav-dropdown-toggle');
    mobileDropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const dropdown = this.parentElement;
            dropdown.classList.toggle('active');
        });
    });
}

// Export functions for global use
window.addToCart = addToCart;
window.buyNow = buyNow;
window.filterByCategory = filterByCategory;
window.scrollToSection = scrollToSection;
