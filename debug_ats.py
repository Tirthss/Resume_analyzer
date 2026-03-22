# Run this to see exactly what's happening with ATS score
from cleaner import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

resume = """
ALEKS LUDKEE Full-Stack Developer
SKILLS
React.js TypeScript Node.js Express.js PostgreSQL MongoDB REST API GraphQL
Docker Kubernetes AWS EC2 S3 JavaScript HTML5 CSS3 Redux Next.js
Jest Cypress CI/CD Git GitHub webpack microservices JWT OAuth2 WebSocket Redis
Built React.js TypeScript frontend with Redux state management
Developed Node.js Express REST API backend with PostgreSQL database
Deployed microservices on AWS using Docker and Kubernetes
Implemented JWT OAuth2 authentication and authorization
Set up CI/CD pipelines using GitHub Actions
Integrated GraphQL Apollo Client for efficient data fetching
"""

job = """
React TypeScript Node.js Express PostgreSQL MongoDB 
Redis Docker Kubernetes AWS EC2 S3 GraphQL Apollo 
JWT OAuth2 WebSocket Socket.io CI/CD GitHub Actions 
Jest Cypress webpack Vite Next.js Redux Toolkit 
HTML5 CSS3 Tailwind microservices REST API Git GitHub 
authentication authorization caching deployment
"""

# Step 1: Show cleaned versions
cleaned_resume = clean_text(resume)
cleaned_job = clean_text(job)

print("CLEANED RESUME WORDS:")
print(cleaned_resume)
print(f"\nTotal words: {len(cleaned_resume.split())}")

print("\nCLEANED JOB WORDS:")
print(cleaned_job)
print(f"\nTotal words: {len(cleaned_job.split())}")

# Step 2: Find common words
resume_words = set(cleaned_resume.split())
job_words = set(cleaned_job.split())
common = resume_words & job_words
print(f"\nCOMMON WORDS ({len(common)}):")
print(common)

# Step 3: Calculate score
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform([cleaned_resume, cleaned_job])
score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
print(f"\nATS SCORE: {round(score * 100, 2)}%")
