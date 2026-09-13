from pathlib import Path
import concurrent.futures, json, requests, re, datetime
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent

def fetch(job):
    result = dict(job)
    try:
        r = requests.get(job['url'], timeout=35, headers={'User-Agent': 'Mozilla/5.0'})
        result.update(status=r.status_code, final_url=r.url, retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
        (ROOT/'sources'/(job['slug']+'.html')).write_text(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        result['title'] = soup.title.get_text(' ', strip=True) if soup.title else ''
        for tag in soup(['script','style','noscript','svg']): tag.decompose()
        lines = [re.sub(r'\s+', ' ', x).strip() for x in soup.get_text('\n', strip=True).splitlines()]
        text = '\n'.join(x for x in lines if x)
        (ROOT/'sources'/(job['slug']+'.txt')).write_text(text)
        result['words'] = len(text.split())
        result['headings'] = [x.get_text(' ',strip=True) for x in soup.find_all(['h1','h2','h3'])]
    except Exception as e:
        result['error'] = str(e)
    (ROOT/'sources'/(job['slug']+'-receipt.json')).write_text(json.dumps(result,indent=2))
    print(job['slug'], result.get('status'), result.get('words'), result.get('error','')[:100], flush=True)
    return result

if __name__ == '__main__':
    jobs = json.loads((ROOT/'page-jobs.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        result = list(pool.map(fetch, jobs))
    (ROOT/'page-receipts.json').write_text(json.dumps(result,indent=2))
