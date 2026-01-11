// =====================================================
// main.js
// AI-Driven 3D Viewer (Three.js)
// =====================================================

// Persistent globals for re-rendering
let scene;
let camera;
let renderer;
let mesh;
let light;

// -----------------------------------------------------
// Initialize the 3D viewer
// -----------------------------------------------------
function initScene() {
    const container = document.getElementById("viewer");

    // Remove previous canvas if it exists
    container.innerHTML = "";

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(0, 0, 3);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Light
    light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    scene.add(light);

    // Ambient light for softer shadows
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
}

// -----------------------------------------------------
// Create geometry based on AI interpretation
// -----------------------------------------------------
function createGeometry(shape) {
    switch (shape) {
        case "sphere":
            return new THREE.SphereGeometry(0.6, 32, 32);
        case "cone":
            return new THREE.ConeGeometry(0.6, 1, 32);
        default:
            return new THREE.BoxGeometry(1, 1, 1);
    }
}

// -----------------------------------------------------
// Load or replace the object
// -----------------------------------------------------
function loadMesh(shape, color) {
    if (!scene) {
        initScene();
    }

    // Remove old mesh if present
    if (mesh) {
        scene.remove(mesh);
    }

    const geometry = createGeometry(shape);

    const material = new THREE.MeshStandardMaterial({
        color: color,
        roughness: 0.5,
        metalness: 0.1
    });

    mesh = new THREE.Mesh(geometry, material);

    // Auto-center object
    mesh.geometry.computeBoundingBox();
    mesh.geometry.center();

    scene.add(mesh);
}

// -----------------------------------------------------
// Animation loop
// -----------------------------------------------------
function animate() {
    requestAnimationFrame(animate);

    if (mesh) {
        mesh.rotation.y += 0.01;
        mesh.rotation.x += 0.005;
    }

    renderer.render(scene, camera);
}

// -----------------------------------------------------
// PUBLIC API (Python → HTML → JS)
// -----------------------------------------------------
window.loadObjectFromAI = function (shape, color) {
    loadMesh(shape, color);
    animate();
};

