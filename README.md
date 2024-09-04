# Inventory Management System

## Overview

This project is an Inventory Management System built with Django. It allows retailers to manage their inventory by adding, updating, and deleting products, and shoppers to view and add products to their cart. The system also includes an admin panel for overall management.

## Features

### Retailer Panel
- **Dashboard**: Overview of inventory items.
- **Add Inventory**: Form to add new inventory items.
- **Update Inventory**: Form to update existing inventory items.
- **Delete Inventory**: Confirmation page to delete inventory items.
- **Upload Inventory**: Upload inventory items via CSV or TXT file.

### Shopper Panel
- **Dashboard**: Overview of available products.
- **Add to Cart**: Form to add products to the cart.
- **View Cart**: View items added to the cart.

### Admin Panel
- **Dashboard**: Overview of total users, active users, retailers, shoppers, products, and categories.
- **Manage Categories**: Add, update, and delete product categories.
- **Manage Users**: View all users.
- **Manage Inventory**: View all inventory items.

## API Endpoints

### Authentication
- **Register**: `/accounts/api/register/`
- **Login**: `/accounts/api/login/`

### Retailer Panel
- **Dashboard**: GET `/retailer-panel/dashboard/`
- **Retailer Edit Profile** : PUT `retailer-panel/profile/edit/`
- **Add Inventory**: POST `/retailer-panel/inventory/add/`
- **List Inventory** GET `/retailer-panel/inventory/`
- **Update Inventory**: PUT/PATCH `/retailer-panel/inventory/<int:pk>/`
- **Delete Inventory**: DELETE `/retailer-panel/inventory/<int:pk>/`
- **Upload Inventory**: `/api/upload-inventory/`
- **List and create Promotion**: GET/POST `/retailer-panel/promotions/`

### Shopper Panel
- **Shopper Dashboard**: GET `/shopper-panel/dashboard/`
- **Shopper Edit Profile** : PUT `shopper-panel/profile/edit/`
- **Add to Cart**: POST `/shopper-panel/cart/add/`
- **Remove from Cart**: DELETE `/shopper-panel/cart/remove/`
- **View Cart**: GET `/shopper-panel/cart/`
- **Fetch Single Product**: GET `/shopper-panel/products/<int:pk>/`
- **Fetch Products Belonging to a Retailer**: GET `/shopper-panel/retailers/<int:retailer_id>/products/`

### Admin Panel
- **Dashboard**: `/admin-panel/dashboard/`
- **Categories**: `/admin-panel/categories/`
- **Add Category**: `/admin-panel/categories/add/`
- **Edit Category**: `/admin-panel/categories/edit/<int:category_id>/`
- **Delete Category**: `/admin-panel/categories/delete/<int:category_id>/`
- **Users**: `/admin-panel/users/`
- **Inventory**: `/admin-panel/inventory/`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JoshAjikaze/StockInch-Inventory-Backend.git
    cd inventory_app
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000/`.(stockinch.ng)

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/`.
- Log in as a retailer to manage inventory.
- Log in as a shopper to browse products and manage the cart.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
-pending (_)

