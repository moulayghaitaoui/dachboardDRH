import re

with open('sdp.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find <script> tags that contain "new Chart" but NOT "DOMContentLoaded"
script_patt = re.compile(r'<script>(?!.*?DOMContentLoaded).*?new Chart\(.*?</script>', re.DOTALL)

def wrap_script(match):
    script_inner = match.group(0).replace('<script>', '').replace('</script>', '').strip()
    return f"<script>\n    document.addEventListener('DOMContentLoaded', function() {{\n        {script_inner}\n    }});\n</script>"

# Apply wrapping to all matching scripts
new_content = script_patt.sub(wrap_script, content)

if new_content != content:
    with open('sdp.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Wrapped charts in DOMContentLoaded")
else:
    print("No charts needed wrapping or already wrapped")

