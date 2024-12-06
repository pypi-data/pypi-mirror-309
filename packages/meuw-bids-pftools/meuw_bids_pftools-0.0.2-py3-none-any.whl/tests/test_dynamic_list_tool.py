from meuw_bids_pftools.tools.dynamic_list import generate_dynamic_list_options, process_selected_variants

# Test generate_dynamic_list_options
inputs_list = ["Option A", "Option B"]
dynamic_options = generate_dynamic_list_options(inputs_list)
print("Dynamic Options:", dynamic_options)

# Test process_selected_variants
selected_variants = ["Option A"]
result = process_selected_variants(selected_variants)
print("Process Selected Variants Result:", result)