# 🧠 Sketch Image Hashing System

A system that generates perceptual hashes from sketch images to detect duplicate and visually similar UI designs.

---

## 📌 Project Overview
This project focuses on image hashing techniques to identify similarities between sketch-based UI designs. It uses perceptual hashing (pHash) to generate unique fingerprints for images, enabling efficient comparison and duplicate detection.

---

## 🛠️ Tech Stack
- Python
- Flask
- OpenCV
- PIL (Pillow)
- ImageHash Library

---

## ✨ Features
- Upload sketch images
- Generate unique image hash
- Compare multiple sketches
- Detect duplicate UI designs
- Fast and efficient similarity detection

---

## 🧠 How It Works
1. Input sketch image is processed
2. Image is converted into a perceptual hash (pHash)
3. Hash values are compared
4. Similarity score is calculated
5. Output shows whether images are similar or different

---

## 📂 Project Structure
- `app.py` → Main application
- `templates/` → Frontend UI
- `static/` → Uploaded images
- `models/` → Hash processing logic

---

## 🚀 How to Run

1. Clone the repository:git clone https://github.com/your-username/image-hash-sketch.git
2. Install dependencies:pip install -r requirements.txt
3. Run the application:python app.py
4. Open in browser:http://localhost:5000


---

## 📊 Example Output
- Hash 1: `ffab23cd...`
- Hash 2: `ffab22cd...`
- Difference Score: `2` → Images are similar

---

## 🎯 Future Improvements
- Improve similarity accuracy using deep learning
- Support real-time comparison
- Store hashes in database
- Integrate with sketch-to-code system

---
