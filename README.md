# Animal Jiu Jitsu

A 3D animation project featuring a cartoon fox performing jiu jitsu movements, built with Blender and Python.

## Quick Start

### Step 1: Run the Script
1. Open **Blender 5.1**
2. Go to **Scripting** workspace (tab at top)
3. In Text Editor, click **Text > Open**
4. Navigate to `scripts/main.py` and open it
5. Press **Alt+P** to run

This creates the fox, scene, and shrimping animation automatically.

### Step 2: Watch the Animation
1. Switch to **Layout** workspace
2. Press **Spacebar** to play/pause
3. Press **Numpad 0** to view through render camera
4. Middle-click drag to orbit the view

### Step 3: Render a Video (Optional)
1. Press **Ctrl+F12** to render animation
2. Find output in `renders/test/` folder

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Spacebar | Play/pause animation |
| Shift+Left | Jump to start |
| Shift+Right | Jump to end |
| Left/Right | Step frame by frame |
| Numpad 0 | Camera view |
| Z | Viewport shading menu |

## Project Structure

```
animated-jiu-jitsu/
├── scripts/
│   └── main.py           # Main script - run this in Blender
├── blend/                 # Blender project files
├── renders/test/          # Output renders
└── README.md
```

## Troubleshooting

### "ModuleNotFoundError" when running script

This was fixed by consolidating all code into a single `main.py` file. If you see this error, make sure you're using the latest version of `scripts/main.py`.

### Script doesn't run

- Make sure you **Open** the file (Text > Open), not copy-paste
- Check the Blender console for errors: **Window > Toggle System Console**

### Animation looks wrong

- Press **Numpad 0** to see the proper camera angle
- Make sure you're in **Object Mode**, not Edit Mode
- Try **View > Frame All** (Home key) to see everything

## What It Creates

- **Fox character**: Orange cartoon fox made from primitive shapes
- **BJJ mat**: Blue ground plane
- **3-point lighting**: Key, fill, and rim lights
- **Shrimping animation**: 2 reps of hip escape drill (~6 seconds)
- **Render settings**: 720p @ 24fps, Eevee renderer
