#/home/axibo-pc3/test_Ws/src/phosphobot/phosphobot/resources/urdf/so-100/urdf/so-100.urdf

import genesis as gs

gs.init(backend=gs.cpu)
scene = gs.Scene(show_viewer=True)

# Add a ground plane
scene.add_entity(gs.morphs.Plane())

# Load SO-101 URDF and fix it to the world by setting `fixed=True`
so101 = scene.add_entity(
    gs.morphs.URDF(
        file="/home/axibo-pc3/test_Ws/src/phosphobot/phosphobot/resources/urdf/so-100/urdf/so-100.urdf",
        fixed=True  # This is key
    )
)

scene.build()

# Step the simulation
for _ in range(1000):
    scene.step()

