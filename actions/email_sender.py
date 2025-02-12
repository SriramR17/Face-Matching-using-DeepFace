import smtplib
import os
import cv2
import mimetypes
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"  # Update for Outlook/Yahoo if needed
SMTP_PORT = 587  # Standard SMTP port for TLS
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')   # ✅ Generate an App Password

def save_matched_images(images, output_folder="matched_images"):
    """ Saves matched images locally before sending via email """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    saved_paths = []
    for idx, img in enumerate(images):
        img_path = os.path.join(output_folder, f"matched_{idx+1}.jpg")
        cv2.imwrite(img_path, img)
        saved_paths.append(img_path)

    return saved_paths

def send_email_with_images(receiver_email, matched_images):
    """ Sends matched images via email as attachments """
    if not matched_images:
        print("🚫 No matched images to send.")
        return

    # Save images locally before attaching
    image_paths = save_matched_images(matched_images)

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg["Subject"] = "Matched Face Images 📸"

    msg.set_content(f"Attached are {len(image_paths)} matched images.")

    # Attach images
    for image_path in image_paths:
        with open(image_path, "rb") as f:
            file_data = f.read()
            file_type, _ = mimetypes.guess_type(image_path)
            msg.add_attachment(file_data, maintype="image", subtype=file_type.split("/")[1], filename=os.path.basename(image_path))

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent successfully to {receiver_email}!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")