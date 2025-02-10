# Face Matching Web Application  

## 📌 Overview  
This web application enables users to:
- **Upload an image** or **take a selfie**  
- Compare the uploaded image with **a folder of group images stored in Google Drive**  
- Display the **matched images** on the webpage  
- **Send the matched images via email** (optional)  

## 🛠 Technologies Used  
- **DeepFace** → Face Matching  
- **OpenCV** → Face Detection  
- **Flask** → Backend API  
- **Google Drive API** → Access group images from the cloud  
- **HTML, Tailwind CSS, JavaScript** → Frontend  

---

## 🚀 Features  
✅ Upload an image from the device  
✅ Take a selfie using the webcam  
✅ Compare the uploaded image with stored group images  
✅ Display matched images on the webpage  
✅ Send matched images to an email  

---

## 💂‍♂️ How to Clone & Run the App  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/yourusername/face-matching-app.git
cd face-matching-app
```

### **2️⃣ Create & Activate Virtual Environment**  
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Google Drive API**  
- Download your **Google Drive API `credentials.json`**  
- Place it in the **project root directory**  
- Set the json file path in goolge_drive_utils.py file

### **5️⃣ Run the Flask Application**  
```sh
python app.py
```
Now, open your browser and go to:  
👉 **http://127.0.0.1:5000/**  


## 📩 Send Matched Images via Email  
- Users can enter their **email address**  
- Click the **"Send Matched Images"** button  
- Matched images will be emailed to them  

---


