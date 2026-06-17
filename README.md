# Portfolio

A selection of projects made by me, covering: machine learning, computer vision, 3D modelling and game development. Below is brief context for each project, but feel free to explore each project/subproject folder.

## Machine Learning & Computer Vision

### `Dolphin Acoustics/`
Here is my work from my time working with the Dolphin Acoustics at the University of St Andrews. The project focused on classifying dolphin species from acoustic data. The files provided cover the parts of the pipeline I helped to develop: automated data retrieval (`ocean_api.py`), dataset preparation (`splitData.py` and `dolphinwhistledataset.py`), and a custom CNN built with PyTorch (`CNNfromScratch_audio.py`/`_network.py`), later optimised using Optuna hyperparameter optimisation. We also had to conduct model evaluation using standard metrics (`metric_calculations.py`) and also explored explainability with LIME (`NLIME.py`), shown in `foo1.png`/`foo2.png` highlighting which regions of a spectrogram drove classification.

###  `ML/agent_exploration`
TLDR: see `ML/agent_exploration/README.md`, CLI grid based world is explored by any LLM agent. 

I created a 2D grid-based world for an LLM agent to navigate, explore, and complete goals. The project was built from-scratch in python in 3 days; written to be easily extended. The agent is able to "perceive" its environment through a field-of-view cone, limiting it to only reason about what is infront of it. The agent is fed a prompt containing its: task, agent's state, memory, what it can see (ASCII grid), adjacent cells, available actions, rules of the game, and response type. The agent is then able to reason about all of this information and output a structured response from the available actions. I also chose to make the program relatively model agnostic. As I do not have any API keys I chose to create a manual mode as well, where I copy and paste prompts and responses between the program and an LLM.

```

=== LLM Agent World ===

Task: Collect the red key and open the red door.

  

Tick: 4

Agent: (3, 2) facing east

Inventory: [key_red]

  

Agent View | Full Map

-----------------------------------

? ? ? ? ? ? ? ? ? ? | . . . . . R . . . .

? ? ? ? ? ? ? ? ? ? | . . . . . R . . . .

? ? ? > . R ? ? ? ? | . . . > . R . r . .

? ? ? . . . ? ? ? ? | . . . . . R . . . .

? ? ? . . D ? ? ? ? | . . . . . D . . . .

? ? ? ? ? ? ? ? ? ? | . k . . . R . . . .

```

### `ML/main_hand.py`
A MediaPipe based hand-tracking project mapping hand used later to generate synth audio from hand positions/gestures. This project taught me the foundations of using MediaPipe which I am using in TouchDesigner currently.

## 3D Modelling (Blender)
### `Blender/`
A set of modelling, shading, and animation exercises. 
- A cell-shaded tree animation, with a stylised pixel version (`CelShade-Trees.blend` and `.mov`)
- Modelling projects (`Donut.blend` and `soy.blend`)
- Short Animated piece for a university fashion show (`Mogged.blend`)

## Game Development (Unity / C#)
### `Game Development/Basic Attack/`
A small top-down combat prototype I worked on for a larger project I had intended to make. The file structure mimics the original structure. Demo in `closer.mov`
- Player movement with WASD and a dash (`PlayerMovement.cs`)
- Attack logic (`PlayerAttack.cs`)
- Simple random enemy movement (`RandomMovement.cs`)

### `Game Development /Physics simulation/`
A verlet-inegration physics simulation. Points affected by gravity, connected by constraint "sticks", as well as support for freezing points in place. Built with a clear project structure as it was a final project for Harvard's CS50x course (`GameManager.cs`, `InputManager.cs`, `UIManager.cs`, plus a `Singleton` base class). Note: the original project was made for an older version of Unity and so is currently not buildable; I included it for the underlying simulation logic and code structure. 

