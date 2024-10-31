from flask import Flask, jsonify, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from appwrite.client import Client
from appwrite.services.databases import Databases
from geopy.geocoders import Nominatim
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # You can change this to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

# Calling the Nominatim tool
geoLoc = Nominatim(user_agent="GetLoc")

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configurations
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = 465
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID')
API_KEY = os.getenv('APPWRITE_API_KEY')
EXISTING_DATABASE_ID = os.getenv('APP_WRITE_DATABASE_ID')
EXISTING_COLLECTION_ID = os.getenv('APPWRITE_COMPLAINTS_COLLECTION_ID')

# Initialize Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project(PROJECT_ID)
client.set_key(API_KEY)
databases = Databases(client)

def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(MAIL_USERNAME, to_address, text)
        server.quit()
        logger.info(f"Email successfully sent to {to_address}")
        return {"message": f"Email successfully sent to {to_address}"}
    except Exception as e:
        logger.error(f"Failed to send email to {to_address}: {str(e)}")
        return {"error": str(e)}

@app.route("/process-complaint", methods=["POST"])
def process_complaint():
    data = request.get_json()
    complaint_id = data.get("complaint_id")

    if not complaint_id:
        logger.warning("Complaint ID is required.")
        return {"error": "Complaint ID is required."}, 400

    logger.info(f"Processing complaint ID: {complaint_id}")

    try:
        complaint = databases.get_document(
            database_id=EXISTING_DATABASE_ID,
            collection_id=EXISTING_COLLECTION_ID,
            document_id=complaint_id
        )
        logger.info(f"Complaint retrieved: {complaint}")
    except Exception as e:
        logger.error(f"Error retrieving complaint: {str(e)}")
        return {"error": str(e)}, 400  # Handle errors gracefully

    upvotes_count = len(complaint.get('upvotes', []))
    user_email = os.getenv('GOVERNMENT_EMAIL')

    logger.info(f"Upvotes count: {upvotes_count} for complaint ID: {complaint_id}")

    if upvotes_count > 5:  # Updated to check for > 5
        # Prepare email for admin
        email_body = f"""
        Subject: {complaint.get('title')}
        Description: {complaint.get('description')}
        Location: {complaint.get('location')}
        Contact Number: {complaint.get('contactNumber')}
        Current Location (GPS): {geoLoc.reverse(complaint.get('currentLocation'))}
        Number of Upvotes: {upvotes_count}
        Image Links: {', '.join(complaint.get('imageLinks', []))}
        """
        
        # Send to admin
        admin_email =  os.getenv('USER_EMAIL')
        response = send_email(admin_email, "Complaint with High Upvotes", email_body)
        
        # Delete the complaint if email was successful
        if response.get("message"):
            databases.delete_document(
                database_id=EXISTING_DATABASE_ID,
                collection_id=EXISTING_COLLECTION_ID,
                document_id=complaint['$id']
            )
            logger.info(f"Complaint sent to {admin_email} and deleted successfully.")
            return {"message": f"Complaint sent to {admin_email} and deleted successfully."}
        else:
            logger.error("Failed to send email to admin.")
            return {"error": "Failed to send email to admin."}

    else:
        # Send notification to the user that upvotes were insufficient
        user_response = send_email(
            user_email,
            "Complaint Update",
            "Your complaint did not have enough upvotes (must be > 5) to notify the admin."
        )
        
        logger.info("User notification sent about insufficient upvotes.")
        return {"message": user_response.get("message", "Failed to send notification email to user.")}

if __name__ == "__main__":
    app.run(debug=True)
