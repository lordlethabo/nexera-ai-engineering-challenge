# =====================================================
# app.py
# NexEra AI → 3D Asset Pipeline (Test 1)
# =====================================================

import gradio as gr
from transformers import pipeline


# -----------------------------------------------------
# 1. Load a lightweight AI model for text reasoning
# -----------------------------------------------------
# We use a small text-generation model for explanation.
# Shape/color reasoning is intentionally deterministic
# for clarity and controllability in a prototype.
generator = pipeline("text-generation", model="gpt2")


# -----------------------------------------------------
# 2. AI reasoning: text → shape, color, explanation
# -----------------------------------------------------
def ai_reason(user_text: str):
    if not user_text or not user_text.strip():
        return "box", "0x00ff00", "Please describe an object."

    text = user_text.lower()

    # ---- Shape detection ----
    shape = "box"
    if "sphere" in text or "ball" in text:
        shape = "sphere"
    elif "cone" in text:
        shape = "cone"

    # ---- Color detection ----
    color = "0x00ff00"  # default green
    if "red" in text:
        color = "0xff0000"
    elif "blue" in text:
        color = "0x0000ff"
    elif "yellow" in text:
        color = "0xffff00"

    # ---- AI-generated educational explanation ----
    prompt = f"Explain what this object is used for in simple terms: {user_text}"
    output = generator(prompt, max_length=60, num_return_sequences=1)
    explanation = output[0]["generated_text"]

    return shape, color, explanation


# -----------------------------------------------------
# 3. Bridge: Python → index.html → main.js
# -----------------------------------------------------
def render_pipeline(user_text):
    shape, color, explanation = ai_reason(user_text)

    # This script calls the JS bridge function in index.html
    js_call = f"""
    <script>
        if (typeof renderFromAI === "function") {{
            renderFromAI("{shape}", {color});
        }}
    </script>
    """

    return explanation, js_call


# -----------------------------------------------------
# 4. Build Gradio interface
# -----------------------------------------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # AI-Powered 3D Learning Prototype  
        Type an object description to generate a 3D learning asset.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(
                label="Describe an object",
                placeholder="e.g. a yellow hard hat or a blue sphere",
                lines=2
            )

            generate_btn = gr.Button("Generate", variant="primary")

            explanation_output = gr.Markdown(
                "AI-generated explanation will appear here."
            )

        with gr.Column(scale=2):
            # Load the frontend shell
            viewer = gr.HTML(
                '<iframe src="index.html" '
                'style="width:100%; height:460px; border:none;"></iframe>'
            )

    generate_btn.click(
        fn=render_pipeline,
        inputs=user_input,
        outputs=[explanation_output, viewer]
    )


# -----------------------------------------------------
# 5. Launch app
# -----------------------------------------------------
demo.launch()
