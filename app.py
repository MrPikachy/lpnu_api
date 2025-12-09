from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

app = Flask(__name__)


# --- MAIN PAGE (Documentation Landing) ---
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LPNU Schedule API</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #333; }
            .badge { background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>LPNU Schedule API</h1>
        <p><span class="badge">Public API</span> <span class="badge">Open Access</span></p>

        <p><strong>Host:</strong> lpnu-api-py6o.onrender.com</p>
        <p>This is a public API designed to retrieve schedule data from the Lviv Polytechnic National University student portal.</p>

        <h3>Documentation & Spec</h3>
        <ul>
            <li><a href="/docs/">Interactive Documentation (ReDoc)</a></li>
            <li><a href="/openapi.json">OpenAPI Specification (JSON)</a></li>
            <li><a href="/openapi.yaml">OpenAPI Specification (YAML)</a></li>
        </ul>

        <h3>Usage Example</h3>
        <code>GET /api/schedule?group=KN-101</code>
    </body>
    </html>
    """


# --- PARSING FUNCTION ---
def parse_html_schedule(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    schedule = []
    lesson_times_map = {
        '1': ('08:30', '10:05'), '2': ('10:20', '11:55'), '3': ('12:10', '13:45'),
        '4': ('14:15', '15:50'), '5': ('16:00', '17:35'), '6': ('17:40', '19:15'),
        '7': ('19:20', '20:55'), '8': ('21:00', '22:35')
    }
    content_div = soup.find('div', {'class': 'view-content'})
    if not content_div:
        return []

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
                if not parts:
                    continue

                subject = parts[0]
                text_lower = full_text.lower()
                subgroup = 0
                if 'sub_1' in elem_id:
                    subgroup = 1
                elif 'sub_2' in elem_id:
                    subgroup = 2

                week_type = 'обидва'
                if 'chys' in elem_id:
                    week_type = 'чисельник'
                elif 'znam' in elem_id:
                    week_type = 'знаменник'

                subject_type = 'Інше'
                if 'лекц' in text_lower:
                    subject_type = 'Лекція'
                elif 'практ' in text_lower:
                    subject_type = 'Практична'
                elif 'лаб' in text_lower:
                    subject_type = 'Лабораторна'
                elif 'екзам' in text_lower:
                    subject_type = 'Екзамен'

                location = ''
                for p in parts:
                    if any(x in p.lower() for x in ['н.к.', 'корп', 'ауд']):
                        location = p
                        break

                start_t, end_t = lesson_times_map.get(current_lesson_num, ('00:00', '00:00'))
                schedule.append({
                    'weekday': current_weekday,
                    'start_time': start_t,
                    'end_time': end_t,
                    'subject': subject,
                    'subject_type': subject_type,
                    'location': location,
                    'subgroup': subgroup,
                    'week_type': week_type
                })
    return schedule


# --- API ENDPOINT: /api/schedule ---
@app.route('/api/schedule')
def get_schedule():
    group = request.args.get('group')
    if not group:
        return jsonify({"error": "Missing 'group' parameter"}), 400

    try:
        encoded_group = urllib.parse.quote(group.strip())
        url = f"https://student.lpnu.ua/students_schedule?studygroup_abbrname={encoded_group}&semestr=1"

        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code != 200:
            return jsonify({"error": "LPNU site unavailable"}), 502

        data = parse_html_schedule(r.text)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- DOCS ROUTES ---
def _docs_dir():
    return os.path.join(app.root_path, 'docs')


@app.route('/openapi.yaml')
def openapi_yaml():
    docs_dir = _docs_dir()
    if not os.path.exists(os.path.join(docs_dir, 'openapi.yaml')):
        return "OpenAPI YAML not found.", 404
    return send_from_directory(docs_dir, 'openapi.yaml')


@app.route('/openapi.json')
def openapi_json():
    docs_dir = _docs_dir()
    if not os.path.exists(os.path.join(docs_dir, 'openapi.json')):
        return "OpenAPI JSON not found.", 404
    return send_from_directory(docs_dir, 'openapi.json')


@app.route('/docs/')
def redoc_ui():
    return render_template('redoc.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))