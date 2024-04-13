class Loop:
    def __init__(self):
        self.state = {}
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": False})}}

    RETURN_TYPES = ("LOOP",)
    FUNCTION = "run"
    CATEGORY = "loopback"

    def run(self, text):
        print("here!")
        print(self)
        return (self.state,)

class LoopStart:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"first_loop": s.RETURN_TYPES, "loop": ("LOOP",)}}

    FUNCTION = "run"
    CATEGORY = "loopback"

    def run(self, first_loop, loop):
        if 'next' in loop:
            return (loop['next'],)
        return (first_loop,)

    @classmethod
    def IS_CHANGED(s, first_loop, loop):
        if 'next' in loop:
            return id(loop['next'])
        return float("NaN")

class LoopEnd:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "send_to_next_loop": (s.LOOP_TYPE,), "loop": ("LOOP",) }}

    RETURN_TYPES = ()
    FUNCTION = "run"
    CATEGORY = "loopback"
    OUTPUT_NODE = True

    def run(self, send_to_next_loop, loop):
        loop['next'] = send_to_next_loop
        return {}

NODE_CLASS_MAPPINGS = {
    "Loop": Loop
}

def addLoopType(t):
    NODE_CLASS_MAPPINGS["LoopStart_" + t] = type("LoopStart_" + t, (LoopStart, ), { "RETURN_TYPES": (t,) })
    NODE_CLASS_MAPPINGS["LoopEnd_" + t] = type("LoopEnd_" + t, (LoopEnd, ), { "LOOP_TYPE": t })

# ComfyUI types
addLoopType("IMAGE")
addLoopType("CONDITIONING")
addLoopType("LATENT")
addLoopType("MASK")
addLoopType("MODEL")

# These don't work for some reason :/
# addLoopType("FLOAT")
# addLoopType("INT")
# addLoopType("STRING")

# Derfuu nodes use these types
addLoopType("FlOAT")
addLoopType("INTEGER")
addLoopType("TUPLE")

# WAS nodes use these types
addLoopType("ASCII")
addLoopType("STR")

# Feel free to add more loopback node types here
