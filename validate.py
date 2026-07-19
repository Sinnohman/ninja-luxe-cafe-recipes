"""Validate the transformed output file."""
import re

with open('/root/ninja-luxe-cafe/index_new.html') as f:
    content = f.read()

# Count steps
steps_count = content.count('steps:')
print(f"Steps: count = {steps_count}")

# Count recipe objects
recipe_objects = len(re.findall(r"\{id:'[^']+',name:'[^']+',type:'", content))
print(f"Recipe objects (id+name+type): {recipe_objects}")

# Check for empty quote pairs in steps arrays
q = chr(39)
empty_pair_count = 0
# Find all steps arrays
pattern = re.compile(r"steps:\[")
for m in pattern.finditer(content):
    # Find matching ]
    depth = 0
    instring = False
    esc = False
    i = m.end() - 1  # at the [
    close = -1
    for j in range(i, len(content)):
        c = content[j]
        if esc: esc = False; continue
        if c == '\\': esc = True; continue
        if c == q and not instring: instring = True; continue
        if c == q and instring: instring = False; continue
        if instring: continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0: close = j; break
    if close > 0:
        arr = content[i:close+1]
        empties = arr.count(q+q)
        if empties > 0:
            empty_pair_count += empties
            # Find the recipe name for context
            before = content[max(0,i-300):i]
            name_m = re.search(r"name:'([^']+)'", before)
            rname = name_m.group(1) if name_m else 'unknown'
            print(f"  Found {empties} empty pairs in {rname}")

print(f"Total empty quote pairs in steps: {empty_pair_count}")

# Check script tag integrity
script_start = content.find('<script>')
script_end = content.find('</script>')
if script_start >= 0 and script_end >= 0:
    print(f"Script tag: OK (lines {content[:script_start].count(chr(10))} - {content[:script_end].count(chr(10))})")
else:
    print("Script tag: MISSING!")

# Check HTML structure
html_open = content.count('<html')
html_close = content.count('</html>')
print(f"HTML tags: {html_open} open, {html_close} close")

# Final verdict
if steps_count == 87 and empty_pair_count == 0 and html_open == 1 and html_close == 1:
    print("\n✓ FILE VALID")
else:
    print("\n✗ ISSUES FOUND")
    if steps_count != 87:
        print(f"  - Wrong steps count: {steps_count} (expected 87)")
    if empty_pair_count > 0:
        print(f"  - Empty quote pairs: {empty_pair_count}")
    if html_open != 1 or html_close != 1:
        print(f"  - HTML structure issue")
