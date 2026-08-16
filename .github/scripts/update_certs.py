import urllib.request
import json
import re
import sys

url = "https://www.credly.com/users/kauemb/badges.json"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

rows_html = ""
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        badges = data.get("data", [])
        
        for badge in badges:
            badge_id = badge.get("id")
            badge_url = f"https://www.credly.com/badge/{badge_id}"
            image_url = badge.get("image_url", "")
            title = badge.get("badge_template", {}).get("name", "")
            description = badge.get("badge_template", {}).get("description", "")
            description_clean = description.replace("\n", " ").strip() if description else ""

            rows_html += f"""      <tr>
         <td align="center"><a href="{badge_url}" target="_blank"><img width="150" src="{image_url}"/></a></td>
         <td>{title}</td>
         <td>{description_clean}</td>
      </tr>\n"""
except Exception as e:
    print(f"Erro ao buscar badges: {e}")
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_table = f"""<!-- certs_start -->
<div class="certifications">
   <h4><b>As certificacoes que obtive:</b></h4>
   <table>
      <tr align="center">
         <th>Badge</th>
         <th>Nome da Certificacao</th>
         <th>Descricao Resumida</th>
      </tr>
{rows_html}   </table>
   <br>
</div>
<!-- certs_end -->"""

new_content = re.sub(r"<!-- certs_start -->.*?<!-- certs_end -->", new_table, content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)