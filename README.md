# Production and Packaging Management System

This Django app is part of a larger factory management system and is responsible for managing production and packaging processes. It tracks models, sizes, pieces, cartons, and production details, providing a comprehensive overview of the production lifecycle.

---

## Features

- **Model Management**: Create, update, and archive models with details like model number, creation date, and shipping status.
- **Size and Amount Tracking**: Track sizes and quantities for each model.
- **Piece Management**: Manage individual pieces, including their types, sizes, and available/used amounts.
- **Production Tracking**: Record production details, including used amounts and factory assignments.
- **Carton and Packaging**: Manage carton dimensions, types, and usage for packaging.
- **Factory Management**: Track factory statuses and their production contributions.
- **PDF Reporting**: Generate PDF reports for production details.
- **Archive and Shipping**: Archive models and mark them as shipped when completed.

---

## Models Overview

### 1. **Model**
   - Tracks model details such as model number, creation date, and shipping status.
   - Includes utility methods for calculating available cartons, usage percentages, and production stats.

### 2. **SizeAmount**
   - Tracks sizes and quantities for each model.
   - Includes packing details (e.g., pieces per carton).

### 3. **Piece**
   - Represents individual pieces of a model, including type, size, and available/used amounts.

### 4. **Factory**
   - Tracks factory details and their current status (e.g., working, stopped, completed).

### 5. **ProductionPiece**
   - Records production details, including used amounts, factory assignments, and comments.

### 6. **Carton**
   - Manages carton dimensions, types, and usage for packaging.

### 7. **Packing**
   - Tracks carton usage for packaging and updates model-level carton usage.

---

## URLs and Views

The app includes the following URLs and views:

- **Model Management**:
  - List, create, update, and delete models.
  - Archive and mark models as shipped.

- **Size and Amount Management**:
  - Add, edit, and delete sizes and amounts for models.

- **Production Management**:
  - Record and manage production pieces.
  - List production details.

- **Carton and Packaging**:
  - Add, edit, and delete cartons.
  - Manage packing details and list packing records.

- **Factory Management**:
  - List, create, update, and delete factories.

- **PDF Reporting**:
  - Generate PDF reports for production details.

---

## Setup Instructions

### Prerequisites
- Python 3.x
- Django 3.x or later
- Bootstrap (for frontend styling)
- JavaScript (for dynamic functionality)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mego354/Honest.git
   cd Honest
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
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

7. Access the app at `http://localhost:8000`.

---

## Usage

1. **Add a Model**:
   - Navigate to the "Create Model" page and fill in the details (e.g., model number, creation date).

2. **Add Sizes and Amounts**:
   - For each model, add sizes and quantities using the "Add Size" form.

3. **Record Production**:
   - Use the "Production Form" to record production details, including used amounts and factory assignments.

4. **Manage Cartons**:
   - Add cartons for each model and track their usage in the packaging process.

5. **Generate Reports**:
   - Use the "Generate PDF" feature to create production reports.

---

## Code Structure

- **Models**: Defined in `models.py`.
- **Views**: Defined in `views.py`.
- **URLs**: Configured in `urls.py`.
- **Templates**: Located in the `templates` folder.
- **Static Files**: Located in the `static` folder (CSS, JS, images).

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---
