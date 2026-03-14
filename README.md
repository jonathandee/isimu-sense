.

🌾 Isimu Sense – Farm Management System
Isimu Sense is a modular farm management system designed to support day‑to‑day agricultural operations.
The platform integrates crop production, livestock management, inventory tracking, financial records, and reporting into a single application.

The system was developed using Python (Flask) and PostgreSQL and is currently being used to support real farm operations.

🚜 Features
Crop Management
Crop type configuration

Field management

Planting records

Input applications (fertilizers, chemicals, etc.)

Harvest tracking

Operational validations (e.g., planting dates, field conflicts)

Livestock Management
Animal registration

Weight tracking

Feed records

Health records

Production tracking

Inventory Management
Inventory categories

Stock tracking

Inventory deduction during farm operations

Low stock monitoring

Financial Management
Income tracking

Expense tracking

Financial categories

Financial reports

Reporting & Analytics
Crop production reports

Livestock reports

Inventory reports

Financial summaries

Farm operational insights

Authentication & Security
User login and logout

Password hashing

Role support (admin / user)

Blueprint‑level access control

🧱 System Architecture
The application follows a modular Flask architecture.

isimu_sense
│
├── app
│   ├── routes
│   │   ├── crop_routes.py
│   │   ├── livestock_routes.py
│   │   ├── inventory_routes.py
│   │   ├── finance_routes.py
│   │   ├── report_routes.py
│   │   └── auth_routes.py
│   │
│   ├── templates
│   ├── static
│   ├── models.py
│   └── __init__.py
│
├── migrations
├── run.py
├── requirements.txt
└── README.md
🗄 Database
The system uses PostgreSQL with SQLAlchemy ORM.

Database migrations are handled using:

Flask‑Migrate (Alembic)
This allows safe schema changes without losing operational data.

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/isimu_sense.git
cd isimu_sense
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Configure PostgreSQL
Create a database:

createdb isimu_sense
Update database URI if necessary:

postgresql://localhost/isimu_sense
4️⃣ Run database migrations
flask db upgrade
5️⃣ Run the application
python run.py
Open in browser:

http://127.0.0.1:5000
👤 Create Admin User
Run:

python create_admin.py
Then login using the admin credentials.

🔐 Data Integrity Rules
Operational records are not deleted to preserve historical farm data.

Editable operational records include:

plantings

applications

harvest records

financial transactions

livestock records

Configuration records that can be modified include:

crop types

fields

inventory categories

🛠 Technology Stack
Python

Flask

PostgreSQL

SQLAlchemy

Flask‑Migrate

Bootstrap

Git

📦 Current Status
Version: V1.0
Status: Operational
Deployment: Local farm system
The system is currently undergoing operational testing before further enhancements in V1.1.

🌱 Future Improvements (Planned)
Farm dashboard analytics

Inventory alerts

Data export (CSV / Excel)

Mobile‑friendly interface

👨‍🌾 Author
Developed by JonathanD_Agri_Tec
Farm Management System Developer & Agricultural Operator

