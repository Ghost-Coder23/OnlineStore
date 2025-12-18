🧠 Accessory Hub – Site Look & User Flow (Complete Overview)
🌐 1. LANDING / HOME PAGE (/)
What the user sees:

Top Navigation Bar

Logo: Accessory Hub

Links: Home | Shop | Cart | Login/Register

Hero Section

Big headline:
“Premium Tech Accessories at Affordable Prices”

Subtext:
Chargers • Earphones • USB Cables • Power Banks

“Shop Now” button

Featured Products Grid

Product image

Product name

Price

“Add to Cart” button

Footer

About | Contact | Social links

User thought:

“This is a clean tech store. Let me browse.”

🛍️ 2. SHOP / PRODUCTS PAGE (/shop)
Layout:

Left side:

Categories (Chargers, Headphones, Cables, Adapters)

Price filter (optional later)

Main area:

Grid of products (cards)

Product Card:
[ Image ]
USB-C Fast Charger
R299
[ Add to Cart ]

User action:

Scroll

Click a product

Add to cart without logging in (session-based cart)

📦 3. PRODUCT DETAILS PAGE (/product/<id>)
Layout:

Left: Large product image

Right:

Product name

Price (bold)

Stock status

Quantity selector (+ / -)

“Add to Cart” button

Short description

Below:

Full description

Compatibility (Android, iPhone, Laptop)

User thought:

“This looks good. I’ll buy this.”

🛒 4. CART PAGE (/cart)
Layout:

Table/list of cart items:

Product | Price | Qty | Subtotal | Remove


Quantity buttons

Total Price

Buttons:

“Continue Shopping”

“Checkout”

Behavior:

If user not logged in:
→ Prompt: “Please login or register to continue”

🔐 5. LOGIN / REGISTER PAGE (/login, /register)
Simple and clean:

Email

Password

Register link if new user

After login:
➡ Redirect back to Checkout

💳 6. CHECKOUT PAGE (/checkout)
Sections:

Delivery Details

Name

Phone number

Address

Order Summary

Products

Total amount

Payment Button

“Place Order”

For MVP: order is saved, status = “Pending”

Later:

Add Paystack / Stripe

✅ 7. ORDER CONFIRMATION PAGE (/order-success)

Message:

🎉 Order Placed Successfully!
We will contact you shortly.

Buttons:

View Orders

Back to Shop

👤 8. USER DASHBOARD (/my-orders)

User sees:

Order ID

Date

Items

Status (Pending, Shipped, Delivered)

Simple table.

🛠️ 9. ADMIN DASHBOARD (/admin)

Only for you (admin).

Sections:

Add Product

Name

Price

Description

Upload Image

Manage Products

Edit

Delete

Orders

Customer name

Total

Status update

Admin thought:

“I can manage my store easily.”

🎨 Overall Design Style

Colors:

Dark blue / black + white

Accent color: orange or green

Font:

Clean sans-serif (Poppins, Roboto)

Style:

Minimal

Modern

Mobile-friendly

Think:

Jumia × Apple Store (simple version)

🔁 FULL USER FLOW (Summary)
Home → Shop → Product → Add to Cart
→ Cart → Login/Register → Checkout
→ Order Success → My Orders


Admin flow:

Admin Login → Dashboard → Add Products → Manage Orders
