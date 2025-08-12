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

##                                              =========== Created using GitHub MCP =======

# 📷 Image Processing Pipeline - GCS + Pub/Sub + Cloud Functions

[![Deploy Status](https://github.com/bikram-singh/Image-Processing-Pipeline-GCS-PubSub-CloudFunction/workflows/deploy-image-processor/badge.svg)](https://github.com/bikram-singh/Image-Processing-Pipeline-GCS-PubSub-CloudFunction/actions)

A robust, event-driven **asynchronous image processing pipeline** built on Google Cloud Platform that automatically generates thumbnails from uploaded images using Cloud Storage, Pub/Sub, Cloud Functions, and GitHub Actions for CI/CD.

## 🏗️ Architecture Overview

This project implements a serverless, scalable image processing pipeline with the following components:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   User Upload   │───▶│ Cloud Storage│───▶│    Pub/Sub      │───▶│  Cloud Function  │
│   (Original)    │    │  (Upload)    │    │   (Events)      │    │ (Image Processor)│
└─────────────────┘    └──────────────┘    └─────────────────┘    └──────────────────┘
                                                                            │
                                                                            ▼
                                                                   ┌──────────────────┐
                                                                   │ Cloud Storage    │
                                                                   │ (Thumbnails)     │
                                                                   └──────────────────┘
```

### 🔧 Components

- **📦 Cloud Storage (GCS)**: Stores original images and generated thumbnails
- **📨 Pub/Sub**: Provides event-driven, decoupled message processing
- **⚡ Cloud Functions Gen2**: Python-based serverless function for image resizing
- **🚀 GitHub Actions**: Automated CI/CD pipeline for deployment
- **🖼️ PIL (Pillow)**: Image processing library for thumbnail generation

## 🌟 Features

- ✅ **Event-driven processing** - Automatically triggers when images are uploaded
- ✅ **Asynchronous operation** - Non-blocking, scalable processing
- ✅ **Automatic thumbnail generation** - Creates 320x320px thumbnails
- ✅ **Multiple format support** - Handles JPEG, PNG, and other PIL-supported formats
- ✅ **Error handling** - Robust error handling and logging
- ✅ **CI/CD integration** - Automated deployment with GitHub Actions
- ✅ **Serverless architecture** - No server management required
- ✅ **Cost-effective** - Pay-per-use pricing model

## 🚀 Workflow

1. **Upload**: User uploads an image to the **upload bucket** (`gs://image-upload-bucket-111`)
2. **Event Trigger**: Cloud Storage automatically publishes an `OBJECT_FINALIZE` event to Pub/Sub topic
3. **Function Trigger**: Cloud Function receives the Pub/Sub message
4. **Processing**: Function downloads the original image, creates a 320x320 thumbnail
5. **Storage**: Processed thumbnail is uploaded to the **thumbnail bucket** (`gs://image-thumbnail-bucket/thumbs/`)

## 📁 Project Structure

```
Image-Processing-Pipeline-GCS-PubSub-CloudFunction/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions workflow
├── functions/
│   └── image_processor/
│       ├── .gcloudignore          # Files to ignore during deployment
│       ├── main.py                # Core image processing function
│       └── requirements.txt       # Python dependencies
└── README.md                      # This file
```

## 🛠️ Setup and Installation

### Prerequisites

- Google Cloud Platform account
- GitHub repository with Actions enabled
- `gcloud` CLI installed (for local testing)

### 1. GCP Configuration

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
    cloudfunctions.googleapis.com \
    pubsub.googleapis.com \
    eventarc.googleapis.com \
    storage.googleapis.com
```

### 2. Infrastructure Setup

#### Create Pub/Sub Topic
```bash
gcloud pubsub topics create image-topic
```

#### Create Storage Buckets
```bash
# Upload bucket for original images
gcloud storage buckets create gs://image-upload-bucket-111 --location=us-central1

# Thumbnail bucket for processed images
gcloud storage buckets create gs://image-thumbnail-bucket --location=us-central1
```

#### Configure Bucket Notifications
```bash
# Link bucket events to Pub/Sub topic
gcloud storage buckets notifications create gs://image-upload-bucket-111 \
    --topic=projects/$PROJECT_ID/topics/image-topic \
    --payload-format=json \
    --event-types=OBJECT_FINALIZE
```

#### Set IAM Permissions
```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

# Grant storage service agent permission to publish to Pub/Sub
gcloud pubsub topics add-iam-policy-binding projects/$PROJECT_ID/topics/image-topic \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-storage.iam.gserviceaccount.com" \
    --role="roles/pubsub.publisher"
```

### 3. GitHub Actions Setup

#### Create Service Account
```bash
# Create service account for GitHub Actions
gcloud iam service-accounts create github-actions-sa \
    --description="Service account for GitHub Actions deployment" \
    --display-name="GitHub Actions SA"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudfunctions.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/pubsub.admin"

# Create and download service account key
gcloud iam service-accounts keys create key.json \
    --iam-account="github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com"
```

#### Configure GitHub Secrets

1. Go to your repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Add the following secrets:
   - `GCP_SA_KEY`: Contents of the `key.json` file (base64 encoded)

### 4. Deploy with GitHub Actions

The deployment is automated via GitHub Actions. Push to the `main` branch to trigger deployment:

```bash
git add .
git commit -m "Deploy image processing pipeline"
git push origin main
```

## 💻 Local Development

### Manual Deployment

```bash
# Clone the repository
git clone https://github.com/bikram-singh/Image-Processing-Pipeline-GCS-PubSub-CloudFunction.git
cd Image-Processing-Pipeline-GCS-PubSub-CloudFunction

# Deploy the function manually
gcloud functions deploy image-processor \
    --gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=functions/image_processor \
    --entry-point=process_gcs_notification \
    --trigger-topic=image-topic \
    --set-env-vars=THUMB_BUCKET=image-thumbnail-bucket
```

### Local Testing

```bash
# Install dependencies locally
pip install -r functions/image_processor/requirements.txt

# Test the function locally (requires additional setup for local Pub/Sub emulator)
```

## 🧪 Testing the Pipeline

### Upload Test Image

```bash
# Upload an image to trigger the pipeline
gsutil cp your-image.jpg gs://image-upload-bucket-111/

# Verify thumbnail generation
gsutil ls gs://image-thumbnail-bucket/thumbs/
```

### Example Output

```bash
admin_@cloudshell:~ (github-actions-111)$ gsutil cp image.jpg gs://image-upload-bucket-111
Copying file://image.jpg [Content-Type=image/jpeg]...
- [1 files][229.9 KiB/229.9 KiB]                                                
Operation completed over 1 objects/229.9 KiB.

admin_@cloudshell:~ (github-actions-111)$ gsutil ls gs://image-thumbnail-bucket/thumbs/                                                                                                                                                                                    
gs://image-thumbnail-bucket/thumbs/image.jpg
Operation completed over 1 objects/14.9 KiB.
```

### Monitor Function Execution

```bash
# View function logs
gcloud functions logs read image-processor --region=us-central1

# Check Pub/Sub topic metrics
gcloud pubsub topics list
```

## 📊 Configuration

### Environment Variables

The Cloud Function uses the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `THUMB_BUCKET` | Destination bucket for thumbnails | `my-thumbnail-bucket` |

### GitHub Actions Variables

Configure these in `.github/workflows/deploy.yml`:

| Variable | Description | Value |
|----------|-------------|-------|
| `PROJECT_ID` | GCP Project ID | `github-actions-111` |
| `REGION` | Deployment region | `us-central1` |
| `TOPIC` | Pub/Sub topic name | `image-topic` |
| `BUCKET` | Upload bucket name | `image-upload-bucket-111` |
| `THUMB_BUCKET` | Thumbnail bucket name | `image-thumbnail-bucket` |
| `FUNCTION_NAME` | Cloud Function name | `image-processor` |

## 📝 Function Details

### Core Function: `process_gcs_notification`

```python
def process_gcs_notification(event, context):
    """
    Pub/Sub-triggered Cloud Function.
    Expects Cloud Storage notification payload (JSON API v1) base64-encoded in event['data'].
    """
```

**Input**: Pub/Sub event containing base64-encoded Cloud Storage notification
**Process**: Downloads image, creates 320x320 thumbnail using PIL
**Output**: Uploads thumbnail to designated bucket with `thumbs/` prefix

### Dependencies

- **google-cloud-storage>=2.0.0**: Google Cloud Storage client library
- **Pillow>=9.0.0**: Python Imaging Library for image processing

## 🔍 Monitoring and Troubleshooting

### Logs and Monitoring

```bash
# View Cloud Function logs
gcloud functions logs read image-processor --region=us-central1

# Monitor Pub/Sub subscription
gcloud pubsub subscriptions list

# Check bucket notifications
gcloud storage buckets notifications list gs://image-upload-bucket-111
```

### Common Issues

1. **Permission Errors**: Ensure service account has proper IAM roles
2. **Function Timeout**: Increase timeout for large images
3. **Invalid Image Format**: Function handles common formats (JPEG, PNG, GIF, BMP)
4. **Storage Quota**: Monitor bucket storage limits

### Debug Steps

1. Check Cloud Function deployment status
2. Verify Pub/Sub topic and subscription configuration
3. Ensure bucket notification is properly configured
4. Review IAM permissions for all service accounts
5. Monitor function execution logs

## 🚦 Performance Considerations

- **Concurrency**: Cloud Functions automatically scale based on incoming requests
- **Memory**: Default allocation should handle most image sizes
- **Timeout**: Current timeout allows processing of large images
- **Cost**: Pay-per-execution model scales with usage

## 🔒 Security Best Practices

- ✅ Use least-privilege IAM roles
- ✅ Store service account keys securely in GitHub Secrets
- ✅ Enable bucket-level permissions and access controls
- ✅ Monitor function execution for anomalies
- ✅ Implement proper error handling and logging

## 📈 Scaling and Enhancement Ideas

- **Multiple Size Thumbnails**: Generate different thumbnail sizes
- **Image Format Conversion**: Convert between different image formats
- **Metadata Extraction**: Extract and store image metadata
- **CDN Integration**: Integrate with Cloud CDN for faster delivery
- **Machine Learning**: Add image recognition/classification
- **Batch Processing**: Process multiple images in a single function call

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Cloud Platform for providing robust cloud services
- PIL/Pillow team for the excellent image processing library
- GitHub Actions for seamless CI/CD integration

## 📞 Support

For support and questions:

- Create an issue in this repository
- Check Google Cloud Function documentation
- Review Pub/Sub troubleshooting guides

---

**Built with ❤️ using Google Cloud Platform**
  
