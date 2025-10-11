# User Guide

Welcome to AutoAgentHire! This guide will help you get started with automating your job search using AI agents.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Setting Up Your Profile](#setting-up-your-profile)
3. [Uploading Your Resume](#uploading-your-resume)
4. [Configuring Job Preferences](#configuring-job-preferences)
5. [Searching for Jobs](#searching-for-jobs)
6. [Understanding Match Scores](#understanding-match-scores)
7. [Applying to Jobs](#applying-to-jobs)
8. [Tracking Applications](#tracking-applications)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Your resume (PDF, DOCX, or TXT format)
- Job search preferences
- OpenAI API key (for AI features)

### First Login

1. Navigate to the application URL
2. Click "Sign Up" to create an account
3. Enter your email and create a secure password
4. Verify your email address
5. Log in with your credentials

## Setting Up Your Profile

### Personal Information

1. Go to **Profile** section
2. Fill in your details:
   - Full Name
   - Email (auto-filled)
   - Phone Number
   - Current Location
   - LinkedIn URL (optional)
   - Portfolio URL (optional)

3. Click **Save Profile**

### Why This Matters

Your profile information is used to:
- Auto-fill job applications
- Match you with relevant opportunities
- Generate personalized cover letters

## Uploading Your Resume

### Supported Formats

- **PDF** (.pdf) - Recommended
- **Word** (.docx)
- **Text** (.txt)

### Upload Steps

1. Go to **Profile** section
2. Click **Upload Resume** button
3. Select your resume file
4. Wait for parsing to complete
5. Review extracted information

### What Gets Extracted

The AI parses your resume to extract:
- **Skills**: Technical and soft skills
- **Experience**: Job history and responsibilities
- **Education**: Degrees and certifications
- **Contact Info**: Name, email, phone

### Tips for Best Results

✅ **Do:**
- Use a well-formatted resume
- Include clear section headers
- List skills explicitly
- Use standard job titles

❌ **Avoid:**
- Complex layouts or tables
- Image-based text
- Unusual fonts or formatting
- Multiple columns

## Configuring Job Preferences

### Setting Preferences

1. Navigate to **Settings** section
2. Configure your preferences:

#### Job Titles
- List desired job titles (one per line)
- Examples:
  - Software Engineer
  - Python Developer
  - Machine Learning Engineer

#### Location Preferences
- Specify desired locations
- Include remote options if applicable

#### Salary Range
- Set minimum salary: $80,000
- Set maximum salary: $150,000
- Leave blank if flexible

#### Job Type
- Full-time
- Part-time
- Contract
- Internship

#### Experience Level
- Entry Level
- Mid Level
- Senior Level
- Lead/Principal

### Automation Settings

#### Auto-Apply (⚠️ Use Carefully)
- **Disabled by default** for safety
- Requires manual confirmation
- Reviews application before submission

#### Daily Job Search
- Automatically searches for new jobs daily
- Sends email with top matches

#### Max Applications Per Day
- Limit: 1-50 applications
- Recommended: 5-10 for quality

#### Email Notifications
- New job matches
- Application status updates
- Daily/weekly summaries

## Searching for Jobs

### Manual Search

1. Go to **Job Search** section
2. Enter search criteria:
   - Keywords (e.g., "Python Developer")
   - Location (e.g., "San Francisco, CA")
   - Experience Level
   - Job Type

3. Click **Search Jobs**
4. Wait for results (may take 30-60 seconds)

### What Happens During Search

The AI agents:
1. **Search** multiple job boards
2. **Extract** job details
3. **Analyze** job descriptions
4. **Calculate** match scores
5. **Rank** opportunities

### Viewing Results

Results display:
- **Job Title** and **Company**
- **Location** and **Job Type**
- **Match Score** (0-100%)
- **Brief Description**
- **Apply Button**

### Match Score Colors

- 🟢 **90-100%**: Excellent match
- 🟡 **75-89%**: Good match
- 🟠 **60-74%**: Fair match
- 🔴 **Below 60%**: Poor match

## Understanding Match Scores

### How Scores Are Calculated

Match scores combine:

1. **Skills Match (40%)**
   - Your skills vs job requirements
   - Weighted by importance

2. **Experience Match (30%)**
   - Years of experience
   - Relevant domain experience

3. **Semantic Similarity (20%)**
   - AI analysis of job description
   - Resume content alignment

4. **Preferences (10%)**
   - Location match
   - Salary alignment
   - Job type preference

### Match Analysis Details

Click on a job to see:
- **Strengths**: What makes you a good fit
- **Gaps**: Skills you may need to develop
- **Reasoning**: AI explanation of the score

#### Example

```
Match Score: 87%

Strengths:
✓ Strong Python experience (5+ years)
✓ FastAPI and Django expertise
✓ Cloud deployment experience

Gaps:
⚠ No Kubernetes experience (required)
⚠ Limited machine learning background

Reasoning:
Your extensive Python and web development 
experience strongly aligns with this role. 
The lack of Kubernetes is a minor gap that 
can be addressed through learning.
```

## Applying to Jobs

### Application Process

1. **Select a Job** from search results or matches
2. **Review Match Analysis**
3. **Generate Cover Letter** (AI-powered)
4. **Review and Edit** the cover letter
5. **Confirm Application Details**
6. **Submit Application**

### AI-Generated Cover Letters

The system:
1. Analyzes job description
2. Retrieves relevant experience from your resume
3. Generates personalized cover letter
4. Highlights your matching qualifications

### Customizing Cover Letters

Always review and customize:
- Add specific company research
- Include personal motivation
- Adjust tone if needed
- Fix any inaccuracies

### Auto-Fill Feature (Beta)

For supported job boards:
1. System navigates to application page
2. Auto-fills form fields
3. Uploads resume
4. **Pauses for your review**
5. You manually submit

⚠️ **Important**: Always review before submitting!

## Tracking Applications

### Application Dashboard

View all applications in **Applications** section:

#### Status Categories
- **Draft**: Prepared but not submitted
- **Applied**: Successfully submitted
- **In Review**: Employer reviewing
- **Interview**: Interview scheduled
- **Rejected**: Application declined
- **Accepted**: Offer received

### Updating Status

1. Click on an application
2. Update status manually
3. Add notes about:
   - Interview dates
   - Feedback received
   - Follow-up actions

### Analytics

Track your job search progress:
- **Applications Sent**: Total count
- **Response Rate**: Percentage
- **Interview Rate**: Percentage
- **Average Match Score**: Your typical score

## Best Practices

### Resume Tips

✅ **Keep it updated** with recent experience
✅ **Use keywords** from target job descriptions
✅ **Quantify achievements** with numbers
✅ **Highlight relevant skills** prominently

### Job Search Strategy

✅ **Quality over quantity** - Focus on good matches
✅ **Customize applications** - Don't rely only on AI
✅ **Research companies** - Show genuine interest
✅ **Follow up** - Check application status regularly

### Using AI Responsibly

✅ **Review AI output** - Don't blindly submit
✅ **Add personal touch** - Make it authentic
✅ **Respect ToS** - Follow job board policies
✅ **Be honest** - Don't exaggerate skills

### Privacy & Security

✅ **Protect credentials** - Use strong passwords
✅ **Review permissions** - Know what data is shared
✅ **Secure API keys** - Don't share with others
✅ **Log out** - On shared computers

## Troubleshooting

### Common Issues

#### Resume Not Parsing

**Problem**: Resume upload fails or extracts incorrectly

**Solutions**:
1. Convert to PDF format
2. Simplify formatting
3. Remove images/graphics
4. Try a different resume version

#### Low Match Scores

**Problem**: Getting consistently low scores

**Solutions**:
1. Update resume with relevant skills
2. Broaden job search criteria
3. Include more keywords in resume
4. Target jobs matching your experience level

#### Application Not Sending

**Problem**: Application submission fails

**Solutions**:
1. Check internet connection
2. Verify all required fields are filled
3. Try manual submission on job board
4. Contact support if persistent

#### No Search Results

**Problem**: Job search returns no results

**Solutions**:
1. Broaden search keywords
2. Remove location filters
3. Try alternative job titles
4. Check if job boards are accessible

### Getting Help

📧 **Email**: support@autoagenthire.com
💬 **Chat**: Available in app (bottom right)
📚 **Docs**: https://docs.autoagenthire.com
🐛 **Report Bug**: GitHub Issues

### Feature Requests

Have an idea? We'd love to hear it!
- Submit on GitHub
- Email: features@autoagenthire.com
- Vote on existing requests

## Privacy & Data

### What We Store

- Resume content (encrypted)
- Job search history
- Application tracking
- Match scores and analysis

### What We Don't Store

- Job board credentials (encrypted separately)
- Credit card information
- Private communications

### Data Controls

You can:
- Export your data (JSON format)
- Delete your account
- Opt out of analytics
- Control email preferences

## Tips for Success

### Week 1: Setup
- Upload and optimize resume
- Configure preferences
- Run test searches
- Review match scores

### Week 2-3: Active Search
- Search 2-3 times per week
- Apply to 5-10 top matches
- Track all applications
- Follow up on responses

### Week 4+: Optimization
- Analyze what works
- Refine resume based on gaps
- Adjust search criteria
- Update skills if needed

## Keyboard Shortcuts

- `Ctrl + K` (Cmd + K): Quick search
- `Ctrl + N` (Cmd + N): New search
- `Ctrl + S` (Cmd + S): Save profile
- `Esc`: Close modals

---

## Feedback

We're constantly improving! Your feedback helps us make AutoAgentHire better.

⭐ **Rate us**: Leave a review
💡 **Suggest**: Share your ideas
🐛 **Report**: Tell us about bugs

Happy job hunting! 🚀
