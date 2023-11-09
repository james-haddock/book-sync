# BookSync
Ebook Reader

https://booksync.jms.cx/

An EPUB book reader web application that allows users to upload and read EPUB files in a web browser, built with Python and Flask.

## Core Features

BookSync enhances reading with a suite of features designed for convenience and engagement:

- **EPUB Management**: Streamlined uploading and storage for your EPUB book collection.
- **Browser-Based Reader**: A sophisticated in-browser reading platform.
- **Bookmarking**: Automatic bookmarking to easily pick up where you left off.
- **Personal Library**: Organize and access your books through a centralized library.
- **Accessibility Options**: Customizable text scaling to accommodate all readers.
- **Adaptive Content**: Content reflow that intelligently adjusts to different screen sizes.
- **Dark Mode**: User-system-settings-responsive dark mode for comfortable reading in any light.
- **Optimized Image Loading**: Lazy loading for efficient, on-demand image rendering.
- **Easy Navigation**: Quick access to book sections via a hyperlinked table of contents.


## Development

### Technologies Used

BookSync is built using a modern tech stack that combines powerful tools and frameworks to create a seamless reading experience. Here’s an overview of the technologies used:

- **Backend Development**: Python and Flask form the backbone of the server-side logic, providing a lightweight yet powerful platform for web development.

- **Database Management**: PostgreSQL offers robust and reliable data storage, while SQLAlchemy serves as the ORM of choice for seamless database migrations and queries.

- **Cloud**: 
  - **Amazon RDS**: Database hosting.
  - **Amazon S3**: Storage for user content and application assets accessed through the boto3 API.
  - **Digital Ocean**: PaaS for app hosting.

- **Frontend Development**: The user interface is crafted with HTML, enriched by Tailwind CSS for styling, and made interactive with JavaScript, creating an intuitive and dynamic user experience.

- **Continuous Integration and Deployment (CI/CD)**: Github Actions.

- **Web Server**: Nginx serves as the reverse proxy and HTTP server for BookSync.

- **Containerization**: Docker encapsulates the application into containers, ensuring consistency across various development and deployment environments.

- **Testing**: Pytest provides a full-featured framework for unit testing, facilitating a bug-free and quality-assured codebase.

- **Package Management**: pip is our tool of choice for managing software packages, making it easy to install and maintain the project's library dependencies.

### Application Architecture

BookSync's architecture embraces principles of abstraction and modularity. It features a decoupled, scalable codebase where concrete classes are abstracted into interfaces, allowing for independent development, testing, and maintenance of each component.

#### Key Architectural Features:

- **Abstraction and Polymorphism:** By coding to interfaces rather than concrete implementations, the system promotes flexibility, allowing for various types of ebooks and user interactions without altering the core logic.

- **Decoupled Components:** The architecture strategically decouples components, which enhances the ability to iterate rapidly and safely introduce new features or modifications.

- **Scalable Infrastructure:** The application is designed to scale with ease, accommodating a growing user base and an expanding library of ebooks while maintaining performance and stability.

- **Testability:** Abstract classes and interfaces make our codebase more amenable to unit testing, leading to a more reliable application as it evolves.

- **Continuous Integration/Continuous Deployment (CI/CD):** CI/CD pipelines are used to ensure that new code changes are automatically tested and deployed efficiently, reducing the time between writing code and bringing features to users.

- **Responsive Design:** The front-end architecture uses a mobile-first approach, ensuring compatibility and a seamless experience across various devices and screen sizes.

- **Performance Optimization:** Front-end and back-end optimizations, like lazy loading of images and efficient database queries, contribute to a snappy user interface and quick access to book content.

- **Security Best Practices:** Security is a cornerstone of our architecture, with measures in place to protect user data and privacy, including secure password handling, data encryption, and adherence to best practices for web security.

- **Cloud-native Services:** Leveraging cloud services for storage and computation, the application ensures high availability and reliable access to user libraries without geographical limitations.

This architectural design is not just a blueprint for current functionalities but also a foundation for future innovation, enabling BookSync to evolve with technological advancements and user expectations.


### Database Design

![BookSync ERD](https://github.com/james-haddock/ABReader/assets/123553781/b1f4f225-d269-40d7-97fb-dab74c40480d)

- **Database Normalisation:** The database is meticulously normalised to eliminate redundancy, ensuring data integrity and query efficiency, which supports the application's scalability and performance.
  
- **One-to-Many Relationships:** Carefully crafted one-to-many relationships, like between `users` and `books`, enable a single user to have an extensive library of ebooks while maintaining data integrity and providing easy management of user-specific data.

- **Scalability:** Designed with scalability in mind, new book types can be added in future without changing any of the existing database infrastructure.

- **Security:** All user passwords are securely hashed before being stored, providing an additional layer of security to user data.

### Testing

BookSync's quality is assured through rigorous testing, with Pytest at the core of our unit testing framework. Key features of our testing approach include:

- **Pytest for Unit and Integration Testing**: employment of Pytest to construct and run a comprehensive suite of unit and integration tests, ensuring each part of the application functions as intended in isolation.

- **Continuous Integration**: Our CI/CD pipeline automatically runs tests on every commit via Github Actions, safeguarding against regressions and maintaining code quality.

This streamlined testing regimen enables us to deliver a dependable and user-friendly eBook reader, continuously refined through a well-established testing culture.

## Cloud Technologies

BookSync harnesses the power of cloud computing to deliver a robust and scalable reading platform:

- **Amazon RDS**: Our database is powered by AWS Relational Database Service (RDS), offering high availability, automated backups, and easy scaling capabilities to handle our application's data needs efficiently.

- **Amazon S3**: The app utilises Amazon Simple Storage Service (S3) for secure and durable storage of EPUB files and images. S3's scalability and data availability ensure users can quickly upload and access their content.

- **Digital Ocean Hosting**: The application itself is hosted on Digital Ocean, chosen for its simplicity, reliability, and ability to scale. This ensures that BookSync remains responsive and accessible globally.

## Continuous Integration and Deployment (CI/CD)

BookSync uses GitHub Actions for CI/CD. This workflow automates the testing and deployment, ensuring consistent quality and rapid iteration.

- **Automated Testing**: Every push and pull request triggers a series of automated tests to validate code changes, maintaining code quality.
- **Streamlined Deployment**: Merges into the main branch automatically deploy the latest version of the application, enabling continuous delivery with minimal downtime.
- **Delivery to Production**: Digital Ocean checks for changes to the main branch and automatically pulls the app to their servers for containerisation and delivery to production.

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
