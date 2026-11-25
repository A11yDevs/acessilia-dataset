#!/usr/bin/env python3
"""Validate case 006 annotations and the reproducible before/after report.

Run from any directory: python3 input/presentation-reference/validate.py
Uses only the Python standard library; does not process accessible outputs.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

FIELDS = ['id', 'manifest_id', 'page', 'kind', 'expected', 'context', 'notes']
KINDS = {'text', 'image', 'chemical-structure', 'formula', 'table',
         'table-header', 'table-row'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_csv(text):
    records = list(csv.reader(io.StringIO(text, newline=''), strict=True))
    require(bool(records) and records[0] == FIELDS, 'unexpected CSV header')
    require(all(len(row) == len(FIELDS) for row in records[1:]), 'CSV row width')
    return [dict(zip(FIELDS, row)) for row in records[1:]]


def validate(root):
    case = root / 'input/presentation-reference'
    rows = read_csv((case / 'ground_truth.csv').read_text(encoding='utf-8'))
    exp = json.loads((case / 'expectations.json').read_text(encoding='utf-8'),
                     object_pairs_hook=unique_keys)
    by = {row['id']: row for row in rows}
    require(len(by) == len(rows), 'duplicate annotation ID')
    require(exp['manifest_id'] == '006', 'JSON manifest ID')
    require(exp['structure']['slide_count'] == 42, 'slide count')
    require({int(r['page']) for r in rows} == set(range(1, 43)), 'page coverage')
    require([int(r['page']) for r in rows] == sorted(int(r['page']) for r in rows),
            'CSV page order')
    seen = set()
    for r in rows:
        require(r['manifest_id'] == '006', f"manifest ID: {r['id']}")
        require(re.fullmatch(r's\d{2}-(?:[xicf]\d{2}|t\d{2}(?:-(?:h|r\d{2}))?)', r['id']),
                f"ID syntax: {r['id']}")
        require(int(r['id'][1:3]) == int(r['page']), f"ID/page: {r['id']}")
        require(r['kind'] in KINDS, f"unsupported kind: {r['id']}")
        require(bool(r['expected'].strip()), f"empty expectation: {r['id']}")
        scope = r['id'].rsplit('-', 1)[0] if r['kind'] in {'table-row', 'table-header'} else (r['context'] if r['kind'] == 'table' else '')
        key = (r['page'], r['kind'], r['expected'], scope)
        require(key not in seen, f"duplicate annotation content: {r['id']}")
        seen.add(key)
        if r['kind'] in {'image', 'chemical-structure'}:
            require(all(alt.strip() for group in r['expected'].split(';')
                        for alt in group.split('|')), f"empty semantic alternative: {r['id']}")
        if r['kind'] in {'table-row', 'table-header'}:
            parent = r['id'].rsplit('-', 1)[0]
            require(parent in by and by[parent]['kind'] == 'table', f"orphan row: {r['id']}")
            columns = int(re.search(r'columns=(\d+)', by[parent]['expected'])[1])
            require(len(r['expected'].split(' | ')) == columns, f"cell count: {r['id']}")
        if r['kind'] == 'table':
            match = re.fullmatch(r'rows=(\d+);columns=(\d+);header=([01])', r['expected'])
            require(match is not None, f"table metadata: {r['id']}")
            children = [x for x in rows if x['id'].startswith(r['id'] + '-')]
            require(sum(x['kind'] == 'table-row' for x in children) == int(match[1]),
                    f"table data count: {r['id']}")
            require(sum(x['kind'] == 'table-header' for x in children) == int(match[3]),
                    f"semantic header count: {r['id']}")
    rules = exp['text']['must_not_match']
    require(len({r['id'] for r in rules}) == len(rules), 'duplicate rule ID')
    for r in rules:
        re.compile(r['pattern'], re.MULTILINE)
    re.compile(exp['structure']['slide_heading']['pattern'])
    for title in exp['structure']['slide_titles']:
        require(any(int(r['page']) == title['page'] and r['kind'] == 'text'
                    and r['expected'] == title['title'] for r in rows), 'title/CSV mismatch')
    audit = exp['audit']
    digest = hashlib.sha256((root / audit['source_pdf']).read_bytes()).hexdigest()
    require(digest == audit['source_sha256'], 'source PDF changed')
    pages = audit['provenance']['pages']
    require([x['page'] for x in pages] == list(range(1, 43)), 'provenance page coverage')
    for rid in audit['provenance']['raster_text_overrides']:
        require(rid in by and by[rid]['kind'] == 'text', f'provenance reference: {rid}')
    for table in audit['table_semantics']:
        require(table['object_id'] in by, 'unknown table reference')
        require(by[table['caption_id']]['kind'] == 'text', 'caption must be text')
        require(by[table['object_id']]['expected'] ==
                f"rows={table['data_rows']};columns={table['columns']};header=0", 'table semantics mismatch')
    chart = audit['chart_data']
    require(by[chart['object_id']]['kind'] == 'image', 'chart object reference')
    require(len(chart['pairs']) == 20, 'chart must contain 20 pairs')
    require(len({x['category'] for x in chart['pairs']}) == 20, 'duplicate chart category')
    terms = by[chart['object_id']]['expected'].split(';')
    for pair in chart['pairs']:
        require(f"{pair['category']}|{pair['category_pt_BR']}" in terms, 'chart category terms')
        value = pair['density']
        require(re.fullmatch(r'\d+\.\d{2}', value), 'printed chart precision')
        require(value + '|' + value.replace('.', ',') in terms, 'chart density terms')
    for item in audit['object_associations']:
        require(item['object_id'] in by, 'unknown association object')
        if 'label_id' in item:
            require(by[item['label_id']]['expected'] == item['substance_literal'] + ' (' + item['state_literal'] + ')', 'photo/label association')
    baseline_text = subprocess.check_output(
        ['git', 'show', audit['baseline_commit'] + ':input/presentation-reference/ground_truth.csv'],
        cwd=root, text=True)
    before = {r['id']: r for r in read_csv(baseline_text)}
    require(before.keys() <= by.keys(), 'existing IDs must be preserved')
    expected_diff = []
    for r in rows:
        previous = before.get(r['id'])
        for field in FIELDS:
            if previous is None or r[field] != previous[field]:
                expected_diff.append(dict(zip(['id', 'page', 'change', 'field', 'before', 'after'],
                    [r['id'], r['page'], 'added' if previous is None else 'modified', field,
                     previous[field] if previous else '', r[field]])))
    with (case / audit['comparison']).open(encoding='utf-8', newline='') as f:
        actual_diff = list(csv.DictReader(f, strict=True))
    require(actual_diff == expected_diff, 'AUDIT_DIFF.csv does not reproduce the baseline diff')
    require((case / audit['report']).is_file(), 'audit report missing')
    result = {'pages': 42, 'rows_before': len(before), 'rows_after': len(rows),
              'added': len(by.keys() - before.keys()), 'removed': 0,
              'modified': sum(r != before[rid] for rid, r in by.items() if rid in before),
              'unique_ids': len(by), 'pdf_sha256': digest,
              'kinds': dict(sorted(collections.Counter(r['kind'] for r in rows).items()))}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        validate(args.root)
    except (ValueError, KeyError, csv.Error) as error:
        parser.exit(1, f'INVALID: {error}\n')
