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
st.markdown("<h1 style='text-align: center; color: darkblue;'>🦵 Muscle Anatomy Quiz Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Test your knowledge on muscle origin, insertion, and action.</p>", unsafe_allow_html=True)

# --- State initialization ---
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.correct_answer = ""
    st.session_state.options = []
    st.session_state.field = ""
    st.session_state.muscle = ""
    st.session_state.feedback = ""
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.asked_questions = set()
    st.session_state.quiz_over = False
    st.session_state.summary = []

# --- Reset Button ---
if st.button("🔄 Reset Quiz"):
    st.session_state.question = None
    st.session_state.correct_answer = ""
    st.session_state.options = []
    st.session_state.field = ""
    st.session_state.muscle = ""
    st.session_state.feedback = ""
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.asked_questions = set()
    st.session_state.quiz_over = False
    st.session_state.summary = []
    st.experimental_rerun()

# --- Quiz Logic ---
def generate_question():
    all_combinations = [(m, f) for m in muscles.keys() for f in ["origin", "insertion", "action"]]
    remaining = [pair for pair in all_combinations if pair not in st.session_state.asked_questions]
    if st.session_state.total >= 10 or not remaining:
        st.session_state.question = None
        st.session_state.quiz_over = True
        st.session_state.feedback = f"🎉 <span style='color: green;'>Quiz complete!</span> Your final score is <strong>{st.session_state.score}</strong> out of <strong>{st.session_state.total}</strong>."
        return

    muscle, field = random.choice(remaining)
    correct = muscles[muscle][field]
    options = [correct]
    while len(options) < 4:
        rand = muscles[random.choice(list(muscles.keys()))][field]
        if rand not in options:
            options.append(rand)
    random.shuffle(options)
    st.session_state.question = f"What is the <span style='color: darkblue;'><strong>{field}</strong></span> of the <strong>{muscle}</strong>?"
    st.session_state.correct_answer = correct
    st.session_state.options = options
    st.session_state.field = field
    st.session_state.muscle = muscle
    st.session_state.feedback = ""
    st.session_state.asked_questions.add((muscle, field))

# --- Display Question ---
if not st.session_state.quiz_over:
    if st.button("🎓 Start / Next Question") or st.session_state.question is None:
        generate_question()

# --- Progress Bar ---
st.progress(st.session_state.total / 10 if st.session_state.total <= 10 else 1.0)

if st.session_state.question:
    st.markdown(f"### {st.session_state.question}", unsafe_allow_html=True)
    selected = st.radio("Choose one:", st.session_state.options, key=st.session_state.total)
    if st.button("Submit Answer"):
        is_correct = selected == st.session_state.correct_answer
        if is_correct:
            st.session_state.feedback = "<span style='color: green;'>✅ Correct!</span>"
            st.session_state.score += 1
        else:
            st.session_state.feedback = f"<span style='color: red;'>❌ Incorrect!</span> The correct answer is: <code>{st.session_state.correct_answer}</code>"
        st.session_state.total += 1

        st.session_state.summary.append({
            "muscle": st.session_state.muscle,
            "field": st.session_state.field,
            "your_answer": selected,
            "correct_answer": st.session_state.correct_answer,
            "result": "✅" if is_correct else "❌"
        })

if st.session_state.feedback:
    st.markdown(f"**{st.session_state.feedback}**", unsafe_allow_html=True)
    st.markdown(f"**Score: <span style='color: darkblue;'>{st.session_state.score} / {st.session_state.total}</span>**", unsafe_allow_html=True)

if st.session_state.quiz_over:
    st.markdown(f"### 🎉 Quiz complete!", unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.feedback}**", unsafe_allow_html=True)

    with st.expander("📋 View Summary of Your Answers"):
        for i, q in enumerate(st.session_state.summary, 1):
            st.markdown(
                f"**Q{i}.** What is the {q['field']} of **{q['muscle']}**?<br>"
                f"<span style='color:blue;'>Your answer:</span> `{q['your_answer']}`<br>"
                f"<span style='color:green;'>Correct answer:</span> `{q['correct_answer']}`<br>"
                f"<strong>Result:</strong> {q['result']}",
                unsafe_allow_html=True
            )
            st.markdown("---")

