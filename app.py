from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

st.set_page_config(
    page_title=f"Celebrity Search - {st.session_state.get('celebrity_name', 'Home')}",
    page_icon="👸",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.markdown("""
    <meta name="description" content="Celebrity Search App powered by OpenAI and Langchain. Search for your favorite celebrities and get insights instantly.">
    <meta name="keywords" content="Celebrity, OpenAI, Langchain, Search, AI App">
    <style>
    body {
        background-color: #f8f9fa; /* Light gray background */
        font-family: 'Arial', sans-serif;
    }
     /* Title Styling */
    .stApp h1 {
        font-size: 3rem;
        font-weight: 700;
        color: #2d408d;
        text-align: center;
        margin-bottom: 1px;
         margin-top: 1px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    /* Subheader Styling */
    .stApp h3 {
        font-size: 1.5rem;
        font-weight: 500;
        color: #495057;
        text-align: center;
        margin-bottom: 1px;
        margin-top: 1px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


st.title("Celebrity Search App ✨")
st.subheader("Powered By OpenAI and Langchain")

st.sidebar.title("Welcome! 👋")
st.sidebar.write("Start your search by entering a celebrity name.")

# Load API Key
_ = load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Custom CSS for consistent alignment, colors, and button design
st.markdown("""
    <style>
    /* Custom input and button styles */
    .input-container {
        display: flex; /* Flexbox for alignment */
        flex-direction: column; /* Stack elements vertically */
        width: 100%; /* Full width of the parent container */
        margin-bottom: 20px; /* Space between multiple input fields */
        padding: 5px 0; /* Padding to create internal spacing */
    }
            
    /* Professional Text Input Box */
    .stTextInput input {
        font-size: 16px; /* Professional font size */
        font-weight: normal; /* Normal weight for a clean look */
        color: #333333; /* Dark text for better readability */
        background-color: #f7f7f7; /* Light gray background */
        border: 1px solid #cccccc; /* Subtle gray border */
        border-radius: 6px; /* Smooth rounded corners */
        padding: 12px; /* Comfortable padding for input */
        height: 50px; /* Fixed height */
        box-sizing: border-box; /* Prevent overflow from padding */
        transition: all 0.2s ease-in-out; /* Smooth transitions */
    }

    /* Input Field Focus State */
    .stTextInput input:focus {
        outline: none; /* Remove default outline */
        background-color: #ffffff; /* White background on focus */
        border-color: #4CAF50; /* Professional green border on focus */
        box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); /* Subtle green glow */
        height: 50px; /* Fixed height */
    }

    /* Placeholder Styling */
    .stTextInput input::placeholder {
        color: #888888; /* Medium gray for placeholder text */
        font-style: italic; /* Subtle italic style */
    height: 50px; /* Fixed height */
    }

    /* Reset Inherited Styles for Inner Container */
    .stTextInput div {
        background-color: transparent !important; /* Force transparent inner container */
        box-shadow: none; /* Remove any unwanted shadows */
        border: none; /* Ensure consistent container styling */
        height: 50px; /* Fixed height */
    }

    /* Professional Dropdown Select Box */
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        background-color: #ffffff; /* Clean white background */
        border: 1px solid #adb5bd; /* Subtle border color */
        border-radius: 8px; /* Rounded corners for a smooth look */
        padding: 12px 20px; /* Added padding for better spacing */
        font-size: 16px; /* Improved font size for readability */
        color: #495057; /* Neutral color for text */
        display: flex; /* Flexbox for proper alignment */
        align-items: center; /* Align text vertically */
        justify-content: space-between; /* Space out the text and arrow */
        position: relative; /* Required for positioning the arrow */
        transition: all 0.3s ease; /* Smooth transition for hover and focus */
        height: 50px; /* Ensure consistent height for the select box */
        width: 100% ;
        overflow: hidden; /* Hide overflowing content */
    }

    /* Ensure selected value (name) is displayed */
    .stSelectbox div[data-baseweb="select"] > div:first-child span {
        color: #495057; /* Neutral color for selected value */
        font-weight: 400; /* Normal weight for better readability */
        height: 50px; /* Ensure consistent height for the select box */
        width: 100% ;
    }

    /* Hover and Focus Effects */
    .stSelectbox div[data-baseweb="select"] > div:first-child:hover {
        border-color: #007bff; /* Professional blue border on hover */
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.2); /* Subtle shadow on hover */
    }

    .stSelectbox div[data-baseweb="select"] > div:first-child:focus-within {
        border-color: #0056b3; /* Stronger blue border on focus */
        box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.25); /* Glowing focus effect */
        height: 50px; /* Ensure consistent height for the select box */
        width: 100% ;
    }

    /* Arrow styling for a cleaner look */
    .stSelectbox div[data-baseweb="select"] > div:first-child::after {
        content: '🔽'; /* Unicode down arrow */
        font-size: 18px;
        color: #007bff; /* Matching blue color for the arrow */
        position: absolute;
        right: 15px; /* Position the arrow correctly on the right */
        top: 50%; /* Align arrow vertically */
        transform: translateY(-50%); /* Center the arrow vertically */
        pointer-events: none; /* Prevent interaction with the arrow */
    }

    /* Ensures that the dropdown's size does not change when it is open */
    .stSelectbox div[data-baseweb="select"] > div:first-child.open {
        height: 50px; /* Keep the height constant when open */
        padding-bottom: 12px; /* Adjust padding to avoid content overflow */
        overflow: hidden; /* Prevent content from overflowing */
        height: 50px; /* Ensure consistent height for the select box */
        width: 100% ;
    }

    /* Button style */
    .stButton button {
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        font-size: 16px;
        font-weight: 500;
        color: #ffffff;
        background-color: #007bff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        cursor: pointer;
        transition: all 0.3s ease;
        width:100%;
        height:50px;
    }
    
    /* Button hover effect */
    .stButton button:hover {
        background-color: #0056b3 !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
        width:100%;
        height:50px;
    }
            
    .stButton button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
        width:100%;
        height:50px;
    }
    
    .stSpinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 10vh; /* Full viewport height */
        text-align: center;
        color: #007bff;
        font-size: 18px;
        font-weight: 600;
        flex-direction: column;
    }
    
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 20%;
        background-color: #f8f9fa; /* Light background similar to input fields */
        text-align: center;
        padding: 20px; /* Adequate padding for spacing */
        font-size: 14px; /* Slightly smaller font for the footer */
        color: #495057; /* Subtle gray color for the text */
        font-weight: 400; /* Lighter weight for the footer text */
        box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow to separate from content */
    }
            
    /* Links Styling */
    .footer a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
        padding: 0 10px;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
            
    /* Footer Text Styling */
    .footer p {
        margin: 5px 0;
        font-family: Arial, sans-serif;
        color: #495057; /* Neutral text color */
    }
    
     /* Font Awesome Icon Styling */
    .footer i {
        margin-right: 8px; /* Space between icon and text */
    }
            
    </style>
    <div class="input-container">
       <div class="footer">
        <p>© 2024 TECHGEAR TECHNOLOGY PRIVATE LIMITED</p>
        <p>Created by Raj Dalsaniya - Made with ❤️ using Streamlit</p>
        <p>
           <a href="https://github.com//RD191295" target="_blank">
                <i class="fa fa-github"></i> GitHub
            </a> |
            <a href="https://www.linkedin.com/in/raj-dalsaniya/" target="_blank">
                <i class="fa fa-linkedin"></i> LinkedIn
            </a> |
            <a href="https://twitter.com/your-profile" target="_blank">
                <i class="fa fa-twitter"></i> Twitter
            </a>
        </p>
    </div>       
""", unsafe_allow_html=True)

# Load Font Awesome CDN for icons
st.markdown("""
    <script src="https://kit.fontawesome.com/a076d05399.js"></script>
""", unsafe_allow_html=True)

with st.container():
    # Input fields for Celebrity Name and Profession (in one row)
    col1, col2, col3 = st.columns([3, 2, 1], gap='small')
    with col1:
        input_text = st.text_input("Enter Celebrity Name", key="celebrity_name", label_visibility="collapsed", max_chars=30, placeholder="e.g., Leonardo DiCaprio")
    with col2:
        profession = st.selectbox(
            "Select Profession (Optional):",
            ["Select Profession", "Actor", "Musician", "Athlete", "Politician", "Writer", "Influencer", "Scientist"],
            key="profession_select",
            label_visibility="collapsed"
        )
    with col3:
        search_button = st.button("🔎 Search", key="Search_Key")
st.markdown('</div>', unsafe_allow_html=True)


if search_button:
    if input_text:
        with st.spinner("Fetching data... Please wait"):
            formattted_input = {
                    "celebrity_name" : input_text,
                    "profession" : profession if profession else "Not Specified"
            }

            prompt_template = ChatPromptTemplate.from_template(
                                template="""
                                    You are an expert who has information about all celebrities. \
                                    Please provide information on the celebrity named: {celebrity_name}. \
                                    Profession: {profession}
                                    """
                                    
                                )

            ## OPENAI LLM Model Define
            llm = ChatOpenAI(temperature=0.8)

            # Define Chain
            chain = prompt_template | llm  | StrOutputParser()

            # Write the result to the text area with custom design
            st.markdown("""
                    <style>
                    .stTextArea textarea {
                        font-size: 16px;
                        padding: 15px;
                        border-radius: 6px;
                        border: 1px solid #cccccc;
                        background-color: #f7f7f7;
                        width: 100%;
                        height: 200px;
                        color: #333;
                        line-height: 1.6;
                    }

                    .stTextArea textarea:focus {
                        outline: none;
                        background-color: #ffffff;
                        border-color: #007bff;
                        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
                    }
                    </style>
                """, unsafe_allow_html=True)
                
            st.text_area("Celebrity Information", chain.invoke(formattted_input), height=250)
    else:
        st.info('Please enter a celebrity name')