from bs4 import BeautifulSoup,Comment

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")

    for tag in soup(["script", "style", "noscript","iframe"]):
        tag.decompose()

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    cleaned_html = soup.prettify()
    return cleaned_html

