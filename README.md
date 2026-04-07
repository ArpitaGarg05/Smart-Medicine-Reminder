<<<<<<< HEAD
# Smart Medicine Reminder App
Complete Django web app for prescription OCR, AI parsing, medicine confirmation, reminders, and stock alerts.
## Features
- User authentication (register, login, logout)
- Upload prescription image
- OCR extraction with `pytesseract`
- AI parsing with Google Gemini API
- Editable medicine confirmation before save
- Medicines list and stock tracking
- Daily reminders with mark-as-taken flow
- Dashboard with low stock alerts
## Setup
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Set Gemini API key:
   - Windows PowerShell: `$env:GEMINI_API_KEY="AIzaSyASsC3-D9pJzxmmexos6C5EyCPAMcSriVo"`
3. Install Tesseract OCR engine on your system and ensure `tesseract` is available in PATH.
4. Run migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
5. Create admin user (optional):
   - `python manage.py createsuperuser`
6. Run server:
   - `python manage.py runserver`
## App Flow
1. Register/Login
2. Upload prescription image
3. OCR text extraction
4. Gemini parses OCR text into structured JSON
5. User edits/validates medicine rows
6. User confirms to save medicines
7. Dashboard shows reminders and low stock alerts
## Notes
- AI output is **never auto-saved** as medicines.
- User must confirm and submit editable rows.
- OCR/AI failures are handled with user-facing error messages.
=======
# smart_medicine_reminder
This web app helps users manage daily medicines easily. Users can add prescriptions, set reminders, and track whether medicines are taken on time. It also allows sharing details with family or caregivers. The app helps avoid missed doses and keeps everything organized for better health and consistency in daily routines.
>>>>>>> aa088919951e186646e6beed9beb6ad7928c167e
