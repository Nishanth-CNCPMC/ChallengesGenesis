import os
import genesis as gs

if os.environ.get("GENESIS_MAIN_PROCESS", "1") == "1":
    gs.init(backend=gs.gpu, debug=False, logging_level=None, logger_verbose_time=False)
    scene = gs.Scene(show_viewer=True)
    scene.viewer.show_fps = False

    plane = scene.add_entity(gs.morphs.Plane())
    so100 = scene.add_entity(
        gs.morphs.URDF(
            file="./urdf/so-100.urdf",
            fixed=True    
        )
    )
    scene.build()
else:
    scene = None
    so100 = None

