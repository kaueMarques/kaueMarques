import urllib.request
import json
import re
import sys
from html.parser import HTMLParser

class BlogHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.posts = []
        self.in_cactus_link = False
        self.current_url = ""
        self.current_title = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attr_dict = dict(attrs)
            href = attr_dict.get('href', '')
            # Identifica links de posts do blog
            if '/posts/' in href and href != '/posts/':
                self.in_cactus_link = True
                self.current_url = href if href.startswith('http') else 'https://kauemarques.github.io' + href

    def handle_data(self, data):
        if self.in_cactus_link:
            self.current_title += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.in_cactus_link:
            title = self.current_title.strip()
            if self.current_url and title:
                # Evita duplicados e adiciona a lista
                if not any(p['url'] == self.current_url for p in self.posts):
                    self.posts.append({'url': self.current_url, 'title': title})
            self.in_cactus_link = False
            self.current_title = ""

try:
    oracle_badge = """      <tr>
         <td align="center"><a href="https://catalog-education.oracle.com/pls/certview/sharebadge?id=F2D2C0108FD8BBAF39FD4E4E3E3F336B015C9653C255A1BE722FD22105F793C4" target="_blank"><img width="150" src="https://brm-workforce.oracle.com/pdf/certview/images/badge_icons/oci_foundations_assoc.png"/></a></td>
         <td>Oracle Cloud Infrastructure Foundations 2021 Associate</td>
         <td>Certificacao baseada em implementacao de ecossistema na nuvem.</td>
      </tr>\n"""

    url_credly = "https://www.credly.com/users/kauemb/badges.json"
    url_profile = "https://www.credly.com/users/kauemb"
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
            rows_certs += f'      <tr><td align="center"><a href="{url_profile}" target="_blank"><img width="150" src="{img}"/></a></td><td>{name}</td><td>{desc}</td></tr>\n'
    
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

    # Le a pagina de posts do blog
    url_posts = "https://kauemarques.github.io/posts/"
    req_posts = urllib.request.Request(url_posts, headers={"User-Agent": "Mozilla/5.0"})
    
    posts_html = "<ul>\n"
    try:
        with urllib.request.urlopen(req_posts) as response:
            html_content = response.read().decode('utf-8')
            parser = BlogHTMLParser()
            parser.feed(html_content)
            
            # Pega os 3 primeiros posts listados na pagina
            top_posts = parser.posts[:3]
            
            if top_posts:
                for post in top_posts:
                    posts_html += f'      <li><a href="{post["url"]}" target="_blank">{post["title"]}</a></li>\n'
            else:
                posts_html += '      <li>Nenhum post encontrado no momento.</li>\n'
    except Exception as e:
        posts_html += '      <li>Nao foi possivel carregar os posts no momento.</li>\n'
    
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