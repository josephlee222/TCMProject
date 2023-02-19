# TCM Shifu
*This project is for NYP App Development module done during Dec 2022 - Feb 2023*
## About
TCM Shifu is a storefront + blog + appointment booking website for a physical clinic. The website features includes:
- User Management
- E-commerce system that the clinic can sell products or treatments
- Coupon discounts system with date scheduling
- Appointment booking for treatments
- Medicine tracker for doctors to input prescriptions
- Enquiries with reply system
- Blog articles for education and clinic news

## Task Allocation
- Joseph: Everything else + integration/bug fixing
- Samuel: Enquiries + Medications
- Iqram: Refunds + a bit of checkout
- Aiden: Blog
- Jing Hao: Products

## Special Features
- Flask-Mail for forget password, enquiry reply and order status change
- JWT for forget password
- Markdown support for blog articles, product + treatments descriptions and enquiries reply
- FullCalender for doctor appointment view
- iCalendar for appointment date exporting and medicine reminders via .ICS file
- Stripe for checkouts, has multiple payment methods

## Installation
This project can be setup on a new environment without pre-existing data. For a quick demo, visit https://joseph222.pythonanywhere.com  
**The recommended python version is 3.9**
1. Clone this repository
2. Open in pycharm (recommended) or any IDE
3. Install `requirements.txt` with `pip install -r requirements.txt`. If you are running on Pycharm, there might be a pop-up for you to create a virtual env with the `requirements.txt` file.
4. Create .env file and fill up the fields for `MAIL_USERNAME` and `MAIL_PASSWORD` if it does not exist
5. Start the project
6. Login into the default admin account with `admin@admin.com` and `Adminpassword`
