from bs4 import BeautifulSoup
import os

class HtmlConsolidator:
    def adjust_path(self, original_file_path, output_path, link_path):
        if "://" in link_path or link_path.startswith("/"):
            return link_path
        
        original_dir = os.path.dirname(original_file_path)
        full_path = os.path.normpath(os.path.join(original_dir, link_path))
        
        rel_path = os.path.relpath(full_path, os.path.dirname(output_path))
        
        return rel_path


    def generate_unique_id(self, file_path, original_id):
        base_name = file_path.split("/")[-1].replace(".html", "").replace(".xhtml", "")
        return f"{base_name}_{original_id}"

    def consolidate_html(self, file_paths, output_path):
        documents = []
        
        for path in file_paths:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                for link_tag in soup.find_all('link', {'rel': 'stylesheet', 'href': True}):
                    link_tag['href'] = self.adjust_path(path, output_path, link_tag['href'])
                
                for image_tag in soup.find_all('image', {'xlink:href': True}):
                    image_tag['xlink:href'] = self.adjust_path(path, output_path, image_tag['xlink:href'])
                
                documents.append(soup)

        included_stylesheets = set()
        for index, doc in enumerate(documents):
            for tag in doc.find_all(True):
                if tag.has_attr('id'):
                    tag['id'] = self.generate_unique_id(file_paths[index], tag['id'])
                
                if tag.name == 'a' and tag.has_attr('href'):
                    href = tag['href']
                    tag['href'] = self.adjust_path(file_paths[index], output_path, href)
                    
                    for path in file_paths:
                        if path.split("/")[-1] in href:
                            original_id = href.split("#")[-1] if "#" in href else ""
                            new_id = self.generate_unique_id(path, original_id)
                            tag['href'] = f"#{new_id}"
                            break
                
                if tag.name in ['img', 'script', 'link'] and tag.has_attr('src'):
                    tag['src'] = self.adjust_path(file_paths[index], output_path, tag['src'])
                if tag.name == 'link' and tag.has_attr('href'):
                    tag['href'] = self.adjust_path(file_paths[index], output_path, tag['href'])
                    
                if tag.name == 'link' and tag.has_attr('rel') and 'stylesheet' in tag['rel'] and tag['href'] not in included_stylesheets:
                    included_stylesheets.add(tag['href'])

        consolidated_soup = BeautifulSoup("<html><head></head><body></body></html>", 'html.parser')
        
        for stylesheet in included_stylesheets:
            link_tag = consolidated_soup.new_tag("link", rel="stylesheet", href=stylesheet)
            consolidated_soup.head.append(link_tag)

        body_contents = [doc.body for doc in documents]
        for content in body_contents:
            consolidated_soup.body.append(content)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(str(consolidated_soup))
