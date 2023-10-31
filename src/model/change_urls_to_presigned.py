from bs4 import BeautifulSoup, Doctype
import os

class change_urls_to_presigned:
    def change_html_links(self, html_content, UUID, aws_bucket, s3):
        soup = BeautifulSoup(html_content, 'html.parser')
        base_s3_directory = f"book/{UUID}/"
        
        if soup.find('doctype') is None:
            soup.insert(0, Doctype('html'))

        for tag in soup.find_all('img', src=True):
            tag['src'] = self.generate_presigned_url_for_path(tag['src'], base_s3_directory, aws_bucket, s3)

        for tag in soup.find_all('a', href=True):
            if tag['href'].startswith('#'):
                continue
            if not ("://" in tag['href'] or tag['href'].startswith("/")):
                tag['href'] = self.generate_presigned_url_for_path(tag['href'], base_s3_directory, aws_bucket, s3)

        for tag in soup.find_all('link', href=True):
            if 'stylesheet' in tag.get('rel', []):
                tag['href'] = self.generate_presigned_url_for_path(tag['href'], base_s3_directory, aws_bucket, s3)

        for tag in soup.find_all('script', src=True):
            tag['src'] = self.generate_presigned_url_for_path(tag['src'], base_s3_directory, aws_bucket, s3)

        for tag in soup.find_all('image', {'xlink:href': True}):
            tag['xlink:href'] = self.generate_presigned_url_for_path(tag['xlink:href'], base_s3_directory, aws_bucket, s3)
            
        return str(soup)
            
    def generate_presigned_url_for_path(self, link_path, base_s3_directory, aws_bucket, s3):
        if "://" in link_path:
            return link_path

        s3_key = os.path.join(base_s3_directory, link_path)
        presigned_url = self.generate_presigned_url(aws_bucket, s3_key, s3)

        return presigned_url if presigned_url else link_path
    
    def generate_presigned_url(self, aws_bucket, object_name, s3, expiration=3600):
        try:
            response = s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': aws_bucket, 'Key': object_name},
                                                        ExpiresIn=expiration)
        except Exception as e:
            print(e)
            return None
        return response