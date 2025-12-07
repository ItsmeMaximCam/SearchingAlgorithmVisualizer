import gradio as gr

def parse_input(array_input):
    try:
        #Remove extra spaces and split by commas
        array = [int(x.strip()) for x in array_input.split(',')]
        return array, None
    except ValueError:
        return None, "Invalid input! Please enter integers separated by commas."

def is_sorted(array):
    return all(array[i] <= array[i+1] for i in range(len(array)-1))

def initialize_search(array_input, target_input):
    ##Parse array
    array, error = parse_input(array_input)
    if error:
        return None, error, ""
    
    
    if len(array) == 0: 
        return None, "Array cannot be empty!", ""
    
    #Check if array is sorted
    if not is_sorted(array):
        return None, "Array must be sorted in ascending order for Binary Search!", ""
    
    #Parse target
    try:
        target = int(target_input.strip())
    except ValueError:
        return None, "Target must be a valid integer!", ""
    
    #Initialize state
    state = {
        'array': array,
        'target': target,
        'left': 0,
        'right': len(array) - 1,
        'step': 0,
        'found': False,
        'found_index': -1,
        'history': [],
        'completed': False
    }
    
    #Create initial visualization
    viz = create_visualization(state)
    status = f"**Searching for {target} in array**\n\n{viz}"
    
    return state, status, "Ready to search! Click 'Next Step' to begin."

def binary_search_step(state):
    #Check if search is already completed
    if state is None:
        return None, "Please initialize the search first!", ""
    
    if state['completed']:
        return state, "Search already completed!", ""
    
    #Check if search space is exhausted
    if state['left'] > state['right']:
        state['completed'] = True
        state['found'] = False
        viz = create_visualization(state)
        status = f"**Target {state['target']} NOT FOUND in the array!**\n\n{viz}"
        step_info = f"**Total Steps:** {state['step']}\n**Comparisons Made:** {state['step']}\n\n The search space has been exhausted."
        return state, status, step_info
    
    #Increment steps
    state['step'] += 1
    
    #Calculate mid index
    mid = (state['left'] + state['right']) // 2
    mid_value = state['array'][mid]
    
    #Store each step's information
    step_data = {
        'step_num': state['step'],
        'left': state['left'],
        'right': state['right'],
        'mid': mid,
        'mid_value': mid_value,
        'comparison': None,
        'action': None
    }
    
    #Compare w/ target
    if mid_value == state['target']:
        #Target found!
        state['found'] = True
        state['found_index'] = mid
        state['completed'] = True
        step_data['comparison'] = 'equal'
        step_data['action'] = 'found'
        state['history'].append(step_data)
        
        viz = create_visualization(state, current_mid=mid, highlight_found=True)
        status = f"**TARGET FOUND at index {mid}!**\n\n{viz}"
        step_info = format_step_info(step_data, state)
        
    elif mid_value < state['target']:
        #Target is in the right half
        step_data['comparison'] = 'less'
        step_data['action'] = 'search_right'
        state['history'].append(step_data)
        state['left'] = mid + 1
        
        viz = create_visualization(state, current_mid=mid)
        status = f"**Step {state['step']}:** Searching...\n\n{viz}"
        step_info = format_step_info(step_data, state)
        
    else:  #mid_value > state['target']
        #Target must be in the left half
        step_data['comparison'] = 'greater'
        step_data['action'] = 'search_left'
        state['history'].append(step_data)
        state['right'] = mid - 1
        
        viz = create_visualization(state, current_mid=mid)
        status = f"**Step {state['step']}:** Searching...\n\n{viz}"
        step_info = format_step_info(step_data, state)
    
    return state, status, step_info

def create_visualization(state, current_mid=None, highlight_found=False):
    array = state['array']
    left = state['left']
    right = state['right']
    
    #Calculate current mid if not provided
    if left <= right and current_mid is None:
        current_mid = (left + right) // 2
    
    viz = "**Array Visualization:**\n\n"
    viz += "```\n"
    
    #Row's index
    viz += "Index: "
    for i in range(len(array)):
        viz += f"{i:^6}"
    viz += "\n"
    
    #Row's value
    viz += "Value: "
    for i, val in enumerate(array):
        if highlight_found and i == state['found_index']:
            viz += f"[{val:^4}]"
        elif i == current_mid and left <= right:
            viz += f"({val:^4})"
        else:
            viz += f"{val:^6}"
    viz += "\n"
    
    #Pointer!
    viz += "       "
    for i in range(len(array)):
        if i == left and i == right and left <= right:
            viz += "  L,R "
        elif i == left and left <= right:
            viz += "  L   "
        elif i == right and left <= right:
            viz += "  R   "
        elif i == current_mid and left <= right:
            viz += "  M   "
        else:
            viz += "      "
    viz += "\n```\n\n"
    
    #Legend
    viz += "**Legend:** L=Left pointer, R=Right pointer, M=Middle pointer"
    if highlight_found:
        viz += ", [  ]=Found!"
    
    return viz

def format_step_info(step_data, state):
    info = f"### Step {step_data['step_num']} Details:\n\n"
    info += f"- **Left pointer:** Index {step_data['left']} (value: {state['array'][step_data['left']]})\n"
    info += f"- **Right pointer:** Index {step_data['right']} (value: {state['array'][step_data['right']]})\n"
    info += f"- **Middle index:** {step_data['mid']} (calculated as ({step_data['left']} + {step_data['right']}) // 2)\n"
    info += f"- **Middle value:** {step_data['mid_value']}\n"
    info += f"- **Target value:** {state['target']}\n\n"
    
    #Comparison
    info += "**Comparison:**\n"
    if step_data['comparison'] == 'equal':
        info += f"{step_data['mid_value']} == {state['target']} → **Target Found!**\n"
    elif step_data['comparison'] == 'less':
        info += f"{step_data['mid_value']} < {state['target']} → Target is in the **right half**\n"
        info += f"   Action: Move left pointer to {step_data['mid'] + 1}\n"
    else:  # greater
        info += f"{step_data['mid_value']} > {state['target']} → Target is in the **left half**\n"
        info += f"   Action: Move right pointer to {step_data['mid'] - 1}\n"
    
    return info

def run_complete_search(array_input, target_input):
    ##Initialize
    state, status, _ = initialize_search(array_input, target_input)
    if state is None:
        return status, ""
    
    #Run all the steps
    all_steps = ""
    step_count = 0
    max_steps = len(state['array'])  #Infinite loop stopper
    
    while not state['completed'] and step_count < max_steps:
        state, _, step_info = binary_search_step(state)
        all_steps += step_info + "\n\n---\n\n"
        step_count += 1
    
    #summary after conclusion
    summary = f"## Binary Search Complete!\n\n"
    summary += f"**Target:** {state['target']}\n"
    summary += f"**Total Steps:** {state['step']}\n"
    summary += f"**Total Comparisons:** {state['step']}\n\n"
    
    if state['found']:
        summary += f"**Result:** Target found at **index {state['found_index']}**\n\n"
    else:
        summary += f"**Result:** Target not found in array\n\n"
    
    #Calculate the efficiency
    import math
    theoretical_max = math.ceil(math.log2(len(state['array']))) if len(state['array']) > 0 else 0
    summary += f"**Algorithm Efficiency:** O(log n) - Maximum possible steps for array of size {len(state['array'])} is {theoretical_max}\n\n"
    
    viz = create_visualization(state, highlight_found=state['found'])
    
    return summary + viz, all_steps

def reset_search():
    return None, "Reset complete. Enter a new array and target to begin.", ""

#this creates gradio interface https://www.gradio.app/guides/blocks-and-event-listeners
with gr.Blocks(title="Binary Search Visualizer") as demo:
    
    gr.Markdown("""
    # Binary Search Algorithm Visualizer
    
    Binary Search is a very efficient algorithm for finding a target value in a sorted array.
    It works by repeatedly dividing the search space in half, giving it O(log n) time complexity.
    
    ### How to Use:
    1. Enter a sorted array of integers seperated by commas.
    2. Enter a target value to search for
    3. Click Initialize Search to set up
    4. Click Next Step to step through the algorithm
    5. Or click Run Complete Search to see all steps at once
    """)
    
    #state management for search
    search_state = gr.State(None)
    
    with gr.Row():
        with gr.Column(scale=2):
            array_input = gr.Textbox(
                label="Enter Sorted Array, Seperate by Commas",
                placeholder="e.g., 1, 3, 5, 7, 9, 11, 13, 15, 17, 19",
                value="2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78"
            )
            target_input = gr.Textbox(
                label="Enter Target Value",
                placeholder="e.g., 23",
                value="23"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### Tips:
            - Array must be sorted in ascending order
            - Integers only
            - Separate values with commas
            - Try edge cases if you want more steps!
            """)
    
    with gr.Row():
        init_btn = gr.Button("Initialize Search", variant="primary")
        step_btn = gr.Button("Next Step", variant="secondary")
        run_btn = gr.Button("Run Complete Search", variant="secondary")
        reset_btn = gr.Button("Reset", variant="stop")
    
    with gr.Row():
        with gr.Column():
            status_output = gr.Markdown(label="Search Status")
        with gr.Column():
            step_output = gr.Markdown(label="Step Details")
    
    complete_output = gr.Markdown(label="Complete Search Results", visible=False)
    
    #Event handling
    init_btn.click(
        fn=initialize_search,
        inputs=[array_input, target_input],
        outputs=[search_state, status_output, step_output]
    )
    
    step_btn.click(
        fn=binary_search_step,
        inputs=[search_state],
        outputs=[search_state, status_output, step_output]
    )
    
    reset_btn.click(
        fn=reset_search,
        inputs=[],
        outputs=[search_state, status_output, step_output]
    )
    
    run_btn.click(
        fn=run_complete_search,
        inputs=[array_input, target_input],
        outputs=[status_output, step_output]
    )
    
    gr.Markdown("""
    ---
    Algorithm Complexity:
    - **Time Complexity:** O(log n) - logarithmic time
    - **Space Complexity:** O(1) - constant space
    - **Requires:** Sorted array as input
    """)

#This launches app
if __name__ == "__main__": #stops from running on import, , solution generated by Claude with my code copied with prompt "Why is this code not working as intended?"
    demo.launch()