# Image-Processing-Pipeline-GCS-PubSub-CloudFunction
This repository is used to automates **asynchronous image processing** in Google Cloud using GCS, Pub/Sub, CloudFunction, GitHubActions
# 📷 GCP Image Thumbnail Pipeline (Cloud Function + Pub/Sub)

This project automates **asynchronous image processing** in Google Cloud using:

- **Cloud Storage** → Stores original images & thumbnails
- **Pub/Sub** → Event-driven decoupled processing
- **Cloud Functions (Gen 2)** → Python function to resize images
- **GitHub Actions** → Automates deployment

---

## 🚀 Overview

**Workflow:**
1. User uploads an image to the **upload bucket**.
2. **Cloud Storage** triggers a **Pub/Sub** message when a new file is finalized.
3. **Cloud Function** receives the message, downloads the image, creates a **320x320 thumbnail**, and uploads it to the **thumbnail bucket**.

---

## 📂 Project Structure

gcp-image-pipeline/
├── .github/
│ └── workflows/
│ └── deploy.yml # GitHub Actions workflow
├── functions/
│ └── image_processor/
│ ├── main.py # Full image processing logic
│ ├── requirements.txt # Dependencies for Pillow + GCS
│ └── .gcloudignore # Ignore unneeded files
├── README.md

  
