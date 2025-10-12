"""
Sample resume generator for testing Run Agent functionality.
Creates a basic text-based resume that can be converted to PDF.
"""

sample_resume_text = """
JOHN SMITH
Senior Python Developer & AI Engineer

Contact Information:
Email: john.smith@email.com
Phone: (555) 123-4567
Location: San Francisco, CA
LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Experienced Python Developer with 5+ years of expertise in software development, 
artificial intelligence, and machine learning. Proven track record of building 
scalable applications, implementing AI solutions, and leading technical teams.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, Java, SQL
• AI/ML Frameworks: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy
• Web Development: FastAPI, Django, Flask, React, Node.js
• Cloud Platforms: AWS, Google Cloud, Azure
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Docker, Kubernetes, Git, Jenkins, Jupyter

WORK EXPERIENCE

Senior Python Developer | TechCorp Inc. | 2022 - Present
• Developed and maintained scalable Python applications serving 1M+ users
• Implemented machine learning models for recommendation systems
• Led a team of 5 developers in building AI-powered features
• Optimized application performance, reducing response times by 40%

Python Developer | StartupXYZ | 2020 - 2022
• Built REST APIs using FastAPI and Django frameworks
• Developed data pipelines for processing large datasets
• Implemented automated testing and CI/CD pipelines
• Collaborated with data scientists to deploy ML models

Junior Software Engineer | DevCompany | 2019 - 2020
• Developed web applications using Python and JavaScript
• Worked with SQL databases and data modeling
• Participated in code reviews and agile development processes

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2019

PROJECTS
• AI Job Matcher: Built an AI system for matching job seekers with relevant positions
• E-commerce Platform: Developed a full-stack e-commerce solution using Python/React
• Data Analytics Dashboard: Created real-time analytics dashboards using Python/D3.js

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional Machine Learning Engineer
• Python Institute PCAP Certification

ACHIEVEMENTS
• Published 3 research papers on machine learning applications
• Speaker at PyCon 2023 on "Building Scalable AI Applications"
• Led team that won company hackathon for AI innovation
"""

print("📄 Sample Resume Content Generated")
print("=" * 50)
print(sample_resume_text)
print("=" * 50)
print("✅ This content simulates a typical Python developer resume")
print("💡 In real usage, the system would extract this text from uploaded PDF files")