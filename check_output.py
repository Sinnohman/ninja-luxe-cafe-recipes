import re

with open('/root/ninja-luxe-cafe/index_new.html') as f:
    content = f.read()

# Check espresso recipe in detail
m = re.search(r"\{id:'espresso',name:'([^']+)'", content)
rname = m.group(1)
ridx = m.start()

# Find steps array
sm = re.search(r'steps:', content[ridx:ridx+800])
skw = ridx + sm.start()
bpos = content.find('[', skw)

# Find matching closing bracket
depth = 0; instring = False; esc = False; cpos = -1
for i in range(bpos, len(content)):
    c = content[i]
    if esc: esc = False; continue
    if c == '\\': esc = True; continue
    if c == "'" and not instring: instring = True; continue
    if c == "'" and instring: instring = False; continue
    if instring: continue
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0: cpos = i; break

raw = content[bpos:cpos+1]
print(f"Full steps ({len(raw)} chars):")
print(raw)
print()

# Now parse and count properly
def parse_steps(raw):
    inner = raw[1:-1]  # remove outer []
    steps = []
    current = ""
    instring = False
    esc = False
    i = 0
    while i < len(inner):
        c = inner[i]
        if esc:
            current += c
            esc = False
            i += 1
            continue
        if c == '\\':
            esc = True
            i += 1
            continue
        if c == "'" and not instring:
            instring = True
            i += 1
            continue
        if c == "'" and instring:
            instring = False
            steps.append(current)
            current = ""
            # skip to next quote or end
            j = i + 1
            while j < len(inner) and inner[j] in ' \t\n\r,':
                j += 1
            i = j
            continue
        if instring:
            current += c
        i += 1
    return steps

steps = parse_steps(raw)
print(f"\nParsed {len(steps)} steps:")
for i, s in enumerate(steps):
    print(f"  [{i}]: {s[:100]}")
