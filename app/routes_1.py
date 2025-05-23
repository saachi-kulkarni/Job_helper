#from fastapi import APIRouter, Header, HTTPException, Depends
from models_1 import UserInput, ChatResponse
import os
from fastapi import APIRouter, Header, HTTPException, Depends
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

def chatbot_response(message):
    msg = message.lower()

    # 💻 Software / IT
    if any(skill in msg for skill in ['python', 'java', 'c++', 'software', 'developer', 'programming', 'coding']):
        return (
            "It sounds like you have technical skills! You might explore roles like Software Developer, QA Engineer, or DevOps Specialist.",
            "tech",
            ["Indeed: Software Jobs", "LinkedIn: Tech Roles", "Stack Overflow Jobs"]
        )

    # 📊 Data / Analytics
    elif any(skill in msg for skill in ['data analysis', 'excel', 'sql', 'power bi', 'tableau', 'data scientist']):
        return (
            "Your data skills are in high demand! Consider roles like Data Analyst, Business Intelligence Analyst, or Data Scientist.",
            "data",
            ["Kaggle Job Board", "LinkedIn: Data Jobs", "Glassdoor: Analytics Roles"]
        )

    # 🎨 Design / Creativity
    elif any(skill in msg for skill in ['graphic design', 'photoshop', 'illustrator', 'ux', 'ui', 'figma', 'adobe']):
        return (
            "Creative skills can lead to exciting careers. You might like Graphic Designer, UI/UX Designer, or Visual Content Creator roles.",
            "creative",
            ["Behance Job Board", "Dribbble Careers", "Remote Design Jobs"]
        )

    # 📈 Marketing / Business
    elif any(skill in msg for skill in ['marketing', 'seo', 'content creation', 'social media', 'sales']):
        return (
            "You have a great marketing profile! Explore opportunities like Digital Marketer, Content Strategist, or Brand Manager.",
            "marketing",
            ["HubSpot Job Board", "We Work Remotely: Marketing", "LinkedIn Marketing Jobs"]
        )

    # 🛠️ Skilled Trades / Mechanical
    elif any(skill in msg for skill in ['mechanic', 'electrician', 'carpenter', 'plumber', 'hvac']):
        return (
            "Skilled trades are essential and well-paid! Look into jobs like Electrician, HVAC Tech, or Maintenance Engineer.",
            "trades",
            ["Angi Pros", "Indeed: Skilled Trades", "ZipRecruiter: Trade Jobs"]
        )

    # 👩‍🏫 Teaching / Education
    elif any(skill in msg for skill in ['teaching', 'tutoring', 'education', 'lesson planning', 'classroom']):
        return (
            "Teaching is a meaningful career. You could explore roles like Teacher, Tutor, or Curriculum Designer.",
            "education",
            ["TeachAway", "EdJoin", "LinkedIn Education Jobs"]
        )

    # 🧑‍⚕️ Healthcare / Medical
    elif any(skill in msg for skill in ['nursing', 'medical', 'healthcare', 'first aid', 'pharmacy', 'patient care']):
        return (
            "Healthcare professionals are vital. You could look into Nurse, Medical Assistant, or Healthcare Administrator roles.",
            "healthcare",
            ["Health eCareers", "LinkedIn: Medical Jobs", "Hospital Job Boards"]
        )

    # 🌐 General fallback
    else:
        return (
            "Thanks for sharing! If you let me know your skills or interests in more detail, I can recommend specific career paths.",
            "general",
            ["LinkedIn", "Indeed", "CareerExplorer"]
        )

# FastAPI endpoint version
@router.post("/find-job", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
def find_job(input: UserInput):
    response_msg, category, resources = job_finder_response(input.message)
    return ChatResponse(
        message=response_msg,
        severity=category,  # reused 'severity' field to reflect job category
        suggested_resources=resources
    )

@router.post("/analyze", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
def analyze_message(input: UserInput):
    response_msg, severity, resources = chatbot_response(input.message)
    return ChatResponse(
        message=response_msg,
        severity=severity,
        suggested_resources=resources
    )
