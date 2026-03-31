# StylePredictor — AI-Powered Fashion Intelligence Platform

StylePredictor is a full-stack Django web application that leverages machine learning to provide fashion classification, recommendation, and data visualization. The platform combines image recognition (CNN/VGG16), text-based classification (KNN, Linear Regression), and collaborative filtering to help users discover fashion trends, predict dress categories, and receive personalized recommendations.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Running the Application](#running-the-application)
- [Application Modules](#application-modules)
- [URL Routes](#url-routes)
- [Default Credentials](#default-credentials)

---

## Features

- **Image Classification** — Upload a fashion image and get a predicted dress category using a CNN model (VGG16-based).
- **Image Recommendation** — Browse visual recommendations across categories (Shirt, Pant, Jacket, Sweater, Shoes, Kurti, Saree) using image similarity.
- **Text Classification** — Predict dress type, fashion event, or dress style based on user attributes (gender, age, fabric, comfort, etc.) using KNN/Linear Regression.
- **Text Recommendation** — Get popularity-based, personalized, and fashion-category-based dress recommendations using collaborative filtering.
- **Tag Recommendation** — Discover related fashion items using Apriori-based association rule mining on hashtags.
- **Similarity Recommendation** — Find similar articles and categories based on TF-IDF content similarity.
- **Data Visualization** — Interactive Chart.js dashboards showing brand ratings and user preference analytics.
- **Social Posts** — Create, like, comment on fashion posts with image uploads and slug-based URLs.
- **User Profiles** — Registration, login, profile management with profile picture uploads.
- **Gallery** — View classified and uploaded fashion images.
- **Responsive Dark Theme** — Modern glassmorphism UI with purple/pink gradient design system.

---

## Tech Stack

| Layer          | Technology                                                  |
|----------------|-------------------------------------------------------------|
| Backend        | Django 4.2, Python 3.11                                     |
| Database       | SQLite3                                                     |
| ML/AI          | TensorFlow 2.13, Keras, scikit-learn, OpenCV, NumPy, Pandas |
| Visualization  | Chart.js 4.4.1                                              |
| Frontend       | Bootstrap 3/4, custom CSS (glassmorphism dark theme)        |
| Animations     | WOW.js, slick-carousel, magnific-popup                      |
| Fonts/Icons    | Google Fonts (Inter), Font Awesome 5                        |
| Association    | Apyori (Apriori algorithm)                                  |
| Production     | Gunicorn, WhiteNoise                                        |

---

## Project Structure

```
stylePredictor/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database
│
├── stylePredictor/            # Django project settings
│   ├── settings.py
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # User authentication app
│   ├── models.py              # Profile model (OneToOne with User)
│   ├── views.py               # Login, Register, Profile, Logout views
│   ├── forms.py               # User registration & profile forms
│   └── urls.py                # Auth routes (login, register, profile, password reset)
│
├── home/                      # Core ML & recommendation app
│   ├── views.py               # Main views (dashboard, classifiers, recommenders)
│   ├── models.py              # UserModal, FashionModel, PlanModel
│   ├── urls.py                # Home app routes
│   ├── Image_Classification.py    # CNN image classification (VGG16 + custom model)
│   ├── Image_Recommendation.py   # Image-based fashion recommendation
│   ├── Text_Classification.py    # KNN/Linear Regression text classification
│   ├── Text_Recommendation.py    # Collaborative filtering recommendations
│   ├── Text_Content_Classification.py  # TF-IDF content similarity
│   ├── Tag_Recommendation.py     # Apriori association rule mining
│   ├── Data_Visualization.py     # Brand rating & user analytics
│   └── Recommenders.py           # Popularity & item similarity recommender classes
│
├── posts_/                    # Social posts app
│   ├── models.py              # Post, Comment models (likes, slugs, images)
│   ├── views.py               # CRUD views for posts (ListView, DetailView, etc.)
│   ├── context_processor.py   # Global context: categories, liked posts, recent posts
│   ├── snippets.py            # Slug generation, choice fields
│   └── urls.py                # Post routes (list, detail, create, update, delete)
│
├── Saved_Models/              # Pre-trained ML models & datasets
│   ├── Classification_using_CNN.h5    # Trained CNN model weights
│   ├── Classification_using_CNN.json  # CNN model architecture
│   ├── fashion_prediction_*.csv       # Training/test datasets
│   ├── Recommendation_Table.csv       # Recommendation lookup tables
│   ├── Similarity.json                # Pre-computed similarity matrix
│   └── Text_Similarity.csv            # TF-IDF similarity scores
│
├── media/                     # User-uploaded content
│   ├── posts/                 # Post images
│   ├── profiles/              # Profile pictures
│   ├── Recommender_Dataset/   # Fashion image dataset (images.csv, styles.csv)
│   └── Sample_images_Classification/
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── professional.css   # Main design system (dark theme, CSS custom properties)
│   │   └── admin.css
│   ├── post/css/style.css     # Post page styles
│   ├── home/                  # Home app assets (JS, images, plugins)
│   └── img/
│
└── templates/                 # Django templates
    ├── Index.html             # Public landing page
    ├── Home.html              # Authenticated user dashboard
    ├── Dbase.html             # Base template for home app pages
    ├── Base.html              # Base template for post pages
    ├── User_Base.html         # Base for auth pages (login, register)
    ├── Image_Classification.html
    ├── Image_Recommendation.html
    ├── Text_Classification.html
    ├── Text_Recommendation.html
    ├── Tag_Recommendation.html
    ├── Content_Classification.html
    ├── Gallery.html
    ├── Help.html
    ├── visuals1.html          # Data visualization charts
    ├── UDetails.html          # User details form
    ├── FDetails.html          # Fashion preferences form
    ├── PDetails.html          # Dress plan management
    ├── registration/          # Login, Register, Profile templates
    ├── posts_/                # Post CRUD templates
    └── partials/              # Reusable template fragments
        ├── _navbar.html
        ├── _footer.html
        ├── _styles.html
        └── _widgets.html
```

---

## Prerequisites

- **Python 3.11.x** (required for TensorFlow 2.13 compatibility)
- **pip** (Python package manager)
- **Git** (optional, for cloning)

---

## Setup Guide

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stylePredictor
```

### 2. Create a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** TensorFlow 2.13 requires Python 3.11. If you encounter issues, ensure your Python version matches.

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Collect Static Files (Optional — for production)

```bash
python manage.py collectstatic --noinput
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## Running the Application

```bash
python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**.

| URL               | Description                        |
|--------------------|------------------------------------|
| `/`                | Landing page (Index)               |
| `/login/`          | User login                         |
| `/register/`       | User registration                  |
| `/home/`           | Dashboard (requires authentication)|
| `/admin/`          | Django admin panel                 |

---

## Application Modules

### Image Classification
Upload a fashion image and the system predicts its category using a pre-trained CNN model built on VGG16 architecture. The model weights are stored in `Saved_Models/Classification_using_CNN.h5`.

### Image Recommendation
Select a fashion category and browse visually similar items. Uses OpenCV and image feature extraction to compute similarity scores across the fashion dataset in `media/Recommender_Dataset/`.

### Text Classification
Three classification modes available via tabbed interface:
1. **Dress Type** — Predicts dress category from attributes (gender, age, fabric, color, quality, comfort, brand)
2. **Fashion Event** — Predicts event type from demographics (profession, education, weather, culture, style)
3. **Dress** — Predicts dress from event and preference attributes

Uses KNN and Linear Regression models trained on datasets in `Saved_Models/`.

### Text Recommendation
Three recommendation approaches via accordion panels:
1. **Popularity-Based** — Top-rated dress categories across all users
2. **Personalized** — User-specific recommendations based on rating history
3. **Fashion Category** — Select a category and discover similar ones

Built on collaborative filtering using the `Recommenders.py` popularity and item similarity models.

### Tag Recommendation
Select a fashion tag and discover associated brands/categories using Apriori association rule mining. Powered by the `apyori` library on the `Fashion_Tags_rec.csv` dataset.

### Similarity Recommendation
Find similar articles by type or category using TF-IDF vectorization and cosine similarity. Combines article attributes and usage data from `Saved_Models/Text_Similarity.csv`.

### Data Visualization
Interactive Chart.js dashboards displaying:
- Brand rating distributions (bar charts)
- User preference breakdowns (doughnut charts)
- Comparative analytics across fashion categories

### Social Posts
Full CRUD system for fashion posts with image uploads, category tagging, event tagging, likes, comments, view counts, and SEO-friendly slug URLs.

---

## URL Routes

### Accounts (`/`)
| Route                                | View              | Description          |
|--------------------------------------|-------------------|----------------------|
| `/`                                  | `index`           | Landing page         |
| `/login/`                            | `LoginView`       | User login           |
| `/logout/`                           | `LogoutView`      | User logout          |
| `/register/`                         | `RegisterView`    | User registration    |
| `/profile/<id>/`                     | `ProfileView`     | Edit profile         |
| `/profile/picture/`                  | `ImageUpdateView` | Change profile pic   |
| `/password_reset/`                   | `PasswordResetView` | Password reset     |

### Home (`/home/`)
| Route                                | View              | Description                     |
|--------------------------------------|-------------------|---------------------------------|
| `/home/`                             | `index1`          | Dashboard with charts           |
| `/home/userDetails`                  | `userDetails`     | User details form               |
| `/home/fashionDetails`               | `fashionDetails`  | Fashion preferences form        |
| `/home/planDetails`                  | `planDetails`     | Dress plan management           |
| `/home/gallery`                      | `gallery`         | Image gallery                   |
| `/home/imgPredictor`                 | `imgPredictor`    | Image classification            |
| `/home/imgRecommender`               | `imgRecommender`  | Image recommendation            |
| `/home/textClassifier`               | `textClassifier`  | Text classification             |
| `/home/textRecommender`              | `textRecommender` | Text recommendation             |
| `/home/tagRecommender`               | `tagRecommender`  | Tag recommendation              |
| `/home/contentClassify`              | `contentClassify` | Content similarity              |

### Posts (`/post/`)
| Route                                | View              | Description          |
|--------------------------------------|-------------------|----------------------|
| `/post/post1`                        | `PostListView`    | All posts            |
| `/post/create/`                      | `PostCreateView`  | Create new post      |
| `/post/<slug>/`                      | `PostDetailView`  | Post detail          |
| `/post/<slug>/update`                | `PostUpdateView`  | Edit post            |
| `/post/<slug>/delete`                | `PostDeleteView`  | Delete post          |
| `/post/dashboard/myposts/`           | `MyPostView`      | User's posts         |

---

## Default Credentials

| Role        | Username          | Password      |
|-------------|-------------------|---------------|
| Regular User| `talha-javaid-1`  | `Talha8715.`  |
| Super Admin | `talha-javaid-2`  | `Talha8715.`  |

---

## License

This project was developed as a Final Year Project (FYP).
