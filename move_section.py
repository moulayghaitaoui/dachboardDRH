import re

with open('sdp.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the section to move
# It starts at "    <!-- وضعية الرخص الإستثنائية -->" 
# and ends right before "    <div class="panel" ... الحصيلة العددية للعرائض 2025"

start_idx = content.find('    <!-- وضعية الرخص الإستثنائية -->')
end_idx = content.find('    <div class="panel"\n        style="margin-top:30px; margin-bottom:20px; background: linear-gradient(135deg, #185FA5, #2980b9); border-radius:12px; text-align:center;">\n        <h2 style="color:#fff; font-size:24px; border:none; padding:15px 0; margin:0; letter-spacing:1px;">الحصيلة\n            العددية للعرائض 2025</h2>')

if start_idx != -1 and end_idx != -1:
    section_to_move = content[start_idx:end_idx]
    
    # Remove it from its current position
    content = content[:start_idx] + content[end_idx:]
    
    # Now find where to insert it: right before "الإحصاء الكلي لحالات الوضع تحت التصرف داخل الولاية وخارجها"
    # Actually, look for the panel containing the title "الإحصاء الكلي لحالات الوضع تحت التصرف داخل الولاية وخارجها"
    
    target_idx = content.find('    <div class="panel"\n        style="margin-bottom:20px; background: linear-gradient(135deg, #185FA5, #2980b9); border-radius:12px; text-align:center;">\n        <h2 style="color:#fff; font-size:22px; border:none; padding:15px 0; margin:0; letter-spacing:1px;">الإحصاء الكلي\n            لحالات الوضع تحت التصرف داخل الولاية وخارجها</h2>')

    if target_idx != -1:
        content = content[:target_idx] + section_to_move + content[target_idx:]
        
        with open('sdp.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success")
    else:
        print("Could not find Target index")
else:
    print("Could not find start or end index for the section to move")

