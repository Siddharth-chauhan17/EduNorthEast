EDUNORTHEAST - An AI-Powered Learning and Employment Platform
EDUNORTHEAST is an intelligent e-learning and job placement platform designed to enhance accessibility to education and employment opportunities. Many students, particularly in rural and tribal regions, face challenges such as inadequate learning resources, poor digital infrastructure, and a lack of career guidance. Traditional education systems often fail to align with industry demands, resulting in limited job opportunities for graduates.

To address these challenges, EDUNORTHEAST provides AI-driven personalized learning experiences, interactive assessments, and real-time job listings. The platform integrates multiple APIs to fetch relevant study materials, including blogs, YouTube videos, and quizzes. Additionally, it connects students with job opportunities by retrieving postings from the LinkedIn API, ensuring a seamless transition from learning to employment.

Platform Functionality
Home page navigation
The platform features an intuitive interface with the following sections:
Start Learning: Provides personalized educational content.
Get Employed: Displays relevant job opportunities.
Profile: Allows users to manage their data and track progress.
About Us: Explains the platform’s mission and objectives.
User registration and data management
Users register by providing essential details such as name, email, field of interest, and location. The system securely stores this data using a Django-powered SQLite database, enabling personalized content recommendations and seamless data retrieval.

Learning module
Users can search for topics, and the system retrieves learning materials from multiple sources:

Google Custom Search API – Fetches blogs and articles.
YouTube API – Provides educational video content.
Google Forms API – Generates quizzes for assessments.
A search history feature ensures easy access to previously explored topics.
Job and internship portal
The platform assists users in finding relevant job opportunities by:
Allowing users to enter their field of interest and location.
Fetching real-time job listings via the LinkedIn API.
Displaying job details, including company name, title, and application links.
User profile management
Users can update personal information, track learning progress, and customize content preferences. All modifications are automatically updated in the database to maintain data integrity.
Technologies Used
Frontend: Bootstrap (Responsive UI Design)
Backend: Django (Business logic, authentication, and data management)
Programming Language: Python
Database: SQLite (Stores user data and search history)
API Integrations:
Google Custom Search API (Blog and article retrieval)
YouTube API (Video content)
Google Forms API (Quizzes)
LinkedIn API (Real-time job postings)
