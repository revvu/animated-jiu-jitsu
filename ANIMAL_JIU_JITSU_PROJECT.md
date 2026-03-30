# Animal Jiu Jitsu - 3D Animation Project

**Project Title:** Little Animals Doing Jiu Jitsu
**Description:** A fun, stylized 3D animation project featuring cartoonish animals (e.g., cats, dogs, foxes, or bears) performing jiu jitsu techniques — guard passes, sweeps, submissions (armbars, triangles, rear-naked chokes), rolls, and playful fights.
The goal is to create short looping clips or a mini animated short using procedural/scripted animation in Blender with Python.

**Target Output:** High-quality rendered video clips (MP4) or image sequences, starting with Eevee for fast iteration and moving to nicer final renders via cloud.

---

## MVP Objectives

**Goal:** Create a single 5-10 second animated clip of a cartoon fox performing a shrimping/hip escape drill, fully scripted via Python in Blender 5.1.

### MVP Scope
1. **Fox Model** - Built from primitives (spheres, cylinders) attached to Rigify rig
2. **Rigify Quadruped Rig** - Blender's built-in, adapted for fox proportions
3. **Shrimping Move** - Solo hip escape animation (fundamental BJJ drill)
4. **Python Animation Script** - Procedural keyframe generation
5. **Simple Scene** - Flat mat/ground plane, basic 3-point lighting
6. **Eevee Render Config** - Optimized for CPU preview renders

### Out of Scope (Post-MVP)
- Second animal / grappling interactions
- Multiple move library
- Advanced fur/hair
- Cloud rendering pipeline
- Camera animation
- Sound/music

---

**Tech Stack:**
- **Primary Tool:** Blender (latest stable version recommended, e.g., 4.x series as of 2026)
- **Language:** Python (via Blender's `bpy` API)
- **Renderer (Development):** Eevee (real-time, GPU/CPU friendly for previews)
- **Renderer (Final):** Eevee or Cycles (offloaded to cloud)
- **Editor:** VS Code (or any text editor) + Blender's built-in Text Editor

---

## Project Goals
- Script procedural or keyframed animations for animal rigs performing jiu jitsu moves.
- Keep models low-to-medium poly and stylized for performance on CPU-only laptops.
- Generate variations easily (different animals, move combinations, camera angles).
- Render nice-looking results **without a local GPU**.

---

## How to Develop the Project

### 1. Initial Setup (Native Windows Recommended)
1. Download and install the latest **Blender** from [blender.org](https://www.blender.org).
2. **Do not develop primarily in WSL2** — Eevee viewport relies on good OpenGL/Vulkan acceleration. Native Windows gives smoother previews on integrated graphics.
3. (Optional but recommended) Install **VS Code** and the "Blender Development" or "Python" extensions for better `bpy` autocompletion.
4. Open Blender → Switch to the **Scripting** workspace.

### 2. Asset Creation
- **Modeling:** Create or import simple cartoon animals (body as subdivided meshes, limbs as separate parts if needed). Use BlenderKit add-on for free base assets.
- **Rigging:** Use the built-in **Rigify** add-on for quick quadruped/humanoid rigs. Adjust for animal proportions (longer spine, paws instead of hands/feet).
- **Materials:** Simple Principled BSDF shaders with vibrant colors. Add basic fur/hair with Particle System or Geometry Nodes for stylized look.

### 3. Animation via Python Scripting
All core animation logic lives in Python scripts:
- Control bone rotations, locations, and scales frame-by-frame.
- Create reusable functions for specific moves (e.g., `do_armbar()`, `sweep_from_guard()`, `rolling_transition()`).
- Use `bpy.context.scene.frame_set()` and `keyframe_insert()` to build sequences.
- Add randomness for variety or physics (rigid body constraints) for dynamic grappling.

**Example Starter Script Structure** (save as `jiu_jitsu_anim.py`):

```python
import bpy
from mathutils import Euler
import math

# Setup
scene = bpy.context.scene
rig = bpy.data.objects.get("AnimalRig")  # Replace with your rig name

def set_pose(frame, bone_rotations):
    scene.frame_set(frame)
    for bone_name, rotation in bone_rotations.items():
        if bone_name in rig.pose.bones:
            rig.pose.bones[bone_name].rotation_euler = Euler(rotation)
            rig.pose.bones[bone_name].keyframe_insert("rotation_euler")

# Example sequence: Guard → Armbar transition
for f in range(1, 241):  # 10 seconds @ 24 fps
    if f < 120:
        # Guard pose
        set_pose(f, {
            "Spine": (math.radians(20), 0, 0),
            "Arm_L": (math.radians(-40), 0, math.radians(30)),
            # Add more bones...
        })
    else:
        # Armbar submission
        set_pose(f, {
            "Arm_L": (math.radians(-90), 0, 0),
            # ...
        })

# Render settings for Eevee
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 24
```

- Iterate by running scripts inside Blender.
- Use the **Graph Editor** and **Dope Sheet** to manually tweak scripted keyframes when needed.
- Keep scenes lightweight during development (fewer objects, lower quality previews).

**Tips:**
- Work mostly in **Solid** or **Material Preview** mode.
- Switch to **Rendered** (Eevee) only for periodic checks.
- Version control your `.blend` files and scripts with Git.

---

## How to Run It Locally

### Daily Workflow (No GPU Needed)
1. Open your `.blend` file in native Blender on Windows.
2. Load and run your Python script from the **Text Editor** (`Alt+P` or Run Script button).
3. Preview the animation in the timeline/viewport.
4. For quick test renders:
   - Set output path in **Output Properties**.
   - Go to **Render → Render Animation** (or script it with `bpy.ops.render.render(animation=True)`).
5. Eevee renders reasonably fast on CPU for short clips and stylized scenes.

**Performance Optimizations:**
- Lower viewport sampling and disable heavy effects (SSR, high shadows) while iterating.
- Use Eevee exclusively for local previews.
- Split long sequences into shorter shots.

Local renders are great for tests and drafts. Expect acceptable quality for cartoon jiu jitsu.

---

## How to Deploy / Get Nice Final Renders

Since the laptop has no dedicated GPU, we offload final high-quality rendering to the cloud **for free**.

### Primary Method: SheepIt Render Farm (Recommended)
SheepIt is a free, community-driven Blender render farm.

**Steps:**
1. Create a free account at [sheepit-renderfarm.com](https://www.sheepit-renderfarm.com).
2. Run the SheepIt client on your laptop (in the background) to earn points by contributing idle CPU time.
3. Prepare your `.blend` file:
   - Pack all external assets (File → External Data → Pack All Into .blend).
   - Test that it renders correctly locally.
   - Set render engine to **Eevee** (fast) or **Cycles** (higher quality, slower but GPU-accelerated on farm machines).
4. Upload the project via the SheepIt web interface.
5. Monitor progress in real-time. Download completed frames or assembled video.

**Notes:**
- New users should run the client for a few days to build points.
- Supports latest Blender versions and both Eevee + Cycles.
- Great for batch rendering image sequences.

### Alternative: Google Colab (Quick GPU Access)
1. Upload your `.blend` file to Google Drive.
2. Use a community Blender Colab notebook (search for updated "Blender Colab render" notebooks — many support Eevee and Cycles with GPU).
3. Run the notebook to render on free cloud GPU (T4 or similar).
4. Output saves back to your Drive.

Colab is excellent for one-off tests but has session timeouts. SheepIt is better for consistent, longer projects.

### Final Output Pipeline
- Render image sequence (PNG) → Assemble into MP4 using Blender's Video Sequence Editor or free tools like DaVinci Resolve / FFmpeg.
- Optional: Add sound effects, music, or text overlays in a video editor.

---

## Next Steps & Tips
- Start small: Rig one animal and script a single simple move (e.g., a basic guard pass).
- Expand to multiple animals and interactions.
- Document bone names and common poses in your scripts for reusability.
- Backup `.blend` files regularly.

This setup keeps development fully local and comfortable while delivering pro-looking rendered results for free via cloud farms.

**Project Folder Structure:**
```
animated-jiu-jitsu/
├── blend/                    # Blender project files
│   └── mvp_scene.blend
├── scripts/
│   ├── main.py               # Entry point - run this!
│   ├── core/
│   │   ├── rig_utils.py      # Bone manipulation helpers
│   │   └── keyframe_utils.py # Keyframe utilities
│   ├── moves/
│   │   └── shrimp.py         # Shrimping animation
│   └── setup/
│       ├── scene_setup.py    # Scene, lighting, camera
│       └── materials.py      # Fox & mat materials
├── assets/
│   └── reference/            # Reference images/videos
├── renders/
│   └── test/                 # Local test renders
└── ANIMAL_JIU_JITSU_PROJECT.md
```

Happy coding! This will be a hilarious and satisfying project once the first animal rolls into an armbar.