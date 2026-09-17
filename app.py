import streamlit as st


from model_logic import (
    process_and_predict
)


from agents import (
    run_agentic_pipeline
)


from rag_engine import (
    search_knowledge
)


from granite_ai import (
    generate_granite_response
)


from impact_engine import (
    calculate_impact
)


from sustainability import (
    get_sustainability_score,
    get_sdg_mapping,
    get_green_challenges,
)


from theme_engine import (
    THEMES,
    apply_theme,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="VerdeSight AI",

    page_icon="♻️",

    layout="wide",

    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "theme" not in st.session_state:

    st.session_state.theme = (
        "Neon Green"
    )


if "green_score" not in st.session_state:

    st.session_state.green_score = 0


if "identified_items" not in st.session_state:

    st.session_state.identified_items = []


if "prediction_history" not in st.session_state:

    st.session_state.prediction_history = []


if "page" not in st.session_state:

    st.session_state.page = (
        "Identify Waste"
    )


# ============================================================
# THEME
# ============================================================

theme_options = list(
    THEMES.keys()
)


if (
    st.session_state.theme
    not in theme_options
):

    st.session_state.theme = (
        theme_options[0]
    )


apply_theme(
    st.session_state.theme
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# ♻️ VerdeSight AI"
    )

    st.caption(
        "AI-Powered Waste Intelligence"
    )

    st.divider()


    # --------------------------------------------------------
    # THEME
    # --------------------------------------------------------

    st.subheader(
        "🎨 Interface Theme"
    )

    selected_theme = st.selectbox(

        "Choose a theme",

        theme_options,

        index=theme_options.index(
            st.session_state.theme
        ),
    )


    if (
        selected_theme
        != st.session_state.theme
    ):

        st.session_state.theme = (
            selected_theme
        )

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.subheader(
        "🧭 Navigation"
    )


    pages = [

        "Identify Waste",

        "Ask VerdeSight",

        "Impact Simulator",

        "Sustainability Planner",

        "Green Challenge",

        "My Green Score",

        "About",
    ]


    current_index = (

        pages.index(
            st.session_state.page
        )

        if (
            st.session_state.page
            in pages
        )

        else 0
    )


    selected_page = st.radio(

        "Select page",

        pages,

        index=current_index,

        label_visibility="collapsed",
    )


    st.session_state.page = (
        selected_page
    )


    st.divider()


    # --------------------------------------------------------
    # GREEN SCORE
    # --------------------------------------------------------

    st.subheader(
        "🌱 Green Score"
    )


    st.metric(

        "Current Score",

        st.session_state.green_score,
    )


    st.caption(
        "Sustainable actions completed"
    )


    st.divider()


    st.caption(
        "© Mili Srivastava"
    )


# ============================================================
# HERO
# ============================================================

st.title(
    "♻️ VerdeSight AI"
)


st.subheader(
    "AI-Powered Waste Intelligence for a Sustainable Future"
)


st.write(
    "Understand waste, improve segregation, "
    "discover recycling options and build "
    "better sustainable habits."
)


st.divider()


# ============================================================
# PAGE 1 — IDENTIFY WASTE
# ============================================================

if (
    st.session_state.page
    == "Identify Waste"
):

    st.header(
        "♻️ Identify Waste"
    )


    st.write(
        "Upload a waste image to classify it "
        "using the trained AI model."
    )


    uploaded_file = st.file_uploader(

        "Upload a waste image",

        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
        ],

        key="waste_image",
    )


    if uploaded_file:

        st.image(

            uploaded_file,

            caption="Uploaded Waste Image",

            width="stretch",
        )


        if st.button(

            "🔍 Analyze Waste",

            width="stretch",

            key="analyze_waste",
        ):

            with st.spinner(
                "AI model and agents are analyzing..."
            ):

                try:

                    # ----------------------------------------
                    # ML
                    # ----------------------------------------

                    prediction = (
                        process_and_predict(
                            uploaded_file
                        )
                    )


                    # ----------------------------------------
                    # AGENTS
                    # ----------------------------------------

                    agent_results = (
                        run_agentic_pipeline(
                            prediction
                        )
                    )


                except Exception as e:

                    st.error(
                        "Could not analyze the image."
                    )

                    st.exception(e)

                    st.stop()


            st.divider()


            # =================================================
            # PREDICTION
            # =================================================

            st.subheader(
                "🎯 Classification Result"
            )


            col1, col2 = (
                st.columns(2)
            )


            with col1:

                st.metric(

                    "Waste Category",

                    prediction[
                        "category"
                    ],
                )


            with col2:

                st.metric(

                    "Confidence",

                    (
                        f'{prediction["confidence"]:.2f}%'
                    ),
                )


            confidence = (
                prediction[
                    "confidence"
                ]
            )


            if confidence >= 80:

                st.success(
                    "High-confidence prediction."
                )

            elif confidence >= 60:

                st.info(
                    "Moderate-confidence prediction."
                )

            elif confidence >= 45:

                st.warning(
                    "Low-confidence prediction."
                )

            else:

                st.error(
                    "The model is uncertain."
                )


            # =================================================
            # TOP 3
            # =================================================

            st.subheader(
                "📊 Top 3 Predictions"
            )


            for index, item in enumerate(

                prediction[
                    "top_predictions"
                ],

                start=1,
            ):

                st.write(

                    f"**{index}. "
                    f"{item['category']}** — "
                    f"{item['confidence']:.2f}%"
                )


            st.divider()


            # =================================================
            # VERIFICATION AGENT
            # =================================================

            st.subheader(
                "🤖 Agentic AI Verification"
            )


            verification = (
                agent_results[
                    "verification"
                ]
            )


            if (
                verification[
                    "decision"
                ]
                == "ACCEPT"
            ):

                st.success(
                    "✅ Prediction Accepted"
                )

            else:

                st.warning(
                    "⚠️ Manual Review Recommended"
                )


            st.write(
                f"**Decision:** "
                f"{verification['decision']}"
            )


            st.write(
                f"**Reason:** "
                f"{verification['reason']}"
            )


            st.write(
                f"**Prediction Gap:** "
                f"{verification['prediction_gap']:.2f}%"
            )


            # =================================================
            # ANALYSIS AGENT
            # =================================================

            st.subheader(
                "🧠 Waste Analysis Agent"
            )


            analysis = (
                agent_results[
                    "analysis"
                ]
            )


            st.info(

                f"**Category:** "
                f"{analysis['category']}\n\n"

                f"**Status:** "
                f"{analysis['status']}"
            )


            # =================================================
            # RECYCLING AGENT
            # =================================================

            st.subheader(
                "♻️ Recycling Agent"
            )


            recycling = (
                agent_results[
                    "recycling"
                ]
            )


            st.success(
                recycling[
                    "guidance"
                ]
            )


            # =================================================
            # ACTION PLAN
            # =================================================

            st.subheader(
                "🌱 Action Planning Agent"
            )


            action_plan = (
                agent_results[
                    "action_plan"
                ]
            )


            for action in (
                action_plan[
                    "actions"
                ]
            ):

                st.write(
                    f"✅ {action}"
                )


            # =================================================
            # ENVIRONMENTAL IMPACT
            # =================================================

            st.subheader(
                "🌍 Environmental Impact"
            )


            try:

                impact = calculate_impact(

                    prediction[
                        "raw_category"
                    ]
                )


                if isinstance(
                    impact,
                    dict
                ):

                    items = list(
                        impact.items()
                    )


                    if items:

                        columns = (
                            st.columns(
                                min(
                                    4,
                                    len(items)
                                )
                            )
                        )


                        for i, (
                            key,
                            value
                        ) in enumerate(
                            items
                        ):

                            with columns[
                                i % len(columns)
                            ]:

                                st.metric(
                                    str(key),
                                    str(value)
                                )


                else:

                    st.info(
                        str(impact)
                    )


            except Exception:

                st.info(
                    "Impact estimation is "
                    "currently unavailable."
                )


            # =================================================
            # SDG
            # =================================================

            st.subheader(
                "🌍 Sustainability Connection"
            )


            try:

                sdg = get_sdg_mapping(

                    prediction[
                        "raw_category"
                    ]
                )


                if isinstance(
                    sdg,
                    dict
                ):

                    for key, value in (
                        sdg.items()
                    ):

                        st.write(
                            f"**{key}:** {value}"
                        )

                else:

                    st.info(
                        str(sdg)
                    )


            except Exception:

                st.info(
                    "Waste reduction and responsible "
                    "resource use support sustainability goals."
                )


            # =================================================
            # HISTORY
            # =================================================

            st.session_state.identified_items.append(

                prediction[
                    "category"
                ]
            )


            st.session_state.prediction_history.append(
                prediction
            )


# ============================================================
# PAGE 2 — ASK VERDESIGHT
# ============================================================

elif (
    st.session_state.page
    == "Ask VerdeSight"
):

    st.header(
        "💬 Ask VerdeSight"
    )


    st.write(
        "Ask questions about waste management, "
        "recycling, composting, sustainability "
        "and responsible consumption."
    )


    question = st.text_area(

        "Your question",

        placeholder=(
            "Example: Can banana peels be composted?\n"
            "Example: How should e-waste be disposed of?\n"
            "Example: What is circular economy?"
        ),

        height=140,
    )


    if st.button(

        "💬 Ask VerdeSight",

        width="stretch",

        key="ask_verdesight",
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching sustainability knowledge..."
            ):

                try:

                    results = search_knowledge(

                        question,

                        top_k=3
                    )

                except Exception:

                    results = []


                context_parts = []


                for item in results:

                    if isinstance(
                        item,
                        dict
                    ):

                        topic = item.get(
                            "topic",
                            "Sustainability"
                        )


                        content = item.get(
                            "response",
                            ""
                        )


                        if content:

                            context_parts.append(

                                f"### {topic}\n\n"
                                f"{content}"
                            )


                context = (
                    "\n\n".join(
                        context_parts
                    )
                )


                try:

                    response = (
                        generate_granite_response(

                            question,

                            context
                        )
                    )

                except Exception:

                    response = (
                        context
                        if context
                        else
                        "Unable to generate a response."
                    )


            st.subheader(
                "🌱 VerdeSight AI"
            )


            st.info(
                response
            )


            if context:

                with st.expander(
                    "🔎 View Retrieved Knowledge"
                ):

                    st.markdown(
                        context
                    )


# ============================================================
# PAGE 3 — IMPACT SIMULATOR
# ============================================================

elif (
    st.session_state.page
    == "Impact Simulator"
):

    st.header(
        "🌍 Impact Simulator"
    )


    st.write(
        "Explore environmental impact estimates "
        "for different waste choices."
    )


    waste_type = st.selectbox(

        "Select waste type",

        [
            "Plastic",
            "Organic",
            "Paper",
            "Cardboard",
            "E-Waste",
            "Metal",
            "Glass",
            "Textile",
        ],
    )


    quantity = st.number_input(

        "Quantity",

        min_value=1,

        max_value=1000,

        value=1,

        step=1,
    )


    unit = st.selectbox(

        "Unit",

        [
            "items",
            "kg",
            "litres",
        ],
    )


    if st.button(

        "🌍 Calculate Impact",

        width="stretch",

        key="impact_button",
    ):

        try:

            result = calculate_impact(
                waste_type
            )


            st.subheader(
                "Estimated Impact"
            )


            if isinstance(
                result,
                dict
            ):

                result_items = list(
                    result.items()
                )


                if result_items:

                    columns = st.columns(
                        min(
                            4,
                            len(
                                result_items
                            )
                        )
                    )


                    for i, (
                        key,
                        value
                    ) in enumerate(
                        result_items
                    ):

                        with columns[
                            i % len(columns)
                        ]:

                            st.metric(
                                str(key),
                                str(value)
                            )


            else:

                st.info(
                    str(result)
                )


        except Exception as e:

            st.warning(
                "Impact calculation is unavailable."
            )

            st.caption(
                str(e)
            )


# ============================================================
# PAGE 4 — SUSTAINABILITY PLANNER
# ============================================================

elif (
    st.session_state.page
    == "Sustainability Planner"
):

    st.header(
        "🌱 Sustainability Planner"
    )


    st.write(
        "Select sustainable actions and "
        "calculate your Green Score."
    )


    col1, col2 = st.columns(2)


    with col1:

        reduce_plastic = st.checkbox(
            "Reduce single-use plastic"
        )

        reuse_items = st.checkbox(
            "Reuse products whenever possible"
        )

        recycle_waste = st.checkbox(
            "Separate recyclable waste"
        )


    with col2:

        compost = st.checkbox(
            "Compost organic waste"
        )

        save_energy = st.checkbox(
            "Reduce unnecessary energy usage"
        )

        use_public_transport = st.checkbox(
            "Prefer public transport"
        )


    actions = [

        reduce_plastic,

        reuse_items,

        recycle_waste,

        compost,

        save_energy,

        use_public_transport,
    ]


    completed = sum(
        actions
    )


    st.write(
        f"Actions selected: "
        f"**{completed}/6**"
    )


    if st.button(

        "🌱 Calculate Sustainability Score",

        width="stretch",

        key="score_button",
    ):

        try:

            score = (
                get_sustainability_score(
                    completed
                )
            )

        except Exception:

            score = (
                completed * 10
            )


        st.session_state.green_score = max(

            st.session_state.green_score,

            score
        )


        st.success(
            f"Your sustainability score is "
            f"{score}/100."
        )


        st.progress(
            min(
                score / 100,
                1.0
            )
        )


# ============================================================
# PAGE 5 — GREEN CHALLENGE
# ============================================================

elif (
    st.session_state.page
    == "Green Challenge"
):

    st.header(
        "🌿 Green Challenge"
    )


    st.write(
        "Complete simple sustainability "
        "challenges."
    )


    try:

        challenges = (
            get_green_challenges()
        )

    except Exception:

        challenges = [

            "Avoid single-use plastic for one day.",

            "Separate wet and dry waste.",

            "Reuse an old item.",

            "Walk or use public transport for a short trip.",

            "Care for a plant.",
        ]


    for i, challenge in enumerate(

        challenges,

        start=1
    ):

        if isinstance(
            challenge,
            dict
        ):

            title = challenge.get(
                "title",
                f"Challenge {i}"
            )

            description = challenge.get(
                "description",
                ""
            )

            text = (
                f"**{title}**\n\n"
                f"{description}"
            )

        else:

            text = str(
                challenge
            )


        st.info(
            text
        )


        completed_challenge = st.checkbox(

            "Mark as completed",

            key=f"challenge_{i}"
        )


        if completed_challenge:

            st.success(
                "Challenge completed! 🌱"
            )


# ============================================================
# PAGE 6 — MY GREEN SCORE
# ============================================================

elif (
    st.session_state.page
    == "My Green Score"
):

    st.header(
        "🌎 My Green Score"
    )


    score = (
        st.session_state.green_score
    )


    col1, col2, col3 = (
        st.columns(3)
    )


    with col1:

        st.metric(
            "Green Score",
            score
        )


    with col2:

        st.metric(

            "Waste Items Analyzed",

            len(
                st.session_state
                .identified_items
            )
        )


    with col3:

        st.metric(

            "Actions Completed",

            score // 10
        )


    st.subheader(
        "Your Progress"
    )


    st.progress(
        min(
            score / 100,
            1.0
        )
    )


    if score == 0:

        st.info(
            "Start completing sustainable "
            "actions to build your score."
        )

    elif score < 40:

        st.warning(
            "Good start! Keep building "
            "sustainable habits."
        )

    elif score < 70:

        st.info(
            "You're making good progress."
        )

    else:

        st.success(
            "You're building strong sustainable habits."
        )


    if st.session_state.identified_items:

        st.subheader(
            "Waste Analysis History"
        )


        for i, item in enumerate(

            st.session_state
            .identified_items,

            start=1
        ):

            st.write(
                f"{i}. ♻️ {item}"
            )


    if st.session_state.prediction_history:

        with st.expander(
            "📊 Model Prediction Details"
        ):

            for prediction in (
                st.session_state
                .prediction_history
            ):

                st.write(

                    f"**{prediction['category']}** — "
                    f"{prediction['confidence']:.2f}%"
                )


# ============================================================
# PAGE 7 — ABOUT
# ============================================================

elif (
    st.session_state.page
    == "About"
):

    st.header(
        "♻️ About VerdeSight AI"
    )


    st.write(
        """
**VerdeSight AI** is an AI-powered waste intelligence
and sustainability platform designed to help users
understand waste, improve segregation, discover
recycling options and build sustainable habits.
"""
    )


    st.subheader(
        "🤖 AI Architecture"
    )


    st.info(
        """
**Computer Vision**

MobileNetV2 transfer learning is used for waste
image classification.

**Agentic AI**

Specialized agents verify predictions, provide
recycling guidance and generate action plans.

**RAG**

A sustainability knowledge base retrieves relevant
information for user questions.

**Granite-Ready Assistant**

The assistant architecture can be connected to
an IBM Granite model for generative responses.

**Environmental Intelligence**

Impact simulation and sustainability scoring
help users understand waste-related choices.
"""
    )


    st.subheader(
        "Core Features"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            "🤖 **AI Waste Intelligence**\n\n"
            "Trained computer-vision model for waste classification."
        )


        st.info(
            "🧠 **Agentic AI**\n\n"
            "Verification, recycling and action-planning agents."
        )


        st.info(
            "💬 **RAG Assistant**\n\n"
            "Knowledge retrieval for sustainability questions."
        )


    with col2:

        st.success(
            "♻️ **Waste Management**\n\n"
            "Segregation and recycling guidance."
        )


        st.success(
            "🌍 **Environmental Impact**\n\n"
            "Waste impact estimation."
        )


        st.success(
            "🌱 **Sustainability Planner**\n\n"
            "Green actions and scoring."
        )


    st.subheader(
        "Sustainable Development Goals"
    )


    try:

        sdg = get_sdg_mapping(
            "waste management"
        )


        if isinstance(
            sdg,
            dict
        ):

            for key, value in (
                sdg.items()
            ):

                st.info(

                    f"**{key}**\n\n"
                    f"{value}"
                )

        else:

            st.info(
                str(sdg)
            )


    except Exception:

        st.info(
            """
**SDG 12 — Responsible Consumption
and Production**

Promoting responsible resource use,
waste reduction and sustainable consumption.
"""
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "♻️ VerdeSight AI • AI-Powered Waste Intelligence"
)


st.caption(
    "© Mili Srivastava"
)