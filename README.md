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

## 🛠 Manual Test (Reduce the image size to **320x320 thumbnail**)

admin_@cloudshell:~ (github-actions-111)$ gsutil cp image.jpg gs://image-upload-bucket-111
Copying file://image.jpg [Content-Type=image/jpeg]...
- [1 files][229.9 KiB/229.9 KiB]                                                
Operation completed over 1 objects/229.9 KiB.

admin_@cloudshell:~ (github-actions-111)$ gsutil ls gs://image-thumbnail-bucket/thumbs/                                                                                                                                                                                    
gs://image-thumbnail-bucket/thumbs/image.jpg
Operation completed over 1 objects/14.9 KiB.


  
