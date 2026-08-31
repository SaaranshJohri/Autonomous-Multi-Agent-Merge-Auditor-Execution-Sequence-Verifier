import streamlit as st
import requests


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="MergeMind",
    page_icon="🧠",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 30px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    background: #161b22;
    border: 1px solid #30363d;
    text-align: center;
}

.metric-number {
    font-size: 32px;
    font-weight: 700;
}

.metric-label {
    color: #9ca3af;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
}

.function-card {
    padding: 16px;
    border-radius: 10px;
    background: #161b22;
    border: 1px solid #30363d;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="title">🧠 MergeMind</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Code Intelligence & Semantic Merge Analysis'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Analysis")

    backend_url = st.text_input(
        "Backend URL",
        "http://127.0.0.1:8000"
    )

    st.divider()

    st.write("### Analysis Pipeline")

    st.write("🟢 Source Code")
    st.write("↓")
    st.write("🟢 AST Parsing")
    st.write("↓")
    st.write("⚪ Dependency Graph")
    st.write("↓")
    st.write("⚪ Conflict Detection")
    st.write("↓")
    st.write("⚪ AI Auditing")


# ---------------------------------------------------------
# CODE INPUT
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📄 Source Code</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 3])

with col1:

    filename = st.text_input(
        "Filename",
        "test.py"
    )

with col2:

    st.write("")


default_code = '''import math
from database import save_user


class User:

    def __init__(self, name):
        self.name = name

    def save(self):
        save_user(self.name)


def calculate_tax(price):
    tax = price * 0.18
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)
        total = price + tax
        return total

    return 0


def checkout(price):

    total = calculate_total(price)

    print(total)

    return total


user = User("Saaransh")

user.save()

checkout(100)
'''


code = st.text_area(
    "Python Code",
    value=default_code,
    height=400
)


analyze = st.button(
    "🔍 Analyze Code",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if analyze:

    with st.spinner("Analyzing source code..."):

        try:

            response = requests.post(
                f"{backend_url}/parse",
                json={
                    "filename": filename,
                    "code": code
                },
                timeout=10
            )

            data = response.json()

            if not data.get("success"):

                st.error(
                    data.get(
                        "error",
                        "Analysis failed"
                    )
                )

            else:

                analysis = data["ast_analysis"]

                st.session_state["analysis"] = analysis

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to MergeMind backend. "
                "Make sure FastAPI is running."
            )

        except Exception as e:

            st.error(f"❌ Error: {str(e)}")


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if "analysis" in st.session_state:

    analysis = st.session_state["analysis"]

    functions = analysis.get(
        "functions",
        []
    )

    classes = analysis.get(
        "classes",
        []
    )

    imports = analysis.get(
        "imports",
        []
    )

    calls = analysis.get(
        "function_calls",
        []
    )

    variables = analysis.get(
        "variables",
        []
    )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Code Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:
        st.metric(
            "Functions",
            len(functions)
        )

    with c2:
        st.metric(
            "Classes",
            len(classes)
        )

    with c3:
        st.metric(
            "Imports",
            len(imports)
        )

    with c4:
        st.metric(
            "Function Calls",
            len(calls)
        )

    with c5:
        st.metric(
            "Variables",
            len(variables)
        )


    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🔬 Code Intelligence</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧩 Structure",
        "🔗 Relationships",
        "⚙️ Functions",
        "📦 Imports"
    ])


    # -----------------------------------------------------
    # STRUCTURE
    # -----------------------------------------------------

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Functions")

            for function in functions:

                st.markdown(
                    f"""
                    <div class="function-card">

                    <b>🔧 {function['name']}</b>

                    <br>

                    Lines:
                    {function['line']} -
                    {function['end_line']}

                    <br>

                    Arguments:
                    {function['argument_count']}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        with col2:

            st.subheader("Classes")

            if not classes:

                st.info(
                    "No classes detected."
                )

            for cls in classes:

                st.markdown(
                    f"""
                    <div class="function-card">

                    <b>🏛️ {cls['name']}</b>

                    <br>

                    Lines:
                    {cls['line']} -
                    {cls['end_line']}

                    <br>

                    Methods:
                    {len(cls['methods'])}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    with tab2:

        st.subheader(
            "Function Relationships"
        )

        has_relationship = False

        for function in functions:

            internal_calls = [
                call
                for call in function.get(
                    "calls",
                    []
                )
                if call.get(
                    "is_internal",
                    False
                )
            ]

            if internal_calls:

                has_relationship = True

                st.markdown(
                    f"### 🔧 {function['name']}"
                )

                for call in internal_calls:

                    st.write(
                        f"↳ calls **{call['name']}** "
                        f"(line {call['line']})"
                    )


        if not has_relationship:

            st.info(
                "No internal function relationships detected."
            )


    # -----------------------------------------------------
    # FUNCTIONS
    # -----------------------------------------------------

    with tab3:

        st.subheader(
            "Detailed Function Analysis"
        )

        for function in functions:

            with st.expander(
                f"🔧 {function['name']}"
            ):

                st.write(
                    f"**Location:** "
                    f"Lines {function['line']} - "
                    f"{function['end_line']}"
                )

                st.write(
                    f"**Arguments:** "
                    f"{function['argument_count']}"
                )

                if function["arguments"]:

                    st.write(
                        "**Parameters**"
                    )

                    for argument in function[
                        "arguments"
                    ]:

                        annotation = argument.get(
                            "annotation"
                        )

                        if annotation:

                            st.write(
                                f"- `{argument['name']}` "
                                f"({annotation})"
                            )

                        else:

                            st.write(
                                f"- `{argument['name']}`"
                            )


                if function["calls"]:

                    st.write(
                        "**Calls**"
                    )

                    for call in function["calls"]:

                        st.write(
                            f"- `{call['name']}` "
                            f"(line {call['line']})"
                        )


                if function["returns"]:

                    st.write(
                        "**Return Statements**"
                    )

                    for ret in function[
                        "returns"
                    ]:

                        st.write(
                            f"- Line {ret['line']} "
                            f"→ "
                            f"{'value returned' if ret['has_value'] else 'empty return'}"
                        )


    # -----------------------------------------------------
    # IMPORTS
    # -----------------------------------------------------

    with tab4:

        st.subheader(
            "Imported Modules"
        )

        if imports:

            for imp in imports:

                if "module" in imp:

                    name = (
                        f"{imp['module']}."
                        f"{imp['name']}"
                    )

                else:

                    name = imp["name"]

                st.write(
                    f"📦 `{name}` "
                    f"— line {imp['line']}"
                )

        else:

            st.info(
                "No imports detected."
            )