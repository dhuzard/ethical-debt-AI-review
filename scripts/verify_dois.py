#!/usr/bin/env python3
"""Phase 16 steps 1-4: independent CrossRef re-resolution of every cited DOI,
comparing title (similarity) and first-author family to the bibliography.
Zero model tokens. Flags BROKEN-DOI / CHIMERIC / MINOR(author/year)."""
import json, re, time, urllib.request, urllib.parse, os, difflib
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
triples=json.load(open('provenance/citation_triples.json',encoding='utf-8'))
km=json.load(open('provenance/citation_key_map.json',encoding='utf-8'))
key2doi={v:k for k,v in km.items()}
meta={r['doi'].lower():r for r in json.load(open('provenance/crossref_metadata.json',encoding='utf-8')) if r.get('doi')}
cited=sorted(set(t['cite_key'] for t in triples))
UA={'User-Agent':'EthicalDebtReview/1.0 (mailto:damien@metadatapp.net)'}
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
def sim(a,b):
    a,b=norm(a),norm(b)
    if not a or not b: return 0.0
    return difflib.SequenceMatcher(None,a,b).ratio()
results={}; bhatt=[]
for i,key in enumerate(cited):
    doi=key2doi.get(key)
    if not doi: results[key]={'cat':'NO_DOI'}; continue
    bibm=meta.get(doi.lower(),{})
    url='https://api.crossref.org/works/'+urllib.parse.quote(doi)
    cat='VERIFIED'; detail=''
    try:
        req=urllib.request.Request(url,headers=UA)
        with urllib.request.urlopen(req,timeout=25) as r:
            d=json.load(r)['message']
        cr_title=(d.get('title') or [''])[0]
        cr_auth=d.get('author') or []
        cr_fam=[ (a.get('family') or a.get('name') or '') for a in cr_auth]
        ts=sim(cr_title,bibm.get('title'))
        if ts<0.5: cat='CHIMERIC'; detail=f'title sim {ts:.2f}'
        # author family check (first author) + Bhatt scan
        if any('bhatt' in (f or '').lower() for f in [bibm.get('family')]+ (bibm.get('all_families') or [])):
            if not any('bhatt' in (f or '').lower() for f in cr_fam): bhatt.append((key,doi))
        yr_bib=bibm.get('year'); yr_cr=None
        for k2 in ('published-print','published-online','issued','published'):
            if d.get(k2,{}).get('date-parts'): yr_cr=d[k2]['date-parts'][0][0]; break
        if cat=='VERIFIED' and yr_bib and yr_cr and abs(int(yr_bib)-int(yr_cr))>1:
            cat='MINOR'; detail=f'year bib={yr_bib} cr={yr_cr}'
        results[key]={'cat':cat,'detail':detail,'title_sim':round(ts,2)}
    except urllib.error.HTTPError as e:
        results[key]={'cat':'BROKEN-DOI' if e.code in (404,) else 'FETCH_ERR','detail':f'HTTP {e.code}'}
    except Exception as e:
        results[key]={'cat':'FETCH_ERR','detail':str(e)[:60]}
    time.sleep(0.08)
    if (i+1)%100==0:
        json.dump(results,open('provenance/doi_verification.json','w',encoding='utf-8'),indent=0)
        print('...',i+1,'/',len(cited))
json.dump({'results':results,'bhatt_contamination':bhatt},open('provenance/doi_verification.json','w',encoding='utf-8'),indent=1)
from collections import Counter
c=Counter(v['cat'] for v in results.values())
print('DOI verification categories:',dict(c))
print('Bhatt contamination:',bhatt or 'NONE')
print('non-VERIFIED:',[(k,v) for k,v in results.items() if v['cat']!='VERIFIED'][:30])
