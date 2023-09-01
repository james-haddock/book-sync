from bs4 import BeautifulSoup

class Consolidator:
    def html(self, html_files: list, output_path: str):
        # Initialize an empty BeautifulSoup object to hold the consolidated HTML
        consolidated_soup = BeautifulSoup("<html><head></head><body></body></html>", "lxml")

        # A dictionary to map original file names to their new anchor names in the consolidated file
        file_to_anchor = {}

        # Loop through each HTML file and append its content to the consolidated_soup
        for idx, html_file in enumerate(html_files):
            with open(html_file, "r", encoding="utf-8") as f:
                file_content = f.read()
                file_soup = BeautifulSoup(file_content, "lxml")
                
                # Create an anchor to mark the beginning of this file's content
                anchor_name = f"page_{idx + 1}"
                anchor_tag = consolidated_soup.new_tag("a", id=anchor_name)
                
                # Map the original file name to the new anchor name
                file_to_anchor[html_file] = anchor_name

                # Append the anchor and the body content of each file to the consolidated_soup's body
                consolidated_soup.body.append(anchor_tag)
                for child in file_soup.body.children:
                    consolidated_soup.body.append(child)

        # Update all hyperlinks in the consolidated_soup to point to the new anchors
        for a_tag in consolidated_soup.find_all("a"):
            href = a_tag.get("href")
            if href and href in file_to_anchor:
                a_tag["href"] = f"#{file_to_anchor[href]}"

        # Write the consolidated HTML content to a new file
        with open(f"{output_path}/consolidated.html", "w", encoding="utf-8") as f:
            f.write(str(consolidated_soup))

# Example usage:
# html_files = ["file1.html", "file2.html"]
# output_path = "./output"
# consolidator = Consolidator()
# consolidator.html(html_files, output_path)
