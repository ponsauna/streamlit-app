import streamlit as st
import requests
from bs4 import BeautifulSoup
def split_into_blocks(text, block_size=1800, separator="＋＋＋＋＋＋＋"):
    blocks = []
    start = 0
    while start < len(text):
        end = start + block_size
        if end > len(text):
            end = len(text)
        blocks.append(text[start:end])
        start = end
    return separator.join(blocks)
def scrape_and_process(base_url, pages=5):
    all_results = []
    for page in range(1, pages + 1):
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        text_elements = soup.find_all('p', class_='p-postCard_text')
        results = []
        for elem in text_elements:
            text_content = ''.join(elem.stripped_strings)
            results.append(text_content)
        combined_results = ''.join(results)
        blocked_results = split_into_blocks(combined_results)
        all_results.append(blocked_results)
    return all_results

st.title('Sauna Reviews Scraper')
base_url = st.text_input('Enter the base URL:', 'https://sauna-ikitai.com/saunas/80262/posts?page={}')
pages = st.number_input('Enter the number of pages to scrape:', min_value=1, value=5)

if st.button('Submit'):
    if base_url:
        results = scrape_and_process(base_url, int(pages))
        for i, result in enumerate(results, start=1):
            st.subheader(f'Page {i}')
            st.text_area('Scraped Data:', result, height=300, key=f"result_{i}")
    else:
        st.error('Please enter a valid URL')
