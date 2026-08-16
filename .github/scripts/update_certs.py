import urllib.request
import json
import re
import sys

try:
    oracle_badge = """      <tr>
         <td align="center"><a href="https://catalog-education.oracle.com/pls/certview/sharebadge?id=F2D2C0108FD8BBAF39FD4E4E3E3F336B015C9653C255A1BE722FD22105F793C4" target="_blank"><img width="150" src="https://brm-workforce.oracle.com/pdf/certview/images/badge_icons/oci_foundations_assoc.png"/></a></td>
         <td>Oracle Cloud Infrastructure Foundations 2021 Associate</td>
         <td>Certificacao baseada em implementacao de infraestrutura de ecossistema na nuvem.</td>
      </tr>\n"""

    url_credly = "https://www.credly.com/users/kauemb/badges.json"
    req_credly = urllib.request.Request(url_credly, headers={"User-Agent": "Mozilla/5.0"})
    
    rows_certs = oracle_badge
    with urllib.request.urlopen(req_credly) as response:
        data_credly = json.loads(response.read().decode())
        badges = data_credly.get("data", [])
        for b in badges:
            url_b = "https://www.credly.com/badge/" + b.get("id", "")
            img = b.get("image_url", "")
            name = b.get("badge_template", {}).get("name", "")
            desc = b.get("badge_template", {}).get("description", "")
            if desc:
                desc = desc.replace("\n", " ").strip()
            rows_certs += f'      <tr><td align="center"><a href="{url_b}" target="_blank"><img width="150" src="{img}"/></a></td><td>{name}</td><td>{desc}</td></tr>\n'
    
    table_certs = f"""<!-- certs_start -->
<div class="certifications">
   <h4><b>As certificacoes que obtive:</b></h4>
   <table>
      <tr align="center">
         <th>Badge</th>
         <th>Nome da Certificacao</th>
         <th>Descricao Resumida</th>
      </tr>
{rows_certs}   </table>
   <br>
</div>
<!-- certs_end -->"""

    # Busca os arquivos na pasta de posts do repositorio do blog via API do GitHub
    url_api = "https://api.github.com/repos/kaueMarques/kauemarques.github.io/contents/src/content/post"
    req_api = urllib.request.Request(url_api, headers={"User-Agent": "Mozilla/5.0"})
    
    posts_html = "<ul>\n"
    try:
        with urllib.request.urlopen(req_api) as response:
            files_data = json.loads(response.read().decode())
            
            post_ids = []
            for file_item in files_data:
                filename = file_item.get("name", "")
                # Procura por padroes como postid-113 ou similar no nome do arquivo ou diretorio
                match = re.search(r'(\d+)', filename)
                if match:
                    post_ids.append(int(match.group(1)))
            
            # Ordena do maior para o menor e pega os 3 primeiros
            post_ids = sorted(list(set(post_ids)), reverse=True)[:3]
            
            for pid in post_ids:
                post_url = f"https://kauemarques.github.io/posts/postid-{pid}/"
                posts_html += f'      <li><a href="{post_url}" target="_blank">Post ID {pid}</a></li>\n'
    except Exception as e:
        posts_html += f'      <li>Nao foi possivel carregar os posts no momento.</li>\n'
    
    posts_html += "   </ul>"

    table_posts = f"""<!-- posts_start -->
<div class="recent-posts">
   <h4><b>Ultimos posts no meu blog:</b></h4>
{posts_html}
</div>
<!-- posts_end -->"""

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    content = re.sub(r"<!-- certs_start -->.*?<!-- certs_end -->", table_certs, content, flags=re.DOTALL)
    content = re.sub(r"<!-- posts_start -->.*?<!-- posts_end -->", table_posts, content, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

except Exception as e:
    print("Erro:", e)
    sys.exit(1)