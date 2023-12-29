import requests
import streamlit as st
import openai
import json
from MoodleAPI import MoodleAPI  # Importieren Sie Ihre MoodleAPI-Klasse

openai.api_key = "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"

# Laden Sie die Konfiguration von config.ini und erstellen Sie eine Instanz der MoodleAPI
api = MoodleAPI("config.ini")

# Benutzer bei Moodle anmelden
if api.login(api.config["moodle"]["username"], api.config["moodle"]["password"]):
    st.success("Login erfolgreich!")
else:
    st.error("Fehler beim Anmelden. Überprüfen Sie Ihre Anmeldeinformationen in der config.ini-Datei.")

moodle_token = "5c1188948fdc76b65150cbee75506c8a"
moodle_url = "https://moodle.htw-berlin.de/webservice/rest/server.php"
api_function_get_site_info = "core_webservice_get_site_info"
api_function_assign_save_submission = "mod_assign_save_submission"
api_function = "mod_assign_get_submissions"
api_function_assign_save_grade = "mod_assign_save_grade"

def generate_response(user_input, user_role):
    role_message = f"{user_role.capitalize()}:" if user_role else "OpenAI:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{role_message} {user_input}"},
        ],
        max_tokens=150,
    )
    return response['choices'][0]['message']['content'].strip()

def call_moodle_api(api_function, params=None, json_data=None):
    params = params or {}
    params.update({
        "wstoken": moodle_token,
        "wsfunction": api_function,
        "moodlewsrestformat": "json",
    })
    response = requests.post(moodle_url, params=params, json=json_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der API-Anfrage. Statuscode: {response.status_code}")
        print(f"Fehlermeldung: {response.text}")
        return None
    
def call_moodle_api(api_function, params=None, json_data=None):
    params = params or {}
    params.update({
        "wstoken": moodle_token,
        "wsfunction": api_function,
        "moodlewsrestformat": "json",
    })
    response = requests.post(moodle_url, params=params, json=json_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der API-Anfrage. Statuscode: {response.status_code}")
        print(f"Fehlermeldung: {response.text}")
        return None
    
def send_submission_to_moodle(student_name, document_name, feedback_form):
    api_function = "mod_assign_save_submission"

    assignment_id = "AUFGABEN_ID_HIER_EINFÜGEN"
    submission_data = {
        "assignmentid": assignment_id,
        "plugindata": {"onlinetext": {"text": "Aufgabentext hier"}},
        "files_filemanager": [
            {
                "name": document_name,
                "base64": "BASE64_ENCODED_FILE_CONTENT_HIER_EINFÜGEN"
            }
        ],
    }

    params = {"wsfunction": api_function_assign_save_submission}
    response_data = call_moodle_api(api_function_assign_save_submission, params=params, json_data=submission_data)

    if response_data:
        print("Aufgabe erfolgreich eingereicht:", response_data)
        record_userfeedback_action(user_id=student_name, action_type="submission", action_data=response_data)

def send_feedback_to_moodle(student_name, feedback):
    api_function = "mod_assign_save_grade"

    assignment_id = "AUFGABEN_ID_HIER_EINFÜGEN"
    feedback_data = {
        "assignmentid": assignment_id,
        "grades": {
            "0": {"userid": 0, "grade": feedback}
        }
    }
    
    params = {"wsfunction": api_function_assign_save_grade}
    response_data = call_moodle_api(api_function_assign_save_grade, params=params, json_data=feedback_data)

    if response_data:
        print("Feedback erfolgreich übermittelt:", response_data)
        record_userfeedback_action(user_id=student_name, action_type="feedback", action_data=response_data)

def record_userfeedback_action(user_id, action_type, action_data):
    api_function = "core\record_userfeedback_action"

    userfeedback_data = {
        "userid": user_id,
        "type": action_type,
        "data": action_data,
    }

    params = {"wsfunction": api_function}
    response_data = call_moodle_api(api_function, params=params, json_data=userfeedback_data)

    if response_data:
        print("Benutzerfeedback-Aktion erfolgreich aufgezeichnet:", response_data)

def get_user_id(username):
    api_function = "core_user_get_users"

    params = {
        "wstoken": moodle_token,
        "wsfunction": api_function,
        "moodlewsrestformat": "json",
        "criteria[0][key]": "username",
        "criteria[0][value]": username,
    }

    response_data = call_moodle_api(api_function, params=params)

    if response_data and 'users' in response_data:
        users = response_data['users']
        if users:
            return users[0]['id']

    return None

def retrieve_grades(user_id):
    api_function = "gradereport_user_get_grade_items"

    params = {
        "wstoken": moodle_token,
        "wsfunction": api_function,
        "moodlewsrestformat": "json",
        "userid": user_id,
    }

    response_data = call_moodle_api(api_function, params=params)

    grades = {}

    if response_data and 'usergrades' in response_data:
        user_grades = response_data['usergrades']
        for grade_item in user_grades:
            course_name = grade_item.get('coursename')
            grade = grade_item.get('gradeformatted')
            grades[course_name] = grade

    return grades

def extract_submissions_summary(student_name):
    api_function = "Ihre_Moodle_API_Funktion_zum_Abrufen_von_Einreichungen"

    user_id = get_user_id(student_name)

    if user_id:
        params = {
            "wstoken": moodle_token,
            "wsfunction": api_function,
            "moodlewsrestformat": "json",
            "userid": user_id,
        }

        response_data = call_moodle_api(api_function, params=params)

        if response_data and 'submissions' in response_data:
            submissions = response_data['submissions']
            summary = ""

            for submission in submissions:
                assignment_name = submission.get('assignment_name')
                grade = submission.get('grade')
                submission_date = submission.get('submission_date')

                summary += f"Assignment: {assignment_name}, Grade: {grade}, Submitted on: {submission_date}\n"

            return summary

    return "Keine Einreichungen gefunden."

def load_chat_history():
    chat_history_json = st.session_state.get("chat_history", "[]")
    return json.loads(chat_history_json)

def save_chat_history(chat_history):
    chat_history_json = json.dumps(chat_history)
    st.session_state["chat_history"] = chat_history_json

def process_chat(user_input, user_name, document_name, user_role, chat_history, user_id):
    chat_history.append({"role": user_role, "user_id": user_id, "content": f"{user_name} ({user_id}): {user_input}"})
    
    if "einreichen" in user_input.lower() and document_name is not None:
        send_submission_to_moodle(user_id, document_name)
        gpt_response = f"Vielen Dank, {user_name} ({user_id})! Ich habe Ihr Dokument '{document_name}' erfolgreich für die Aufgabe eingereicht."

    elif "rückmeldungen" in user_input.lower():
        feedback_form = st.text_area("Geben Sie Ihre Rückmeldungen ein:")
        send_feedback_to_moodle(user_id, feedback_form)
        gpt_response = f"Danke für Ihr Feedback, {user_name} ({user_id})! Es wurde erfolgreich übermittelt."

    elif "noten abrufen" in user_input.lower():
        if user_id:
            grades = retrieve_grades(user_id)
            gpt_response = f"{user_role.capitalize()} ({user_id}): Ihre Noten: {', '.join([f'{course}: {grade}' for course, grade in grades.items()])}"
        else:
            gpt_response = "Fehler beim Abrufen der Benutzer-ID."

    else:
        gpt_response = generate_response(user_input, user_role)
        if not any(msg.get('content') == f"OpenAI: {gpt_response}" for msg in chat_history):
            chat_history.append({"role": "assistant", "content": f"OpenAI: {gpt_response}"})

    return gpt_response

def process_and_save_student_chat(user_name, document_name, feedback_submission, chat_history):
    user_input = f"{user_name} submitted {document_name} with feedback: {feedback_submission}"
    user_role = "student"
    user_id = get_user_id(user_name)

    response = process_chat(user_input, user_name, document_name, user_role, chat_history, user_id)
    chat_history.append({"role": "assistant", "content": f"OpenAI: {response}"})
    save_chat_history(chat_history)

def chat_section():
    st.title("Moodle Chat Interface")
    user_input = st.text_input("Chat:")
    user_name = ""
    user_role = ""
    document_upload = st.file_uploader("Upload your document:", type=["pdf", "docx"])

    chat_history = load_chat_history()

    if user_input:
        user_id = get_user_id(user_name)

        response = process_chat(user_input, user_name, document_upload.name if document_upload else None, user_role, chat_history, user_id)

        if user_id:
            chat_history.append({"role": "system", "content": f"System: User role is {user_role}, User ID is {user_id}"})

        save_chat_history(chat_history)

        st.write("Antwort:", response)
        st.subheader("Chat History:")
        for msg in chat_history:
            st.text(f"{msg['role']}: {msg['content']}")

def submit_assignment(user_name, document_upload, feedback_submission):
    assignment_id = "AUFGABEN_ID_HIER_EINFÜGEN"  # Fügen Sie die tatsächliche Aufgaben-ID hier ein

    # Datei temporär speichern
    temp_file_path = f"temp/{document_upload.name}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(document_upload.read())

    # API-Aufruf an Moodle
    submission_data = {
        "assignmentid": assignment_id,
        "plugindata": {"onlinetext": {"text": "Aufgabentext hier"}},
        "files_filemanager": [
            {
                "name": document_upload.name,
                "base64": st.file_uploader.encode_file(temp_file_path)
            }
        ],
    }

    params = {"wsfunction": api_function_assign_save_submission, "wstoken": moodle_token}
    response_data = requests.post(moodle_url, params=params, json=submission_data).json()

    if response_data and "status" in response_data and response_data["status"]:
        st.success(f"Aufgabe erfolgreich eingereicht: {response_data}")
        record_userfeedback_action(user_id=user_name, action_type="submission", action_data=response_data)
    else:
        st.error(f"Fehler beim Einreichen der Aufgabe: {response_data}")

def main():
    submissions_data = {}
    user_role = st.sidebar.radio("Choose your role:", ["Student", "Teacher", "Chat"])

    if user_role == "Student":
        student_section()
    elif user_role == "Teacher":
        teacher_section(submissions_data)
    else:
        chat_section()

def student_section():
    st.header("Student Section")
    user_name = st.text_input("Your Name:")
    assignment_id = "IHR_ASSIGNMENT_ID_HIER_EINFÜGEN"  # Fügen Sie die tatsächliche Aufgaben-ID hier ein
    document_upload = st.file_uploader("Upload your document:", type=["pdf", "docx"])
    feedback_submission = st.text_area("Provide initial feedback:")

    action = st.selectbox("Select Action:", ["Submit Assignment", "Provide Feedback", "Retrieve Grades"])
    if st.button("Perform Action"):
        if action == "Submit Assignment":
            if document_upload is not None:
                submit_assignment(user_name, document_upload, feedback_submission)

        elif action == "Provide Feedback":
            provide_feedback(user_name, feedback_submission)
        
        elif action == "Retrieve Grades":
            retrieve_and_display_grades(user_name)

def submit_assignment(user_name, document_upload, feedback_submission):
    send_submission_to_moodle(user_name, document_upload.name, feedback_submission)

def provide_feedback(user_name, feedback_submission):
    send_feedback_to_moodle(user_name, feedback_submission)

def retrieve_and_display_grades(user_name):
    grades = retrieve_grades(get_user_id(user_name))
    st.write(f"{user_name}'s Grades: {grades}")

def teacher_section(submissions_data):
    st.header("Teacher Section")
    selected_student = st.selectbox("Select Student:", list(submissions_data.keys()))

    if selected_student in submissions_data:
        submission = submissions_data[selected_student]
        st.subheader("Student Submission:")
        st.write(f"Student: {selected_student}")
        st.write(f"Document: {submission['Document']}")
        st.write(f"Feedback: {submission['Feedback'] or 'No feedback provided'}")

        feedback = st.text_area(f"Provide feedback for {selected_student}'s assignment:")
        if st.button("Submit Feedback"):
            submissions_data[selected_student]["Feedback"] = feedback
            st.success(f"Feedback submitted successfully for {selected_student}.")

        retrieve_and_display_grades(selected_student)

        submissions_summary = extract_submissions_summary(selected_student)
        st.write("Submission Summary:")
        st.write(submissions_summary)

if __name__ == "__main__":
    main()
