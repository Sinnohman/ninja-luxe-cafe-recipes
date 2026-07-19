"""Check which recipes were NOT changed and why."""
import re
import sys
sys.path.insert(0, '/root/ninja-luxe-cafe')
from transform_recipes import (
    load_file, transform_step, parse_recipe_object, 
    extract_field, parse_array_strings, has_machine_detail
)

with open('/root/ninja-luxe-cafe/index.html') as f:
    original = f.read()

with open('/root/ninja-luxe-cafe/index_new.html') as f:
    new = f.read()

# Find all recipes in original
arr_start = original.find('const RECIPES = [')
bracket_open = original.index('[', arr_start)
depth = 0; instring = False; esc = False; bracket_close = -1
for i in range(bracket_open, len(original)):
    c = original[i]
    if esc: esc = False; continue
    if c == '\\': esc = True; continue
    if c == "'" and not instring: instring = True; continue
    if c == "'" and instring: instring = False; continue
    if instring: continue
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0: bracket_close = i; break

arr_inner = original[bracket_open + 1:bracket_close]

# Parse recipes
recipes = []
pos = 0
while pos < len(arr_inner):
    while pos < len(arr_inner) and arr_inner[pos] in ' \t\n\r,':
        pos += 1
    if pos >= len(arr_inner): break
    if arr_inner[pos] == '{':
        obj_text, end = parse_recipe_object(arr_inner, pos)
        if obj_text:
            recipes.append(obj_text)
            pos = end
        else:
            pos += 1
    else:
        pos += 1

# Check each
unchanged = []
for rt in recipes:
    rid = extract_field(rt, 'id') or 'unknown'
    rname = extract_field(rt, 'name') or 'Unknown'
    rtype = extract_field(rt, 'type') or 'espresso'
    steps_arr = extract_field(rt, 'steps')
    if not steps_arr:
        unchanged.append((rid, rname, "NO STEPS"))
        continue
    
    old_steps = parse_array_strings(steps_arr)
    all_str = " | ".join(old_steps)
    
    any_changed = False
    for step in old_steps:
        new_step = transform_step(step, rtype, rname, rid, all_str)
        if new_step != step:
            any_changed = True
            break
    
    if not any_changed:
        unchanged.append((rid, rname, rtype))

print(f"Unchanged recipes: {len(unchanged)}")
for rid, rname, rtype in unchanged:
    print(f"  {rid}: {rname} (type={rtype})")
