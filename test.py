import logging
import sys
import streamlit as st
import streamlit.components.v1 as components
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)


BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "0ac617e2-fc14-4076-8881-b8400125d1eb"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-7lUBw": {},
  "ChatOutput-zBFSq": {},
  "Prompt-Sm5iS": {},
  "Memory-6K51Z": {},
  "GoogleGenerativeAIModel-ux27o": {}
}



BASE_AVATAR_URL = "data:image/png;base64,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"


def main():
    # Set page configuration
    st.set_page_config(layout="wide", page_title="Accessible UI")

    # Create two columns
    col1, col2 = st.columns(2)
    # Custom CSS to set the background color for the entire page

    # Content for the second column (currently empty)
    with col1:
        st.markdown("""
            <style>
                body {
                    font-family: 'Verdana', sans-serif;
                    background-color: #d6f7da;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #c4f3cb;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }
                .main_title {
                    font-family: 'Orbitron';font-size: 40px;
                }
                h1 {
                    font-family: 'Orbitron';
                    font-size: 40px;
                    color: #3a3a3a;
                }
                p {
                    font-size: 18px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                    color: #4d4d4d;
                    text-align: left
                }
                li {
                    font-size: 18px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                    color: #4d4d4d;
                    text-align: left
                }
                a {
                    color: #0066cc;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .footer {
                    font-size: 16px;
                    color: #666;
                    text-align: left;
                }
            </style>
        """, unsafe_allow_html=True)


        # Create the container for the content
        st.markdown("""
    <link class="git_link" href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet'>
    

<a href="https://github.com/row-huh/AccessibleUI" class="git_button">View Project on GitHub</a>
            </p>
            <div class="container">
                <p class="main_title">ACCESSIBLE UI<p>
    <li>
        A total of 780 million globally are dyslexic, 285 million are visually impaired, and 390 million have motor disabilities.
    </li>
    <li>
        This data highlights the significant number of people who will be impacted by an inaccessible web.
    </li>
    <li>
        These statistics underscore the need for a responsible, inclusive, and accessible web for all.
    </li>
    <li>
        Accessibility is not just an option but an essential component of any successful website. Many disabled users prefer websites that prioritize accessibility over aesthetic considerations.
    </li>
    <li>
        An application like AccessibleUI, which helps designers create accessible websites, can greatly enhance the user experience for people with disabilities. It ensures that everyone, regardless of their physical or cognitive abilities, can access and navigate the web with ease. By integrating accessibility into the design process, designers can build websites that are both functional and inclusive, catering to a diverse audience and promoting equal access to information and services.
    </li>
                </p>
                </div>
        """, unsafe_allow_html=True)



    # Content for the first column
    with col2:
        # Your existing Streamlit code for styling

        st.markdown("""
        <link class="git_link" href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet'>
        <style>
        .git_link {
            font-color:white;
            background-color:black
        }
        .main_title {
            font-family: 'Orbitron';font-size: 40px;
        }
        .stApp {
            background-color: #c4f3cb !important;
        }
        </style>

        <p class="main_title">    </p>
        """, unsafe_allow_html=True)

        # Create a custom HTML component for the LangFlow chat
        langflow_chat_html = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.3/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
        window_title="AccessibleUI"
        flow_id="0ac617e2-fc14-4076-8881-b8400125d1eb"
        host_url="http://localhost:7860"
        ></langflow-chat>
        <style>
        langflow-chat {
            width: 100%;
            height: 100%;
        }
        </style>
        """

        # Render the custom HTML component
        components.html(langflow_chat_html, height=700)


if __name__ == "__main__":
    main()