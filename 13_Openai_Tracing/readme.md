**OpenAI key and Logs**
1. Goto https://platform.openai.com/docs/overview
2. Login/Signup
3. Goto Dashboaerd Goto API Keys from sidebar
4. Click on Create New Secret Key
5. Paste the OPENAI_AP_KEY in .env
6. Remove tracing_disabled=True from Run Config

**Do the below two steps in main.py**
1. from dotenv import load_dotenv
2. load_dotenv()


**Watch it working**
1. Goto Dashboard
2. Goto Logs from sidebar
3. Goto Traces