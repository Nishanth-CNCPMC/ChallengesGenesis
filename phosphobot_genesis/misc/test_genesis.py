import genesis as gs

# Initialize Genesis with CPU backend
gs.init(backend=gs.cpu)

# Create a scene with viewer enabled and disable FPS profiling
scene = gs.Scene(
    show_viewer=True,
    show_FPS=False  # ✅ disable FPS logging directly
)

# Add a plane to the scene
plane = scene.add_entity(gs.morphs.Plane())

# Add the Franka Emika Panda robot using MJCF
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml')
)

# Build the scene
scene.build()

# Step the simulation
for i in range(1000):
    scene.step()

