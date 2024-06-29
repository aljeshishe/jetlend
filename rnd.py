import sys
import click
import requests
from pathlib import Path
import json
import shutil
from tqdm import tqdm
from loguru import logger

headers_str = """Host: jetlend.ru
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0
Accept: application/json, text/plain, */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Content-Type: application/json;charset=utf-8
Connection: keep-alive
Referer: https://jetlend.ru/invest/v3/company/21130/loans
Cookie: _jl_uid=vETZ4WYnngoGKbUsB0IrAg==; _ym_uid=165529886474569422; _ym_d=1713872395; _gcl_au=1.1.9203485.1713872396; referrer=direct; _ga_NR0DV46HQK=GS1.1.1719689231.3.1.1719689255.36.0.0; _ga=GA1.2.304190505.1713872396; tmr_lvid=cf3853f8e126ef5af0107ed27ea51ba8; tmr_lvidTS=1655298863696; csrftoken=I1jaiZNm2sNJOK1zXi6kPT2kTGURMyW3; _tt_enable_cookie=1; _ttp=edS85OjPAoMmLAmUhluSg2cXvwu; sessionid=8lle7p41yey6hlbtpe2th2jpmefm6hid; __cflb=02DiuGLLJyp3aE1Ak9tV66zwoNvVDYhPEmnER99e9bXSt; _ym_isad=1; _gid=GA1.2.1311683181.1719689232; domain_sid=FWuTlpmQMeoQsQ1bNrxdZ%3A1719689233254; tmr_detect=1%7C1719689256228
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=1
Pragma: no-cache
Cache-Control: no-cache
TE: trailers"""
import email
headers = email.message_from_string(headers_str)



OUTPUTS = Path("outputs")




def get(id: int):
    file = OUTPUTS / f"{id}.json"
    if file.exists():
        return
    
    url = f"https://jetlend.ru/invest/api/requests/{id}/loans"
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        data = dict(status="error", error=str(e))
    content = json.dumps(data, sort_keys=True, indent=4)
    file.write_text(content)



@click.command()
@click.option('-c', '--clean', default=False, is_flag=True, help='Clear outputs')
def main(clean):
    logger.remove()
    format = "{time:YYYY-MM-DD HH:mm:ss}|{name:10.10s}|{function:10.10s}|{level:4.4s}| {message}"
    logger.add(sys.stdout,  level='DEBUG', format=format)
    logger.add("log.log", level='DEBUG', format=format)
    logger.enable("")

    if clean and OUTPUTS.exists():
        shutil.rmtree(OUTPUTS)
    OUTPUTS.mkdir(exist_ok=True, parents=True)
    

    for i in tqdm(range(21200)):
        with logger.catch():
            get(i)


if __name__ == "__main__":
    main()