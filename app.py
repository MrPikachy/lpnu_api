from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)


@app.route('/')
def documentation():
    return """
    <h1>LPNU Schedule API</h1>
    <p>This is a public API for retrieving schedule data.</p>
    <p><strong>Hostname:</strong> lpnu-api-py6o.onrender.com</p>
    <p><strong>Status:</strong> Open to the public.</p>
    <p>Documentation endpoint required for PythonAnywhere allowlist.</p>
    """
    
# --- ФУНКЦІЯ ПАРСИНГУ ---
def parse_html_schedule(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    schedule = []
    lesson_times_map = {
        '1': ('08:30', '10:05'), '2': ('10:20', '11:55'), '3': ('12:10', '13:45'),
        '4': ('14:15', '15:50'), '5': ('16:00', '17:35'), '6': ('17:40', '19:15'),
        '7': ('19:20', '20:55'), '8': ('21:00', '22:35')
    }
    content_div = soup.find('div', {'class': 'view-content'})
    if not content_div: return []

    current_weekday = None
    current_lesson_num = "1"

    for element in content_div.find_all(recursive=False):
        if element.name == 'span' and 'view-grouping-header' in element.get('class', []):
            current_weekday = element.get_text(strip=True)
            continue
        if element.name == 'h3':
            current_lesson_num = element.get_text(strip=True)
            continue
        if element.name == 'div' and 'stud_schedule' in element.get('class', []):
            content_blocks = element.find_all('div', {'class': 'group_content'})
            for content_block in content_blocks:
                parent = content_block.find_parent('div', id=True)
                elem_id = parent.get('id', '') if parent else ''
                full_text = content_block.get_text(separator='|', strip=True)
                parts = [p.strip() for p in full_text.split('|') if p.strip()]
                if not parts: continue
                
                subject = parts[0]
                text_lower = full_text.lower()
                subgroup = 0
                if 'sub_1' in elem_id: subgroup = 1
                elif 'sub_2' in elem_id: subgroup = 2
                
                week_type = 'обидва'
                if 'chys' in elem_id: week_type = 'чисельник'
                elif 'znam' in elem_id: week_type = 'знаменник'
                
                subject_type = 'Інше'
                if 'лекц' in text_lower: subject_type = 'Лекція'
                elif 'практ' in text_lower: subject_type = 'Практична'
                elif 'лаб' in text_lower: subject_type = 'Лабораторна'
                elif 'екзам' in text_lower: subject_type = 'Екзамен'
                
                location = ''
                for p in parts:
                    if any(x in p.lower() for x in ['н.к.', 'корп', 'ауд']):
                        location = p
                        break
                
                start_t, end_t = lesson_times_map.get(current_lesson_num, ('00:00', '00:00'))
                schedule.append({
                    'weekday': current_weekday, 'start_time': start_t, 'end_time': end_t,
                    'subject': subject, 'subject_type': subject_type,
                    'location': location, 'subgroup': subgroup, 'week_type': week_type
                })
    return schedule

# --- API ---
@app.route('/')
def home():
    return jsonify({"status": "API is running. Use /api/schedule?group=GROUP_NAME"})

@app.route('/api/schedule')
def get_schedule():
    group = request.args.get('group')
    if not group:
        return jsonify({"error": "Missing 'group' parameter"}), 400
    
    try:
        import urllib.parse
        encoded_group = urllib.parse.quote(group.strip())
        url = f"https://student.lpnu.ua/students_schedule?studygroup_abbrname={encoded_group}&semestr=1"
        
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code != 200:
            return jsonify({"error": "LPNU site unavailable"}), 502
            
        data = parse_html_schedule(r.text)
        return jsonify(data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

