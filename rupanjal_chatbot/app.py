import gradio as gr
import PyPDF2
import os
import re

class ResumeChatbot:
    def __init__(self, pdf_path="Rupanjal-Dasgupta-SoftwareEngineer-Resume.pdf"):
        self.pdf_path = pdf_path
        self.resume_text = ""
        self.resume_data = {}
        self.load_resume()
    
    def load_resume(self):
        """Load and parse the resume PDF file"""
        try:
            # Check if file exists
            if not os.path.exists(self.pdf_path):
                print(f"PDF file not found: {self.pdf_path}")
                self.resume_text = "Resume file not found. Please ensure the resume PDF is uploaded to the space."
                return
            
            # Read the PDF file
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                self.resume_text = text.strip()
                
                if self.resume_text:
                    self.parse_resume_data()
                    print(f"Resume loaded successfully. Text length: {len(self.resume_text)}")
                else:
                    print("Could not extract text from PDF")
                    self.resume_text = "Could not extract text from the PDF file."
                    
        except Exception as e:
            print(f"Error loading resume: {e}")
            self.resume_text = f"Error loading resume: {str(e)}"
    
    def parse_resume_data(self):
        """Extract key information from resume text"""
        try:
            # Extract contact info
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.resume_text)
            phone = re.search(r'\d{3}[.\-]?\d{3}[.\-]?\d{4}', self.resume_text)
            
            # Extract experience years
            exp_match = re.search(r'(\d+)\s+years?\s+of\s+experience', self.resume_text, re.IGNORECASE)
            exp_years = exp_match.group(1) if exp_match else "7+"
            
            # Extract education
            education_match = re.search(r'Bachelor.*?(\d{4})', self.resume_text, re.IGNORECASE)
            education = education_match.group(0) if education_match else "Bachelor of Art in Information Technology"
            
            # Extract skills
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
        except Exception as e:
            print(f"Error parsing resume data: {e}")
    
    def extract_section(self, section_name):
        """Extract a specific section from resume"""
        pattern = rf'{section_name}(.*?)(?:^[A-Z]+|$)'
        match = re.search(pattern, self.resume_text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def find_relevant_section(self, question):
        """Find the most relevant section of the resume for the question"""
        question_lower = question.lower()
        
        # Define section keywords
        section_keywords = {
            'contact': ['contact', 'email', 'phone', 'reach', 'connect', 'address'],
            'experience': ['experience', 'work', 'job', 'role', 'position', 'company', 'career'],
            'skills': ['skill', 'technology', 'programming', 'tool', 'technical', 'proficient', 'language'],
            'education': ['education', 'degree', 'university', 'college', 'study', 'graduation'],
            'certifications': ['certification', 'certificate', 'certified', 'credential'],
            'projects': ['project', 'built', 'developed', 'created', 'implemented', 'worked on'],
            'summary': ['summary', 'about', 'overview', 'background', 'profile', 'objective']
        }
        
        # Find best matching sections
        matches = []
        for section, keywords in section_keywords.items():
            score = sum(1 for keyword in keywords if keyword in question_lower)
            if score > 0:
                matches.append((section, score))
        
        # Sort by relevance
        matches.sort(key=lambda x: x[1], reverse=True)
        
        if matches:
            return matches[0][0]
        return 'general'
    
    def generate_answer(self, question):
        """Generate answer based on the question"""
        if not self.resume_text or "Error" in self.resume_text or "not found" in self.resume_text:
            return "❌ Resume data is not available. Please ensure the resume PDF file is uploaded to the Hugging Face Space."
        
        question_lower = question.lower()
        section = self.find_relevant_section(question)
        
        # Handle different types of questions
        if any(word in question_lower for word in ['name', 'who are you', 'who is', 'yourself']):
            return f"👋 Hi! I'm **{self.resume_data['name']}**, a {self.resume_data['title']} based in {self.resume_data['location']}."
        
        elif section == 'contact' or any(word in question_lower for word in ['contact', 'email', 'phone', 'reach']):
            return f"""📧 **Contact Information:**
- **Name:** {self.resume_data['name']}
- **Email:** {self.resume_data['email']}
- **Phone:** {self.resume_data['phone']}
- **Location:** {self.resume_data['location']}"""
        
        elif section == 'experience' or any(word in question_lower for word in ['experience', 'work', 'career', 'worked']):
            exp_section = self.extract_section('Software Engineer')
            if exp_section:
                return f"""💼 **Professional Experience ({self.resume_data['experience_years']} years):**

{exp_section[:1500]}...

**Key Highlights:**
• 7+ years building production solutions with Python, Java, SQL, and AWS
• Designed data-driven backend workflows and CI/CD pipelines
• Supported mission-critical applications for CVS Health, Sarepta, and J&J
• Expert in Agile SCRUM, automated deployments, and code reviews"""
            else:
                return "I have 7+ years of experience as a Software Engineer. Would you like details about specific companies or projects?"
        
        elif section == 'skills' or any(word in question_lower for word in ['skill', 'technology', 'programming', 'language']):
            return f"""🛠️ **Technical Skills:**

**Languages:** Python, Java, Groovy, SQL, PL/SQL, JavaScript, Shell Script

**Cloud & Big Data:** AWS (S3, Lambda, EC2, IAM, Glue, Redshift)

**Databases:** MySQL, Oracle, SQL Server

**Tools & Platforms:**
• Jenkins (orchestration, pipeline, CI/CD)
• Docker, Git/Bit-Bucket, GitHub, Jira
• Tableau, PyCharm, Eclipse, Selenium
• AWS Services, Apache Hadoop

**Specializations:**
• Backend Data Analysis
• Continuous Integration/Deployment/Testing
• Agile SCRUM Development
• Data-driven Architecture"""
        
        elif section == 'education' or any(word in question_lower for word in ['education', 'degree', 'university', 'school']):
            return f"""🎓 **Education:**
**{self.resume_data['education']}** from Rutgers University, NJ, USA (GPA 3.631/4.0)

**Research Experience:**
• Research Assistant at Rutgers University (Jan - July 2017)
• Conducted research on fake news detection using Python, LIWC, Tableau, and NLP
• Scraped and cleaned raw data, created dashboards and visualizations
• Co-authored academic publications"""
        
        elif section == 'certifications' or any(word in question_lower for word in ['certification', 'certificate', 'certified']):
            return f"""🏆 **Certifications & Professional Development:**
• IBM Data Analyst Professional Certificate (Coursera, August 2022)
• Google Prompting Essentials (Coursera, April 2025)
• Google AI Essentials (Coursera, May 2025)
• IBM AI Developer (In Progress)
• AWS Cloud Technical Essentials (In Progress)"""
        
        elif any(word in question_lower for word in ['project', 'built', 'developed', 'worked']):
            return """🚀 **Key Projects & Achievements:**

**CVS Health (Jan 2023 - Sep 2024):**
• Designed and optimized data engineering pipelines across Glue, Redshift, and S3
• Automated end-to-end retail data workflows using AWS services
• Developed and optimized complex SQL queries for backend development
• Managed testing and UAT phases for analytics solutions

**Sarepta Therapeutics (Feb 2021 - Aug 2022):**
• Led AWS validation and data integrity initiatives
• Designed data requirements for configuration parameters
• Automated data management tasks through Python
• Performed comprehensive data checks on millions of records

**Johnson & Johnson (July 2017 - Mar 2020):**
• Consulted on data projects using AWS, SQL, Python, Groovy, and Hadoop
• Verified data load jobs in Hive from S3 data stores
• Developed automated Tableau dashboards
• Spearheaded CI/CD pipeline customization with Jenkins

**Rutgers University Research (Jan - July 2017):**
• Conducted fake news detection research using NLP and Python
• Created dashboards and visualizations with Tableau"""
        
        elif any(word in question_lower for word in ['summary', 'about', 'overview', 'objective']):
            return f"""👨‍💻 **Professional Summary:**

I'm **{self.resume_data['name']}**, a results-driven Software Engineer with {self.resume_data['experience_years']} years of experience building production solutions using Python, Java, SQL, AWS, and CI/CD pipelines.

**Core Expertise:**
🔧 **Software Development** - Building scalable, test-driven solutions
☁️ **Cloud Architecture** - AWS services (S3, Lambda, EC2, Glue, Redshift)
📊 **Data Engineering** - Backend workflows, ETL, and data validation
🏗️ **Enterprise Solutions** - CVS Health, Sarepta, Johnson & Johnson

**What I Bring:**
• Designed and maintained data-driven backend workflows
• Automated deployments with Jenkins and CI/CD pipelines
• Daily collaboration in Agile SCRUM teams
• Strong code review and mentoring experience
• Focus on data quality, reliability, and system optimization"""
        
        else:
            # Generic response for other questions
            return f"""🤔 I'd be happy to help! Here are some topics you can ask me about:

**📋 Quick Topics:**
• Work experience and companies I've worked at
• Technical skills and programming languages
• Education and certifications
• Specific projects and achievements
• Contact information
• Professional background and summary

**💡 Try asking:**
- "What is your work experience?"
- "Tell me about your technical skills"
- "What companies have you worked at?"
- "How can I contact you?"
- "What certifications do you have?"
- "Tell me about your projects"
- "What's your educational background?"
- "Give me a professional summary"

Or feel free to ask any specific question about my background!"""

def create_chat_interface():
    """Create the main chat interface"""
    
    # Initialize chatbot
    chatbot = ResumeChatbot()
    
    def respond(message, history):
        """Handle chat responses"""
        if not message.strip():
            return "Please ask me a question about my background!"
        
        try:
            response = chatbot.generate_answer(message)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Sorry, I encountered an error: {str(e)}. Please try asking your question differently."
    
    # Create Gradio interface
    with gr.Blocks(
        title="Ask Rupanjal - Resume Chatbot",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .chat-container {
            height: 600px !important;
        }
        """
    ) as demo:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2563eb; margin-bottom: 10px;">💼 Ask Rupanjal</h1>
            <h2 style="color: #64748b; font-weight: normal; margin-bottom: 20px;">
                Interactive Resume Chatbot
            </h2>
            <p style="color: #64748b; font-size: 16px;">
                Hi! I'm Rupanjal Dasgupta, a Software Engineer with 7+ years of IT experience. 
                Ask me anything about my background, skills, experience, or projects!
            </p>
        </div>
        """)
        
        # Chat interface
        chatbot_interface = gr.ChatInterface(
            fn=respond,
            title="",
            description="",
            examples=[
                "What is your work experience?",
                "Tell me about your technical skills",
                "What companies have you worked at?", 
                "What's your educational background?",
                "How can I contact you?",
                "What certifications do you have?",
                "Tell me about your projects",
                "Give me a professional summary"
            ],
            cache_examples=False,
            retry_btn=None,
            undo_btn=None,
            clear_btn="🗑️ Clear Chat",
            submit_btn="Send 📤",
            stop_btn="Stop ⏹️",
            chatbot=gr.Chatbot(
                height=500,
                show_label=False,
                container=True,
                show_copy_button=True
            )
        )
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px; border-top: 1px solid #e5e7eb; margin-top: 20px;">
            <h3 style="color: #374151; margin-bottom: 15px;">🚀 About This Chatbot</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px;">
                <div style="text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 5px;">📄</div>
                    <strong>PDF-Powered</strong><br>
                    <span style="color: #6b7280;">Reads resume dynamically from PDF</span>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 5px;">🤖</div>
                    <strong>Smart Responses</strong><br>
                    <span style="color: #6b7280;">Context-aware answers</span>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 5px;">⚡</div>
                    <strong>Fast & Reliable</strong><br>
                    <span style="color: #6b7280;">Instant responses</span>
                </div>
            </div>
            <p style="color: #6b7280; margin-top: 15px; font-size: 14px;">
                Built with Gradio • Deployed on Hugging Face Spaces
            </p>
        </div>
        """)
    
    return demo

# Launch the application
if __name__ == "__main__":
    demo = create_chat_interface()
    demo.launch()