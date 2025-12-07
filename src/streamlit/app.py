import json

import streamlit as st

from src.app.config import Settings, VectorstoreSettings, LLMModelSettings, MailSettings
from src.app.database.langchain_qdrant_wrapper import QdrantLangchainWrapper
from src.app.services.action import create_action_proposal_on_given_insight
from src.app.services.approval import accept_approval, decline_approval
from src.app.services.ingest import show_files
from src.app.services.insight import create_insight
from src.app.services.prompt import get_prompts, edit_prompt
from src.app.schemas.prompt import PromptLoader

if "insight" not in st.session_state:
    st.session_state.insight = None
if "proposal" not in st.session_state:
    st.session_state.proposal = None
if "accept" not in st.session_state:
    st.session_state.accept = None
if "action" not in st.session_state:
    st.session_state.action = None
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""
if "upload_pw_input" not in st.session_state:
    st.session_state.upload_pw_input = None
if "locked" not in st.session_state:
    st.session_state.locked = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

example_prompts=[
    "How can we improve our effort in improving the health of this planet?",
    "How can we improve our financial performance for next year?"
]

st.title("Generic Insight → Action Demo")

enable_upload = st.checkbox("Advanced Settings to Upload Files", disabled=True, value=False)

@st.dialog("Show current files", width="medium")
def show_current_files(settings: Settings):
    st.write("Current Files:")
    response = show_files(settings)

    files = response.get("files")
    st.table(files)

@st.dialog("Insight Action settings", width="medium")
def show_ai_assistant_settings(settings: Settings):
    st.write("Display and Edit the Current Prompt Settings")
    prompts = get_prompts(settings)
    create_insight_prompt = prompts.get("insight_prompt")
    create_proposal_prompt = prompts.get("propose_action_prompt")
    st.text_area(
        label="Ingest Settings:",
        value=create_insight_prompt,
        height=350,
    )
    st.text_area(
        label="Propose Action Settings:",
        value=create_proposal_prompt,
        height=350,
    )

    if st.button("Close", type="primary"):
        st.rerun()

def set_api_key():
    if st.session_state.api_key_input:
        st.session_state.api_key = st.session_state.api_key_input
        st.session_state.locked = True

def unlock_fields():
    st.session_state.locked = False


vectorstore_settings = VectorstoreSettings(
    embedding_model=st.secrets["EMBEDDING_MODEL"],
    collection_name=st.secrets["COLLECTION_NAME"],
    dimension=st.secrets["DIMENSION"],
    retrieve_documents_count=st.secrets["RETRIEVE_DOCUMENTS_COUNT"],
    distance=st.secrets["DISTANCE"],
    qdrant_endpoint=st.secrets["QDRANT_ENDPOINT"],
    qdrant_api_key=st.secrets["QDRANT_API_KEY"],
)

llmmodel_settings = LLMModelSettings(
    model_name=st.secrets["MODEL_NAME"],
    temperature=st.secrets["TEMPERATURE"],
    openai_api_key=st.session_state.api_key,
    prompts=PromptLoader(),
)

mail_settings = MailSettings(
    smtp_host=st.secrets["SMTP_HOST"],
    smtp_port=st.secrets["SMTP_PORT"],
    smtp_from=st.secrets["SMTP_FROM"],
    smtp_to=st.secrets["SMTP_TO"],
    smtp_username=st.secrets["SMTP_USERNAME"],
    smtp_password=st.secrets["SMTP_PASSWORD"],
)

settings = Settings(
    raw_dir=st.secrets["RAW_DIR"],
    data_dir=st.secrets["DATA_DIR"],

    vectorstore=vectorstore_settings,
    llm_model=llmmodel_settings,
    mail=mail_settings,
)

if st.button("Show current loaded files"):
    show_current_files(settings)

if st.button("Show current AI Assistant settings"):
    show_ai_assistant_settings(settings)

st.divider()

st.text_input(
        key="api_key_input",
        label="API Key:",
        type="password",
        disabled=st.session_state.locked)

if st.session_state.locked:
    st.button(
        key="unlock_button",
        label="Update API Key",
        on_click=unlock_fields)
else:
    st.button(
        key="set_model_api_key",
        label="Set API Key",
        on_click=set_api_key)

if not st.session_state.locked:
    st.warning("Please set your Openai API Key before starting.")
else:

    qdrant_langchain_wrapper = QdrantLangchainWrapper(vectorstore_settings)

    with st.expander("See example prompts"):
        for prompt in example_prompts:
            if st.button(prompt, type="tertiary"):
                st.session_state.prompt_input = prompt


    query = st.text_input("What should we work on today? ", value=st.session_state.prompt_input)
    if query:
        if st.button("Create Insight for query"):
            with st.spinner("AI Assistant creates Insights based on given documents..."):
                st.session_state.insight = create_insight(query, settings, qdrant_langchain_wrapper)

        if st.session_state.insight:
            show_json = st.checkbox("Show advanced Insight Infos", value=False)
            st.write("**Title of the Insight**")
            st.write(st.session_state.insight.title)
            st.write("**Summary**")
            st.write(st.session_state.insight.summary)
            if show_json:
                st.json(st.session_state.insight)

            if st.button("Propose action based on this Insight"):
                with st.spinner("AI Assistant proposes Action based on the learned Insight..."):
                    st.session_state.proposal = create_action_proposal_on_given_insight(st.session_state.insight, settings)

            if st.session_state.proposal:
                show_json_action = st.checkbox("Show advanced Action Infos", value=False)
                st.write("**Title of the Action**")
                st.write(st.session_state.proposal.title)
                st.write("**Description**")
                st.write(st.session_state.proposal.description)
                if show_json_action:
                    st.json(st.session_state.proposal)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Accepting this Action"):
                        st.session_state.action = accept_approval(st.session_state.proposal, settings)
                        st.session_state.accept = True
                with col2:
                    if st.button("Rejecting this Action"):
                        st.session_state.action = decline_approval(st.session_state.proposal)
                        st.session_state.accept = False

                if st.session_state.action:
                    st.json(st.session_state.action)

            if st.button("Create a new Insight", type="primary"):
                st.session_state.insight = None
                st.session_state.proposal = None
                st.session_state.action = None
                st.rerun()

    else:
        st.write("No query provided")
