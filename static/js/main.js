
// Accessory Hub JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const originalText = this.textContent;
            
            // Mobile-friendly feedback
            this.textContent = 'Adding...';
            this.disabled = true;

            // Send AJAX request to add item to cart
            fetch('/add-to-cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: productId }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.textContent = 'Added!';
                        // Show mobile-friendly notification
                        showMobileNotification('Product added to cart!');
                        // Update cart count if navbar has cart counter
                        updateCartCount();
                    } else {
                        this.textContent = 'Try Again';
                        showMobileNotification(data.message || 'Error adding product to cart.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.textContent = 'Error';
                    showMobileNotification('Error adding product to cart.', 'error');
                })
                .finally(() => {
                    // Reset button after delay
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.disabled = false;
                    }, 2000);
                });
        });
    });

    // Mobile menu toggle
    const menuToggle = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            
            // Close menu when clicking outside on mobile
            document.addEventListener('click', closeMenuOutside, { once: true });
        });
    }
    
    // Function to close menu when clicking outside
    function closeMenuOutside(event) {
        if (!navLinks.contains(event.target) && !menuToggle.contains(event.target)) {
            navLinks.classList.remove('active');
        }
    }

    // Mobile notification system
    function showMobileNotification(message, type = 'success') {
        // Remove existing notifications
        const existing = document.querySelector('.mobile-notification');
        if (existing) {
            existing.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `mobile-notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'error' ? '#ef4444' : '#10b981'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 10000;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            animation: slideInDown 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutUp 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Update cart count in navbar (if cart counter exists)
    function updateCartCount() {
        // This could be enhanced to show actual cart count
        const cartLink = document.querySelector('a[href="/cart"]');
        if (cartLink) {
            // Add a small visual indicator
            cartLink.style.position = 'relative';
        }
    }

    // Add CSS animations for notifications
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInDown {
            from {
                transform: translate(-50%, -100%);
                opacity: 0;
            }
            to {
                transform: translate(-50%, 0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutUp {
            from {
                transform: translate(-50%, 0);
                opacity: 1;
            }
            to {
                transform: translate(-50%, -100%);
                opacity: 0;
            }
        }
        
        .mobile-notification {
            max-width: 90%;
            text-align: center;
        }
        
        @media (max-width: 480px) {
            .mobile-notification {
                top: 70px;
                font-size: 13px;
                padding: 10px 16px;
            }
        }
    `;
    document.head.appendChild(style);
});
