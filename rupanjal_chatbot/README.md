---
title: Ask Rupanjal - Resume Chatbot
emoji: 💼
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
python_version: "3.9"
---

# 💼 Ask Rupanjal - Interactive Resume Chatbot

An intelligent chatbot that dynamically reads and answers questions about professional background from PDF resume, built with Gradio and deployed on Hugging Face Spaces.

## 🚀 Key Features

- **📄 Dynamic PDF Reading**: Reads LinkedInProfile.pdf file directly from the space
- **🤖 Smart Q&A**: Extracts and provides answers from actual PDF content  
- **⚡ Lightweight**: Only 2 dependencies - gradio + PyPDF2
- **💬 Interactive Chat**: User-friendly interface with example questions
- **📱 Mobile Responsive**: Works seamlessly on all devices
- **🔄 No Embedded Text**: 100% dynamic content extraction from PDF

## 🛠️ Technical Architecture

- **Frontend**: Gradio 4.x (ChatInterface)
- **PDF Processing**: PyPDF2 3.x (Dynamic text extraction)
- **Text Processing**: Built-in Python (regex, string methods)
- **Deployment**: Hugging Face Spaces
- **Runtime**: Python 3.9
- **Storage**: File-based (no databases required)

## 📋 What You Can Ask

### 💼 Professional Topics
- Current role and company details
- Work experience and career progression
- Key responsibilities and achievements
- Professional projects and contributions

### 🛠️ Technical Skills
- Programming languages and frameworks
- Cloud platforms and databases
- Data analysis and visualization tools
- AI/ML and analytics expertise

### 🎓 Background
- Educational qualifications
- Certifications and training
- Research experience
- Academic achievements

### 📧 Contact & Links
- Email and professional contact info
- LinkedIn profile and social media
- Portfolio and blog links
- Location and availability

## 💡 Example Questions

```
"What is your current role?"
"Tell me about your technical skills"
"What's your work experience?"
"How can I contact you?"
"What certifications do you have?"
"Tell me about your projects"
"What's your educational background?"
"Give me a professional summary"
```

## 🎯 Perfect For

- **🔍 Recruiters**: Quick candidate background overview
- **🤝 Networking**: Professional experience exploration
- **💼 Interviews**: Interactive qualification review
- **📊 Portfolio**: Engaging resume presentation
- **🔗 Website Integration**: Embeddable resume chatbot

## 🚀 How It Works

1. **PDF Loading**: Automatically reads `LinkedInProfile.pdf` from space
2. **Content Parsing**: Extracts text and identifies key sections
3. **Question Analysis**: Understands user intent and finds relevant content
4. **Dynamic Response**: Returns actual information from the PDF
5. **Context Awareness**: Provides section-specific detailed answers

## 📁 Required Files

```
├── app.py                 # Main chatbot application
├── requirements.txt       # Dependencies (gradio>=4.0.0, PyPDF2>=3.0.0)
├── LinkedInProfile.pdf    # Resume PDF file (must be present)
└── README.md             # This documentation file
```

## ⚙️ Deployment Instructions

### For Hugging Face Spaces:

1. **Create New Space**
   - Go to https://huggingface.co/new-space
   - Choose "Gradio" SDK
   - Name your space

2. **Upload Files**
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `LinkedInProfile.pdf` (resume file)
   - `README.md` (this file)

3. **Auto-Deploy**
   - Space builds automatically
   - Ready to use in ~2-3 minutes

### For Local Development:

```bash
# Clone or download files
git clone <your-repo>
cd resume-chatbot

# Install dependencies
pip install -r requirements.txt

# Ensure PDF file is present
ls LinkedInProfile.pdf

# Run application
python app.py
```

## 🔧 Customization

To use with a different resume:

1. **Replace PDF**: Upload your own resume as `LinkedInProfile.pdf`
2. **Update Content**: The chatbot automatically adapts to new content
3. **Modify Parsing**: Adjust extraction methods in `app.py` if needed
4. **Update README**: Change personal details in this file

## 🌟 Technical Highlights

- **Zero Hardcoding**: No embedded resume text in source code
- **Pattern Recognition**: Smart content extraction using regex and keywords
- **Error Resilient**: Graceful handling of PDF parsing issues
- **Memory Efficient**: Minimal resource usage for fast responses
- **Scalable Design**: Easy to adapt for different resumes/profiles

## 📊 Performance

- **Load Time**: ~2-3 seconds (PDF parsing)
- **Response Time**: <1 second per query
- **Memory Usage**: <100MB total
- **Dependencies**: Only 2 packages
- **Compatibility**: Python 3.9+ and modern browsers

## 🔒 Privacy & Security

- **Local Processing**: PDF content processed in-memory only
- **No Data Storage**: No persistent storage of resume content
- **Session Based**: Content cleared between sessions
- **Public Space**: Suitable for public resume sharing

## 🤝 Connect & Support

- **Issues**: Report problems via Hugging Face Space discussions
- **Improvements**: Suggest features in space community tab
- **Fork**: Create your own version by duplicating the space
- **Contact**: Professional contact info available through the chatbot

---

**🎯 Ready to try?** Ask me anything about the professional background!

*Built with ❤️ using Gradio | Deployed on 🤗 Hugging Face Spaces | 100% Dynamic PDF Reading*