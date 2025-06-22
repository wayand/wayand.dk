# Wayand.dk Blog Platform

A Flask-based blog platform with an administrative interface and frontend blog display. Currently powering [wayand.dk](https://wayand.dk).

## Features

### Blog Frontend (`/blog`)
- Post listing with pagination
- Category-based post filtering (`/blog/categories/<category>`)
- Tag-based post filtering (`/blog/tags/<tag>`)
- Individual post view with SEO-friendly URLs (`/blog/<slug>`)
- Automatic heading anchors for post navigation
- SEO optimization with meta titles and descriptions
- Sitemap generation

### Admin Dashboard (`/admin`)
- Secure login system
- Post Management:
  - Create/Edit/Delete posts
  - Rich text editor (TinyMCE)
  - Featured image upload
  - Draft/Publish workflow
  - Bulk actions (trash, restore, delete)
  - SEO metadata management
- Category and Tag Management
- Profile Management
- Post filtering by status (Published/Draft/Trash)
- Search functionality

### API Endpoints (`/apiv1`)
- Post management endpoints
- Category and tag operations
- Profile operations
- Secure authentication required

## Tech Stack
- **Backend**: Flask with Blueprints
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**:
  - Admin: Bootstrap-based dashboard
  - Blog: Custom responsive design
- **Editor**: TinyMCE for rich text editing
- **Security**: Flask-Login for authentication

## Installation

1. Clone the repository and create a virtual environment:
```bash
git clone git@github.com:wayand/wayand.dk.git
cd wayand.dk/python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.sample .env
```

Required environment variables:
```
FLASK_APP=run.py
FLASK_DEBUG=1  # Set to 0 in production
FLASK_ENV=development  # Set to production in production
SECRET_KEY=your-secure-secret-key
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/wayand_dk
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the development server:
```bash
flask run
```

## Project Structure
```
.
├── app/
│   ├── admin/         # Admin interface blueprint
│   ├── api/          # API endpoints (v1)
│   ├── blog/         # Blog frontend blueprint
│   ├── forms/        # WTForms definitions
│   ├── models/       # SQLAlchemy models
│   ├── static/       # Static assets
│   │   ├── admin/    # Admin dashboard assets
│   │   └── frontend/ # Blog frontend assets
│   ├── templates/    # Jinja2 templates
│   └── utils/        # Utility functions
├── migrations/       # Database migrations
└── config.py        # Configuration management
```

## API Routes

### Posts
- `GET /apiv1/posts` - List all posts
- `PATCH /apiv1/posts/<id>/slug` - Update post slug
- `PATCH /apiv1/posts/bulk-trash` - Move posts to trash
- `PATCH /apiv1/posts/bulk-restore` - Restore posts from trash
- `DELETE /apiv1/posts/<id>` - Delete a post
- `DELETE /apiv1/posts/bulk-delete` - Delete multiple posts

### Categories & Tags
- `DELETE /apiv1/categories/<id>` - Delete a category
- `DELETE /apiv1/categories` - Bulk delete categories
- `DELETE /apiv1/tags` - Bulk delete tags

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
flask db migrate -m "Migration message"
flask db upgrade
```

## License
This project is licensed under the MIT License.
