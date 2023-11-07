# BookSync
Ebook Reader

https://booksync.jms.cx/

An EPUB book reader web application that allows users to upload and read EPUB files in a web browser, built with Python and Flask.

## Features

- Upload and store EPUB books
- In-browser reading experience
- Automatic bookmarking functionality
- Book library
- Text scaling for accessibility
- Dynamically reflows content based on viewport size
- Dark mode based on user system settings
- Lazy loading of imagery to fetch content only when it's about to come into the viewport.

## Prerequisites

This app has been tested on Python 3.11. Use Docker / Docker Compose to deploy locally.

## Installation

Clone the repository to your local machine:

```zsh
1. Clone the repository:
git clone https://github.com/yourusername/epub-reader-flask.git

2. Navigate to the project directory:
cd abreader
```

## Usage

```zsh
3. Define environment variables (.env):

FLASK_SECRET_KEY=

(Database Credentials)
DATABASE_URL=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

(S3 Storage Credentials)
DO_ACCESS_KEY=
DO_SECRET_KEY=
DO_REGION=
DO_ENDPOINT_URL=
DO_BUCKET_NAME=

4. To create app cluster and start the application, run:

docker-compose up --build

5. Then, navigate to `http://127.0.0.1/` in your web browser to use the application.
```
## License

This project is licensed under the GNU Affero General Public License - see the LICENSE.md file for details.

## Authors

- **James Haddock** - [james-haddock](https://github.com/james-haddock)
