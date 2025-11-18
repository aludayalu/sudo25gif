memory = [0] * (100)
import random
occupied = {}
free_pairs = {}

def alloc(size): # in deployment, the addresses will be randomly sorted so ordering of returned pointers WILL NOT match memory layout AT ALL.
    sizes_available = sorted(free_pairs.keys())
    random.shuffle(sizes_available)
    found_pair_size = 0
    found_pair = False

    for available_size in sizes_available:
        if available_size >= size:
            print("hi", available_size, size)
            found_pair_size = available_size
            found_pair = True
            break

    if found_pair:
        random.shuffle(free_pairs[found_pair_size])
        starts_at = free_pairs[found_pair_size][0]
        free_pairs[found_pair_size].pop(0)
        if len(free_pairs[found_pair_size]) == 0:
            del free_pairs[found_pair_size]
        ends_at = starts_at + size - 1
        new_segment_starts_at = ends_at + 1
        new_segment_ends_at = starts_at + found_pair_size - 1
        new_segment_size = new_segment_ends_at - new_segment_starts_at + 1
        if new_segment_size > 0:
            if new_segment_size not in free_pairs:
                free_pairs[new_segment_size] = [new_segment_starts_at]
            else:
                free_pairs[new_segment_size].append(new_segment_starts_at)
        return starts_at

    i = 0
    found_free = 0
    memory_length = len(memory)
    while found_free != size and i < memory_length:
        if i not in occupied:
            found_free+=1
        else:
            found_free = 0
        i+=1
    if i >= memory_length:
        return -1
    
    
    for j in range(i - found_free, i - found_free + size):
        occupied[j] = 1

    return i - found_free

def free(starts_at, size):
    if size not in free_pairs:
        free_pairs[size] = [starts_at]
    else:
        free_pairs[size].append(starts_at)
    
    for i in range(starts_at, starts_at + size): # unoptimized but will be fixed as we can just leave all of them to be occupied anyways
        del occupied[i]