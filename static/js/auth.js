// Authentication JavaScript for Robotech Store
console.log('🔐 Auth.js file loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    console.log('Auth.js DOMContentLoaded fired');
    setupAuthEventListeners();
    checkAuthRedirect();
});

// Also try to initialize immediately in case DOMContentLoaded already fired
if (document.readyState === 'loading') {
    // Document still loading, wait for DOMContentLoaded
} else {
    // Document already loaded, initialize immediately
    console.log('Document already loaded, initializing auth immediately');
    initializeAuth();
}

function setupAuthEventListeners() {
    console.log('Setting up auth event listeners');

    // Phone login form
    const phoneForm = document.getElementById('phoneLoginForm');
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    const verifyOtpBtn = document.getElementById('verifyOtpBtn');

    console.log('Phone form:', phoneForm);
    console.log('Send OTP button:', sendOtpBtn);
    console.log('Verify OTP button:', verifyOtpBtn);

    if (sendOtpBtn) {
        console.log('Adding click listener to send OTP button');
        sendOtpBtn.addEventListener('click', function(e) {
            console.log('Send OTP button clicked via event listener');
            e.preventDefault();
            sendOTP();
        });
    } else {
        console.log('Send OTP button not found!');
    }

    if (verifyOtpBtn) {
        verifyOtpBtn.addEventListener('click', verifyOTP);
    }

    if (phoneForm) {
        phoneForm.addEventListener('submit', function(e) {
            e.preventDefault();
            verifyOTP();
        });
    }

    // OTP input validation
    const otpInput = document.getElementById('otp');
    if (otpInput) {
        otpInput.addEventListener('input', function(e) {
            // Only allow numbers
            this.value = this.value.replace(/[^0-9]/g, '');

            // Auto-submit when 6 digits entered
            if (this.value.length === 6) {
                verifyOTP();
            }
        });
    }

    // Phone number input validation
    const phoneInput = document.getElementById('phoneNumber');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Only allow numbers and limit to 10 digits
            this.value = this.value.replace(/[^0-9]/g, '').substring(0, 10);
        });
    }
}

function showLoginTab(tabType) {
    // Update tab buttons
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[onclick="showLoginTab('${tabType}')"]`).classList.add('active');

    // Update tab content
    document.querySelectorAll('.auth-tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabType}LoginTab`).classList.add('active');
}

function sendOTP() {
    console.log('sendOTP function called');

    const phoneInput = document.getElementById('phoneNumber');
    const phone = phoneInput.value.trim();

    console.log('Phone input value:', phone);

    if (!validatePhoneNumber(phone)) {
        console.log('Phone validation failed');
        showNotification('Please enter a valid 10-digit phone number', 'error');
        phoneInput.focus();
        return;
    }

    console.log('Phone validation passed, calling server API');

    // Show loading state
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    sendOtpBtn.disabled = true;
    sendOtpBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // DEMO MODE: Mock send OTP API
    console.log('Demo mode: Mock send OTP API called for phone:', phone);

    // Simulate API delay
    setTimeout(() => {
        // Mock successful OTP send response
        const mockResponse = {
            success: true,
            otp: '123456', // Always use demo OTP
            message: 'OTP sent successfully'
        };

        console.log('Mock OTP send success:', mockResponse);

            // Show OTP input field
            document.getElementById('otpGroup').style.display = 'block';
            document.getElementById('sendOtpBtn').style.display = 'none';
            document.getElementById('verifyOtpBtn').style.display = 'block';

            // Start OTP timer
            startOTPTimer();

            // Reset button
            sendOtpBtn.disabled = false;
            sendOtpBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';

            // Focus on OTP input
            document.getElementById('otp').focus();

        // Show the demo OTP
        const serverOTP = mockResponse.otp;
            console.log('========================================');
            console.log(`🔐 DEMO OTP for ${phone}: ${serverOTP}`);
            console.log('========================================');

            // Display OTP to user
            try {
                alert(`🔐 DEMO OTP\n\n📱 Your OTP Code: ${serverOTP}\n\n📝 Enter this code in the login form.`);
                console.log('Alert shown successfully');
            } catch (alertError) {
                console.error('Alert failed:', alertError);
            }

            showNotification('OTP sent successfully! Check the popup for your code.', 'success');
    }, 800); // Simulate 0.8 second API delay
}

function verifyOTP() {
    const phoneInput = document.getElementById('phoneNumber');
    const otpInput = document.getElementById('otp');
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
    const verifyBtn = document.getElementById('verifyOtpBtn');
    verifyBtn.disabled = true;
    verifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    // Prepare login data
    const loginData = {
        phone: phone,
        otp: otp
    };

    // DEMO MODE: Mock login API
    console.log('Demo mode: Mock login API called with:', loginData);

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

            console.log('Mock login success:', mockResponse);

            // Set current user and store login data
            if (typeof currentUser !== 'undefined') {
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

                console.log('Login successful, user data stored:', currentUser);
            }

            showNotification('Login successful! Welcome to Robotech Store!', 'success');

            // Redirect to products page after login
            setTimeout(() => {
                window.location.href = 'products.html';
            }, 1500);
        } else {
            // Mock failed login
            console.log('Mock login failed - invalid OTP');
            showNotification('Invalid OTP. Please try again.', 'error');
            verifyBtn.disabled = false;
            verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify OTP';
        }
    }, 1000); // Simulate 1 second API delay
}

function loginWithGmail() {
    // Show loading state
    const gmailBtn = document.querySelector('.btn-gmail');
    gmailBtn.disabled = true;
    gmailBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';

    // In a real implementation, this would integrate with Google OAuth
    // For demo purposes, we'll simulate a successful login

    setTimeout(() => {
        showNotification('Gmail authentication not implemented yet. Use phone login instead.', 'warning');
        gmailBtn.disabled = false;
        gmailBtn.innerHTML = '<i class="fab fa-google"></i> Continue with Google';
    }, 2000);
}

function startOTPTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('otpTimer');
    const resendBtn = document.getElementById('resendOtpBtn');

    const timer = setInterval(() => {
        timerElement.textContent = `Resend OTP in ${timeLeft}s`;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            timerElement.textContent = 'OTP expired';
            resendBtn.disabled = false;
            resendBtn.addEventListener('click', resendOTP);
        }
    }, 1000);
}

function resendOTP() {
    const phoneInput = document.getElementById('phoneNumber');
    const phone = phoneInput.value.trim();

    if (!validatePhoneNumber(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }

    // Reset OTP input
    document.getElementById('otp').value = '';

    // Disable resend button
    const resendBtn = document.getElementById('resendOtpBtn');
    resendBtn.disabled = true;

    // Send new OTP
    sendOTP();
}

function validatePhoneNumber(phone) {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone);
}

function generateDemoOTP() {
    // Generate a random 6-digit OTP for demo purposes
    return Math.floor(100000 + Math.random() * 900000).toString();
}


function checkAuthRedirect() {
    // Check if user was redirected here after trying to access protected content
    const urlParams = new URLSearchParams(window.location.search);
    const redirect = urlParams.get('redirect');

    if (redirect) {
        showNotification('Please login to continue', 'info');
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
