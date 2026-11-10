
import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI-Assisted Research Workflow")
st.subheader("Childhood Obesity Prevention | Cluster RCT")

st.write(
    "An AI-powered assistant to help understand and organize "
    "the quantitative research workflow."
)

SYSTEM_PROMPT = """
You are an AI-Assisted Quantitative Research Assistant.

Help the user understand and organize this finalized research proposal.

TITLE:
Impact of an Integrated Physical Activity and Sedentary Behaviour
Intervention on Adiposity and Cardiometabolic Health in School-Aged
Children: A Cluster Randomized Controlled Trial.

SETTING: USA, public elementary schools.
POPULATION: Children aged 6-10 years.
DESIGN: Parallel-group Cluster Randomized Controlled Trial.
INTERVENTION: 6 months.
FOLLOW-UP: 6 months.
FRAMEWORK: Social Cognitive Theory.

PRIMARY OUTCOME: BMI-for-age z-score.

SECONDARY OUTCOMES:
- Physical activity and MVPA
- Sedentary time
- Waist circumference
- Waist-to-height ratio
- Blood pressure
- Selected metabolic markers, subject to feasibility

Help with:
1. Research design
2. Study population
3. Intervention and control groups
4. Study variables and outcomes
5. Data collection
6. Statistical analysis

Give accurate, clear and understandable academic explanations.

Do not change the finalized proposal.
Do not invent sample sizes, findings or references.
Explain technical terms in simple language.
"""

sections = [
    "Research Design",
    "Study Population",
    "Intervention and Control Groups",
    "Study Variables and Outcomes",
    "Data Collection",
    "Statistical Analysis",
    "General Research Questions"
]

st.sidebar.title("Research Workflow")
selected_section = st.sidebar.selectbox(
    "Select a research section",
    sections
)

st.sidebar.info(
    "Study duration: 12 months\n\n"
    "Intervention: 6 months\n\n"
    "Follow-up: 6 months"
)

st.header(selected_section)

question = st.text_area(
    "Enter your research question:",
    placeholder="e.g. Explain how mixed-effects models will be used in this study."
)

if st.button("Generate AI Response", type="primary"):

    if not question.strip():
        st.warning("Please enter a research question.")

    else:
        try:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                api_key = os.environ.get("GROQ_API_KEY")

            if not api_key:
                st.error("Groq API key is not configured.")
            else:
                client = Groq(api_key=api_key)

                with st.spinner("Generating research explanation..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": (
                                    "Research section: "
                                    + selected_section
                                    + "\nQuestion: "
                                    + question
                                )
                            }
                        ],
                        temperature=0.3
                    )

                st.success("Response generated successfully!")

                st.markdown("### AI Research Explanation")
                st.markdown(
                    response.choices[0].message.content
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()

st.caption(
    "AI-Assisted Quantitative Research Tool | "
    "Cluster Randomized Controlled Trial"
)
