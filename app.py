from __future__ import print_function

# ✅ Complete clinic_app.py with all core functionality
import json
import random
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

import mysql
from flask import session, jsonify
from flask_mail import Message
from fpdf import FPDF
import os
import re

import sys
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3, os
from fpdf import FPDF
from jinja2 import Template
from mysql import connector
from numpy.f2py.auxfuncs import throw_error
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
'''appi.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(appi)
from flask import g, request

@babel.localeselector
def get_locale():
    return session.get('lang', 'en')

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('add_appointment'))'''

EMAIL_USER = 'clinic.management.system.app@gmail.com'
EMAIL_PASS = 'dduk eozt owlo qgvr'  # NOT your Gmail password, use App Password
global filename, file_data
app = Flask(__name__)
from flask_mail import Mail, Message

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=EMAIL_USER,
    MAIL_PASSWORD=EMAIL_PASS  # Use App Password if Gmail 2FA enabled
)

mail = Mail(app)
from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'AC370fb27a4df33acde95e3f0055cf7ab0'
TWILIO_AUTH_TOKEN = '107d96a3d19d3b7994e4fd845dd434f2'
TWILIO_PHONE_NUMBER = '+14793780721'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app.secret_key = 'clinic123'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from twilio.rest import Client

# Twilio credentials
TWILIO_SID = 'AC370fb27a4df33acde95e3f0055cf7ab0'
TWILIO_AUTH = '107d96a3d19d3b7994e4fd845dd434f2'
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'  # sandbox sender

twilio_client = Client(TWILIO_SID, TWILIO_AUTH)


from io import BytesIO
import csv

from flask import send_file
from io import StringIO, BytesIO
import csv
import traceback

import openai
from datetime import datetime, timedelta
from flask import request, jsonify

openai.api_key = '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'

from fpdf import FPDF
from datetime import datetime

import requests

import stripe


from twilio.rest import Client


from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
from flask_babel import Babel, _

app.config['BABEL_DEFAULT_LOCALE'] = 'mr'  # Marathi
babel = Babel(app)

from datetime import datetime, timedelta
from flask import g

from datetime import datetime, date

import datetime

from datetime import datetime, timedelta
import sqlite3

from flask import request, flash, redirect
import os
from mysql.connector import pooling

'''conn = mysql.connector.connect(
        host = 'database-1.c5uqc6su0nzd.ap-south-1.rds.amazonaws.com',
        user = 'admin',
        password = 'ClinicApp1!',
        database = 'clinicdb'
)'''

conn = mysql.connector.connect(
    host='localhost',
    user='clinic_user',
    password='ClinicApp1!',
    database='clinic_app'
)

pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **conn)

# Flask backend routes and models for IPD/ICU/NICU

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('clinic.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/ipd_dashboard')
def ipd_dashboard():
    if not session.get("logged_in"): return redirect(url_for('login'))
    c = conn.cursor()
    c.execute('SELECT * FROM ipd WHERE status="Admitted"')
    ipd_patients = c.fetchall()
    c.execute('SELECT * FROM icu WHERE status="Admitted"')
    icu_patients = c.fetchall()
    c.execute('SELECT * FROM nicu WHERE status="Admitted"')
    nicu_patients = c.fetchall()
    return render_template('ipd_dashboard.html', ipd_patients=ipd_patients, icu_patients=icu_patients, nicu_patients=nicu_patients)

@app.route('/ipd/<int:patient_id>/discharge')
def discharge_ipd(patient_id):
    if not session.get("logged_in"): return redirect(url_for('login'))
    c = conn.cursor()
    c.execute('UPDATE ipd SET status = "Discharged" WHERE id = ?', (patient_id,))
    conn.commit()
    flash("✅ IPD patient discharged.")
    return redirect(url_for('ipd_dashboard'))

@app.route('/icu/<int:patient_id>/discharge')
def discharge_icu(patient_id):
    if not session.get("logged_in"): return redirect(url_for('login'))
    c = conn.cursor()
    c.execute('UPDATE icu SET status = "Discharged" WHERE id = ?', (patient_id,))
    conn.commit()
    flash("✅ ICU patient discharged.")
    return redirect(url_for('ipd_dashboard'))

@app.route('/nicu/<int:patient_id>/discharge')
def discharge_nicu(patient_id):
    if not session.get("logged_in"): return redirect(url_for('login'))
    c = conn.cursor()
    c.execute('UPDATE nicu SET status = "Discharged" WHERE id = ?', (patient_id,))
    conn.commit()
    flash("✅ NICU patient discharged.")
    return redirect(url_for('ipd_dashboard'))

@app.route("/ipd/add", methods=["GET", "POST"])
def add_ipd_patient():
    if not session.get("logged_in"): return redirect(url_for('login'))
    if request.method == "POST":
        name = request.form['name']
        admission_date = request.form['admission_date']
        bed_no = request.form['bed_no']
        doctor = request.form['doctor']
        status = request.form['status']

        c= conn.cursor()
        c.execute("INSERT INTO ipd (name, admission_date, bed_no, doctor, status) VALUES (?, ?, ?, ?, 'admitted')",
                     (name, admission_date, bed_no, doctor,status))
        conn.commit()
        flash("✅ Patient admitted successfully.")
        return redirect(url_for("ipd_dashboard"))
    return render_template("add_ipd_patient.html")

import requests

from datetime import datetime, timedelta
import mysql.connector
import smtplib


def send_subscription_reminders():
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().date()
    check_date = today + timedelta(days=3)

    query = """
        SELECT clinic_id, plan, end_date, status 
        FROM subscriptions 
        WHERE status = 'active' 
        AND end_date <= %s
    """
    cursor.execute(query, (check_date,))
    results = cursor.fetchall()

    for row in results:
        clinic_id = row['clinic_id']
        plan = row['plan']
        end_date = row['end_date']

        # You can fetch email from clinics table using clinic_id
        # For now, mock example:
        cursor = conn.cursor()
        cursor.execute("""
                    select email, phone, name from clinics where id=%s""", (clinic_id,))
        result = cursor.fetchall()
        if result and result[1]:
            if result[0]:
                send_mail(f"Subscription Renewal Reminder for Clinic: {result[2]}", f"Your {plan} subscription is expiring on {end_date}. Please renew to avoid service disruption. Visit your dashboard to renew now.", result[0])
                send_mail(f"Subscription Renewal Reminder for Clinic: {result[2]}", f"Your {plan} subscription is expiring on {end_date}. Please renew to avoid service disruption. Visit your dashboard to renew now.", "clinic.management.system.app@gmail.com")
            if result[1]:
                send_whatsapp_message(f"91{result[1]}", f"Your {plan} subscription is expiring on {end_date}. Please renew to avoid service disruption. Visit your dashboard to renew now.")
    conn.close()


from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('cron', id='subscription_reminder', hour=9)
def daily_reminder():
    send_subscription_reminders()

# This can be scheduled using APScheduler or cron

@app.route('/book_demo', methods=['GET', 'POST'])
def book_demo():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        clinic_name = request.form.get('clinic_name', '')
        demo_time = request.form.get('demo_time', '')
        message = request.form.get('message', '')

        # (Optional) Save to DB
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO demo_requests (name, email, phone, clinic_name, demo_time, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, clinic_name, demo_time, message))
        conn.commit()
        conn.close()

        # (Optional) Send email notification
        send_mail("New Demo Request",
                  f"Name: {name}\nEmail: {email}\nPhone: {phone}\nClinic: {clinic_name}\nTime: {demo_time}\n\n{message}",
                    email)

        flash("✅ Thank you! Your demo has been booked. We’ll contact you shortly.", "success")
        return redirect('/book_demo')

    return render_template("demo.html")

def send_mail(subject, body, email):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = email
    # Attach text body
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        throw_error("Email Error:", e)


@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    from flask import request, redirect, flash
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    full_message = f"Feedback received:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = "clinic.management.system.app@gmail.com"
    msg['Subject'] = "New Feedback Received"
    msg.attach(MIMEText(full_message))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        flash("✅ Feedback sent. Thank you!", "success")
    except Exception as e:
        flash("❌ Failed to send feedback.", "danger")
        throw_error("Error sending feedback")

    return redirect(request.referrer or '/')


GUPSHUP_API_URL = "https://api.gupshup.io/sm/api/v1/msg"
GUPSHUP_API_KEY = "mpfokcnwp73llfowrwwgyaphfdvfjvub"  # Replace with your key


def send_whatsapp_message(to_number, message_text):
    payload = {
        "channel": "whatsapp",
        "source": "917834811114",  # registered number
        "destination": to_number,
        "message": message_text,
        "src.name": "ClinicmanagementsystemApp"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": GUPSHUP_API_KEY
    }

    response = requests.post(GUPSHUP_API_URL, data=payload, headers=headers)

    if response.status_code == 200:
        print("✅ WhatsApp message sent successfully.")
    else:
        print("❌ Failed to send message:", response.text)


@app.route("/save_bill/<int:patient_id>/<int:appointment_id>", methods=['POST'])
def save_bill(patient_id, appointment_id):
    data = request.form
    bill_date = datetime.now()
    payment_mode = data.get("paymentMode")
    payment_amount = data.get("paymentAmount")
    notes = data.get("notes", "")
    clinic_id = session.get("clinic")

    billed = float(data.get("billedAmount", 0))
    discount = float(data.get("discountAmount", 0))
    tax = float(data.get("taxAmount", 0))
    final = float(data.get("finalAmount", 0))
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO bills 
                (patient_id, appointment_id, clinic_id, bill_date, total_amount, discount_amount, tax_amount, final_amount, payment_mode, payment_amount, notes)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                   (patient_id, appointment_id, clinic_id, bill_date, billed, discount, tax, final, payment_mode, payment_amount, notes)
                   )

    conn.commit()
    bill_id = cursor.lastrowid

    # Save line items
    rows = 0
    while True:
        if f'name_{rows}' not in data: break
        name = data.get(f'name_{rows}')
        qty = int(data.get(f'qty_{rows}', 0))
        price = float(data.get(f'price_{rows}', 0))
        gst = float(data.get(f'gst_{rows}', 0))
        disc = float(data.get(f'discount_{rows}', 0))
        total = qty * price + (qty * price * gst / 100) - disc

        cursor.execute("""INSERT INTO bill_items (bill_id, appointment_id, service_name, quantity, unit_price, gst, discount, total_price)
                                  VALUES (%s,%s, %s, %s, %s, %s, %s, %s)""",
                       (bill_id, appointment_id, name, qty, price, gst, disc, total))
        rows += 1

    conn.commit()
    flash("✅ Bill saved successfully.")

    return redirect(url_for('view_history'))

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_token():
    creds = None
    if os.path.exists('token.json'):
        print("Token already exists.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token.json
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("✅ token.json created successfully.")



@app.route('/manage_services', methods=['GET', 'POST'])
def manage_services():
    if not session.get("logged_in"): return redirect(url_for('login'))

    cursor = conn.cursor(buffered=True)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        tax = request.form['tax']
        cursor.execute("INSERT INTO services (name, price, tax) VALUES (%s, %s, %s)",
                       (name, price, tax ))
        conn.commit()
        flash("✅ Service added")

    cursor.execute("SELECT id, name, price, tax FROM services")
    services = cursor.fetchall()
    return render_template("manage_services.html", services=services)

@app.route("/delete_service/<int:service_id>")
def delete_service(service_id):
    if not session.get("logged_in"): return redirect(url_for('login'))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE id = %s", (service_id, ))
    conn.commit()
    flash("🗑️ Service deleted")
    return redirect(url_for("manage_services"))


from flask import make_response

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


@app.route('/email_covid_certificate')
def email_covid_certificate():
    data = session.get('cert_data')
    pdf = FPDF()
    filename = f"Covid_Fitness_Certificate_for_{data['name']}.pdf"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Font and Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'To Whomsoever Concerned', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)

    # Extract fields
    name = data.get("name", "_________")
    age = data.get("age", "___")
    gender = data.get("gender", "___")
    treatment = data.get("treatment", "___")
    days = data.get("days", "___")
    email = data.get("email", "___")

    # Write the content
    pdf.multi_cell(0, 10,
                   f"This is to certify that {name}, {age}y, {gender} was under my treatment for COVID pneumoniae. {name} has completed {treatment} treatment and has no active symptoms now.\n"
                   f"{name} has completed {days} quarantine period as per new guidelines.\n"
                   f"{name} is clinically fit to resume routine activity."
                   )

    # Save
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename = filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'

    body = f"Hello,\nPlease find your covid fitness certificate.\n- Clinic Team"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = "Your Covid Fitness Certificate"
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    if filename and os.path.exists(filename):
        with open(filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
            msg.attach(part)


    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return (f"✅ Sent reminder to {email}")
    except Exception as e:
        return (f"❌ Failed to send to {email}: {e}")



@app.route('/print_covid_certificate')
def print_covid_certificate():
    data = session.get('cert_data')
    pdf = FPDF()
    filename = f"Covid_Fitness_Certificate_for_{data['name']}.pdf"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Font and Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'To Whomsoever Concerned', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)

    # Extract fields
    name = data.get("name", "_________")
    age = data.get("age", "___")
    gender = data.get("gender", "___")
    treatment = data.get("treatment", "___")
    days = data.get("days", "___")


    # Write the content
    pdf.multi_cell(0, 10,
                   f"This is to certify that {name}, {age}y, {gender} was under my treatment for COVID pneumoniae. {name} has completed {treatment} treatment and has no active symptoms now.\n"
                   f"{name} has completed {days} quarantine period as per new guidelines.\n"
                   f"{name} is clinically fit to resume routine activity."
                   )

    # Save
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename = filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'
    return send_file(filename, download_name=filename, as_attachment=True)


@app.route('/form/covid_fit', methods=['GET', 'POST'])
def covid_fit_form():

    if request.method == 'POST':
        session['cert_data'] = request.form.to_dict()
        flash("✅ Certificate saved.")
        return redirect('/form/covid_fit')

    return render_template('form_covid_fit.html',data=session.get('cert_data'))


@app.route('/forms', methods=['GET', 'POST'])
def forms():
    if not session.get("logged_in"): return redirect(url_for('login'))

    c = conn.cursor(buffered=True)

    if request.method == 'POST':
        selected_form = request.form.get('form_type')
        if selected_form == "covid_fit":
            return redirect(url_for('covid_fit_form'))
        if selected_form == "health_cert":
            return redirect(url_for('form_certificate'))

    # You can extend with more form types
    form_options = [
        ("", "-- Select Form --"),
        ("covid_fit", "COVID Fitness Certificate"),
        ("health_cert", "Health Certificate")
    ]

    '''c.execute("SELECT name, age, gender FROM patients WHERE id=?", (patient_id,))
    patient = c.fetchone()
    conn.close()'''

    return render_template('forms.html', form_options=form_options)


@app.route('/billing_services')
def billing_services():
    c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM services")
    services = c.fetchall()
    return render_template('billing_services.html', services=services)

@app.route('/get_rx_group')
def get_rx_group():
    diagnosis = request.args.get('diagnosis')
    c = conn.cursor(buffered=True)
    c.execute("SELECT medicine, dose, timing, frequency, duration, note FROM rx_groups WHERE diagnosis = %s", (diagnosis,))
    rows = c.fetchall()
    result = [
        {"medicine": r[0], "dose": r[1], "timing": r[2], "frequency": r[3], "duration": r[4], "note": r[5]}
        for r in rows
    ]
    return jsonify(result)

@app.route("/rx_templates")
def rx_templates():
    c = conn.cursor(buffered=True)
    c.execute("SELECT id, diagnosis, medicine, dose,timing, frequency,duration , note FROM rx_groups")
    groups = c.fetchall()
    return render_template("rx_templates.html", groups=groups)

@app.route('/create_rx_group', methods=['POST'])
def create_rx_group():
    group_name = request.form.get('group_name')
    clinic_id = session['clinic']
    if not group_name:
        flash("Group name is required.")
        return redirect(url_for('manage_rx_groups'))

    c = conn.cursor(buffered=True)
    c.execute("INSERT INTO rx_groups (group_name, clinic_id) VALUES (%s, %s)", (group_name, clinic_id))
    conn.commit()

    flash("✅ Rx Group created successfully.")
    return redirect(url_for('manage_rx_groups'))

@app.route('/delete_rx/<int:rx_id>')
def delete_rx( rx_id):
    c = conn.cursor(buffered=True)
    c.execute("DELETE FROM rx_groups WHERE id = %s", (rx_id,))
    conn.commit()
    flash("RX deleted.", "info")
    return redirect(url_for('manage_rx_groups'))

@app.route('/edit_rx/<int:rx_id>', methods=['GET', 'POST'])
def edit_rx(rx_id):
    c = conn.cursor(buffered=True)

    if request.method == 'POST':
        medicine = request.form['medicine']
        dose = request.form['dose']
        note = request.form['note']
        timing = request.form['timing']
        frequency = request.form['frequency']
        duration = request.form['duration']

        c.execute('''
            UPDATE rx_groups
            SET medicine = %s, dose = %s, note = %s, timing = %s, frequency = %s, duration = %s
            WHERE id = %s
        ''', (medicine, dose, note, timing, frequency, duration, rx_id))
        conn.commit()
        flash("RX updated successfully.", "success")
        return redirect(url_for('manage_rx_groups'))

    c.execute("SELECT * FROM rx_groups WHERE id = %s", (rx_id,))
    rx = c.fetchone()
    return render_template('edit_rx.html', rx=rx)


@app.route("/manage_rx_groups", methods=["GET", "POST"])
def manage_rx_groups():
    clinic_id = session['clinic']
    c = conn.cursor(buffered=True)

    if request.method == "POST":
        diagnosis = request.form.get('diagnosis')
        medicine = request.form.get('medicine')
        dose = request.form.get('dose')
        timing = request.form.get('timing')
        frequency = request.form.get('frequency')
        duration = request.form.get('duration')
        note = request.form.get('note')
        c.execute("INSERT INTO rx_groups (diagnosis, medicine, dose, timing, frequency , duration, note) VALUES (%s, %s, %s, %s, %s ,%s ,%s)", (diagnosis, medicine, dose, timing, frequency , duration, note))
        conn.commit()
        flash("New RX Group created.", "success")
        return redirect(url_for('manage_rx_groups'))

    # Fetch groups and their items
    c.execute("SELECT id, diagnosis, medicine, dose, timing, frequency , duration, note FROM rx_groups")
    rx_map = c.fetchall()

    '''rx_map = {}
    for group in groups:
        group_name = group[1]
        c.execute("SELECT * FROM rx_groups WHERE diagnosis = %s", (group_name,))
        rx_map[group_name] = c.fetchall()'''

    return render_template("manage_rx_groups.html",  rx_map=rx_map)

@app.route('/add_rx_to_group/<string:diagnosis>', methods=['POST'])
def add_rx_to_group(diagnosis):
    med = request.form.get('medicine')
    dose = request.form.get('dose')
    timing = request.form.get('timing')
    frequency = request.form.get('frequency')
    duration = request.form.get('duration')
    note = request.form.get('note')

    c = conn.cursor(buffered=True)
    c.execute('''INSERT INTO rx_groups 
               (id, diagnosis, medicine, dose, timing, frequency, duration, note)
               VALUES (%s, %s, %s, %s, %s, %s, %s)''',
              (id, diagnosis, med, dose, timing, frequency, duration, note))
    conn.commit()

    flash("✅ Medicine added to group.")
    return redirect(url_for('rx_templates'))


@app.route('/get_rx_template/<int:template_id>')
def get_rx_template(template_id):
    c = conn.cursor(buffered=True)
    c.execute("SELECT name, dose, timing, frequency, duration, note FROM rx_templates WHERE group_id=%s", (template_id,))
    meds = [{"name": row[0], "dose": row[1], "timing": row[2], "frequency": row[3], "duration": row[4], "note": row[5]}
            for row in c.fetchall()]
    return jsonify({"medicines": meds})


@app.route('/support', methods=['POST'])
def support():
    module = request.form.get('module')
    issue_type = request.form.get('issue_type')
    description = request.form.get('description')
    file = request.files.get('attachment')

    # Optional: Save the file to uploads folder
    if file and file.filename:
        filepath = os.path.join('static/uploads', file.filename)
        file.save(filepath)

    subject = "Support Issue Reported"
    body = f"Issue in module {module}: Issue Type {issue_type}: Description {description}"

    send_new_email('clinic.management.system.app@gmail.com', subject, body,filepath)
    flash("Support request submitted ✅")
    return redirect(request.referrer or '/')


@app.route('/doctor/profile', methods=['GET', 'POST'])
def doctor_profile():
    if request.method == 'POST':
        logo = request.files.get('logo')
        signature = request.files.get('signature')

        logo_path = signature_path = None
        if logo:
            logo_path = f"static/uploads/logo_{session['username']}.png"
            logo.save(logo_path)
        if signature:
            signature_path = f"static/uploads/signature_{session['username']}.png"
            signature.save(signature_path)

        c = conn.cursor(buffered=True)
        c.execute("UPDATE doctors SET logo_path=%s, signature_path=%s WHERE username=%s",
                  (logo_path, signature_path, session['username']))
        conn.commit()
        flash("✅ Uploaded successfully.")

    return render_template('doctor_profile.html')


def schedule_recurring_appointments(base_appt, recurrence_type, end_date, patient_id, date, time, reason, clinic):
    c = conn.cursor(buffered=True)
    current_date = datetime.strptime(str(base_appt['date']), "%Y-%m-%d").date()
    end_dt = datetime.strptime(str(end_date), "%Y-%m-%d").date()

    while True:
            if recurrence_type == "weekly":
                current_date += timedelta(weeks=1)
            elif recurrence_type == "monthly":
                current_date += timedelta(days=30)  # simple approx for 1 month
            else:
                break

            if current_date > end_dt:
                break


            c = conn.cursor(buffered=True)
            c.execute(
                "INSERT INTO appointments (patient_id, clinic_id, date, time, reason, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (patient_id, clinic, str(current_date), base_appt['time'], reason, "Scheduled"))
            conn.commit()

@app.route('/checkin/<int:appointment_id>')
def checkin(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET checkin_time = datetime('now') WHERE id = %s", (appointment_id,))
    conn.commit()
    flash("✅ Patient Checked-In!")
    return redirect(url_for('view_history'))




@app.route('/add_recurring_appointment/<int:patient_id>', methods=['GET', 'POST'])
def add_recurring_appointment(patient_id):
    if not session.get('logged_in'): return redirect(url_for('login'))

    c = conn.cursor(buffered=True)
    c.execute("SELECT name, age, gender FROM patients WHERE id=%s AND clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()

    if request.method == 'POST':
        start_date = request.form['start_date']
        time = request.form['time']
        frequency = request.form['frequency']  # daily, weekly, monthly
        count = int(request.form['count'])
        reason = request.form['reason']

        appointments = []
        base_date = datetime.strptime(start_date, "%Y-%m-%d")
        for i in range(count):
            if frequency == "daily":
                date = base_date + timedelta(days=i)
            elif frequency == "weekly":
                date = base_date + timedelta(weeks=i)
            elif frequency == "monthly":
                date = base_date + timedelta(days=30 * i)
            appointments.append((patient_id, session['clinic'], date.strftime("%Y-%m-%d"), time, reason, 'Scheduled'))

        c = conn.cursor(buffered=True)
        c.executemany(
            "INSERT INTO appointments (patient_id, clinic_id, date, time, reason, status) VALUES (%s, %s, %s, %s, %s, %s)",
            appointments)
        conn.commit()
        flash("✅ Recurring appointments added.")
        return redirect(url_for('patient_profile', patient_id=patient_id))

    return render_template('recurring_appointment.html', patient_id=patient_id, patient=patient)


@app.route("/templates/<int:patient_id>", methods=["GET", "POST"])
def templates(patient_id):
    if not session.get("logged_in"): return  redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("INSERT INTO certificate_templates (title, content, clinic_id) VALUES (%s, %s, %s)",
                  (title, content, session['clinic']))
        conn.commit()
    c.execute("SELECT id, title FROM certificate_templates WHERE clinic_id=%s", (session['clinic'],))
    templates = c.fetchall()
    return render_template("templates.html", templates=templates, patient_id=patient_id)


@app.route("/generate_certificate/<int:template_id>/<int:patient_id>")
def generate_certificate(template_id, patient_id):
    if not session.get("logged_in"): return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    c.execute("SELECT name, age, gender FROM patients WHERE id=%s",
              (patient_id,))
    patient = c.fetchone()
    c.execute("SELECT content FROM certificate_templates WHERE id=%s AND clinic_id=%s",
              (template_id, session['clinic']))
    template_raw = c.fetchone()
    if not patient or not template_raw:
        flash("Patient or template not found.")
        return redirect("/templates")

    data = {
        "name": patient[0],
        "age": patient[1],
        "gender": patient[2],
        "date": datetime.now().strftime("%d-%b-%Y")
    }

    rendered = Template(template_raw[0]).render(data)
    filename = f"static/certificates/certificate_{patient_id}_{template_id}.pdf"
    os.makedirs("static/certificates", exist_ok=True)
    generate_pdf(rendered, filename)

    return send_file(filename, as_attachment=True)


def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()

    logo_path = "static/logo.jpeg"
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)
    pdf.output(filename)


@app.route('/consent_form/<int:patient_id>', methods=['GET', 'POST'])
def consent_form(patient_id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        signature = request.form['signature_data']  # base64 image
        consent_text = request.form['consent_text']

        # Save PDF
        filename = f"static/consents/consent_{patient_id}_{date}.pdf"
        generate_consent_pdf(name, date, consent_text, signature, filename)

        # Store path in DB if needed
        c = conn.cursor(buffered=True)
        c.execute("INSERT INTO consents (patient_id, file_path, date) VALUES (%s, %s, %s)",
                  (patient_id, filename, date))
        conn.commit()

        flash("✅ Consent Form Saved")
        return redirect(url_for('patient_profile', patient_id=patient_id))

    return render_template("consent_form.html", patient_id=patient_id)

from fpdf import FPDF
import base64

def generate_consent_pdf(name, date, text, signature_data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.ln(10)
    pdf.cell(0, 10, f"Name: {name}")
    pdf.ln(10)
    pdf.cell(0, 10, f"Date: {date}")
    pdf.ln(10)

    # Add signature
    if signature_data.startswith("data:image"):
        img_data = base64.b64decode(signature_data.split(",")[1])
        with open("temp_signature.png", "wb") as f:
            f.write(img_data)
        pdf.image("temp_signature.png", x=10, y=pdf.get_y(), w=60)

    pdf.output(filename)


@app.route("/calendar")
def appointment_calendar():
    if not session.get('logged_in'): return redirect(url_for('login'))

    today = date.today().isoformat()

    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT a.id, a.date, a.time, p.name, a.reason
                FROM appointments a, doctors d , patients p where a.patient_id = p.id
                and  a.clinic_id=%s and d.username=p.doctor_id and d.username= %s
            """, (session['clinic'],session['username']))
    appointments = c.fetchall()

    events = []
    for row in appointments:
        appt_date = row[1]
        status_color = "#0d6efd"  # default (blue)

        if appt_date < today:
            status_color = "#dc3545"  # 🔴 Missed (red)
        elif appt_date == today:
            status_color = "#ffc107"  # 🟡 Today (yellow)
        else:
            status_color = "#198754"  # 🟢 Future (green)

        events.append({
            'id': row[0],
            'title': f"{row[3]}-{row[4]}-{row[0]}",
            'start': f"{row[1]}T{row[2]}",
            'color': status_color
        })
    return render_template("calendar.html", events=events)

    from flask import request, jsonify


@app.route('/trigger_reminders')
def trigger_reminders():
    if not session.get('logged_in'): return redirect(url_for('login'))

    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT a.date, a.time, p.name, p.email, p.contact
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.date=%s AND a.clinic_id=%s
            """, (tomorrow, session['clinic']))
    reminders = c.fetchall()

    for r in reminders:
        date, time, name, email, contact = r
        subject = "Appointment Reminder"
        body = f"Dear {name},\n\nThis is a reminder that you have an appointment on {date} at {time}.\n\n– Clinic Team"
        send_new_email(email, subject, body,'')
        # send_sms(contact, body)  # Uncomment if SMS integrated
        send_whatsapp_message(f"91{contact}", body)  # Uncomment if WhatsApp integrated

    flash(f"✅ Sent {len(reminders)} reminders for {tomorrow}.")
    return redirect(url_for('doctor_calendar'))

def send_new_email(email, subject, body,filename):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = email
    # Attach text body
    msg.attach(MIMEText(body, 'plain'))

    if filename and os.path.exists(filename):
        with open(filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
            msg.attach(part)
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return redirect(f"✅ Sent reminder to {email}")
    except Exception as e:
        return redirect(f"❌ Failed to send to {email}: {e}")

@app.route('/update_appointment_date/<int:appointment_id>', methods=['POST'])
def update_appointment_date(appointment_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        new_datetime = data['new_datetime']  # e.g., '2025-07-08T11:30:00'

        if 'T' not in new_datetime:
            return jsonify({'error': 'Invalid datetime format'}), 400

        new_date, new_time = new_datetime.split('T')

        c = conn.cursor(buffered=True)
        c.execute("""
                        UPDATE appointments SET date=%s, time=%s
                        WHERE id=%s AND clinic_id=%s
                    """, (new_date, new_time, appointment_id, session['clinic']))
        conn.commit()
        c = conn.cursor(buffered=True)
        c.execute("""
                       select p.email,p.name,p.contact from appointments a, patients p wHERE a.id=%s AND a.clinic_id=%s and a.patient_id=p.id
                   """, (appointment_id, session['clinic']))
        result = c.fetchone()
        subject = "Appointment Rescheduled!"
        body = f"Dear {result[1]},\n\nYour appointment has been moved to {new_date} at {new_time}.\n\n– Clinic Team"
        send_new_email(result[0], subject, body, '')
        send_whatsapp_message(result[2],body)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upcoming')
def upcoming_appointments():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    today = datetime.now().strftime('%Y-%m-%d')
    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT a.date, a.time, p.name, p.age, p.gender, p.contact, a.reason, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.date >= %s AND a.clinic_id=%s
                ORDER BY a.date, a.time
            """, (today, session['clinic']))
    appointments = c.fetchall()

    return render_template('upcoming.html', appointments=appointments)


@app.route('/kiosk', methods=['GET', 'POST'])
def kiosk_checkin():
    if request.method == 'POST':
        contact = request.form['contact']
        date = datetime.now().strftime('%Y-%m-%d')

        c = conn.cursor(buffered=True)
        c.execute("""
                        SELECT a.id, p.name, a.time FROM appointments a
                        JOIN patients p ON a.patient_id = p.id
                        WHERE p.contact=%s AND a.date=%s AND a.clinic_id=%s
                    """, (contact, date, session.get('clinic')))
        result = c.fetchone()

        if result:
            # Mark appointment as 'Checked-In'
            c.execute("UPDATE appointments SET status='Checked-In' WHERE id=%s", (result[0],))
            conn.commit()
            return render_template('kiosk_success.html', name=result[1], time=result[2])
        else:
            flash('No appointment found for this number.')
            return redirect('/kiosk')

    return render_template('kiosk_checkin.html')

@app.route('/save_chat/<int:patient_id>', methods=['POST'])
def save_chat(patient_id):
    chat = request.form.get('chat')
    if not chat:
        return '❌ No chat text provided', 400

    c = conn.cursor(buffered=True)
    c.execute("INSERT INTO chat_history (patient_id, chat) VALUES (%s, %s)", (patient_id, chat))
    conn.commit()
    return '✅ Chat saved', 200

'''@app.before_request
def calculate_trial_remaining():
    g.remaining = None  # default if not logged in
    if session.get('logged_in'):
        clinic_id =session.get('clinic')
        c = conn.cursor(buffered=True)
        c.execute("SELECT start_date,end_date FROM subscriptions WHERE clinic_id=%s", (clinic_id,))
        row = c.fetchone()
        if row:
            trial_start = datetime.strptime(str(row[0]), '%Y-%m-%d')
            trial_end = datetime.strptime(str(row[1]), '%Y-%m-%d')
            remaining = (trial_end - trial_start).days
            g.remaining = max(0, remaining)'''

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

from flask import Blueprint, session, redirect, request, url_for
import os, datetime, uuid
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

#google_bp = Blueprint('google_auth', __name__)
#print(google_bp)
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CLIENT_SECRETS_FILE = 'credentials.json'

'''@google_bp.route("/create_meeting/<int:patient_id>")
def create_meeting(patient_id):
    c = conn.cursor(buffered=True)
        c.execute("SELECT email FROM patients WHERE id=%s", (patient_id))
        appt = c.fetchone()
    session['email'] = appt[0]
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES,
        redirect_uri=url_for('google_auth.oauth2callback', _external=True))
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@google_bp.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES,
        redirect_uri=url_for('google_auth.oauth2callback', _external=True))
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    service = build('calendar', 'v3', credentials=credentials)

    email = session['email']
    now = datetime.datetime.utcnow()
    event = {
        'summary': 'Clinic Appointment',
        'start': {'dateTime': (now + datetime.timedelta(minutes=10)).isoformat() + 'Z'},
        'end': {'dateTime': (now + datetime.timedelta(minutes=40)).isoformat() + 'Z'},
        'attendees': [{'email': email}],
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    result = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    meet_link = result.get('hangoutLink')
    return f"<h3>✅ Google Meet created:</h3><p>{meet_link}</p>"
'''

import uuid


@app.route('/start_8x8_meeting/<int:appointment_id>')
def start_8x8_meeting(appointment_id):
    room_id = str(uuid.uuid4())[:8]
    meeting_url = f"https://8x8.vc/clinicapp/{room_id}"

    # Optional: Save this link to DB for the appointment
    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET video_room=%s WHERE id=%s", (meeting_url, appointment_id))
    conn.commit()

    return redirect(meeting_url)


@app.route('/appointment/<int:appointment_id>')
def appointment_detail(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM appointments WHERE id=%s AND clinic_id=%s", (appointment_id, session['clinic']))
    appt = c.fetchone()

    video_room = f"clinic_{session['clinic']}_appointment_{appointment_id}"
    video_link = f"https://meet.jit.si/{video_room}"
    return render_template('appointment_detail.html', appt=appt, video_link=video_link)

import requests
import jwt
import time

ZOOM_API_KEY = 'w7IxK4kRSTPloBy3jxegA'
ZOOM_API_SECRET = 'DjYfhTnnk6wDxAa3KkiIDm4Y4viWfVzb'

def generate_zoom_jwt():
    payload = {
        'iss': ZOOM_API_KEY,
        'exp': int(time.time()) + 5000
    }
    return jwt.encode(payload, ZOOM_API_SECRET, algorithm='HS256')

def create_zoom_meeting(topic="Clinic Consultation", duration=30):
    jwt_token = generate_zoom_jwt()
    if isinstance(jwt_token, bytes):
        jwt_token = jwt_token.decode('utf-8')
    headers = {
        'authorization': f'Bearer {jwt_token}',
        'content-type': 'application/json'
    }
    data = {
        "topic": topic,
        "type": 1,  # Instant Meeting
        "duration": duration,
        "timezone": "Asia/Kolkata",
        "settings": {
            "host_video": True,
            "participant_video": True
        }
    }

    response = requests.post(
        f"https://api.zoom.us/v2/users/me/meetings",
        headers=headers,
        json=data
    )
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@app.route('/start_consultation/<int:appointment_id>', methods=['POST'])
def start_consultation(appointment_id):
    if not session.get("logged_in"): return redirect(url_for("login"))
    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET consult_start_time = datetime('now') WHERE id = %s", (appointment_id,))
    conn.commit()

    c = conn.cursor(buffered=True)
    c.execute("SELECT video_room FROM appointments WHERE id=%s AND clinic_id=%s", (appointment_id, session['clinic']))
    result = c.fetchone()

    # If video already created, redirect to it
    if result and result[0]:
        return redirect(result[0])
    if session.get('creating_meeting'):
        flash("Please wait, meeting is being created.")
        return redirect(url_for('view_history'))

    session['creating_meeting'] = True

    zoom_data = create_zoom_meeting(f"Appointment #{appointment_id}")

    session['creating_meeting'] = False
    # Else create Zoom meeting
    join_url = zoom_data.get("join_url")

    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET video_room=%s WHERE id=%s", (join_url, appointment_id))
    conn.commit()

    return redirect(join_url)

import uuid
from flask import redirect, session

@app.route('/schedule_meeting/<int:appointment_id>')
def schedule_meeting(appointment_id):
    # Generate a unique room ID
    room_id = str(uuid.uuid4())[:8]
    meeting_url = f"https://8x8.vc/clinicapp/{room_id}"

    # Save in DB
    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET video_room=%s WHERE id=%s AND clinic_id=%s",
              (meeting_url, appointment_id, session['clinic']))
    conn.commit()

    return redirect(url_for('view_history'))  # or confirmation page


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

@app.route("/create_meeting/")
def create_meeting():
    if not session.get("logged_in"): return redirect(url_for('login'))
    """Shows basic usage of the Google Meet API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        client = meet_v2.SpacesServiceClient(credentials=creds)
        request = meet_v2.CreateSpaceRequest()
        response = client.create_space(request=request)
        return redirect(response.meeting_uri)
    except Exception as error:
        return(f'An error occurred: {error}')

@app.route('/kyc', methods=['GET', 'POST'])
def kyc_step1():
    if request.method == 'POST':
        phone = request.form.get('phone')
        otp = request.form.get('otp')
        clinic = session.get('clinic')
        if otp == '123456':  # 🔐 Replace with real OTP check logic
            session['phone_verified'] = phone
            c = conn.cursor(buffered=True)
            # 1. Create clinic
            c.execute("UPDATE clinics SET phone=%s WHERE id=%s",
                      (phone, clinic))
            return redirect(url_for('kyc_step2'))
        flash("Invalid OTP. Try 123456 for test.")
    return render_template('kyc_step1.html')

@app.route('/kyc/documents', methods=['GET', 'POST'])
def kyc_step2():
    '''if 'phone_verified' not in session:
        return redirect(url_for('kyc_step1'))'''
    clinic_name = session.get('clinic_name')
    email = session.get('email')
    c = conn.cursor(buffered=True)
    # 1. Create clinic
    c.execute("select kyc_verification from clinics WHERE name=%s and email=%s",
              (clinic_name, email))
    result = c.fetchone()
    if result and result[0] == "Approved":
        return redirect(url_for('kyc_step3'))
    elif result and result[0] == "Pending Approval":
        flash("KYC pending Approval. Please wait for approval.")

    if request.method == 'POST':
        kyc_file = request.files.get('kyc_file')
        kyc_type = request.form.get('kyc_type')
        kyc_number = request.form.get('kyc_number')

        if kyc_file:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{kyc_file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            kyc_file.save(filepath)
            session['kyc_doc'] = filename
            c = conn.cursor(buffered=True)
            # 1. Create clinic
            c.execute(
                "UPDATE clinics SET kyc_file=%s, kyc_type=%s, kyc_number=%s, kyc_verification=%s WHERE name=%s and email=%s",
                (filepath, kyc_type, kyc_number, "Pending Approval", clinic_name, email))
            conn.commit()
            flash("Document Uploaded. Please wait for KYC approval.", 'danger')
            send_mail(f"KYC document Verification for clinic:{clinic_name}",
                      f"KYC document Verification for clinic:{clinic_name}",
                      'clinic.management.system.app@gmail.com')
            return redirect(url_for('kyc_step2'))
        flash("Please upload a document.")
    return render_template('kyc_step2.html')

@app.route('/kyc/payment', methods=['GET', 'POST'])
def kyc_step3():
    expire_old_subscriptions(conn)
    username = request.form.get('username')
    if not username:
        username= session.get('username')
    password = request.form.get('password')
    if not password:
        password= session.get('password')

    plan = request.form.get('plan')
    clinic = session.get('clinic', '')
    admin_id=""
    if request.method == 'POST':
        upi_txn = request.form.get('upi_txn')
        c = conn.cursor(buffered=True)
        if plan!='free':            
            c.execute(
                """select password,id,clinic_id from admins a where a.username=%s""",
                (username,))
            result = c.fetchone()
            if result and check_password_hash(result[0], password):
                admin_id = result[1]
                clinic = result[2]
                if plan == 'free' and hasFreeTrialEnded(result[1]):
                    flash("⏰ Your free trial has expired. Please subscribe to continue.")
                    return redirect('/kyc/payment')
                # Save transaction ID for manual verification
                kyc_file = session.get('kyc_doc', '')
                add_subscription(clinic, plan)
                if plan != 'free' and upi_txn:
                    c = conn.cursor(buffered=True)
                    c.execute("UPDATE clinics SET plan=%s, payment_mode=%s, payment_verification=%s WHERE id=%s",
                              (plan, "UPI", "Pending Approval", clinic))
                    conn.commit()
                    flash("⏰ UPI payment is being verified. Please re-check in some time")
                    send_mail(f"Payment Verification txn_id:{upi_txn}","UPI payment is being verified. Please re-check in some time", 'clinic.management.system.app@gmail.com')
                    send_whatsapp_message("919029356559",f"Payment Verification txn_id:{upi_txn}")
                else:
                    flash("⏰ Free trial has expired. Please pay to access")
            return redirect(url_for('kyc_step3'))
        else:
            c.execute(
                """select a.password,c.plan,c.payment_mode,c.payment_verification, a.clinic_id from admins a, clinics c where a.username =%s and c.id=a.clinic_id and c.kyc_verification='Approved' """,
                (username,))
            result = c.fetchone()
            if result and check_password_hash(result[0], password):
                paymentStatus = result[3]
                if paymentStatus == "Approved" and is_subscription_active(result[4]):
                    session['admin_logged_in'] = True
                    session['clinic'] = result[4]
                    return redirect('/admin_dashboard')
                elif paymentStatus == "Pending Approval":
                    flash("⏰ UPI payment is being verified")
                else:
                    if not is_free_subscription_done(result[4]):
                        flash("⏰ Your free trial is initiated.")
                        add_subscription(result[4], 'free')
                        render_template('success.html')
    flash("⏰ Your free trial is over! Please login via admin to activate new subscription!")
    return render_template('kyc_step3.html')

import sqlite3
from datetime import datetime, timedelta

def add_subscription(clinic_id, plan):
    today = datetime.today().date()
    if plan == "monthly":
        end_date = today + timedelta(days=30)
        amount = 499
    elif plan == "yearly":
        end_date = today + timedelta(days=365)
        amount = 4999
    else:
        end_date = today + timedelta(days=7)
        amount = 0

    
    c = conn.cursor(buffered=True)
    if not is_subscription_active(clinic_id):
        if not hasFreeTrialEnded('clinic_id'):
            c.execute("""
                INSERT INTO subscriptions (clinic_id, plan, amount, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, 'active')
            """, (clinic_id, plan, amount, today, end_date))
            conn.commit()


def is_free_subscription_done(clinic_id):
    today = datetime.today().date()
    
    c = conn.cursor(buffered=True)
    c.execute("""
        SELECT end_date FROM subscriptions
        WHERE clinic_id = %s AND plan='free'
        ORDER BY end_date DESC LIMIT 1
    """, (clinic_id,))
    row = c.fetchone()
    return row is not None and datetime.strptime(str(row[0]), "%Y-%m-%d").date() <= today

def is_subscription_active(clinic_id):
    today = datetime.today().date()
    
    c = conn.cursor(buffered=True)
    c.execute("""
        SELECT end_date FROM subscriptions
        WHERE clinic_id = %s AND status = 'active'
        ORDER BY end_date DESC LIMIT 1
    """, (clinic_id,))
    row = c.fetchone()
    return row is not None and datetime.strptime(str(row[0]), "%Y-%m-%d").date() >= today

def hasFreeTrialEnded(clinic_id):
    today = datetime.today().date()
    
    c = conn.cursor(buffered=True)
    c.execute("""
        SELECT end_date FROM subscriptions
        WHERE clinic_id = %s and plan='free'
        ORDER BY end_date DESC LIMIT 1
    """, (clinic_id,))
    row = c.fetchone()
    return (row is not None and datetime.strptime(str(row[0]), "%Y-%m-%d").date() <= today)

def expire_old_subscriptions(conn):
    from datetime import datetime
    today = datetime.today().date()

    c = conn.cursor(buffered=True)
    c.execute("""
        UPDATE subscriptions 
        SET status = 'expired' 
        WHERE end_date <= %s AND status = 'active'
    """, (today,))
    conn.commit()

@app.context_processor
def inject_subscription_status():
    if 'clinic' in session:
        valid = is_subscription_active(session['clinic'])
    else:
        valid = True
    return dict(subscription_valid=valid)

@app.route('/kyc/success')
def kyc_success():
    return render_template('success.html')

TWILIO_ACCOUNT_SID = 'AC370fb27a4df33acde95e3f0055cf7ab0'
TWILIO_AUTH_TOKEN = '107d96a3d19d3b7994e4fd845dd434f2'
TWILIO_PHONE_NUMBER = '+14793780721'

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.form['phone']
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Your ClinicApp OTP is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    return "OTP Sent"

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    entered = request.form['otp']
    if entered == session.get('otp'):
        return "✅ Verified"
    else:
        return "❌ Invalid OTP"

'''stripe.api_key = 'your_stripe_secret_key'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Clinic Account Subscription',
                },
                'unit_amount': 50000,  # ₹500
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('kyc_step3', _external=True),
        cancel_url=url_for('register', _external=True),
    )'''

@app.route('/create-checkout-session', methods=['POST'])
def confirm_upi_payment():
    upi_txn = request.form.get('upi_txn')
    if upi_txn:
        # Save transaction ID for manual verification
        plan = request.form.get('plan')
        kyc_file = session.get('kyc_doc', '')
        clinic = session.get('clinic_name', '')
        c = conn.cursor(buffered=True)
        c.execute("UPDATE clinics SET plan=%s, payment_mode=%s, payment_verification=%s WHERE id=%s",
                  (plan, "UPI", "Not Approved", clinic))
        conn.commit()
        # ⚠️ Integrate Stripe or UPI here
        conn.commit()
        flash("Submitted. We'll verify and activate shortly.")
        return redirect(url_for('kyc_success'))
    else:
        flash("Enter a valid UPI transaction ID.")
        return redirect('/kyc/payment')

    return redirect(session.url, code=303)

def get_rxnorm_data(drug_name):
    # Get RxCUI
    rxcui_url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json%sname={drug_name}"
    rxcui_response = requests.get(rxcui_url).json()

    rx_id = rxcui_response.get('idGroup', {}).get('rxnormId', [None])[0]
    if not rx_id:
        return f"No RxNorm ID found for '{drug_name}'"

    # Get Properties
    props_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rx_id}/properties.json"
    props = requests.get(props_url).json().get('properties', {})

    return {
        "RxCUI": rx_id,
        "Name": props.get('name'),
        "Synonym": props.get('synonym'),
        "TTY": props.get('tty')
    }


# Test



def generate_bill_pdf(patient_name, services, total, filename):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Clinic Invoice", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.today().strftime('%d-%b-%Y')}", ln=True)
    pdf.cell(0, 10, f"Patient: {patient_name}", ln=True)
    pdf.ln(5)

    headers = ['#', 'Service', 'Qty', 'Unit Price', 'GST %', 'Discount', 'Total']
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 12)
    for header in headers:
        pdf.cell(28, 10, header, 1, 0, 'C', fill=True)
    pdf.ln()

    pdf.set_font("Arial", '', 12)
    for idx, svc in enumerate(services, start=1):
        total_price = round((svc['qty'] * svc['price']) * (1 + svc['gst']/100) - svc['discount'])

        pdf.cell(28, 10, str(idx), 1)
        pdf.cell(28, 10, svc['name'][:12], 1)
        pdf.cell(28, 10, str(svc['qty']), 1)
        pdf.cell(28, 10, str(svc['price']), 1)
        pdf.cell(28, 10, f"{svc['gst']}%", 1)
        pdf.cell(28, 10, str(svc['discount']), 1)
        pdf.cell(28, 10, f"INR {total_price}", 1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Total Billed Amount: INR{total}", ln=True, align='R')

    pdf.output(filename)
    return filename

from flask import request, send_file

@app.route('/print_bill/<int:patient_id>', methods=['GET', 'POST'])
def print_bill(patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = request.form

    # Fetch patient
    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT name FROM patients
                WHERE id = %s AND clinic_id = %s
            """, (patient_id, session['clinic']))
    row = c.fetchone()
    patient_name = row[0] if row else "Unknown"

    # Total from paymentAmount
    total = float(form.get('paymentAmount', 0))
    bill_date = form.get('bill_date', '')
    # Extract dynamic service rows
    services = []
    i = 0
    while True:
        name = form.get(f'name_{i}')
        if not name:
            break
        services.append({
            'name': name,
            'qty': int(form.get(f'qty_{i}', 0)),
            'price': float(form.get(f'price_{i}', 0)),
            'gst': float(form.get(f'gst_{i}', 0)),
            'discount': float(form.get(f'discount_{i}', 0))
        })
        i += 1

    # Create PDF
    filename = f"test.pdf"
    generate_bill_pdf(patient_name, services, total, filename)
    return send_file(filename, as_attachment=True)


@app.route('/billing/<int:patient_id>/<int:appointment_id>', methods=['GET', 'POST'])
def billing(patient_id, appointment_id):
    services = []
    c = conn.cursor(buffered=True)
    c.execute("""SELECT name, price FROM services""")
    services = c.fetchall()
    if request.method == 'POST':
        session['bill_data'] = request.form.to_dict()
        c = conn.cursor(buffered=True)
        c.execute("""SELECT name, price, tax FROM services""")
        services = c.fetchall()
        flash("✅ Certificate saved.")

    c = conn.cursor(buffered=True)
    c.execute("""select  b.bill_date, i.* from bills b, bill_items i where b.patient_id=%s and b.appointment_id=%s and b.id in (select max(id) from bills where patient_id=%s and appointment_id=%s) and i.bill_id=b.id""", (patient_id, appointment_id,patient_id, appointment_id))
    bill_items = c.fetchall()
    if bill_items:
        return render_template('view_bill.html', bill_items=bill_items, patient_id=patient_id)

    return render_template('billing.html', patient_id=patient_id, data=session.get('bill_data'), services=services, appointment_id=appointment_id)


@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/form_certificate', methods=['GET', 'POST'])
def form_certificate():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        # Save logic here (e.g., to DB or session)
        session['cert_data'] = request.form.to_dict()
        flash("✅ Certificate saved.")
        return redirect('/form_certificate')

    return render_template('healthCertificate.html', data=session.get('cert_data'))


@app.route('/print_certificate')
def print_certificate():
    data = session.get('cert_data')
    pdf = FPDF()
    filename = f"Medical_Certificate_for_{data['name']}.pdf"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Font and Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'To Whomsoever Concerned', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)

    # Extract fields
    name = data.get("name", "_________")
    age = data.get("age", "___")
    gender = data.get("gender", "___")
    condition = data.get("condition", "______________")
    since_date = datetime.strptime(data.get("since_date", ""), "%Y-%m-%d").strftime("%d-%b-%Y")
    pronoun = data.get("pronoun", "He/She")
    rest_period = data.get("rest_period", "____")

    # Write the content
    pdf.multi_cell(0, 10,
                   f"This is to certify that {name}, {age}y, {gender} is under my care for {condition} since {since_date}.\n"
                   f"{pronoun} has been advised rest for {rest_period}.\n\n"
                   "Kindly do the needful.\nThank you."
                   )

    # Save
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename = filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'
    return send_file(filename, download_name=filename, as_attachment=True)


@app.route('/email_certificate')
def email_certificate():
    data = session.get('cert_data')
    pdf = FPDF()
    filename = f"Medical_Certificate_for_{data['name']}.pdf"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Font and Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'To Whomsoever Concerned', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)

    # Extract fields
    name = data.get("name", "_________")
    age = data.get("age", "___")
    gender = data.get("gender", "___")
    condition = data.get("condition", "______________")
    since_date = datetime.strptime(data.get("since_date", ""), "%Y-%m-%d").strftime("%d-%b-%Y")
    pronoun = data.get("pronoun", "He/She")
    rest_period = data.get("rest_period", "____")

    # Write the content
    pdf.multi_cell(0, 10,
                   f"This is to certify that {name}, {age}y, {gender} is under my care for {condition} since {since_date}.\n"
                   f"{pronoun} has been advised rest for {rest_period}.\n\n"
                   "Kindly do the needful.\nThank you."
                   )

    # Save
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename = filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'

    data = session.get('cert_data')
    name = data.get("name", "_________")
    age = data.get("age", "___")
    gender = data.get("gender", "___")
    date = datetime.strptime(data.get("since_date", ""), "%Y-%m-%d").strftime("%d-%b-%Y")
    email = data.get("email", "___")
    subject = f"Prescription of {name} for {date}",
    body = f"Dear {name},\nYour prescription for {date}.\n- Clinic Team",

    # logic to render HTML, convert to PDF and email
    '''msg = Message(
        subject=f"Prescription of {name} for {date}",
        sender="rohitnbhilare@gmail.com",  # ✅ required
        recipients=[email],  # recipient from DB
        body=f"Dear {name},\nYour prescription for {date}.\n- Clinic Team",
    )'''
    body = f"Hello,\nPlease find your medical certificate.\n- Clinic Team"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = "Your Medical Certificate"
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    if filename and os.path.exists(filename):
        with open(filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
            msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return(f"✅ Sent reminder to {email}")
    except Exception as e:
        return(f"❌ Failed to send to {email}: {e}")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json.get('message')
    clinic_id = session.get('clinic')

    # Send to GPT
    prompt = f"""You are a chatbot for a medical clinic. When users give appointment details, extract name, age, gender, date, time, and reason. Respond briefly and confirm booking.
User: {message}
Extracted:
"""
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=200
    )
    extracted = response.choices[0].text.strip()

    # Parse GPT output
    try:
        lines = extracted.splitlines()
        data = {line.split(":")[0].strip().lower(): line.split(":")[1].strip() for line in lines}
        name = data.get("name")
        age = int(data.get("age", "0"))
        gender = data.get("gender", "Other")
        date = data.get("date")
        time = data.get("time")
        reason = data.get("reason", "Not specified")

        # Insert or update patient
        c = conn.cursor(buffered=True)
        c.execute("SELECT id FROM patients WHERE name=%s AND clinic_id=%s", (name, clinic_id))
        row = c.fetchone()
        if row:
            patient_id = row[0]
        else:
            c.execute("INSERT INTO patients (name, age, gender, contact, clinic_id) VALUES (%s, %s, %s, %s, %s)",
                      (name, age, gender, "", clinic_id))
            patient_id = c.lastrowid

        # Book appointment
        c.execute("""INSERT INTO appointments (patient_id, date, time, reason, status, clinic_id) 
                                 VALUES (%s, %s, %s, %s, 'Scheduled', %s)""",
                  (patient_id, date, time, reason, clinic_id))
        conn.commit()

        return jsonify({"reply": f"✅ Appointment booked for {name} on {date} at {time}."})
    except Exception as e:
        return jsonify({"reply": f"❌ Sorry, couldn't understand. Try: 'Book me on Friday at 4 PM'. Error: {e}"}), 500

@app.route('/api/appointments')
def get_appointments():
    doctor = session['username']  # assuming doctor is logged in
    clinic_id = session.get('clinic')
    c = conn.cursor(buffered=True)
    c.execute(
        "SELECT a.id, p.name, a.date, a.time, a.reason FROM appointments a , patients p, doctors d where a.patient_id = p.id and a.clinic_id=%s and d.username=p.doctor_id and d.username=%s",
        (clinic_id,doctor))
    rows = c.fetchall()
    events = []
    for row in rows:
        events.append({
            'title': f"{row[1]} - {row[4]}",
            'start': f"{row[2]}T{row[3]}",
            'url': url_for('add_prescription', appointment_id=row[0])
        })

    return jsonify(events)

@app.route('/doctor_calendar')
def doctor_calendar():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('doctor_calendar.html')



@app.route('/smart_search', methods=['GET', 'POST'])
def smart_search():
    if not session.get('logged_in'): return redirect(url_for('login'))
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        filters = parse_nlp_query(query)
        results = run_patient_query(filters)

    return render_template('smart_search.html', results=results, query=query)

def run_patient_query(filters):
    query = "SELECT DISTINCT p.* FROM patients p LEFT JOIN appointments a ON p.id = a.patient_id WHERE p.clinic_id=%s"
    params = [session['clinic']]

    if filters["gender"]:
        query += " AND p.gender=%s"
        params.append(filters["gender"])
    if filters["age_min"]:
        query += " AND p.age >= %s"
        params.append(filters["age_min"])
    if filters["age_max"]:
        query += " AND p.age <= %s"
        params.append(filters["age_max"])
    if filters["diagnosis"]:
        diag_clauses = []
        for diag in filters["diagnosis"]:
            diag_clauses.append("a.diagnosis LIKE %s")
            params.append(f"%{diag.strip()}%")
        query += " AND (" + " OR ".join(diag_clauses) + ")"
    if filters["drug"]:
        diag_clauses = []
        for diag in filters["drug"]:
            diag_clauses.append("a.prescription LIKE %s")
            params.append(f"%{diag.strip()}%")
        query += " AND (" + " OR ".join(diag_clauses) + ")"

    c = conn.cursor(buffered=True)
    c.execute(query, params)
    return c.fetchall()

def parse_nlp_query(query):
    # Lowercase and basic filters (expandable)
    query = query.lower()
    filters = {"age_min": None, "age_max": None, "gender": None, "diagnosis": None, "drug": None}

    if "female" in query:
        filters["gender"] = "Female"
    if "male" in query:
        filters["gender"] = "Male"
    if "age >" in query:
        filters["age_min"] = int(query.split("age >")[1].split()[0])
    if "age <" in query:
        filters["age_max"] = int(query.split("age <")[1].split()[0])
        # Diagnosis after keyword
    match = re.search(r'diagnosis(%s: is|:)%s.*%s([a-z\s,]+)', query)
    if match:
        diag_text = match.group(1).strip()
        # Keep only keywords, split by "or"/"and"/"," etc.
        filters["diagnosis"] = re.split(r'[,|and|or]+', diag_text)
    match = re.search(r'drug(%s: is|:)%s.*%s([a-z\s,]+)', query)
    if match:
        diag_text = match.group(1).strip()
        # Keep only keywords, split by "or"/"and"/"," etc.
        filters["drug"] = re.split(r'[,|and|or]+', diag_text)

    return filters


@app.route('/get_patient_by_contact')
def get_patient_by_contact():
    contact = request.args.get('contact')
    clinic_id = session.get('clinic')
    c = conn.cursor()
    c.execute(
        "SELECT name, age, gender, email, allergies, chronic_conditions FROM patients WHERE contact=%s AND clinic_id=%s",
        (contact, clinic_id))
    row = c.fetchone()
    if row:
        return jsonify({
            'name': row[0],
            'age': row[1],
            'gender': row[2],
            'email': row[3],
            'allergies': row[4],
            'chronic': row[5]
        })
    else:
        return jsonify({})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        clinic_name = request.form['clinic_name']
        username = request.form['username']
        role = request.form['role']
        address = request.form['address']
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        session['clinic_name'] = clinic_name
        session['email'] = email
        c = conn.cursor(buffered=True)
        c.execute("""select * from admins where username =%s """, (username,))
        result = c.fetchone()
        '''if result:
            flash('Please use a different username', 'success')
            return redirect(url_for('register'))'''
        # 1. Create clinic
        c.execute(
            """select c.email_verified,a.password from admins a, clinics c where a.clinic_id=c.id and a.username=%s and a.email=%s """,
            (username, email))
        result = c.fetchone()
        if result and check_password_hash(result[1], password):
            if result[0] == 1:
                flash('Admin Account created! Please provide KYC documents and start free trial', 'success')
                return redirect(url_for('kyc_step2'))
            else:
                flash('Admin Account created! Please verify your email', 'success')
                return redirect(url_for('register'))

        # KYC details
        phone = request.form.get('phone', '').strip()
        kyc_type = request.form.get('kyc_type', '').strip()
        kyc_number = request.form.get('kyc_number', '').strip()
        '''kyc_file =  request.form.get('kyc_file', '').strip()
        kyc_path = f"static/kyc_docs/{username}_{kyc_file.filename}"
        kyc_file.save(kyc_path)'''

        # Payment
        plan = request.form.get('plan', '').strip()
        payment_mode = request.form.get('payment_mode', '').strip()

        c = conn.cursor(buffered=True)
        c.execute("""INSERT INTO clinics
                          (name, address, phone, email)
                          VALUES (%s, %s, %s, %s)
                          """, (clinic_name, address, phone, email))


        session['clinic_name'] = clinic_name
        clinic_id = c.lastrowid
        session['clinic'] = clinic_id
        now = datetime.now().strftime("%Y-%m-%d")


        c.execute("""select * from admins where username =%s and password =%s and email=%s and role=%s and clinic_id=%s""",
                  (username, hashed_password, email, role, clinic_id))
        if not c.fetchone():
            # 2. Create user for clinic
            c.execute("""INSERT INTO admins (username, password, email, role, clinic_id)
                                                     VALUES (%s, %s, %s, %s, %s)""",
                      (username, hashed_password, email, role, clinic_id))
            conn.commit()
        # Send email
        token = generate_verification_token(email)
        send_verification_email(email, token, app)
        flash("✅ Registration complete. Please check your email to verify.")
        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/verify/<token>')
def verify_email(token):
    email = confirm_token(token)
    if not email:
        return "❌ Verification link expired or invalid."

    c = conn.cursor(buffered=True)
    c.execute("UPDATE users SET email_verified = 1 WHERE email = %s", (email,))
    c.execute("UPDATE admins SET email_verified = 1 WHERE email = %s", (email,))
    c.execute("UPDATE clinics SET email_verified = 1 WHERE email = %s", (email,))
    conn.commit()

    return "✅ Email verified! You can now login."

import smtplib
from email.mime.text import MIMEText
from flask import url_for

def send_verification_email(user_email, token, app):
    link = url_for('verify_email', token=token, _external=True)
    subject = "✅ Verify your Clinic App Email"
    body = f"""
    Hello,

    Please verify your email by clicking the link below:

    {link}

    If you did not register, ignore this email.

    - Clinic App Team
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = user_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

from itsdangerous import URLSafeTimedSerializer

s = URLSafeTimedSerializer("rohitbhi")

def generate_verification_token(email):
    return s.dumps(email, salt='email-verify')

def confirm_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='email-verify', max_age=expiration)
    except:
        return False
    return email


@app.errorhandler(500)
def server_error(e):
    return f"<pre>{traceback.format_exc()}</pre>", 500

@app.route('/export/patients')
def export_patients():
    clinic_id = session.get('clinic_id', 'default')

    # Step 1: Write CSV to a StringIO buffer
    text_stream = StringIO()
    writer = csv.writer(text_stream)
    writer.writerow(['ID', 'Name', 'Age', 'Gender', 'Contact', 'Photo', 'Email', 'Allergies', 'Chronic Conditions', 'Clinic ID', 'Doctor Name'])

    c = conn.cursor(buffered=True)
    c.execute(
        "SELECT id, name, age, gender, contact, photo, email, allergies, chronic_conditions, clinic_id, doctor_id FROM patients WHERE clinic_id=%s",
        (session.get('clinic'),))
    for row in c.fetchall():
        writer.writerow(row)

    # Step 2: Convert text to BytesIO
    mem = BytesIO()
    mem.write(text_stream.getvalue().encode('utf-8'))
    mem.seek(0)

    # Step 3: Return as downloadable CSV
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name='patients.csv'
    )


@app.route('/export/appointments')
def export_appointments():
    import csv
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Patient Name', 'Date', 'Time', 'Reason', 'Status'])

    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT a.id, p.name, a.date, a.time, a.reason, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.clinic_id=%s
            """, (session['clinic'],))
    rows = c.fetchall()
    for row in rows:
        writer.writerow(row)

    # Step 2: Convert text to BytesIO
    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)

    # Step 3: Return as downloadable CSV
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name='appointments.csv'
    )

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        file = request.files['file']
        import_type = request.form['type']
        clinic_id = session.get('clinic_id', 'default')

        if file.filename.endswith('.csv'):
            import csv
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)

            c = conn.cursor(buffered=True)

            if import_type == 'patients':
                for row in reader:
                    c.execute(
                        "INSERT INTO patients ( name, age, gender, contact, photo, email, allergies, chronic_conditions, clinic_id, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (row['Name'], row['Age'], row['Gender'], row['Contact'], row['Photo'], row['Email'],
                         row.get('Allergies', ''), row.get('Chronic Conditions', ''), row.get('Clinic ID', ''),
                         row.get('Doctor Name', '')))
            conn.commit()

            flash(f"{import_type.title()} imported successfully!", "success")

    return render_template('import.html')

@app.route('/send_prescription_pdf/<int:patient_id>')
def send_prescription_pdf(patient_id):
    # Get patient and latest prescription
    c = conn.cursor(buffered=True)
    c.execute("SELECT name, email , contact FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()
    if not patient:
        flash("Patient not found", "danger")
        return redirect(request.referrer)

    name, email, contact = patient

    # Get latest prescription for this patient
    '''c.execute("""
              SELECT date, prescription, rx_json
              FROM appointments
              WHERE patient_id = %s
              ORDER BY date DESC LIMIT 1
              """, (patient_id,))'''
    c.execute("""
                      SELECT p.name,
                             p.age,
                             p.gender,
                             p.contact,
                             p.photo,
                             a.date,
                             a.time,
                             a.reason,
                             a.prescription,
                             a.rx_json,
                             p.id,
                            a.notes
                      FROM appointments a
                               JOIN patients p ON a.patient_id = p.id
                      WHERE p.id = %s and p.clinic_id =%s
                      """, (patient_id, session['clinic']))
    record = c.fetchone()

    if not record:
        flash("No prescriptions found for this patient", "warning")
        return redirect(request.referrer)


    # Generate PDF
    name, age, gender, contact, photo, date, time, reason, prescription, rx_json, patient_id , notes= record

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()

    logo_path = "static/logo.jpeg"
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)
    c.execute("SELECT name, address, phone FROM clinics WHERE id=%s", (session['clinic'],))
    clinic = c.fetchone()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, clinic[0], ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "", ln=1, align='C')
    pdf.cell(200, 10, clinic[1], ln=1, align='C')
    pdf.cell(200, 10, clinic[2], ln=1, align='C')

    pdf.ln(10)

    # Patient Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Prescription for {name}", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 8, f"Age: {age}", ln=0)
    pdf.cell(100, 8, f"Gender: {gender}", ln=1)
    pdf.cell(100, 8, f"Contact: {contact}", ln=0)
    pdf.cell(100, 8, f"Date: {date} {time}", ln=1)
    pdf.cell(200, 8, f"Reason: {reason}", ln=1)
    pdf.ln(5)

    # Prescription
    pdf.set_font("Arial", 'B', 12)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, notes if notes else "")
    pdf.ln(10)

    pdf.cell(200, 10, "Prescription:", ln=1)
    pdf.ln(2)
    # Parse Rx lines from text
    pdf.multi_cell(0, 8, prescription if prescription else "")
    if rx_json:
        try:
            rx_list = json.loads(rx_json)
            if rx_list:
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Rx", ln=1)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(40, 8, "Medicine", 1)
                pdf.cell(25, 8, "Dose", 1)
                pdf.cell(25, 8, "Timing", 1)
                pdf.cell(25, 8, "Freq.", 1)
                pdf.cell(25, 8, "Duration", 1)
                pdf.cell(50, 8, "Note", 1)
                pdf.ln()
                pdf.set_font("Arial", size=10)
                for rx in rx_list:
                    pdf.cell(40, 8, rx['medicine'], 1)
                    pdf.cell(25, 8, rx['dose'], 1)
                    pdf.cell(25, 8, rx['timing'], 1)
                    pdf.cell(25, 8, rx['frequency'], 1)
                    pdf.cell(25, 8, rx['duration'], 1)
                    pdf.cell(50, 8, rx['note'], 1)
                    pdf.ln()
        except Exception as e:
            pdf.cell(200, 10, txt="Error reading prescription table.", ln=1)

    # Signature
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    sign_path = "static/signature.png"
    name = patient[2]
    if patient[1] and os.path.exists(patient[1]):
        pdf.image(patient[1], x=150, y=pdf.get_y(), w=40)
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, f"Signature  Dr.{name}", ln=1, align='R')


    # Output
    file = f"Prescription for {name} - {date}.pdf"
    pdf.output(file)
    '''os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)'''
    subject = f"""✅ Your Prescription from {clinic[0]}"""
    body = f"""
        Dear {name},
        Please find attached Prescription for {date}:{time} :
        - Clinic App Team
        """
    send_whatsapp_message(contact,file)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = email
    # Attach text body
    msg.attach(MIMEText(body, 'plain'))
    # Attach files
    if file and os.path.exists(file):
        with open(file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
            msg.attach(part)


    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return(f"✅ Sent reminder to {email}")
    except Exception as e:
        return(f"❌ Failed to send to {email}: {e}")

    return redirect(request.referrer)


@app.route('/send_whatsapp/<int:appointment_id>')
def send_whatsapp(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute(
        "SELECT p.name, p.contact, a.date, a.time FROM appointments a JOIN patients p ON a.patient_id = p.id WHERE a.id=%s and p.clinic_id=%s",
        (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid appointment ID"

    name, contact, date, time = row
    to_number = f"whatsapp:{contact}"

    body = f"\"\"\"👋 Hello {name},\n\nThis is a reminder for your appointment at Sunrise Clinic on {date} at {time}.\n\n- Clinic Team\"\"\""

    try:
        msg = twilio_client.messages.create(
            body=body,
            from_=TWILIO_WHATSAPP_FROM,
            to=to_number
        )
        return f"✅ WhatsApp message sent: {msg.sid}"
    except Exception as e:
        return f"❌ Failed: {str(e)}"

@app.route('/send_sms/<int:appointment_id>')
def send_sms(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute(
        "SELECT p.name, p.contact, a.date, a.time FROM appointments a JOIN patients p ON a.patient_id = p.id WHERE a.id=%s and a.clinic_id=%s",
        (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid Appointment ID"

    name, phone, date, time = row
    message = twilio_client.messages.create(
        body=f"Hello {name}, your appointment is scheduled for {date} at {time}.",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    return f"SMS sent: {message.sid}"

@app.route('/send_bulk_email', methods=['GET', 'POST'])
def send_bulk_email():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form.get('subject', '')
        body = request.form.get('body', '')
        files = request.files.getlist('attachments')

        c = conn.cursor(buffered=True)
        c.execute("SELECT email, contact FROM patients WHERE email IS NOT NULL AND email != '' and clinic_id=%s",
                  (session['clinic'],))
        emails = c.fetchall()
        for email in emails:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = EMAIL_USER
            msg['To'] = email[0]
            # Attach text body
            msg.attach(MIMEText(body, 'plain'))

            # Attach file
            for file in files:
                if file and file.filename:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{file.filename}"')
                    msg.attach(part)
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.send_message(msg)
                server.quit()
            except Exception as e:
                print("Email Error:", e)

        for contact in emails:
            for file in files:
                if file:
                    filename = secure_filename(file.filename)
                    save_path = os.path.join('static', 'uploads', filename)
                    file.save(save_path)
                    file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
                    send_file_via_gupshup(f"91{contact[1]}", file_url, file.filename)

        flash(f"📧 Sent to {len(emails)} patients", "success")

    return render_template('send_bulk_email.html')

import requests

def send_file_via_gupshup(phone_number, file_url, filename):
    url = "https://api.gupshup.io/sm/api/v1/msg"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": "mpfokcnwp73llfowrwwgyaphfdvfjvub"
    }
    payload = {
        "channel": "whatsapp",
        "source": "917834811114",
        "destination": phone_number,
        "message": f'{{"type":"file","originalUrl":"{file_url}","caption":"{filename}"}}',
        "src.name": "ClinicmanagementsystemApp"
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.status_code, response.text)

@app.route('/send_email/<int:appointment_id>')
def send_email(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute(
        "SELECT p.name, p.contact, p.email, a.date, a.time, a.rx_json FROM appointments a JOIN patients p ON a.patient_id = p.id WHERE a.id=%s and a.clinic_id=%s",
        (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid Appointment ID"
    c = conn.cursor(buffered=True)
    c.execute("""
                   SELECT p.email,p.name, p.age, p.gender, p.contact, p.photo, a.date, a.time, a.reason, a.prescription, a.rx_json, p.id, a.notes
                   FROM appointments a
                   JOIN patients p ON a.patient_id = p.id
                   WHERE a.id=%s and a.clinic_id=%s
               """, (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid appointment ID"

    email,name, age, gender, contact, photo, date, time, reason, prescription, rx_json, patient_id, notes = row

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()

    logo_path = "static/logo.jpeg"
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)

    c.execute("SELECT name, address, phone FROM clinics WHERE id=%s", (session['clinic'],))
    clinic = c.fetchone()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, clinic[0], ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "", ln=1, align='C')
    pdf.cell(200, 10, clinic[1], ln=1, align='C')
    pdf.cell(200, 10, clinic[2], ln=1, align='C')

    # Patient Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Prescription for {name}", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, f"Age: {age}", ln=0)
    pdf.cell(100, 8, f"Gender: {gender}", ln=1)
    pdf.cell(100, 8, f"Contact: {contact}", ln=0)
    pdf.cell(100, 8, f"Date: {date} {time}", ln=1)
    pdf.cell(200, 8, f"Reason: {reason}", ln=1)
    pdf.ln(5)

    # Prescription
    pdf.set_font("Arial", 'B', 12)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, notes if notes else "")
    pdf.ln(10)

    pdf.cell(200, 10, "Prescription:", ln=1)
    pdf.ln(2)
    # Parse Rx lines from text
    pdf.multi_cell(0, 8, prescription if prescription else "")
    if rx_json:
        try:
            rx_list = json.loads(rx_json)
            if rx_list:
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Rx", ln=1)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(40, 8, "Medicine", 1)
                pdf.cell(25, 8, "Dose", 1)
                pdf.cell(25, 8, "Timing", 1)
                pdf.cell(25, 8, "Freq.", 1)
                pdf.cell(25, 8, "Duration", 1)
                pdf.cell(50, 8, "Note", 1)
                pdf.ln()
                pdf.set_font("Arial", size=10)
                for rx in rx_list:
                    pdf.cell(40, 8, rx['medicine'], 1)
                    pdf.cell(25, 8, rx['dose'], 1)
                    pdf.cell(25, 8, rx['timing'], 1)
                    pdf.cell(25, 8, rx['frequency'], 1)
                    pdf.cell(25, 8, rx['duration'], 1)
                    pdf.cell(50, 8, rx['note'], 1)
                    pdf.ln()
        except Exception as e:
            pdf.cell(200, 10, txt="Error reading prescription table.", ln=1)

    # Signature
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()

    sign_path = "static/signature.png"
    name= patient[2]
    if patient[1] and os.path.exists(patient[1]):
        pdf.image(patient[1], x=150, y=pdf.get_y(), w=40)
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, f"Signature  Dr.{name}", ln=1, align='R')

    # QR Code
    # Output
    global filename, file_data
    filename = f"Prescription for {name} - {date}.pdf"
    pdf.output(filename)

    subject=f"Prescription of {name} for {date}",
    sender="rohitnbhilare@gmail.com",  # ✅ required
    recipients=[email],  # recipient from DB
    body=f"Dear {name},\nYour prescription for {date} at {time}.\n- Clinic Team"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = email
    # Attach text body
    msg.attach(MIMEText(body, 'plain'))
    # Attach files
    if filename and os.path.exists(filename):
        with open(filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
            msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return (f"✅ Sent reminder to {email}")
    except Exception as e:
        return (f"❌ Failed to send to {email}: {e}")


@app.route('/admin/clinics', methods=['GET', 'POST'])
def manage_clinics():
    if not session.get('admin_logged_in'): return redirect(url_for('login'))

    c = conn.cursor(buffered=True)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        c.execute("INSERT INTO clinics (name, address, phone) VALUES (%s, %s, %s)", (name, address, phone))
        conn.commit()
        flash("Clinic added!", "success")

    c.execute("SELECT * FROM clinics")
    clinics = c.fetchall()

    return render_template("admin_clinics.html", clinics=clinics)


@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if not session.get('admin_logged_in'): return redirect(url_for('login'))

    c = conn.cursor(buffered=True)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        clinic_id = request.form['clinic_id']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        c.execute("INSERT INTO users (username, password, role, clinic_id) VALUES (%s, %s, %s, %s)",
                  (username, hashed_password, role, clinic_id))
        conn.commit()
        flash("User added!", "success")

        c.execute("SELECT users.id, users.username, users.role, clinics.name FROM users LEFT JOIN clinics ON users.clinic_id = clinics.id")
        users = c.fetchall()

        c.execute("SELECT id, name FROM clinics")
        clinics = c.fetchall()

    return render_template("admin_users.html", users=users, clinics=clinics)


# --- Authentication ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user, pwd = request.form['username'], request.form['password']

        c = conn.cursor(buffered=True)
        c.execute(
            "select d.password, d.clinic_id, d.id, c.payment_verification,c.kyc_verification, c.email_verified FROM doctors d, clinics c WHERE d.username=%s and c.id=d.clinic_id",
            (user,))
        result = c.fetchone()
        if result and check_password_hash(result[0], pwd):
            if (result[1] and hasFreeTrialEnded(result[1]) and result[3] == 'Approved' and result[4] == 'Approved' and
                    result[5] == 1):
                if is_subscription_active(result[1]):
                    session['username'] = user
                    session['logged_in'] = True
                    session['clinic'] = result[1]
                    session['admin_id'] = result[2]
                    return redirect(url_for('add_appointment'))
                else:
                    flash('No active subscriptions, please pay to continue')
                    return redirect(url_for('kyc_step3'))
            if result[3] == 'Approved' and result[4] == 'Approved' and result[5] == 1:
                if is_subscription_active(result[1]):
                    session['username'] = user
                    session['logged_in'] = True
                    session['clinic'] = result[1]
                    session['admin_id'] = result[2]
                    return redirect(url_for('add_appointment'))
                else:
                    flash('No active subscriptions, please pay to continue')
                    return redirect(url_for('kyc_step3'))
            if result[3] != 'Approved' and result[4] == 'Approved' and result[5] == 1:
                if not result[3]:
                    if hasFreeTrialEnded(result[1]):
                        flash('Free Trial is over', 'danger')
                        return redirect(url_for('kyc_step3'))
                    session['username'] = user
                    session['logged_in'] = True
                    session['clinic'] = result[1]
                    if not is_free_subscription_done(result[1]):
                        add_subscription(result[1], 'free')
                    flash('Free trial is in progress.', 'danger')
                    return redirect(url_for('add_appointment'))
                return redirect(url_for('kyc_step3'))
            if result[3] != 'Approved' and result[4] != 'Approved' and result[5] == 1:
                return redirect(url_for('kyc_step2'))
            if result[3] != 'Approved' and result[4] != 'Approved' and result[5] != 1:
                return redirect(url_for('register'))
            if hasFreeTrialEnded(result[1]):
                flash('Free Trial is over', 'danger')
                return redirect(url_for('login'))
            flash('Invalid Credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from flask import request

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    ip = request.remote_addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = request.form.get('username')
    if not username:
        username=session.get('username')
    password = request.form.get('password')
    if not password:
        password=session.get('password')

    # Check if IP is blocked
    '''c = conn.cursor(buffered=True)

        c.execute("""
            SELECT COUNT(*) FROM login_logs
            WHERE ip_address = %s AND status = 'failed' AND
                  timestamp > datetime('now', '-1 hour')
        """, (ip,))
        failure_count = c.fetchone()[0]'''

    '''if failure_count >= 5:
            flash("🚫 Too many failed attempts. Try again after some time.", "danger")
            return render_template("admin_login.html")'''

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['username'] = username
        session['password'] = password
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user, pwd = request.form['username'], request.form['password']

        c = conn.cursor(buffered=True)
        c.execute(
            "SELECT d.password, d.clinic_id, d.id, c.payment_verification,c.kyc_verification, c.email_verified FROM admins d, clinics c WHERE d.username=%s and c.id=d.clinic_id",
            (user,))
        result = c.fetchone()
        if result and check_password_hash(result[0], pwd):
            if hasFreeTrialEnded(result[1]) and result[3] == 'Approved' and result[4] == 'Approved' and result[5] == 1:
                if is_subscription_active(result[1]):
                    session['username'] = user
                    session['admin_logged_in'] = True
                    session['clinic'] = result[1]
                    session['admin_id'] = result[2]
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('No active subscriptions, please pay to continue')
                    return redirect(url_for('kyc_step3'))
            if result[3] == 'Approved' and result[4] == 'Approved' and result[5] == 1:
                if is_subscription_active(result[1]):
                    session['username'] = user
                    session['admin_logged_in'] = True
                    session['clinic'] = result[1]
                    session['admin_id'] = result[2]
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('No active subscriptions, please pay to continue')
                    return redirect(url_for('kyc_step3'))

            if result[3] != 'Approved' and result[4] == 'Approved' and result[5] == 1:
                if not result[3]:
                    if hasFreeTrialEnded(result[1]):
                        flash('Free Trial is over', 'danger')
                        return redirect(url_for('kyc_step3'))
                    session['username'] = user
                    session['admin_logged_in'] = True
                    session['clinic'] = result[1]
                    session['admin_id'] = result[2]
                    if not is_free_subscription_done(result[1]):
                        add_subscription(result[1], 'free')
                    flash('Free trial is in progress', 'danger')
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('kyc_step3'))
            if result[3] != 'Approved' and result[4] != 'Approved' and result[5] == 1:
                return redirect(url_for('kyc_step2'))
            if result[3] != 'Approved' and result[4] != 'Approved' and result[5] != 1:
                return redirect(url_for('register'))
            if hasFreeTrialEnded(result[1]):
                flash('Free Trial is over', 'danger')
                return redirect(url_for('admin_login'))
        flash('Invalid Credentials', 'danger')
        return redirect(url_for('admin_login'))

        c = conn.cursor(buffered=True)
        c.execute(
            "SELECT a.id FROM admins a, clinics c WHERE a.username=%s and c.id=a.clinic_id",
            (username,))
        result = c.fetchone()
        if result and result[0]:
            session['admin_id'] = result[0]
        c = conn.cursor(buffered=True)
        c.execute(
            "SELECT a.clinic_id,a.password ,c.kyc_verification , a.email_verified,c.payment_verification FROM admins a, clinics c WHERE a.username=%s and c.id=a.clinic_id",
            (username,))
        result = c.fetchone()
        if result and check_password_hash(result[1], password):
            if not is_subscription_active(result[0]):
                if result[4] and result[4] == "Pending Approval":
                    flash("⏰ Your free trial has expired. Please subscribe to continue.")
                    return redirect('/kyc/payment')
            if result[3] != 1:
                flash("🚫 Email verification is pending, Please submit verification via email", "danger")
                return redirect("/kyc/documents")
            if not result[2]:
                flash("🚫 KYC verification is pending, please enter details", "danger")
                return redirect('/kyc/documents')
            elif result[2] == "Pending Approval":
                flash("🚫 KYC verification is pending, once verified will notify", "danger")
                return redirect("/kyc/documents")
        c.execute(
            "SELECT a.password ,c.kyc_verification , a.email_verified, c.payment_verification FROM admins a, clinics c WHERE a.username=%s and c.id=a.clinic_id",
            (username,))
        result = c.fetchone()
        if result and check_password_hash(result[0], password):
            # ✅ Log success
            c.execute("INSERT INTO login_logs (username, ip_address, timestamp, status) VALUES (%s, %s, %s, %s)",
                      (username, ip, now, 'success'))
            conn.commit()

            session['super_admin_logged_in'] = False
            session['admin_logged_in'] = True
            if result[3]=="Approved":
                flash("Welcome, Admin!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                print("🚫 KYC payment is pending", "danger")
                return redirect('/kyc/payment')
        else:
            c.execute("SELECT password, clinic_id FROM users WHERE username=%s", (username,))
            result = c.fetchone()
            if result and check_password_hash(result[0], password):
                # ✅ Log success
                c.execute("INSERT INTO login_logs (username, ip_address, timestamp, status) VALUES (%s, %s, %s, %s)",
                          (username, ip, now, 'success'))
                conn.commit()
                session['super_admin_logged_in'] = False
                session['admin_logged_in'] = True
                session['clinic'] = result[1]
                flash("Welcome, Admin!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                # ❌ Log failure
                c.execute("INSERT INTO login_logs (username, ip_address, timestamp, status) VALUES (%s, %s, %s, %s)",
                          (username, ip, now, 'failed'))
                conn.commit()
                session['super_admin_logged_in'] = False
                session['admin_logged_in'] = False
                flash("Invalid username or password", "danger")
            # ❌ Log failure
            c.execute("INSERT INTO login_logs (username, ip_address, timestamp, status) VALUES (%s, %s, %s, %s)",
                      (username, ip, now, 'failed'))
            conn.commit()
            session['super_admin_logged_in'] = False
            session['admin_logged_in'] = False
            flash("Invalid username or password", "danger")
            return render_template("admin_login.html")
    return render_template("admin_login.html")

@app.route('/admin_login_logs')
def admin_login_logs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    c = conn.cursor(buffered=True)
    c.execute("SELECT username, ip_address, timestamp, status FROM login_logs ORDER BY timestamp DESC LIMIT 100")
    logs = c.fetchall()

    return render_template("admin_login_logs.html", logs=logs)


@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/manage_doctors', methods=['GET', 'POST'])
def manage_doctors():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))

    c = conn.cursor(buffered=True)
    clinic = session.get("clinic")
    c.execute("SELECT * FROM clinics WHERE id=%s", (clinic,))
    result = c.fetchone()
    clinic_id = ""
    if result:
        clinic_id = result[0]
    if request.method == 'POST':
        c.execute("SELECT * FROM clinics WHERE id=%s", (clinic,))
        clinics = c.fetchone()
        if result:
            clinic_id = clinics[0]
        try:
            passwd = request.form['password']
            admin_id = session['admin_id']
            hashed_password = generate_password_hash(passwd, method='pbkdf2:sha256', salt_length=8)
            c.execute("INSERT INTO doctors(username, password, clinic_id, admin_id, name) VALUES (%s, %s ,%s,%s,%s)",
                      (request.form['username'], hashed_password, clinic_id, admin_id, request.form['name']))
            conn.commit()
        except Exception as e:
            flash('Doctor already exists', 'warning')
        '''logo = request.files.get('logo')
        signature = request.files.get('signature')
        logo_path = signature_path = None
        if logo:
            logo_path = f"static/uploads/logo_{request.form['username']}.png"
            logo.save(logo_path)
        if signature:
            signature_path = f"static/uploads/signature_{request.form['username']}.png"
            signature.save(signature_path)

        c = conn.cursor(buffered=True)
        c.execute("UPDATE doctors SET logo_path=%s, signature_path=%s WHERE clinic_id=%s",
                  (logo_path, signature_path, clinic_id))
        conn.commit()'''
    flash("✅ Uploaded successfully.")
    c.execute("SELECT id ,username FROM doctors where clinic_id=%s", (clinic_id,))
    doctors = c.fetchall()
    c.execute("SELECT  name FROM clinics")
    allClinicsNames = c.fetchall()


    return render_template('manage_doctors.html', doctors=doctors , clinics=allClinicsNames)

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
    conn.commit()

    return redirect(url_for('manage_doctors'))

@app.route('/delete_clinic/<int:clinic_id>')
def delete_clinic(clinic_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn.execute("DELETE FROM clinics WHERE id=%s", (clinic_id,))
    conn.commit()

    return redirect(url_for('manage_clinics'))

@app.route('/delete_users/<int:user_id>')
def delete_users(user_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))

    conn.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    return redirect(url_for('manage_users'))

# --- Appointments ---
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        allergies = request.form['allergies']
        chronic_conditions = request.form['chronic_conditions']
        email = request.form.get('email', '').strip()
        photo = request.files.get('photo')
        is_recurring = request.form.get('is_recurring')
        recurrence_type = request.form['recurrence_type']
        recurrence_end_date = request.form['recurrence_end_date']

        filename = ''
        clinic =session.get('clinic')

        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        date = str(request.form['date'])
        time = request.form['time']
        reason = request.form['reason']
        c = conn.cursor(buffered=True)
        # ✅ Check for existing patient (by name + contact)
        c.execute("SELECT id FROM patients WHERE name=%s AND contact=%s and clinic_id=%s",
                  (name, contact, session.get('clinic')))
        existing = c.fetchone()

        if existing:
            patient_id = existing[0]
        else:
            c.execute(
                "INSERT INTO patients(name, age, gender, contact, photo, email, allergies, chronic_conditions, clinic_id, doctor_id) VALUES (%s, %s, %s, %s, %s , %s, %s , %s, %s, %s)",
                (name, age, gender, contact, filename, email, allergies, chronic_conditions, clinic,
                 session.get('username')))
            patient_id = c.lastrowid
            conn.commit()

        # ✅ Add appointment regardless
        c.execute("INSERT INTO appointments(patient_id, date, time, reason, clinic_id) VALUES (%s, %s, %s, %s, %s)",
                  (patient_id, date, time, reason, clinic))
        conn.commit()
        if is_recurring:
            schedule_recurring_appointments(request.form, recurrence_type, recurrence_end_date, patient_id, date, time,
                                            reason, clinic)

        flash('Appointment Added!', 'success')

    return render_template('add_appointment.html')


@app.route('/history', methods=['GET', 'POST'])
def view_history():
    if not session.get('logged_in'): return redirect(url_for('login'))

    appointments = []
    name = ''

    if request.method == 'POST':
        name = request.form['name']
        #session['last_search_name'] = name  # 🔐 Save in session
    #else:
        #name = session.get('last_search_name', '')  # 💾 Use if available
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if name:
        c = conn.cursor(buffered=True)
        if session.get('clinic'):
            c.execute("SELECT id, name FROM patients WHERE name LIKE %s and clinic_id=%s",
                      ('%' + name + '%', session.get('clinic')))
        else:
            c.execute("SELECT id, name FROM patients WHERE name LIKE %s",
                      ('%' + name + '%',))
        patient = c.fetchone()
        print(patient)
        if patient:
            doctor_id = session['username']
            print( session.get('clinic'), doctor_id)
            if session.get('clinic'):
                c.execute(
                    "SELECT a.date, a.time, a.reason, a.id, a.status, a.patient_id, b.name, a.consult_start_time, a.checkin_time, b.age, b.gender, b.contact, b.email  FROM appointments a, patients b , doctors d  WHERE a.patient_id=%s and b.id=a.patient_id and a.clinic_id=%s  and d.username=b.doctor_id and d.username= %s ORDER BY a.date, a.time DESC",
                    (patient[0], session['clinic'], doctor_id))
            else:
                c.execute(
                    "SELECT a.date, a.time, a.reason, a.id, a.status, a.patient_id, b.name,a.consult_start_time, a.checkin_time, b.age, b.gender, b.contact, b.email  FROM appointments a, patients b , doctors d WHERE a.patient_id=%s and b.id=a.patient_id  and d.username=b.doctor_id and d.username= %s ORDER BY a.date, a.time DESC",
                    (patient[0],doctor_id))
            appointments = c.fetchall()
            print(appointments)
    if name == '':
        doctor_id = session['username']
        c = conn.cursor(buffered=True)
        if start_date and end_date:
            c.execute(
                "SELECT a.date, a.time, a.reason, a.id, a.status, a.patient_id, b.name, a.consult_start_time, a.checkin_time, b.age, b.gender, b.contact, b.email FROM appointments a, patients b , doctors d WHERE b.id=a.patient_id and a.clinic_id=%s  and d.username=b.doctor_id and d.username= %s and date BETWEEN %s AND %s ORDER BY a.date, a.time DESC",
                (session.get('clinic'), doctor_id, start_date, end_date))
        else:
            c.execute(
                "SELECT a.date, a.time, a.reason, a.id, a.status, a.patient_id, b.name, a.consult_start_time, a.checkin_time, b.age, b.gender, b.contact, b.email  FROM appointments a, patients b , doctors d WHERE b.id=a.patient_id and a.clinic_id=%s  and d.username=b.doctor_id and d.username= %s ORDER BY a.date, a.time DESC",
                (session.get('clinic'),doctor_id))
        appointments = c.fetchall()

    return render_template('view_history.html', appointments=appointments)


@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient_profile(patient_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        email = request.form['email']
        photo = request.files.get('photo')
        allergies = request.form.get("allergies")
        chronic = request.form.get("chronic_conditions")
        clinic = session['clinic']
        # save to DB
        c.execute("UPDATE patients SET allergies=%s, chronic_conditions=%s WHERE id=%s and clinic_id=%s",
                  (allergies, chronic, patient_id, clinic))

        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            c.execute(
                "UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s, email=%s, photo=%s WHERE id=%s and clinic_id=%s",
                (name, age, gender, contact, email, filename, patient_id, clinic))
        else:
            c.execute("UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s , email=%s  WHERE id=%s and clinic_id=%s",
                      (name, age, gender, contact, email, patient_id, clinic))
        conn.commit()
    c.execute("SELECT * FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()
    if patient:
        allergies = (patient[7])
        chronic_conditions = (patient[8])
        c.execute("SELECT * FROM appointments WHERE patient_id=%s and clinic_id=%s ORDER BY date DESC",
                  (patient_id, session['clinic']))
        appointments = c.fetchall()
        c = conn.cursor(buffered=True)
        c.execute("SELECT * FROM patients WHERE id=%s", (patient_id,))
        patient = c.fetchone()

        c.execute("SELECT id, chat, timestamp FROM chat_history WHERE patient_id=%s ORDER BY timestamp DESC",
                  (patient_id,))
        chats = c.fetchall()
        return render_template('patient_profile.html', patient=patient, allergies=allergies,
                               chronic_conditions=chronic_conditions, appointments=appointments,
                               patient_id=patient_id, chat_history=chats)

    return render_template('patient_profile.html', patient_id=patient_id)


@app.route('/update_status/<int:appointment_id>/<string:status>')
def update_status(appointment_id, status):
    if not session.get('logged_in'): return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    c.execute("UPDATE appointments SET status=%s WHERE id=%s", (status, appointment_id))
    conn.commit()
    return redirect(url_for('view_history'))

# --- Prescriptions ---
@app.route('/add_prescription/<int:appointment_id>', methods=['GET', 'POST'])
def add_prescription(appointment_id):
    if request.method == 'POST':
        new_complaint = request.form.get("complaint", "").strip().upper()

        if new_complaint:
            c = conn.cursor(buffered=True)
            c.execute("SELECT * FROM complaints_master WHERE complaint=%s", (new_complaint,))
            result = c.fetchone()
            if not result:
                c = conn.cursor(buffered=True)
                c.execute("INSERT OR IGNORE INTO complaints_master (complaint) VALUES (%s)", (new_complaint,))
                conn.commit()

        data = request.form

        # Get vitals & diagnosis
        height = data.get('height')
        weight = data.get('weight')
        pulse = data.get('pulse')
        bp = data.get('bp')
        temp = data.get('temp')
        oxygen =data.get('oxygen')
        complaint = data.get('complaint')
        frequency = data.get('frequency')
        severity = data.get('severity')
        duration = data.get('duration')
        complaint_date = data.get('complaint_date')

        diagnosis = data.get('diagnosis')
        diagnosis_duration = data.get('diagnosis_duration')
        diagnosis_date = data.get('diagnosis_date')

        prescription = data.get('prescription')
        notes = data.get('notes')
        advice = request.form.get("advice")
        tests_requested = request.form.get("tests_requested")
        if request.form.get("next_visit_num") !='':
            next_visit_num = request.form.get("next_visit_num")
        else:
            next_visit_num = 0
        next_visit_unit = request.form.get("next_visit_unit")
        next_visit_date = request.form.get("next_visit_date")
        ref_doctor = request.form.get("ref_doctor")
        ref_speciality = request.form.get("ref_speciality")
        ref_phone = request.form.get("ref_phone")
        ref_email = request.form.get("ref_email")
        systemic_exam = request.form.get("systemic_exam")
        past_meds = request.form.get("past_meds")

        # then insert/update in DB

        rx_json = data.get('rx_json')
        clinic = session['clinic']
        c = conn.cursor(buffered=True)
        c.execute("""
                        UPDATE appointments SET
                            height=%s, weight=%s, pulse=%s, bp=%s, temp=%s,oxygen=%s,
                            complaint=%s, frequency=%s, severity=%s, duration=%s, complaint_date=%s,
                            diagnosis=%s, diagnosis_duration=%s, diagnosis_date=%s, notes=%s,
                            prescription=%s, rx_json=%s, advice=%s,tests_requested=%s, next_visit_num=%s,
                            next_visit_unit=%s,next_visit_date=%s,ref_doctor=%s,ref_speciality=%s,
                            ref_phone=%s,ref_email=%s,systemic_exam=%s,past_meds=%s
                        WHERE id=%s and clinic_id=%s
                    """, (
            height, weight, pulse, bp, temp, oxygen,
            complaint, frequency, severity, duration, complaint_date,
            diagnosis, diagnosis_duration, diagnosis_date, notes,
            prescription, rx_json, advice, tests_requested, next_visit_num,
            next_visit_unit, next_visit_date, ref_doctor, ref_speciality,
            ref_phone, ref_email, systemic_exam, past_meds,
            appointment_id, clinic
        ))
        conn.commit()

        flash("Prescription saved successfully", "success")
        return redirect(url_for('view_history'))

    else:
        c = conn.cursor(buffered=True)
        c.execute("SELECT * FROM appointments WHERE id=%s and clinic_id=%s", (appointment_id, session['clinic']))
        appt = c.fetchone()

        # use column indices from DB schema
        if appt:
            data = {
                'height': appt[8],
                'weight': appt[9],
                'pulse': appt[10],
                'bp': appt[11],
                'temp': appt[12],
                'complaint': appt[13],
                'frequency': appt[14],
                'severity': appt[15],
                'duration': appt[16],
                'complaint_date': appt[17],
                'diagnosis': appt[18],
                'diagnosis_duration': appt[19],
                'diagnosis_date': appt[20],
                'notes': appt[7],
                'prescription': appt[5],
                'rx_json': appt[21],
                'advice': appt[23],
                'tests_requested': appt[24],
                'next_visit_num': appt[25],
                'next_visit_unit': appt[26],
                'next_visit_date': appt[27],
                'ref_doctor': appt[28],
                'ref_speciality': appt[29],
                'ref_phone': appt[30],
                'ref_email': appt[31],
                'systemic_exam': appt[32],
                'past_meds': appt[33],
                'oxygen':appt[34]
            }
        else:
            data = {}

        rx_json = request.form.get("rx_json", "")
        rx_rows = []
        try:
            if appt[21]:
                rx_rows = json.loads(appt[21])
                c = conn.cursor(buffered=True)
                for rx in rx_rows:
                    med = rx.get('medicine', '').strip().upper()
                    if med:
                        c = conn.cursor(buffered=True)
                        c.execute("SELECT medicine FROM medicines_master where medicine=%s", (med,))
                        result = c.fetchone()
                        if not result:
                            c.execute("INSERT INTO medicines_master (medicine) VALUES (%s)", (med,))
                conn.commit()
        except Exception as e:
            print("❌ Rx JSON parse error:")

        c = conn.cursor(buffered=True)
        c.execute("SELECT medicine FROM medicines_master ORDER BY medicine")
        medicine_list = [row[0] for row in c.fetchall()]

        c = conn.cursor(buffered=True)
        c.execute("SELECT complaint FROM complaints_master ORDER BY complaint")
        complaints_list = [row[0] for row in c.fetchall()]
        if appt:
            new_diagnosis = appt[18]
            if new_diagnosis:
                c = conn.cursor(buffered=True)
                c.execute("SELECT diagnosis FROM diagnosis_master where diagnosis=%s", (new_diagnosis,))
                result = c.fetchone()
                if not result:
                    c = conn.cursor(buffered=True)
                    c.execute("INSERT INTO diagnosis_master (diagnosis) VALUES (%s)", (new_diagnosis,))
                    conn.commit()
        c.execute("SELECT diagnosis FROM diagnosis_master ORDER BY diagnosis")
        diagnosis_list = [row[0] for row in c.fetchall()]
        c = conn.cursor(buffered=True)
        c.execute("SELECT patient_id FROM appointments where id=%s", (appointment_id,))
        result = c.fetchone()
        patient_id = result[0]
        c = conn.cursor(buffered=True)
        # Get patient name
        c.execute("SELECT name FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
        patient = c.fetchone()
        # Appointments + prescriptions
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now()
        current_time = now.time()
        formatted_time = datetime.now().strftime("%H:%M:%S")

        c.execute("""SELECT 'appointment' AS type, date, time, reason, status, id, prescription, rx_json, notes,diagnosis
                        FROM appointments
                        WHERE patient_id=%s and clinic_id=%s and date < %s
                    """, (patient_id, session['clinic'], today,))
        appointments = c.fetchall()
        uploads = []

        if appointments:
            prescription = appointments[0] if appointments[0] else ''

            rx_list = json.loads(prescription[7]) if prescription[7] else ''
            # Uploads
            c.execute("""
                            SELECT 'upload' AS type, upload_date AS date, '' AS time, category, '' AS status, filename, ''
                            FROM uploads
                            WHERE patient_id=%s
                        """, (patient_id,))
            uploads = c.fetchall()


        # Combine and sort by date descending
        timeline = appointments + uploads
        timeline.sort(key=lambda x: x[1], reverse=True)
        c = conn.cursor(buffered=True)
        c.execute("SELECT * FROM rx_groups")
        rx_groups = c.fetchall()
        return render_template("add_prescription.html", **data , complaints=complaints_list, diagnosis_list=diagnosis_list, medicine_list=medicine_list, patient_id=result[0], patient=patient, timeline=timeline, rx_groups=rx_groups, rx_rows=rx_rows)


@app.route('/download_prescription/<int:appointment_id>')
def download_prescription(appointment_id):
    c = conn.cursor(buffered=True)
    c.execute("""
                      SELECT p.name,
                             p.age,
                             p.gender,
                             p.contact,
                             p.photo,
                             a.date,
                             a.time,
                             a.reason,
                             a.prescription,
                             a.rx_json,
                             p.id,
                             a.notes
                      FROM appointments a
                               JOIN patients p ON a.patient_id = p.id
                      WHERE a.id = %s and a.clinic_id=%s
                      """, (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid appointment ID"

    name, age, gender, contact, photo, date, time, reason, prescription, rx_json, patient_id, notes = row

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)

    c.execute("SELECT name, address, phone FROM clinics WHERE id=%s", ( session['clinic'],))
    clinic = c.fetchone()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, clinic[0], ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "", ln=1, align='C')
    pdf.cell(200, 10, clinic[1], ln=1, align='C')
    pdf.cell(200, 10, clinic[2], ln=1, align='C')

    # Patient Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Prescription for {name}", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, f"Age: {age}", ln=0)
    pdf.cell(100, 8, f"Gender: {gender}", ln=1)
    pdf.cell(100, 8, f"Contact: {contact}", ln=0)
    pdf.cell(100, 8, f"Date: {date} {time}", ln=1)
    pdf.cell(200, 8, f"Reason: {reason}", ln=1)
    pdf.ln(5)

    # Prescription
    pdf.set_font("Arial", 'B', 12)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, notes if notes else "")
    pdf.ln(10)

    pdf.cell(200, 10, "Prescription:", ln=1)
    pdf.ln(2)
    pdf.multi_cell(0, 8, prescription if prescription else "")
    # Parse Rx lines from text
    if rx_json:
        try:
            rx_list = json.loads(rx_json)
            if rx_list:
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Rx", ln=1)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(60, 8, "Medicine", 1)
                pdf.cell(15, 8, "Dose", 1)
                pdf.cell(25, 8, "Timing", 1)
                pdf.cell(25, 8, "Freq.", 1)
                pdf.cell(25, 8, "Duration", 1)
                pdf.cell(50, 8, "Note", 1)
                pdf.ln()
                pdf.set_font("Arial", size=10)
                for rx in rx_list:
                    pdf.cell(60, 8, rx['medicine'], 1)
                    pdf.cell(15, 8, rx['dose'], 1)
                    pdf.cell(25, 8, rx['timing'], 1)
                    pdf.cell(25, 8, rx['frequency'], 1)
                    pdf.cell(25, 8, rx['duration'], 1)
                    pdf.cell(50, 8, rx['note'], 1)
                    pdf.ln()
        except Exception as e:
            pdf.cell(200, 10, txt="Error reading prescription table.", ln=1)

    # Signature
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    sign_path = "static/signature.png"
    name=patient[2]
    if patient[1] and os.path.exists(patient[1]):
        pdf.image(patient[1], x=150, y=pdf.get_y(), w=40)
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, f"Signature  Dr.{name}", ln=1, align='R')

    # QR Code
    # Output
    global filename, file_dat
    filename = f"Prescription for {name} - {date}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename = filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'
    return send_file(filename, download_name=filename, as_attachment=True)

def pdfmail (appointment_id):
    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT p.name, p.age, p.gender, p.contact, p.photo, a.date, a.time, a.reason, a.prescription, a.rx_json, p.id, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.id=%s and a.clinic_id=%s
            """, (appointment_id, session['clinic']))
    row = c.fetchone()

    if not row:
        return "Invalid appointment ID"

    name, age, gender, contact, photo, date, time, reason, prescription,rx_json, patient_id , notes= row

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    logo_path = "static/logo.jpeg"
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)

    c.execute("SELECT name, address, phone FROM clinics WHERE id=%s", (session['clinic'],))
    clinic = c.fetchone()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, clinic[0], ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "", ln=1, align='C')
    pdf.cell(200, 10, clinic[1], ln=1, align='C')
    pdf.cell(200, 10, clinic[2], ln=1, align='C')

    # Patient Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Prescription for {name}", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, f"Age: {age}", ln=0)
    pdf.cell(100, 8, f"Gender: {gender}", ln=1)
    pdf.cell(100, 8, f"Contact: {contact}", ln=0)
    pdf.cell(100, 8, f"Date: {date} {time}", ln=1)
    pdf.cell(200, 8, f"Reason: {reason}", ln=1)
    pdf.ln(5)

    # Prescription
    pdf.set_font("Arial", 'B', 12)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, notes if notes else "")
    pdf.ln(10)

    pdf.cell(200, 10, "Prescription:", ln=1)
    pdf.ln(2)
    # Parse Rx lines from text
    pdf.multi_cell(0, 8, prescription if prescription else "")
    if rx_json:
        try:
            rx_list = json.loads(rx_json)
            if rx_list:
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Rx", ln=1)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(40, 8, "Medicine", 1)
                pdf.cell(25, 8, "Dose", 1)
                pdf.cell(25, 8, "Timing", 1)
                pdf.cell(25, 8, "Freq.", 1)
                pdf.cell(25, 8, "Duration", 1)
                pdf.cell(50, 8, "Note", 1)
                pdf.ln()
                pdf.set_font("Arial", size=10)
                for rx in rx_list:
                    pdf.cell(40, 8, rx['medicine'], 1)
                    pdf.cell(25, 8, rx['dose'], 1)
                    pdf.cell(25, 8, rx['timing'], 1)
                    pdf.cell(25, 8, rx['frequency'], 1)
                    pdf.cell(25, 8, rx['duration'], 1)
                    pdf.cell(50, 8, rx['note'], 1)
                    pdf.ln()
        except Exception as e:
            pdf.cell(200, 10, txt="Error reading prescription table.", ln=1)

    # Signature
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    sign_path = "static/signature.png"
    name=patient[2]
    if patient[1] and os.path.exists(patient[1]):
        pdf.image(patient[1], x=150, y=pdf.get_y(), w=40)
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, f"Signature  Dr.{name}", ln=1, align='R')

    # QR Code
    # Output
    global filename, file_data
    filename = f"Prescription for {name}_{date}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        file_data = f.read()
        filename=filename
        part = MIMEApplication(file_data, Name="prescription.pdf")
        part['Content-Disposition'] = 'attachment; filename="prescription.pdf"'
    return send_file(filename, download_name=filename, as_attachment=True)


# ✅ Feature: Prescription History Per Patient
@app.route('/prescriptions/<int:patient_id>')
def view_prescriptions(patient_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    c.execute("""
                SELECT a.date, a.time, a.reason, a.prescription, a.id, a.rx_json
                FROM appointments a
                WHERE a.patient_id=%s and a.clinic_id=%s
                ORDER BY a.date DESC
            """, (patient_id, session['clinic']))
    prescriptions = c.fetchall()
    prescription = prescriptions[0] if prescriptions[0] else ''
    rx_list = json.loads(prescription[5]) if prescription[5] else ''
    c.execute("SELECT name FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()
    #return render_template('prescription_history.html', prescriptions=prescriptions, patient_name=patient[0] if patient else '', patient_id=patient_id)
    return render_template('prescription_history.html' , prescriptions=prescriptions , patient_name=patient[0] if patient else '', patient_id=patient_id, rx_list=rx_list)


from datetime import date
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload/<int:patient_id>', methods=['GET', 'POST'])
def upload_file(patient_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        category = request.form['category']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            c = conn.cursor(buffered=True)
            c.execute("INSERT INTO uploads(patient_id, filename, category, upload_date) VALUES (%s, %s, %s, %s)",
                         (patient_id, filename, category, date.today()))
            conn.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('view_uploads', patient_id=patient_id))
    return render_template('upload_file.html', patient_id=patient_id)

@app.route('/uploads/<int:patient_id>')
def view_uploads(patient_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM uploads WHERE patient_id=%s ORDER BY upload_date DESC", (patient_id,))
    files = c.fetchall()
    c.execute("SELECT name FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()

    return render_template('view_uploads.html', files=files, patient_name=patient[0] if patient else '', patient_id=patient_id)

from datetime import datetime, timedelta

def send_appointment_reminders():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    c = conn.cursor(buffered=True)
    c.execute('''
                SELECT p.name, p.email, a.date, a.time
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.date=%s AND p.email IS NOT NULL and p.clinic_id=%s
            ''', (tomorrow, session['clinic']))
    appointments = c.fetchall()
    for name, email, date, time in appointments:
        subject = "Appointment Reminder"
        body = f"Dear {name},\n\nThis is a reminder that you have an appointment on {date} at {time}.\n\n– Clinic Team"

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            print(f"Sent reminder to {email}")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")

@app.route('/patient/<int:patient_id>/timeline')
def patient_timeline(patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    c = conn.cursor(buffered=True)
    # Get patient name
    c.execute("SELECT name FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()

    # Appointments + prescriptions
    c.execute("""
                SELECT 'appointment' AS type, date, time, reason, status, id, prescription, rx_json
                FROM appointments
                WHERE patient_id=%s and clinic_id=%s
            """, (patient_id, session['clinic']))
    appointments = c.fetchall()
    prescription = appointments[0] if appointments[0] else ''

    rx_list = json.loads(prescription[7]) if prescription[7] else ''
    # Uploads
    c.execute("""
                SELECT 'upload' AS type, upload_date AS date, '' AS time, category, '' AS status, filename, ''
                FROM uploads
                WHERE patient_id=%s
            """, (patient_id,))
    uploads = c.fetchall()

    # Combine and sort by date descending
    timeline = appointments + uploads
    timeline.sort(key=lambda x: x[1], reverse=True)

    return render_template('patient_timeline.html', patient_name=patient[0], patient_id=patient_id, timeline=timeline, rx_list=rx_list)

from fpdf import FPDF

from flask import request, render_template_string
from io import BytesIO
from fpdf import FPDF
from datetime import datetime

@app.route('/export_timeline/<int:patient_id>', methods=['GET', 'POST'])
def export_timeline(patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    c = conn.cursor(buffered=True)
    c.execute("SELECT name FROM patients WHERE id=%s and clinic_id=%s", (patient_id, session['clinic']))
    patient = c.fetchone()

    start = request.args.get('start_date', '')
    end = request.args.get('end_date', '')

    query = "SELECT date, time, reason, status, prescription,notes FROM appointments WHERE patient_id=%s and clinic_id=%s"
    params = [patient_id, session['clinic']]

    if start and end:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start, end])

    query += " ORDER BY date DESC"
    c.execute(query, params)
    appointments = c.fetchall()

    # Uploads
    upload_query = "SELECT upload_date, category, filename FROM uploads WHERE patient_id=%s"
    if start and end:
        upload_query += " AND upload_date BETWEEN %s AND %s"
    c.execute(upload_query + " ORDER BY upload_date DESC", params)
    uploads = c.fetchall()

    # PDF generation
    pdf = FPDF()
    pdf.add_page()

    # Logo + Header
    c = conn.cursor(buffered=True)
    c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
    patient = c.fetchone()
    logo_path = "static/logo.jpeg"  # Add a logo to your project folder
    if patient[0] and os.path.exists(patient[0]):
        pdf.image(patient[0], x=10, y=8, w=30)
        pdf.set_y(20)
    c.execute("SELECT name, address, phone FROM clinics WHERE id=%s", (session['clinic'],))
    clinic = c.fetchone()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, clinic[0], ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "", ln=1, align='C')
    pdf.cell(200, 10, clinic[1], ln=1, align='C')
    pdf.cell(200, 10, clinic[2], ln=1, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Patient: {patient[0]}", ln=1)
    if start and end:
        pdf.cell(200, 8, txt=f"Filtered Date Range: {start} to {end}", ln=1)
    pdf.ln(4)

    # Appointments
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Appointments & Prescriptions", ln=1)

    pdf.set_font("Arial", size=11)
    for appt in appointments:
        pdf.multi_cell(100, 8, f" {appt[0]} {appt[1]} | Reason: {appt[2]} | Status: {appt[3]}")
        if appt[4]:
            pdf.set_font("Arial", 'I', 11)
            pdf.multi_cell(0, 7, f"Prescription:\n{appt[4]}")
            pdf.multi_cell(0, 7, f"Notes:\n{appt[5]}")
            pdf.set_font("Arial", size=11)
        pdf.ln(2)

    # Uploads
    if uploads:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Uploaded Documents", ln=1)
        pdf.set_font("Arial", size=11)
        for u in uploads:
            pdf.multi_cell(0, 8, f" {u[1]}: {u[2]} (Uploaded on {u[0]})")
            pdf.ln(1)

        # Signature
        c = conn.cursor(buffered=True)
        c.execute("SELECT logo_path, signature_path, name FROM doctors WHERE clinic_id=%s", (session['clinic'],))
        patient = c.fetchone()
        sign_path = "static/signature.png"
        name=patient[2]
        if patient[1] and os.path.exists(patient[1]):
            pdf.image(patient[1], x=150, y=pdf.get_y(), w=40)
            pdf.ln(15)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 6, f"Signature  Dr.{name}", ln=1, align='R')
    # Export to memory
    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    filename = f"timeline_patient_{patient_id}.pdf"
    return send_file(output, download_name=filename, as_attachment=True)

@app.route('/templates', methods=['GET', 'POST'])
def manage_templates():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    c = conn.cursor(buffered=True)
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        c.execute("INSERT INTO templates(name, content) VALUES (%s, %s)", (name, content))
        conn.commit()
    c.execute("SELECT * FROM templates")
    templates = c.fetchall()
    return render_template('manage_templates.html', templates=templates)

@app.route('/template/<int:template_id>')
def get_template_content(template_id):
    c = conn.cursor(buffered=True)
    c.execute("SELECT content FROM templates WHERE id=%s", (template_id,))
    row = c.fetchone()
    return row[0] if row else ''

@app.route('/delete_upload/<int:upload_id>/<int:patient_id>')
def delete_upload(upload_id, patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    c = conn.cursor(buffered=True)
    # Get filename before deleting
    c.execute("SELECT filename FROM uploads WHERE id=%s", (upload_id,))
    row = c.fetchone()
    if row:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], row[0])
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        # Delete DB record
        c.execute("DELETE FROM uploads WHERE id=%s", (upload_id,))
        conn.commit()
        flash('Upload deleted.', 'success')
    else:
        flash('File not found.', 'danger')

    return redirect(url_for('view_uploads', patient_id=patient_id))

@app.route("/")
def landing_page():
    return render_template("landing.html")

from flask import redirect, request, session, url_for

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))  # redirect back



if __name__ == '__main__':
    '''cursor = conn.cursor(buffered=True)
    cursor.execute("SHOW TABLES;")
    for table in cursor.fetchall():
        print(table)'''
    '''generate_token()

    expire_old_subscriptions(conn)
    if len(sys.argv) > 1 and sys.argv[1] == "reminder":
        send_appointment_reminders()
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
        from flask_babel import Babel

        babel = Babel(app)


        @babel.default_locale
        def get_locale():
            return session.get('lang', 'en')  # default to English

        from flask_babel import _

        flash(_("Patient added successfully"))'''

    from flask import Flask
    import os

    app = Flask(__name__)


    @app.route("/")  # ✅ must exist
    def home():
        return "Hello, Render!"


    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

