import gradio as gr
import PyPDF2
import os
import re
import requests

# PDF source
PDF_URL = "https://huggingface.co/rupimon/data/resolve/main/Rupanjal-Dasgupta-SoftwareEngineer-Resume.pdf"
PDF_LOCAL = "Rupanjal-Dasgupta-SoftwareEngineer-Resume.pdf"

# Download PDF if not exists
if not os.path.exists(PDF_LOCAL):
    try:
        r = requests.get(PDF_URL)
        r.raise_for_status()
        with open(PDF_LOCAL, "wb") as f:
            f.write(r.content)
        print(f"Downloaded resume to {PDF_LOCAL}")
    except Exception as e:
        print(f"Failed to download resume: {e}")

class ResumeChatbot:
    def __init__(self, pdf_path=PDF_LOCAL):
        self.pdf_path = pdf_path
        self.resume_text = ""
        self.resume_data = {}
        self.load_resume()
    
    def load_resume(self):
        """Load and parse the resume PDF file"""
        try:
            if not os.path.exists(self.pdf_path):
                self.resume_text = "Resume file not found."
                return
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                self.resume_text = text.strip()
                if self.resume_text:
                    self.parse_resume_data()
        except Exception as e:
            self.resume_text = f"Error loading resume: {str(e)}"
    
    def parse_resume_data(self):
        """Extract key info from resume text"""
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.resume_text)
        phone = re.search(r'\d{3}[.\-]?\d{3}[.\-]?\d{4}', self.resume_text)
        exp_match = re.search(r'(\d+)\s+years?\s+of\s+experience', self.resume_text, re.IGNORECASE)
        exp_years = exp_match.group(1) if exp_match else "7+"
        education_match = re.search(r'Bachelor.*?(\d{4})', self.resume_text, re.IGNORECASE)
        education = education_match.group(0) if education_match else "Bachelor of Art in Information Technology"
        skills_section = re.search(r'SKILLS(.*?)(?:PROFESSIONAL|EDUCATION)', self.resume_text, re.DOTALL | re.IGNORECASE)
        skills_text = skills_section.group(1) if skills_section else ""

        self.resume_data = {
            'name': 'Rupanjal Dasgupta',
            'title': 'Software Engineer | 7+ Years in IT',
            'location': 'Iselin, NJ',
            'email': email.group(0) if email else 'rupimon@gmail.com',
            'phone': phone.group(0) if phone else '732.589.6436',
            'experience_years': exp_years,
            'education': education,
            'skills_text': skills_text.strip()
        }

    def wrap_collapsible(self, title, content):
        """Utility to wrap content in collapsible HTML"""
        return f"<details><summary>{title}</summary><pre style='white-space: pre-wrap'>{content}</pre></details>"

    def generate_answer(self, question):
        """Generate answer with collapsible sections and keyword-based search"""
        if not self.resume_text or "Error" in self.resume_text:
            return "❌ Resume data is not available."

        q = question.lower()

        # Direct keyword triggers
        if any(word in q for word in ['contact', 'email', 'phone']):
            content = f"Email: {self.resume_data['email']}\nPhone: {self.resume_data['phone']}\nLocation: {self.resume_data['location']}"
            return self.wrap_collapsible("📧 Contact Information", content)

        elif any(word in q for word in ['experience', 'work', 'career', 'job', 'company']):
            experience_details = {
                "CVS Health (Jan 2023 - Sep 2024)": """• Designed and optimized data engineering pipelines across Glue, Redshift, and S3
• Automated end-to-end retail data workflows using AWS services
• Developed and optimized complex SQL queries
• Managed testing and UAT phases""",
                "Sarepta Therapeutics (Feb 2021 - Aug 2022)": """• Led AWS validation and data integrity initiatives
• Designed data requirements for configuration parameters
• Automated data management tasks through Python
• Performed comprehensive data checks""",
                "Johnson & Johnson (July 2017 - Mar 2020)": """• Consulted on data projects using AWS, SQL, Python, Groovy, and Hadoop
• Verified data load jobs in Hive from S3
• Developed automated Tableau dashboards
• Spearheaded CI/CD pipelines""",
                "Rutgers University Research (Jan - July 2017)": """• Conducted fake news detection research using NLP and Python
• Created dashboards and visualizations with Tableau"""
            }
            collapsible_exp = ""
            for company, details in experience_details.items():
                collapsible_exp += self.wrap_collapsible(company, details) + "\n"
            return self.wrap_collapsible(f"💼 Professional Experience ({self.resume_data['experience_years']} years)", collapsible_exp)

        elif any(word in q for word in ['skills', 'technologies', 'languages']):
            skills_categories = {
                "Languages": "Python, Java, Groovy, SQL, PL/SQL, JavaScript, Shell Script",
                "Cloud & Big Data": "AWS (S3, Lambda, EC2, IAM, Glue, Redshift)",
                "Databases": "MySQL, Oracle, SQL Server",
                "Tools & Platforms": "Jenkins, Docker, Git/Bit-Bucket, GitHub, Jira, Tableau, PyCharm, Eclipse, Selenium, AWS Services, Apache Hadoop",
                "Specializations": "Backend Data Analysis, CI/CD, Agile SCRUM, Data-driven Architecture"
            }
            collapsible_skills = ""
            for title, content in skills_categories.items():
                collapsible_skills += self.wrap_collapsible(title, content) + "\n"
            return self.wrap_collapsible("🛠️ Technical Skills", collapsible_skills)

        elif any(word in q for word in ['education', 'degree', 'university', 'school', 'research']):
            education_details = {
                "Degree": self.resume_data['education'] + " from Rutgers University, NJ, USA (GPA 3.631/4.0)",
                "Research Experience": """• Research Assistant at Rutgers University (Jan - July 2017)
• Conducted research on fake news detection using Python, LIWC, Tableau, and NLP
• Scraped and cleaned raw data, created dashboards and visualizations
• Co-authored academic publications"""
            }
            collapsible_edu = ""
            for title, content in education_details.items():
                collapsible_edu += self.wrap_collapsible(title, content) + "\n"
            return self.wrap_collapsible("🎓 Education & Research", collapsible_edu)

        elif any(word in q for word in ['projects', 'achievement', 'built', 'developed']):
            projects = {
                "CVS Health": "Designed pipelines, automated workflows, optimized SQL queries, managed testing/UAT.",
                "Sarepta Therapeutics": "AWS validation, Python automation, data integrity, millions of records processed.",
                "Johnson & Johnson": "Data consulting, Tableau dashboards, CI/CD Jenkins pipelines.",
                "Rutgers Research": "Fake news detection research using Python, NLP, and Tableau."
            }
            collapsible_projects = ""
            for title, content in projects.items():
                collapsible_projects += self.wrap_collapsible(title, content) + "\n"
            return self.wrap_collapsible("🚀 Projects & Achievements", collapsible_projects)

        elif any(word in q for word in ['certification', 'certificate', 'certified']):
            certs = {
                "IBM Data Analyst": "Coursera, August 2022",
                "Google AI Essentials": "Coursera, May 2025",
                "Google Prompting Essentials": "Coursera, April 2025",
                "AWS Cloud Technical Essentials": "In Progress",
                "IBM AI Developer": "In Progress"
            }
            collapsible_certs = ""
            for title, content in certs.items():
                collapsible_certs += self.wrap_collapsible(title, content) + "\n"
            return self.wrap_collapsible("🏆 Certifications & Professional Development", collapsible_certs)

        elif any(word in q for word in ['summary', 'about', 'overview', 'objective']):
            summary_content = f"{self.resume_data['name']} is a Software Engineer with {self.resume_data['experience_years']} years of experience in Python, Java, SQL, AWS, and CI/CD pipelines."
            return self.wrap_collapsible("👨‍💻 Professional Summary", summary_content)

        elif any(word in q for word in ['name', 'who']):
            return f"👋 Hi! I'm <b>{self.resume_data['name']}</b>, a {self.resume_data['title']} based in {self.resume_data['location']}."

        else:
            return "Type a keyword like 'experience', 'skills', 'education', 'projects', 'certifications', 'contact', or 'summary' to see the section."

# Gradio interface
def create_chat_interface():
    chatbot = ResumeChatbot()
    
    def respond(message, history):
        if not message.strip():
            return "Please ask a question!"
        try:
            return chatbot.generate_answer(message)
        except Exception as e:
            return f"Error: {str(e)}"
    
    with gr.Blocks(title="Ask Rupanjal - Resume Chatbot", theme=gr.themes.Soft()) as demo:
        gr.HTML("""
        <div style="text-align:center; padding:20px;">
            <h1>💼 Ask Rupanjal</h1>
            <p>Type keywords like <b>skills</b>, <b>experience</b>, <b>education</b>, <b>projects</b>, <b>certifications</b>, <b>contact</b>, or <b>summary</b> to jump to sections.</p>
        </div>
        """)
        
        gr.ChatInterface(
            fn=respond,
            examples=[
                "Show my skills",
                "Tell me about my projects",
                "What's my education?",
                "List my certifications",
                "Show contact information",
                "Give a professional summary"
            ],
            clear_btn="🗑️ Clear Chat",
            submit_btn="Send 📤",
            stop_btn="Stop ⏹️",
        )
    return demo

if __name__ == "__main__":
    demo = create_chat_interface()
    demo.launch()
