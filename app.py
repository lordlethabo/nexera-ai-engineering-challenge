# app.py
import gradio as gr
from transformers import pipeline

# ---------------------------
# 1️ Load a text generation model
# ---------------------------
# This pipeline uses GPT-2 (pretrained) to generate a short explanation based on user input
generator = pipeline("text-generation", model="gpt2")

# ---------------------------
# 2️ Function to generate AI explanation
# ---------------------------
def generate_explanation(user_text):
    """
    Takes user input text and generates an AI explanation.
    If the input is empty, it asks the user to type something.
    """
    if not user_text.strip():
        return "Please type an object description."
    output = generator(user_text, max_length=50, num_return_sequences=1)
    explanation_text = output[0]['generated_text']
    return explanation_text

# ---------------------------
# 3️ Function to generate 3D model HTML
# ---------------------------
def generate_3d_html(user_text):
    """
    Converts the user's text into a simple 3D object using three.js.
    Supports cube, sphere, cone and basic colors (red, green, blue, yellow).
    """
    # Default values
    shape = "box"  # default shape is cube
    color = "0x00ff00"  # default color green

    # Normalize input for easier detection
    text_lower = user_text.lower()

    # Detect shape keywords
    if "sphere" in text_lower:
        shape = "sphere"
    elif "cone" in text_lower:
        shape = "cone"

    # Detect color keywords
    if "red" in text_lower:
        color = "0xff0000"
    elif "blue" in text_lower:
        color = "0x0000ff"
    elif "yellow" in text_lower:
        color = "0xffff00"
    
    # HTML + JavaScript for three.js rendering
    html_code = f"""
    <div id="container" style="width:100%; height:400px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
    <script>
        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias:true}});
        renderer.setSize(400, 400);
        document.getElementById('container').appendChild(renderer.domElement);
        // Geometry selection
        let geometry;
        if("{shape}" === "box") {{
            geometry = new THREE.BoxGeometry();
        }} else if("{shape}" === "sphere") {{
            geometry = new THREE.SphereGeometry(0.5, 32, 32);
        }} else if("{shape}" === "cone") {{
            geometry = new THREE.ConeGeometry(0.5, 1, 32);
        }}
        // Material
        const material = new THREE.MeshBasicMaterial({{color: {color}}});
        const object = new THREE.Mesh(geometry, material);
        scene.add(object);
        // Camera position
        camera.position.z = 3;
        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            object.rotation.x += 0.01;
            object.rotation.y += 0.01;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    return html_code

# ---------------------------
# 4️ Build the Gradio interface
# ---------------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # AI-Powered 3D Learning Prototype  
        _Type an object description and explore it in 3D_
        """
    )

    with gr.Row():
        # Left column: input + AI explanation
        with gr.Column(scale=1):
            user_input = gr.Textbox(
                label="Describe an object",
                placeholder="e.g. a yellow sphere",
                lines=2
            )

            generate_btn = gr.Button(
                "Generate",
                variant="primary"
            )

            explanation = gr.Markdown("AI explanation will appear here.")

        # Right column: 3D Viewer
        with gr.Column(scale=2):
            three_d_viewer = gr.HTML("<div>3D Viewer will load here</div>")

    # ---------------------------
    # 5️ Connect the button click
    # ---------------------------
    generate_btn.click(
        fn=lambda text: [generate_explanation(text), generate_3d_html(text)],
        inputs=user_input,
        outputs=[explanation, three_d_viewer]
    )

# ---------------------------
# 6️ Launch the Gradio app
# ---------------------------
demo.launch()
