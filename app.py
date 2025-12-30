from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SECRET_KEY
from config import SUPABASE_URL, SUPABASE_KEY, SECRET_KEY
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Supabase setup
# Supabase setup
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Admin Configuration
ADMIN_EMAIL = "testadmin@accesoryhub.com"

def is_admin_user():
    if 'user' not in session:
        return False
    return session['user']['email'] == ADMIN_EMAIL

@app.context_processor
def inject_admin_status():
    return dict(is_admin=is_admin_user())

@app.route('/')
def home():
    # Fetch featured products from Supabase
    response = supabase.table('products').select('*').limit(6).execute()
    featured_products = response.data if response.data else []
    return render_template('home.html', featured_products=featured_products)

@app.route('/shop')
def shop():
    # Fetch all products from Supabase
    response = supabase.table('products').select('*').execute()
    products = response.data if response.data else []
    return render_template('shop.html', products=products)

@app.route('/product/<product_id>')
def product_details(product_id):
    # Fetch product details from Supabase
    response = supabase.table('products').select('*').eq('id', product_id).execute()
    product = response.data[0] if response.data else None
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    # Fetch cart items with product details
    response = supabase.table('cart_items').select('*, products(*)').eq('user_id', user_id).execute()
    cart_items = response.data if response.data else []
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    product_id = data.get('product_id')
    user_id = session['user']['id']

    # Check if item already in cart
    existing = supabase.table('cart_items').select('*').eq('user_id', user_id).eq('product_id', product_id).execute()

    if existing.data:
        # Update quantity
        new_quantity = existing.data[0]['quantity'] + 1
        response = supabase.table('cart_items').update({'quantity': new_quantity}).eq('id', existing.data[0]['id']).execute()
    else:
        # Add new item
        cart_item = {
            'user_id': user_id,
            'product_id': product_id,
            'quantity': 1
        }
        response = supabase.table('cart_items').insert(cart_item).execute()

    if response.data:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error adding to cart'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # For MVP, we'll use Supabase Auth
        try:
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user'] = {
                'id': auth_response.user.id,
                'email': auth_response.user.email
            }
            return redirect(url_for('home'))
        except Exception as e:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        try:
            auth_response = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {
                        "name": name
                    }
                }
            })
            
            # Try to create user profile in users table (this may fail due to RLS)
            try:
                user_data = {
                    'id': auth_response.user.id,
                    'email': email,
                    'name': name
                }
                supabase.table('users').insert(user_data).execute()
                print("User profile created successfully")
            except Exception as profile_error:
                # This is likely due to RLS policies - the trigger should handle it
                print(f"Profile creation failed (may be handled by trigger): {profile_error}")
                # Continue with registration even if profile creation fails
            
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Registration error: {str(e)}")
            error_message = str(e)
            # Provide more user-friendly error messages
            if "already registered" in error_message.lower():
                error_message = "An account with this email already exists"
            elif "password" in error_message.lower():
                error_message = "Password should be at least 6 characters"
            else:
                error_message = "Registration failed. Please try again."
            
            return render_template('register.html', error=error_message)

    return render_template('register.html')

@app.route('/update-cart', methods=['POST'])
def update_cart():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')

    if quantity <= 0:
        # Remove item if quantity is 0 or less
        response = supabase.table('cart_items').delete().eq('id', cart_item_id).execute()
    else:
        response = supabase.table('cart_items').update({'quantity': quantity}).eq('id', cart_item_id).execute()

    if response.data:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating cart'})

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    cart_item_id = data.get('cart_item_id')

    response = supabase.table('cart_items').delete().eq('id', cart_item_id).execute()

    if response.data:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error removing item'})

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    # Fetch cart items with product details
    response = supabase.table('cart_items').select('*, products(*)').eq('user_id', user_id).execute()
    cart_items = response.data if response.data else []

    # Calculate total
    total = sum(item['products']['price'] * item['quantity'] for item in cart_items)

    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place-order', methods=['POST'])
def place_order():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    delivery_details = data.get('delivery_details')
    user_id = session['user']['id']

    # Fetch cart items
    cart_response = supabase.table('cart_items').select('*, products(*)').eq('user_id', user_id).execute()
    cart_items = cart_response.data if cart_response.data else []

    if not cart_items:
        return jsonify({'success': False, 'message': 'Cart is empty'})

    # Calculate total
    total = sum(item['products']['price'] * item['quantity'] for item in cart_items)

    # Create order
    order_data = {
        'user_id': user_id,
        'total_amount': total,
        'delivery_details': delivery_details,
        'status': 'Pending'
    }

    order_response = supabase.table('orders').insert(order_data).execute()

    if order_response.data:
        order_id = order_response.data[0]['id']
        # Clear cart
        supabase.table('cart_items').delete().eq('user_id', user_id).execute()
        return jsonify({'success': True, 'order_id': order_id})
    else:
        return jsonify({'success': False, 'message': 'Error creating order'})

@app.route('/order-success')
def order_success():
    return render_template('order_success.html')

@app.route('/my-orders')
def my_orders():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    response = supabase.table('orders').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
    orders = response.data if response.data else []

    return render_template('my_orders.html', orders=orders)

@app.route('/logout')
def logout():
    session.pop('user', None)
    supabase.auth.sign_out()
    return redirect(url_for('home'))

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    if not is_admin_user():
        return redirect(url_for('home'))
        
    # Fetch all products
    products_header = supabase.table('products').select('*').execute()
    products = products_header.data if products_header.data else []
    
    # Fetch all orders
    orders_header = supabase.table('orders').select('*').order('created_at', desc=True).execute()
    orders = orders_header.data if orders_header.data else []
    
    return render_template('admin.html', products=products, orders=orders, admin_email=ADMIN_EMAIL)

@app.route('/admin/add-product', methods=['POST'])
def admin_add_product():
    if not is_admin_user():
        return jsonify({'success': False, 'message': 'Unauthorized'})
        
    try:
        data = {}
        
        # Handle regular form fields
        data['name'] = request.form.get('name')
        data['price'] = request.form.get('price')
        data['description'] = request.form.get('description')
        data['stock_quantity'] = request.form.get('stock_quantity')
        
        image_url = request.form.get('image_url')
        
        # Handle file upload if present
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                # Add timestamp to avoid collisions
                unique_filename = f"{int(time.time())}_{filename}"
                file_content = file.read()
                
                # Upload to Supabase Storage
                bucket_name = "product-images"
                content_type = file.content_type
                
                # Note: supabase-py storage upload currently needs file options for content-type
                storage_response = supabase.storage.from_(bucket_name).upload(
                    path=unique_filename,
                    file=file_content,
                    file_options={"content-type": content_type}
                )
                
                # Get public URL
                public_url_response = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
                image_url = public_url_response # It returns the URL directly in recent versions or we verify
                
        data['image_url'] = image_url
        
        supabase.table('products').insert(data).execute()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding product: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete-product', methods=['POST'])
def admin_delete_product():
    if not is_admin_user():
        return jsonify({'success': False, 'message': 'Unauthorized'})
        
    product_id = request.json.get('product_id')
    try:
        supabase.table('products').delete().eq('id', product_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/update-order', methods=['POST'])
def admin_update_order():
    if not is_admin_user():
        return jsonify({'success': False, 'message': 'Unauthorized'})
        
    data = request.json
    order_id = data.get('order_id')
    new_status = data.get('status')
    
    try:
        supabase.table('orders').update({'status': new_status}).eq('id', order_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run()
