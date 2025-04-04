
import streamlit as st
import random

# --- Muscle Data ---
muscles = {
    "Rectus Femoris": {
        "origin": "Anterior inferior iliac spine (AIIS)",
        "insertion": "Tibial tuberosity via patellar ligament",
        "action": "Extends the knee and flexes the hip"
    },
    "Vastus Lateralis": {
        "origin": "Greater trochanter and lateral lip of linea aspera",
        "insertion": "Tibial tuberosity via patellar ligament",
        "action": "Extends the knee"
    },
    "Sartorius": {
        "origin": "Anterior superior iliac spine (ASIS)",
        "insertion": "Medial surface of proximal tibia (pes anserinus)",
        "action": "Flexes, abducts, and laterally rotates the hip; flexes the knee"
    },
    "Gastrocnemius": {
        "origin": "Lateral and medial condyles of femur",
        "insertion": "Posterior surface of calcaneus via Achilles tendon",
        "action": "Plantarflexes foot and flexes knee"
    },
    "Tibialis Anterior": {
        "origin": "Lateral condyle and lateral surface of tibia",
        "insertion": "Medial cuneiform and base of first metatarsal",
        "action": "Dorsiflexes and inverts foot"
    }
}

# --- Streamlit UI ---
st.set_page_config(page_title="Muscle Anatomy Quiz", layout="centered")
st.title("🦵 Muscle Anatomy Quiz Simulator")
st.write("Test your knowledge on muscle origin, insertion, and action.")

# --- State initialization ---
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.correct_answer = ""
    st.session_state.options = []
    st.session_state.field = ""
    st.session_state.muscle = ""
    st.session_state.feedback = ""

# --- Quiz Logic ---
def generate_question():
    muscle = random.choice(list(muscles.keys()))
    field = random.choice(["origin", "insertion", "action"])
    correct = muscles[muscle][field]
    options = [correct]
    while len(options) < 4:
        rand = muscles[random.choice(list(muscles.keys()))][field]
        if rand not in options:
            options.append(rand)
    random.shuffle(options)
    st.session_state.question = f"What is the **{field}** of the **{muscle}**?"
    st.session_state.correct_answer = correct
    st.session_state.options = options
    st.session_state.field = field
    st.session_state.muscle = muscle
    st.session_state.feedback = ""

# --- Display Question ---
if st.button("🎓 Start / Next Question") or st.session_state.question is None:
    generate_question()

if st.session_state.question:
    st.markdown(f"### {st.session_state.question}")
    selected = st.radio("Choose one:", st.session_state.options)
    if st.button("Submit Answer"):
        if selected == st.session_state.correct_answer:
            st.session_state.feedback = "✅ Correct!"
        else:
            st.session_state.feedback = f"❌ Incorrect! The correct answer is: {st.session_state.correct_answer}"

if st.session_state.feedback:
    st.markdown(f"**{st.session_state.feedback}**")
