import logging
import re


def last_sentence(paragraph):
    # Use regex to split the paragraph into sentences based on common sentence-ending punctuation
    # (periods, question marks, exclamation points) followed by optional whitespace.
    sentences = re.split(r'[.!?]+\s*', paragraph)

    # Filter out any empty strings that might result from splitting
    sentences = [s.strip() for s in sentences if s.strip()]

    # Get the last sentence
    if sentences:
        last_sentence = sentences[-1]
        logging.info(last_sentence)
    return last_sentence

#Style elemeent pools
art_styles = [
    "hand-painted 2D/3D hybrid animation with soft brush textures and tactile imperfections",
    "1970s romantic drama shot on 35mm film with halation and warm Kodak tones",
    "hyperreal CG cinematic with volumetric fog, photoreal lighting, and fine surface scattering",
    "stop-motion inspired miniature set with practical lighting and real shadows",
    "anime slice-of-life visual style with gentle pastel palette and parallax background layers",
    "oil-painted rotoscope animation with expressive brushstrokes and uneven frame rhythm",
    "lo-fi VHS aesthetic with chromatic bleed, scanline texture, and handheld realism",
    "dreamlike surrealist motion inspired by René Magritte, with floating objects and impossible light physics",
    "noir-inspired monochrome film with hard shadows, cigarette smoke, and Venetian-blind lighting",
    "digital art motion with painterly depth, dynamic particle effects, and vivid saturation",
    "early 2000s video-game cinematic aesthetic with matte-painted skies and bloom lighting",
    "watercolor animation with fluid color bleeding and paper texture visible through highlights",
    "claymation miniature aesthetic with handcrafted sets and visible imperfections",
    "retro-futuristic synthwave visual style with magenta-blue gradients and wireframe geometry",
    "minimalist art-house tone with static compositions and desaturated color palette",
    "steampunk-inspired industrial design with brass gears, valves, and mechanical ambiance",
    "fantasy illustration brought to life — ornate costumes, glowing runes, misty atmosphere",
    "impressionist visual tone reminiscent of Monet — soft edges, color vibration, light shimmer",
    "cyberpunk neon dystopia rendered in ultra-realistic 3D with wet reflections and backlit haze",
    "mid-century modern animation look with geometric simplicity and paper-cut motion style"
]

lighting_moods = [
    "golden-hour sunlight streaming through dust motes",
    "rainy neon reflections on wet pavement",
    "soft moonlight with gentle practical spill",
    "studio setup with strong key/fill ratio for contrast",
    "candlelit warmth with flickering highlights",
    "harsh noon sunlight with deep shadows and high contrast",
    "overcast daylight with diffuse shadows and cool tones",
    "backlit silhouette with glowing rim light",
    "blue-hour ambient wash with faint window reflections",
    "sunset flare through foliage, orange-pink hues across faces",
    "misty dawn light cutting through fog",
    "fluorescent industrial lighting with cool green tint",
    "dappled light under trees, moving leaf shadows",
    "underwater caustic lighting with moving wave reflections",
    "firelight flicker casting dynamic shadows on walls",
    "high-contrast noir key light from a single exposed bulb",
    "bi-color lighting mix of cold and warm practicals for emotional contrast",
    "soft fill with strong practical key — cinematic portrait balance",
    "window light spill with volumetric shafts of dust and air texture",
    "strobe-lit club environment with rhythmic flashes and color shifts"
]

lenses = [
    "18mm ultra-wide for immersive perspective and depth exaggeration",
    "24mm wide-angle for environmental storytelling",
    "35mm spherical for balanced naturalistic framing",
    "40mm spherical with subtle perspective compression",
    "50mm anamorphic for cinematic bokeh and lens flares",
    "65mm large-format lens with shallow depth and dreamy compression",
    "85mm portrait lens for intimate close-ups and background blur",
    "100mm telephoto for distant isolation and cinematic parallax",
    "14mm fisheye for surreal distortion and spatial exaggeration",
    "macro lens for close detail shots — eyes, textures, or hands in motion"
]
movements = [
    "slow dolly-in for emotional focus",
    "slow dolly-out revealing wider context",
    "handheld micro-shake for realism and intimacy",
    "static locked-off composition with no camera movement",
    "crane pull-back revealing entire environment",
    "tracking shot following character motion through space",
    "orbit shot circling the subject for dramatic emphasis",
    "gimbal-stabilized glide through complex space",
    "aerial drone descent establishing the scene",
    "push-in rack focus shifting between foreground and background",
    "handheld whip-pan capturing sudden action",
    "steady tripod shot for composed framing",
    "low-angle tilt-up to convey power or transformation",
    "top-down overhead shot for geometric symmetry",
    "POV tracking from character perspective",
    "time-lapse pan across changing light conditions"
]