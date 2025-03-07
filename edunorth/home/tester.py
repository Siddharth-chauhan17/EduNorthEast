# import os
# import google.generativeai as genai
# import json
# import re
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# # 🔹 Set up API keys
# GEMINI_API_KEY = "AIzaSyDWu4QANcgH80v3scLzz3JDTHO4QMIPkf8"  # Replace with your actual Gemini API key

# # 🔹 Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # 🔹 Path to Google Forms API credentials.json
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# SERVICE_ACCOUNT_FILE = os.path.join(CURRENT_DIR, "swift-district-452822-r5-c88ba05e3991.json")   # Ensure this file is present

# # 🔹 Authenticate Google Forms API
# SCOPES = ["https://www.googleapis.com/auth/forms.body"]
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# forms_service = build("forms", "v1", credentials=creds)

# # 📌 Function to extract and clean JSON from Gemini API response
# def extract_json(text):
#     match = re.search(r"\{.*\}", text, re.DOTALL)  # Find JSON block
#     return match.group(0) if match else ""

# # 📌 Function to generate a quiz using Gemini API
# def get_quiz(subtopic):
#     model = genai.GenerativeModel("gemini-1.5-pro")
#     prompt = f"""
#     Generate a structured 10-question multiple-choice quiz on '{topic}'.
#     Provide the response in valid JSON format without explanations:
#     {{
#         "questions": [
#             {{
#                 "question": "Example question about {topic}?",
#                 "options": ["Option A", "Option B", "Option C", "Option D"],
#                 "correct_answer": "Option A"
#             }},
#             ...
#         ]
#     }}
#     """

#     response = model.generate_content(prompt)
#     raw_text = response.text.strip()
#     json_text = extract_json(raw_text)

#     try:
#         quiz_data = json.loads(json_text)
#         if "questions" in quiz_data and len(quiz_data["questions"]) == 10:
#             return quiz_data  # Return valid quiz
#     except json.JSONDecodeError:
#         pass

#     return {"questions": []}  # Return empty quiz if failed

# # 📌 Function to create a Google Form for a quiz
# def create_google_form(subtopic, quiz_data):
#     form_data = {"info": {"title": f"Quiz on {topic}", "documentTitle": f"Quiz on {topic}"}}
#     form = forms_service.forms().create(body=form_data).execute()
#     form_id = form["formId"]

#     questions = [
#         {
#             "createItem": {
#                 "item": {
#                     "title": q["question"],
#                     "questionItem": {
#                         "question": {
#                             "required": True,
#                             "choiceQuestion": {
#                                 "type": "RADIO",
#                                 "options": [{"value": opt} for opt in q["options"]],
#                                 "shuffle": True,
#                             },
#                         }
#                     },
#                 },
#                 "location": {"index": i},
#             }
#         }
#         for i, q in enumerate(quiz_data["questions"])
#     ]

#     forms_service.forms().batchUpdate(formId=form_id, body={"requests": questions}).execute()
#     return f"https://docs.google.com/forms/d/{form_id}/edit"

# # 📌 Main Execution
# if __name__ == "__main__":
#     user_topic = input("Enter a topic: ")
#     quiz_data = get_quiz(user_topic)

#     if quiz_data["questions"]:
#         # print(json.dumps(quiz_data, indent=2))  # ✅ Only prints quiz JSON
#         print(create_google_form(user_topic, quiz_data))  # ✅ Only prints Google Form link


import os
import google.generativeai as genai
import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build


# 🔹 Configure Gemini AI API
GEMINI_API_KEY = "AIzaSyDWu4QANcgH80v3scLzz3JDTHO4QMIPkf8"  # ✅ Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 Google Forms API Credentials
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(CURRENT_DIR, "gang4-452910-e26650de4b4f.json")  # ✅ Ensure the file is present
SCOPES = ["https://www.googleapis.com/auth/forms.body"]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
forms_service = build("forms", "v1", credentials=creds)

# 📌 Extract JSON from AI response
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else ""

# 📌 Generate Quiz Using Gemini AI
# def get_quiz(subtopic):
#     model = genai.GenerativeModel("gemini-1.5-pro")
#     prompt = f"""
#     Generate a structured 10-question multiple-choice quiz on '{subtopic}'.
#     Provide the response in valid JSON format without explanations:
#     {{
#         "questions": [
#             {{
#                 "question": "Example question about {subtopic}?",
#                 "options": ["Option A", "Option B", "Option C", "Option D"],
#                 "correct_answer": "Option A"
#             }},
#             ...
#         ]
#     }}
#     """
    
#     response = model.generate_content(prompt)
#     raw_text = response.text.strip()
#     json_text = extract_json(raw_text)

#     try:
#         quiz_data = json.loads(json_text)
#         if "questions" in quiz_data and len(quiz_data["questions"]) == 10:
#             return quiz_data  # ✅ Return valid quiz
#     except json.JSONDecodeError:
#         pass

#     return {"questions": []}  # ✅ Return empty quiz if failed


def get_quiz(subtopic):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    Generate a structured 10-question multiple-choice quiz on '{subtopic}'.
    Provide the response in valid JSON format without explanations:
    {{
        "questions": [
            {{
                "question": "Example question about {subtopic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            }},
            ...
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        print(f"🔍 Raw AI Response:\n{raw_text}")  # ✅ Debugging Step

        # ✅ Attempt to parse JSON directly
        quiz_data = json.loads(raw_text)

        # ✅ Ensure quiz_data has 10 questions before returning
        if "questions" in quiz_data and len(quiz_data["questions"]) == 10:
            print(f"✅ Successfully Generated Quiz for '{subtopic}'")
            return quiz_data

    except json.JSONDecodeError:
        print(f"❌ JSON Parsing Failed for '{subtopic}'")

    # ✅ Return a default quiz structure if parsing fails
    return {
        "questions": [
            {
                "question": f"What is {subtopic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            }
        ]
    }


# 📌 Create Google Form Quiz
def create_google_form(subtopic, quiz_data):
    form_data = {"info": {"title": f"Quiz on {subtopic}", "documentTitle": f"Quiz on {subtopic}"}}
    form = forms_service.forms().create(body=form_data).execute()
    form_id = form["formId"]

    questions = [
        {
            "createItem": {
                "item": {
                    "title": q["question"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [{"value": opt} for opt in q["options"]],
                                "shuffle": True,
                            },
                        }
                    },
                },
                "location": {"index": i},
            }
        }
        for i, q in enumerate(quiz_data["questions"])
    ]

    forms_service.forms().batchUpdate(formId=form_id, body={"requests": questions}).execute()
    return f"https://docs.google.com/forms/d/{form_id}/edit"
