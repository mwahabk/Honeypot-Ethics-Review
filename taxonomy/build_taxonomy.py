"""Build taxonomy.sqlite: honeypot ethics taxonomy (stages x categories x risks) linked to the
codebook, the final open coding (papers and tool documentation) and dataset v3.1.

Usage: python build_taxonomy.py --codebook codebook.csv --dataset honeypot_ethics_dataset.csv \
       --papers scientific-pdf-coding-final-2026-11-16.sqlite3 --tools ns-tool-documentation-final-2026-11-16.sqlite3 \
       --out taxonomy.sqlite
"""
import argparse, csv, re, sqlite3, html, os
from taxonomy_content import STAGES, CATEGORIES, RISKS, CONTEXT_CODES

SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE stage(id TEXT PRIMARY KEY, name TEXT, description TEXT, ord INTEGER);
CREATE TABLE category(id TEXT PRIMARY KEY, name TEXT, description TEXT, ord INTEGER);
CREATE TABLE risk(id TEXT PRIMARY KEY, category_id TEXT REFERENCES category(id), name TEXT, definition TEXT,
                  manifestation TEXT, tradeoff TEXT, indicator TEXT,
                  papers_affected INTEGER, tools_affected INTEGER, papers_evidence INTEGER, tools_evidence INTEGER, ord INTEGER);
CREATE TABLE risk_stage(risk_id TEXT REFERENCES risk(id), stage_id TEXT REFERENCES stage(id), PRIMARY KEY(risk_id, stage_id));
CREATE TABLE mitigation(id TEXT PRIMARY KEY, risk_id TEXT REFERENCES risk(id), text TEXT, ord INTEGER);
CREATE TABLE code(name TEXT PRIMARY KEY, description TEXT, example TEXT, kind TEXT);
CREATE TABLE risk_code(risk_id TEXT REFERENCES risk(id), code TEXT REFERENCES code(name), PRIMARY KEY(risk_id, code));
CREATE TABLE entry(id INTEGER PRIMARY KEY, source_type TEXT, identifier TEXT, domain TEXT, deployment TEXT, data_sensitivity TEXT, link TEXT);
CREATE TABLE evidence(id INTEGER PRIMARY KEY, entry_id INTEGER REFERENCES entry(id), document TEXT, code TEXT REFERENCES code(name), quote TEXT);
CREATE TABLE risk_entry(risk_id TEXT REFERENCES risk(id), entry_id INTEGER REFERENCES entry(id), PRIMARY KEY(risk_id, entry_id));
CREATE INDEX ev_code ON evidence(code);
CREATE INDEX ev_entry ON evidence(entry_id);
"""

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def main(a):
    book = list(csv.DictReader(open(a.codebook, encoding='utf-8-sig')))
    names = {r['tag'] for r in book}
    mapped = {c for r in RISKS for c in r['codes']} | set(CONTEXT_CODES)
    assert names == mapped, f'codebook vs taxonomy mismatch: {names ^ mapped}'
    rows = list(csv.DictReader(open(a.dataset, encoding='utf-8-sig')))
    assert len(rows) == 239 and 'source_type' in rows[0], 'expected the unified 239-row dataset'

    if os.path.exists(a.out): os.remove(a.out)
    db = sqlite3.connect(a.out); db.executescript(SCHEMA)
    db.executemany('INSERT INTO meta VALUES (?,?)', [('version', '0.1 (basic)'), ('built', __import__('datetime').date.today().isoformat()),
                   ('sources', 'codebook (69 codes); final open coding 2026-11-16 (38 papers, 201 tools); dataset v3.1 (239 entries)')])
    db.executemany('INSERT INTO stage VALUES (?,?,?,?)', [(i, n, d, k) for k, (i, n, d) in enumerate(STAGES)])
    db.executemany('INSERT INTO category VALUES (?,?,?,?)', [(i, n, d, k) for k, (i, n, d) in enumerate(CATEGORIES)])
    db.executemany('INSERT INTO code VALUES (?,?,?,?)', [(r['tag'], r['description'], r.get('example', ''), 'context' if r['tag'] in CONTEXT_CODES else 'risk') for r in book])

    # entries: dataset rows (id = row number), with a lookup by identifier for coding documents
    ent = {}
    for i, r in enumerate(rows, start=1):
        db.execute('INSERT INTO entry VALUES (?,?,?,?,?,?,?)', (i, r['source_type'], r['identifier'].strip(), r['domain'], r['deployment'], r['data_sensitivity'], r['link']))
        ent[r['identifier'].strip()] = i
    sci_ids = [i for i, r in enumerate(rows, start=1) if r['source_type'] == 'Scientific']

    # evidence from both coding projects
    def load(path, to_entry):
        c = sqlite3.connect(path); n = 0
        q = '''select d.name, d.contents, t.path, h.snippet from highlights h join documents d on d.id=h.document_id
               join highlight_tags ht on ht.highlight_id=h.id join tags t on t.id=ht.tag_id order by d.name, h.start_offset'''
        for doc, contents, tag, snip in c.execute(q):
            eid = to_entry(doc, contents)
            db.execute('INSERT INTO evidence(entry_id, document, code, quote) VALUES (?,?,?,?)', (eid, doc, tag, clean(snip))); n += 1
        return n
    n1 = load(a.papers, lambda doc, _: sci_ids[int(doc[4:7]) - 1])
    def tool_entry(doc, contents):
        ident = clean(re.search(r'NAME / IDENTIFIER: ([^<]*)<', contents).group(1))
        return ent[ident]
    n2 = load(a.tools, tool_entry)

    # risks
    for k, r in enumerate(RISKS):
        ind = r['indicator']
        pa = ta = None
        if ind:
            hits = []
            for i, row in enumerate(rows, start=1):
                low = {c: (row[c] or '').strip().lower() for c in row}
                low['sens_head'] = low['data_sensitivity_justification'].split('[earlier value')[0].split('. attacker behaviour')[0]
                if row['data_sensitivity'] == 'Not available' and 'sens_head' in ind: continue
                if eval(ind[1], {}, {'r': low}): hits.append((i, row['source_type']))
            db.executemany('INSERT INTO risk_entry VALUES (?,?)', [(r['id'], i) for i, _ in hits])
            pa = sum(1 for _, s in hits if s == 'Scientific'); ta = sum(1 for _, s in hits if s != 'Scientific')
        qm = ','.join('?' * len(r['codes']))
        pe, te = db.execute(f"""select count(distinct case when e.source_type='Scientific' then v.entry_id end),
                                       count(distinct case when e.source_type!='Scientific' then v.entry_id end)
                                from evidence v join entry e on e.id=v.entry_id where v.code in ({qm})""", r['codes']).fetchone()
        db.execute('INSERT INTO risk VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (r['id'], r['cat'], r['name'], r['definition'], r['manifestation'],
                   r['tradeoff'], ind[0] if ind else None, pa, ta, pe, te, k))
        db.executemany('INSERT INTO risk_stage VALUES (?,?)', [(r['id'], s) for s in r['stages']])
        db.executemany('INSERT INTO risk_code VALUES (?,?)', [(r['id'], c) for c in r['codes']])
        db.executemany('INSERT INTO mitigation VALUES (?,?,?,?)', [(f"{r['id']}-M{j+1}", r['id'], m, j) for j, m in enumerate(r['mitigations'])])
    db.commit()
    items = sum(db.execute(f'select count(*) from {t}').fetchone()[0] for t in ('stage', 'category', 'risk', 'mitigation'))
    print(f'taxonomy items: {items} (stages {len(STAGES)}, categories {len(CATEGORIES)}, risks {len(RISKS)}, mitigations {items-len(STAGES)-len(CATEGORIES)-len(RISKS)})')
    print(f'evidence quotes: papers {n1}, tools {n2}; entries {len(rows)}')
    db.execute('vacuum'); db.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--codebook', default='codebook.csv'); p.add_argument('--dataset', default='honeypot_ethics_dataset.csv')
    p.add_argument('--papers', default='scientific-pdf-coding-final-2026-11-16.sqlite3')
    p.add_argument('--tools', default='ns-tool-documentation-final-2026-11-16.sqlite3'); p.add_argument('--out', default='taxonomy.sqlite')
    main(p.parse_args())
