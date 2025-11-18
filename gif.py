import memory as mem, os

# Official Ark-Enzo GIF Implementation Spec Subset with double replays for each GIF as per the spec
base_GIF = {
    "frames_played": 0,  # unsupported and will be added later
    "number_of_frames": 0,
    "frames": [],
    "current_frame": 0,
    "apply_shader_transformer": "" # unsupported and will be added later
}


base_frame = {
    "height": 0,
    "width": 0,
    "frame_content": -1 # location
}

def trigger_flag():
    open("flag.txt", "w").write(os.environ["flag"])

def pre_process_gif(gif):
    gif["rewind_function_string"] = "" # exec() might cause bugs so we removed this feature until implemented later for a challenge

def process_gif(gif_pointer):
    try: exec(mem.memory[gif_pointer]) # practically guaranteed to be always an empty string as each GIF is pre-processed
    except: pass
    # process_base() is called on the native adapter where the code is hosted
    frames_pointer_array_location = mem.memory[gif_pointer + 2]
    number_of_frames = mem.memory[gif_pointer + 1]

    frame_buffer_location = -1 #
    frame_buffer_size = 0 #

    for i in range(frames_pointer_array_location, frames_pointer_array_location + number_of_frames):
        frame = mem.memory[i]

        if frame_buffer_size != (frame["height"] * frame["width"]): # prevents double free bugs caused due to realloc (implementation is hooked in)
            frame_buffer_location = re_alloc(frame_buffer_location, frame_buffer_size, frame["height"] * frame["width"])
            frame_buffer_size = frame["height"] * frame["width"]

        mem.memory[frame_buffer_location] = mem.memory[i]["content"]
        
        # play_frame() is called on the native adapter where the code is hosted

def re_alloc(location, old_size, new_size):
    mem.free(location, old_size)
    return mem.alloc(new_size)

def _play_gif_once(gif_object, first = True):
    pre_process_gif(gif_object)
    gif_pointer = mem.alloc(5)
    frames_pointer = mem.alloc(gif_object["number_of_frames"])

    if first: # we are already forcing the string to be null so this is safe to do and more peformant as we don't waste CPU time on second replay
        mem.memory[gif_pointer] = gif_object["apply_shader_transformer"]
    mem.memory[gif_pointer + 1] = gif_object["number_of_frames"]
    mem.memory[gif_pointer + 2] = frames_pointer

    for i in range(len(gif_object["frames"])):
        mem.memory[frames_pointer + i] = gif_object["frames"][i]
    
    process_gif(gif_pointer)

def play_gif(gif_object):
    _play_gif_once(gif_object)
    _play_gif_once(gif_object, False)