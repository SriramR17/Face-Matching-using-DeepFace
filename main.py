from actions.google_drive_utils import download_images_from_drive
from actions.face_matching import match_faces
from actions.display_results import display_images
from actions.email_sender import send_email_with_images

# Paths & Configurations
reference_image_path = "https://a1cf74336522e87f135f-2f21ace9a6cf0052456644b80fa06d4f.ssl.cf2.rackcdn.com/images/characters/large/800/Phil-Dunphy.Modern-Family.webp"  # Change to your reference image
google_drive_folder_id = "1"  # Replace with your Drive folder ID 
receiver_email = "bigiljd282@gmail.com"  # ✅ Update with recipient email

# Download only missing images from Drive
group_photos = download_images_from_drive(google_drive_folder_id)

# Perform Face Matching
matched_images, unmatched_images = match_faces(reference_image_path, group_photos)

# Display Results
display_images(matched_images, "Matched ✅")
display_images(unmatched_images, "Unmatched ❌")

# Send matched images via email
send_email_with_images(receiver_email, matched_images)

