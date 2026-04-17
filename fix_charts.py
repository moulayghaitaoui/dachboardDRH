import re

with open('sdp.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Identify and extract the wilayaChart script
# It's currently between lines 1930 and 1976 in the file I just saw
# Look for: <script>\s+const ctx = document.getElementById('wilayaChart') ... </script>

wilaya_script_pattern = re.compile(r'<script>\s+const ctx = document\.getElementById\(\'wilayaChart\'\)\.getContext\(\'2d\'\);.*?new Chart\(ctx, \{.*?\}\);\s+</script>', re.DOTALL)
match = wilaya_script_pattern.search(content)

if match:
    wilaya_script = match.group(0)
    # Remove it from its current position
    content = content.replace(wilaya_script, '')
    
    # Wrap it in DOMContentLoaded and put it after its canvas (id="wilayaChart")
    canvas_str = '<canvas id="wilayaChart"></canvas>'
    insert_pos = content.find(canvas_str)
    if insert_pos != -1:
        # Find the end of the div containing the canvas
        div_end = content.find('</div>', insert_pos)
        insert_after_div = div_end + 6
        
        # Prepare wrapped script
        wrapped_script = "\n    <script>\n        document.addEventListener('DOMContentLoaded', function() {\n            " + wilaya_script.replace('<script>', '').replace('</script>', '').strip() + "\n        });\n    </script>"
        
        content = content[:insert_after_div] + wrapped_script + content[insert_after_div:]
        print("Moved and wrapped wilayaChart script")
    else:
        print("Could not find wilayaChart canvas")
else:
    print("Could not find wilayaChart script")

# 2. Wrap responseChart and decisionChart script in DOMContentLoaded as well to be safe
# These are near lines 1997 and 2041

response_script_pattern = re.compile(r'<script>\s+const ctx2 = document\.getElementById\(\'responseChart\'\)\.getContext\(\'2d\'\);.*?new Chart\(ctx2, \{.*?\}\);\s+</script>', re.DOTALL)
match2 = response_script_pattern.search(content)
if match2:
    resp_script = match2.group(0)
    wrapped_resp = "<script>\n        document.addEventListener('DOMContentLoaded', function() {\n            " + resp_script.replace('<script>', '').replace('</script>', '').strip() + "\n        });\n    </script>"
    content = content.replace(resp_script, wrapped_resp)
    print("Wrapped responseChart script")

decision_script_pattern = re.compile(r'<script>\s+const ctx3 = document\.getElementById\(\'decisionChart\'\)\.getContext\(\'2d\'\);.*?new Chart\(ctx3, \{.*?\}\);\s+</script>', re.DOTALL)
match3 = decision_script_pattern.search(content)
if match3:
    dec_script = match3.group(0)
    wrapped_dec = "<script>\n        document.addEventListener('DOMContentLoaded', function() {\n            " + dec_script.replace('<script>', '').replace('</script>', '').strip() + "\n        });\n    </script>"
    content = content.replace(dec_script, wrapped_dec)
    print("Wrapped decisionChart script")

with open('sdp.html', 'w', encoding='utf-8') as f:
    f.write(content)

