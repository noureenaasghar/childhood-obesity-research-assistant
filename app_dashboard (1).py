import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# ---------- Dashboard styling ----------
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .workflow-banner {
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        background: linear-gradient(110deg, #102f4f, #176b78);
        color: white;
        margin-bottom: 1.2rem;
    }
    .workflow-banner h1 {color: white; margin: 0 0 .35rem 0;}
    .workflow-banner p {color: #e5f3f5; margin: 0;}
    .step-note {
        padding: .8rem 1rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 10px;
        margin: .25rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="workflow-banner">
      <h1>🔬 AI-Assisted Research Workflow</h1>
      <p>Childhood Obesity Prevention | Quantitative Research | Cluster Randomized Controlled Trial</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Work through the research stages in sequence. Each step has its own tab; "
    "the final tab brings the approved study components together into a proposal draft."
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
7. General research questions

Give accurate, clear and understandable academic explanations.
Do not change the finalized proposal.
Do not invent sample sizes, findings or references.
Explain technical terms in simple language.
"""

sections = [
    ("01", "Research Design"),
    ("02", "Study Population"),
    ("03", "Intervention and Control Groups"),
    ("04", "Study Variables and Outcomes"),
    ("05", "Data Collection"),
    ("06", "Statistical Analysis"),
    ("07", "General Research Questions"),
]

def get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API key is not configured. Add GROQ_API_KEY in Streamlit Secrets.")
        return None

    return Groq(api_key=api_key)


def generate_response(user_prompt, temperature=0.3):
    client = get_client()
    if client is None:
        return None

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content


# ---------- Workflow overview ----------
st.subheader("Your Research Workflow")
overview_cols = st.columns(7)
for col, (number, name) in zip(overview_cols, sections):
    with col:
        st.markdown(
            f"""
            <div class="step-note" style="min-height:105px">
              <div style="font-size:12px;opacity:.7;font-weight:700">STEP {number}</div>
              <div style="font-weight:650;font-size:14px;margin-top:7px">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.info(
    "**Study timeline:** 12 months total  |  "
    "**Intervention:** 6 months  |  **Follow-up:** 6 months"
)

# Keep user entries and generated explanations when moving between tabs.
for number, name in sections:
    st.session_state.setdefault(f"question_{number}", "")
    st.session_state.setdefault(f"answer_{number}", "")

st.session_state.setdefault("final_proposal", "")

tab_labels = [f"{number} · {name}" for number, name in sections]
tab_labels.append("08 · Final Research Proposal")
tabs = st.tabs(tab_labels)

# ---------- Steps 1 to 7 ----------
for tab, (number, name) in zip(tabs[:7], sections):
    with tab:
        st.header(f"Step {number}: {name}")
        st.caption(f"Research workflow stage {int(number)} of 7")

        question = st.text_area(
            "Enter your research question:",
            key=f"question_{number}",
            height=130,
            placeholder=(
                "Type your question about this research stage..."
            )
        )

        if st.button(
            "Generate AI Response",
            key=f"generate_{number}",
            type="primary"
        ):
            if not question.strip():
                st.warning("Please enter a research question.")
            else:
                try:
                    with st.spinner("Generating research explanation..."):
                        answer = generate_response(
                            f"Research section: {name}\nQuestion: {question}"
                        )
                    if answer:
                        st.session_state[f"answer_{number}"] = answer
                        st.success("Response generated successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        if st.session_state[f"answer_{number}"]:
            st.divider()
            st.markdown("### AI Research Explanation")
            st.markdown(st.session_state[f"answer_{number}"])

# ---------- Final proposal tab ----------
with tabs[7]:
    st.header("Step 08: Final Research Proposal Development")
    st.write(
        "Bring the finalized research framework and the seven workflow stages "
        "together into one structured quantitative research proposal."
    )

    st.markdown(
        """
        **The final proposal will be organized into:**
        1. Title and abstract
        2. Background and rationale
        3. Research aim and objectives
        4. Research question and hypothesis
        5. Methodology and study design
        6. Study population and sampling
        7. Intervention and control conditions
        8. Study variables and outcome measures
        9. Data collection and study timeline
        10. Statistical analysis
        11. Ethical considerations
        12. Limitations and expected contribution
        """
    )

    st.warning(
        "The assistant will not invent missing details such as sample size, "
        "specific recruitment numbers, study findings, or references. "
        "Items needing a decision will be clearly marked for completion."
    )

    if st.button(
        "Develop Final Research Proposal",
        type="primary",
        key="develop_final_proposal"
    ):
        collected_stages = []
        for number, name in sections:
            question = st.session_state.get(f"question_{number}", "").strip()
            answer = st.session_state.get(f"answer_{number}", "").strip()
            if question or answer:
                collected_stages.append(
                    f"STAGE {number}: {name}\n"
                    f"User question: {question or 'Not provided'}\n"
                    f"AI explanation: {answer or 'No AI explanation generated'}"
                )

        stage_context = "\n\n".join(collected_stages) if collected_stages else (
            "No additional stage-specific questions or AI explanations have "
            "been saved. Use only the finalized study details in the system prompt."
        )

        final_prompt = f"""
Develop a coherent, academically structured quantitative research proposal
based strictly on the finalized study details in the system instructions.

Use the following headings where appropriate:
- Title
- Abstract (do not invent results)
- Background and rationale
- Aim and objectives
- Research question and hypothesis
- Study design and setting
- Study population and eligibility criteria
- Sampling and recruitment
- Randomization and allocation
- Intervention and control conditions
- Study variables and outcome measures
- Data collection and assessment time points
- Statistical analysis
- Ethical considerations
- Potential limitations
- Significance and expected contribution

Use the saved workflow material below only as supporting context. Do not
introduce contradictions or change the finalized proposal. Do not invent a
sample size, power calculation, recruitment target, exact measurement device,
laboratory panel, results, or references. If an essential methodological
detail has not been supplied, label it "[To be specified]" and briefly state
what decision is needed. Keep the 6-month intervention and 6-month follow-up
within the 12-month study period clear. Explain the cluster randomization
and account for school-level clustering and repeated measurements in the
analysis plan.

SAVED WORKFLOW MATERIAL:
{stage_context}
"""
        try:
            with st.spinner("Developing the integrated research proposal..."):
                proposal = generate_response(final_prompt, temperature=0.2)
            if proposal:
                st.session_state["final_proposal"] = proposal
                st.success("Final proposal draft generated!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.session_state["final_proposal"]:
        st.divider()
        st.markdown("### Final Research Proposal Draft")
        st.markdown(st.session_state["final_proposal"])
        st.download_button(
            "Download proposal as Markdown",
            data=st.session_state["final_proposal"],
            file_name="childhood_obesity_research_proposal.md",
            mime="text/markdown"
        )

st.divider()
st.caption(
    "AI-Assisted Quantitative Research Tool | "
    "Childhood Obesity Prevention | Cluster Randomized Controlled Trial"
)
