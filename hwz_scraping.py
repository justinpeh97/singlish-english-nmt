from bs4 import BeautifulSoup
from requests import get
import re
import argparse
import time
import random
import concurrent.futures
from helper_functions import clean_comments_hwz, custom_splitting, convert_to_sentences, percentage_alphabets, filter_sentences

def obtain_threads(url, num_threads):
    print("Start - Scraping URLS of threads of interest")
    start_time = time.time()
    all_threads = []
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    max_pages = obtain_max_pages(html_soup)
    max_pages = int(max_pages)
    summary = html_soup.find_all('div', class_="structItem-title")
    if num_threads is None:
        num_pages = max_pages + 1
    else:
        num_pages = int((num_threads // 20 ) + 1) + 1
    urls = [url + "/page-" +  str(page) for page in range(1,num_pages)]
    
    def scrape_forum_page(url):
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        summary = html_soup.find_all('div', class_="structItem-title")
        for article in summary:
            thread_url = "https://forums.hardwarezone.com.sg"+article.find('a')['href']
            all_threads.append(thread_url)
        return

    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(scrape_forum_page, url): url for url in urls}
        completed = 0
        for future in concurrent.futures.as_completed(future_to_url):
            completed += 1
            if completed % 100 == 0:
                print("Progress:", completed * 100 / num_pages, "%")

    print("Completed - Scraped URLs of threads of interest")
    print("Time taken:", time.time() - start_time)

    return list(dict.fromkeys(all_threads))[:num_threads]



def obtain_max_pages(html_soup):
    page_nums = html_soup.find_all('ul', class_ = 'pageNav-main')
    if page_nums == []:
        return 1
    else:
        return page_nums[0].find_all('li')[-1].text

def scrape_hwz(threads, max_per_thread, output):
    print("Scraping replies")
    textfile = open(output, "w", encoding='utf-8')
    start = time.time()
    def comments_from_thread(url, max_per_thread):
        #print(url)
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        max_pages = obtain_max_pages(html_soup) if int(obtain_max_pages(html_soup)) < max_per_thread // 20 else max_per_thread // 20
        pages = [url + "page-" + str(page) for page in range(1, int(max_pages)+1)]
        for page in pages:
            response = get(page)
            html_soup = BeautifulSoup(response.text,'html.parser')
            for soup in html_soup.find_all("div", class_ = "bbWrapper"):
                comment = soup.text
                comment = re.sub('[\n|\t]+',".",comment)
                #textfile.write(comment + "\n")
                comments_cleaned = clean_comments_hwz([comment])
                sentences = convert_to_sentences(comments_cleaned)
                cleaned_sentences = filter_sentences(sentences)
                for sentence in cleaned_sentences:
                    textfile.write(sentence + "\n")
        return 
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(comments_from_thread, thread, max_per_thread): thread for thread in threads}
        completed = 0
        for future in concurrent.futures.as_completed(future_to_url):
            completed += 1
            if completed % 100 == 0:
                print("Progress:", completed * 100 / len(threads), "%")

    print("Time taken:", time.time() - start)




def main():
    parser = argparse.ArgumentParser(description = "Inputs to HWZ Scraper")
    parser.add_argument('--num_threads', type=int, default = None, help='Number of threads to scrape')
    parser.add_argument('--max-per-thread', type=int, default = 500000000, help='maximum number of comments from each thread')
    parser.add_argument('--thread', type=str, default = "https://forums.hardwarezone.com.sg/forums/eat-drink-man-woman.16", help = "thread to scrape")
    parser.add_argument('--output', type=str, default = "datasets/raw/raw_singlish.txt", help = "name of output  file")

    args = parser.parse_args()

    threads = obtain_threads(args.thread,args.num_threads)
    scrape_hwz(threads, args.max_per_thread, args.output)

       

if __name__ == '__main__':
    main()

