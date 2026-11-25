#!/usr/bin/env python3
"""Validate the integrity of the case 036 reference, not Acessilia outputs.

Requires Python 3.9+ and Git history containing the recorded baseline commit.
Run: python3 input/math-reference/validate.py [--root DATASET_CLONE]
"""
import argparse
import contextlib
import shutil
import tempfile
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

FIELDS = ['id', 'manifest_id', 'page', 'kind', 'expected_latex', 'context', 'notes']
PDF_SHA = 'ab72d5c0b524c4b1d2d34e4ccbf0342b217e41394e3eb9bee7188076729c7787'
PERMISSIONS_SHA = 'e09ba4546b1bebc0264ff4c12dbed239393ad167067ee6dcd0051cd3f4cf13f7'
DISPLAY_COUNTS = {1: 2, 2: 3, 3: 7, 4: 1, 5: 3}
ARITY = {'symbol': (0, 0), 'number': (0, 0), 'infinity': (0, 0), 'ellipsis': (0, 0),
         'subscript': (2, 2), 'power': (2, 2), 'group': (1, 1), 'add': (2, None),
         'subtract': (2, 2), 'multiply': (2, None), 'divide': (2, 2), 'call': (2, None),
         'equality_chain': (2, None), 'greater_than': (2, 2), 'greater_equal': (2, 2),
         'not_equal': (2, 2), 'member': (2, 2), 'interval': (2, 2), 'union': (2, None),
         'set_builder': (3, 3), 'and': (2, None), 'domain': (1, 1), 'limit': (3, 3),
         'with_condition': (2, 2), 'negate': (1, 1)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_keys)


def read_rows(text):
    data = list(csv.reader(io.StringIO(text, newline=''), strict=True))
    require(bool(data) and data[0] == FIELDS, 'CSV header')
    require(all(len(row) == len(FIELDS) for row in data[1:]), 'CSV row width')
    return [dict(zip(FIELDS, row)) for row in data[1:]]


def tree_nodes(node, path=''):
    require(isinstance(node, dict) and node.get('op') in ARITY, 'unknown AST operator')
    args = node.get('args', [])
    require(isinstance(args, list), 'AST args must be a list')
    low, high = ARITY[node['op']]
    require(len(args) >= low and (high is None or len(args) <= high), 'AST operator arity')
    if node['op'] == 'number':
        require(re.fullmatch(r'-?\d+(?:[,.]\d+)?', node.get('literal', '')), 'AST number')
    if node['op'] == 'symbol':
        require(bool(node.get('name')), 'AST symbol name')
    if node['op'] == 'interval':
        require(type(node.get('left_closed')) is bool and type(node.get('right_closed')) is bool,
                'interval open/closed flags')
    yield path, node
    for index, child in enumerate(args):
        yield from tree_nodes(child, path + '/args/' + str(index))


def box_ok(box):
    return (isinstance(box, list) and len(box) == 4
            and all(isinstance(n, (int, float)) for n in box)
            and 0 <= box[0] < box[2] <= 612 and 0 <= box[1] < box[3] <= 792)


def baseline_file(root, commit, name):
    return subprocess.check_output(['git', 'show', commit + ':input/math-reference/' + name], cwd=root)


def validate(root):
    case = root / 'input/math-reference'
    rows = read_rows((case / 'ground_truth.csv').read_text(encoding='utf-8'))
    exp = read_json(case / 'expectations.json')
    sem = read_json(case / 'semantic_reference.json')
    require(sem['schema_version'] == '1.0.0', 'semantic schema version')
    require(exp['manifest_id'] == sem['manifest_id'] == '036', 'manifest ID')
    require(sem['source']['sha256'] == PDF_SHA, 'declared PDF hash')
    require(hashlib.sha256((case / 'velocidade-instantanea.pdf').read_bytes()).hexdigest() == PDF_SHA,
            'source PDF changed')
    require(sem['source']['permissions_sha256'] == PERMISSIONS_SHA, 'declared permission hash')
    require(hashlib.sha256((case / 'PERMISSIONS.md').read_bytes()).hexdigest() == PERMISSIONS_SHA,
            'PERMISSIONS.md changed')
    base = sem['source']['baseline_commit']
    require(exp['audit']['baseline_commit'] == base, 'baseline reference mismatch')
    require(baseline_file(root, base, 'PERMISSIONS.md') == (case / 'PERMISSIONS.md').read_bytes(),
            'permissions differ from baseline')
    require(hashlib.sha256(baseline_file(root, base, 'velocidade-instantanea.pdf')).hexdigest() == PDF_SHA,
            'PDF differs from baseline')
    before = {r['id']: r for r in read_rows(baseline_file(root, base, 'ground_truth.csv').decode('utf-8'))}
    by = {r['id']: r for r in rows}
    require(len(by) == len(rows), 'duplicate CSV ID')
    require(before.keys() <= by.keys(), 'missing baseline ID')
    require(len(before) == 91, 'unexpected baseline inventory')
    require({int(r['page']) for r in rows} == set(range(1, 6)), 'five-page coverage')
    require([int(r['page']) for r in rows] == sorted(int(r['page']) for r in rows), 'CSV page order')
    kinds = {'i': 'inline', 'd': 'display', 't': ('table-header', 'table-cell')}
    for r in rows:
        match = re.fullmatch(r'p([1-5])-([idt])(\d{2})', r['id'])
        require(match is not None, 'CSV ID syntax')
        require(match[1] == r['page'] and r['manifest_id'] == '036', 'ID/page/manifest mismatch')
        require(r['kind'] in ((kinds[match[2]],) if match[2] != 't' else kinds['t']), 'kind/ID mismatch')
        require(bool(r['expected_latex'].strip()) and bool(r['context'].strip()), 'empty CSV expectation/context')
    occurrences = sem['occurrences']
    require(occurrences.keys() == by.keys(), 'occurrence/CSV coverage')
    for rid, occ in occurrences.items():
        require(occ['page'] == int(by[rid]['page']) and occ['kind'] == by[rid]['kind'], 'occurrence page/kind')
        require(occ['anchor'] == by[rid]['context'] and box_ok(occ['bbox_pt']), 'occurrence anchor/region')
        require(occ['same_latex_ordinal_on_page'] >= 1, 'occurrence ordinal')
    for rid in sem['inline_constraints']:
        require(rid in by and by[rid]['kind'] == 'inline', 'inline constraint reference')
    require(sem['inline_constraints']['p4-i10']['listed_variables'] == ['s_0', 'a'], 'inline membership variables')
    require(Counter(int(r['page']) for r in rows if r['kind'] == 'display') == DISPLAY_COUNTS,
            '16 display formulas/page distribution')
    display = {r['id'] for r in rows if r['kind'] == 'display'}
    require(sem['display_formulas'].keys() == display, 'semantic display coverage')
    require(set(sem['ast_schema']['operators']) == set(ARITY), 'AST schema operator coverage')
    for rid, formula in sem['display_formulas'].items():
        require(formula['literal_latex'] == by[rid]['expected_latex'], 'semantic literal/CSV mismatch')
        require(formula['math_latex'] == re.sub(r'\s*\\tag\{1\}', '', formula['literal_latex']),
                'equation label included in mathematical content')
        require(formula['page'] == int(by[rid]['page']) and box_ok(formula['bbox_pt']), 'formula page/region')
        nodes = list(tree_nodes(formula['ast']))
        require(dict(Counter(node['op'] for _, node in nodes)) == formula['node_counts'], 'AST node counts')
        invariants = [{'path': path + '/' + key, 'equals': node[key]}
                      for path, node in nodes for key in node if key != 'args']
        stored = formula['semantic_invariants']
        require(isinstance(stored, dict), 'AST invariants must map paths to values')
        require({x['path']: x['equals'] for x in invariants} == stored,
                'AST semantic invariant changed')
        speech = formula['speech']
        require(speech['language'] == 'pt-BR' and len(speech['required_relations']) >= 1,
                'missing relational speech specification')
        require(len(set(speech['acceptable_examples'])) >= 2, 'speech paraphrase examples')
        main = formula['ast']['args'][0] if formula['ast']['op'] == 'with_condition' else formula['ast']
        count = len(main['args']) if main['op'] == 'equality_chain' else 1
        require(formula['segmentation']['ordered_stages'] == count, 'equality chain stage count')
    require('2^8' in by['p2-d03']['expected_latex'] and r'\tag{1}' in by['p2-d03']['expected_latex'],
            'printed exponent or equation label silently changed')
    require(by['p4-i10']['expected_latex'] == r's_0, a \in \mathbb{R}', 'printed variable list altered')
    require('acontence' in by['p3-i11']['context'], 'source spelling silently repaired')
    rules = exp['speech']['formulas']
    require(len(rules) == 16 and {r['formula'] for r in rules} == display, '16 speech references required')
    for rule in rules:
        require(bool(rule['any_of']) and all(isinstance(w, str) and w for w in rule['any_of']),
                'empty legacy speech proxy')
        require(rule['semantic_reference'] == 'semantic_reference.json#/display_formulas/' + rule['formula'] + '/speech',
                'speech cross-reference')
    for section in ('must_match', 'must_not_match'):
        require(len({r['id'] for r in exp['text'][section]}) == len(exp['text'][section]), 'duplicate regex ID')
        for rule in exp['text'][section]:
            re.compile(rule['pattern'])
    table_refs = {r['id'] for r in rows if r['kind'] in {'table-header', 'table-cell'}}
    registered = set()
    filled = blanks = 0
    empty_slots = set()
    require(len(sem['tables']) == len(exp['structure']['tables']) == 2, 'two tables required')
    require([t['page'] for t in sem['tables']] == [2, 5], 'table pages')
    cell_ids = [c['id'] for t in sem['tables'] for c in t['headers'] + t['data']]
    require(len(set(cell_ids)) == len(cell_ids), 'duplicate semantic cell ID')
    for table, legacy in zip(sem['tables'], exp['structure']['tables']):
        page = table['page']
        require((table['rows'], table['columns'], table['header_rows']) ==
                ((7, 3, 1) if page == 2 else (5, 3, 1)), 'table shape')
        require((legacy['rows'], legacy['columns'], legacy['header_rows'], legacy['page']) ==
                (table['rows'], table['columns'], table['header_rows'], page), 'legacy table shape mismatch')
        require(legacy['semantic_table_id'] == table['id'], 'legacy semantic table reference')
        require(len(table['headers']) == 3 and [h['column'] for h in table['headers']] == [1, 2, 3],
                'three column headers')
        require(legacy['math_headers'] == [h['annotation_id'] for h in table['headers']], 'header references')
        for header in table['headers']:
            rid = header['annotation_id']
            require(rid in table_refs and by[rid]['kind'] == 'table-header', 'header CSV ID')
            require(header['latex'] == by[rid]['expected_latex'] and box_ok(header['bbox_pt']), 'header content/box')
            require(header['id'] == rid and header['row'] == 1, 'header coordinates')
            registered.add(rid)
        positions = {(c['row'], c['column']) for c in table['data']}
        require(len(positions) == len(table['data']) and positions ==
                {(r, c) for r in range(2, table['rows'] + 1) for c in range(1, 4)}, 'table grid positions')
        expected_ids = []
        for cell in table['data']:
            require(cell['data_row'] == cell['row'] - 1 and box_ok(cell['bbox_pt']), 'data cell coordinates')
            require(cell['column_header_id'] == f"p{page}-t{cell['column']:02}", 'cell/header association')
            row_key = next(x['literal'] for x in table['data'] if x['row'] == cell['row'] and x['column'] == 1)
            require(cell['row_key'] == row_key, 'cell/row association')
            if cell['state'] == 'empty':
                blanks += 1
                empty_slots.add((page, cell['row'], cell['column']))
                require(cell['annotation_id'] is None and cell['literal'] is None and cell['latex'] is None,
                        'empty exercise cell was filled')
            else:
                require(cell['state'] == 'filled', 'unknown cell state')
                filled += 1
                rid = cell['annotation_id']
                require(rid in by and by[rid]['kind'] == 'table-cell', 'filled cell CSV reference')
                require(cell['id'] == rid and cell['latex'] == by[rid]['expected_latex'], 'cell literal/CSV')
                literal = cell['latex'].replace('{,}', ',').replace('-', '−')
                require(literal == cell['literal'], 'printed cell value')
                registered.add(rid)
                expected_ids.append(rid)
        require(legacy['math_cells'] == expected_ids, 'legacy cell coverage')
    require(filled == 25 and blanks == 5, '25 filled and 5 empty positions required')
    require(empty_slots == {(5, 3, 3), (5, 4, 2), (5, 4, 3), (5, 5, 2), (5, 5, 3)},
            'intentional blank positions changed')
    require(registered == table_refs and len(table_refs) == 31, 'table/CSV coverage')
    eqs = sem['equations']
    require(len(eqs) == 1 and eqs[0]['formula_id'] == 'p2-d03' and eqs[0]['number'] == '1'
            and eqs[0]['label_is_operand'] is False, 'equation label association')
    require(sem['display_formulas']['p2-d03']['equation_label'] == '1', 'semantic equation label')
    require(exp['structure']['equation_numbers'] == [{'formula': 'p2-d03', 'number': '1'}], 'legacy equation label')
    refs = sem['equation_references']
    require(len(refs) == 2 and eqs[0]['reference_ids'] == [r['id'] for r in refs], 'two equation references')
    require({r['formula_context_id'] for r in refs} == {'p3-i04', 'p3-i07'}, 'equation reference occurrences')
    for ref in refs:
        require(ref['target_equation'] == eqs[0]['id'] and ref['page'] == 3 and box_ok(ref['bbox_pt']),
                'equation reference target')
    require(exp['semantic_reference']['file'] == 'semantic_reference.json' and
            exp['semantic_reference']['schema_version'] == sem['schema_version'], 'semantic file reference')
    structure = sem['document_structure']
    require(len(structure['lists']) == len(exp['structure']['ordered_lists']) == 2 and
            [x['page'] for x in structure['lists']] == [4, 5], 'two ordered lists required')
    require(len(structure['callouts']) == len(exp['structure']['callouts']) == 2, 'two callouts required')
    require(structure['headings'] == exp['structure']['headings'], 'heading references')
    item_map = {}
    tables_by_id = {t['id']: t for t in sem['tables']}
    for lst, legacy in zip(structure['lists'], exp['structure']['ordered_lists']):
        count = 4 if lst['page'] == 4 else 3
        require(lst['start'] == 1 and lst['ordered'] is True and lst['item_count'] == count
                and len(lst['items']) == count, 'ordered list structure')
        require(lst['item_ids'] == [item['id'] for item in lst['items']] and
                [i['number'] for i in lst['items']] == list(range(1, count + 1)), 'list numbering')
        require(legacy['items'] == count and legacy['page'] == lst['page'] and
                legacy['first_item_starts'] == lst['items'][0]['starts'], 'legacy list consistency')
        for item in lst['items']:
            item_map[item['id']] = item
            for rid in item['contains']:
                require(rid in by or rid in tables_by_id, 'list child reference')
                require(int(by[rid]['page']) == lst['page'] if rid in by else tables_by_id[rid]['page'] == lst['page'],
                        'list child page')
    for formula, item in [('p4-d01', 'p4-list01-item1'), ('p5-d02', 'p5-list01-item2')]:
        require(sem['display_formulas'][formula]['list_item'] == item and formula in item_map[item]['contains'],
                'formula/list association')
    require(tables_by_id['p5-table01']['list_item'] == 'p5-list01-item1' and
            'p5-table01' in item_map['p5-list01-item1']['contains'], 'table/list association')
    for callout, legacy in zip(structure['callouts'], exp['structure']['callouts']):
        require(callout['literal_text'] == legacy['literal_text'] and callout['id'] == legacy['semantic_id'],
                'complete callout reference')
        require(all(rid in by for rid in callout['math_ids']), 'callout math references')
    known = set(by) | set(tables_by_id) | {r['id'] for r in refs} | {x['id'] for x in structure['lists']}
    for category, expected in [('negative', 'reject'), ('positive', 'accept-if-complete')]:
        controls = sem['controls'][category]
        require(len({x['id'] for x in controls}) == len(controls), 'duplicate control ID')
        require(all(c['target'] in known and c['expected'] == expected for c in controls), 'control cross-reference')
    comparison = []
    for row in rows:
        prev = before.get(row['id'])
        for field in FIELDS:
            if prev is None or row[field] != prev[field]:
                comparison.append(dict(zip(['id', 'page', 'change', 'field', 'before', 'after'],
                    [row['id'], row['page'], 'added' if prev is None else 'modified', field,
                     prev[field] if prev else '', row[field]])))
    with (case / 'AUDIT_DIFF.csv').open(encoding='utf-8', newline='') as stream:
        require(list(csv.DictReader(stream, strict=True)) == comparison, 'AUDIT_DIFF.csv out of date')
    require((case / 'AUDIT.md').is_file(), 'audit report missing')
    result = {'pages': 5, 'before': len(before), 'after': len(rows), 'added': len(by.keys() - before.keys()),
              'modified': sum(row != before[rid] for rid, row in by.items() if rid in before),
              'removed': 0, 'unique_ids': len(by), 'kinds': dict(Counter(r['kind'] for r in rows)),
              'filled_cells': filled, 'intentional_blanks': blanks, 'semantic_display_formulas': len(display),
              'speech_references': len(rules), 'pdf_sha256': PDF_SHA, 'permissions_unchanged': True}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def self_test(root):
    """Mutate disposable copies. These controls test reference integrity only."""
    source = root / 'input/math-reference'
    snapshots = {name: (source / name).read_bytes() for name in
                 ('ground_truth.csv', 'expectations.json', 'semantic_reference.json',
                  'AUDIT_DIFF.csv', 'velocidade-instantanea.pdf', 'PERMISSIONS.md')}
    failures = []
    with tempfile.TemporaryDirectory(prefix='case036-validator-') as temp:
        target = Path(temp)
        case = target / 'input/math-reference'
        shutil.copytree(source, case)
        (target / '.git').symlink_to((root / '.git').resolve(), target_is_directory=True)

        def reset():
            for name, data in snapshots.items():
                (case / name).write_bytes(data)

        def mutate_csv(fn):
            rows = read_rows((case / 'ground_truth.csv').read_text())
            fn(rows)
            with (case / 'ground_truth.csv').open('w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n')
                writer.writeheader()
                writer.writerows(rows)

        def mutate_json(name, fn):
            value = read_json(case / name)
            fn(value)
            (case / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        def run(name, mutate):
            reset()
            mutate()
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    validate(target)
            except (ValueError, KeyError, TypeError, IndexError) as error:
                failures.append({'control': name, 'result': 'rejected', 'reason': str(error)})
            else:
                raise ValueError('negative validator control unexpectedly passed: ' + name)

        def sem(fn):
            mutate_json('semantic_reference.json', fn)

        run('duplicate CSV ID', lambda: mutate_csv(lambda rows: rows.append(rows[0].copy())))
        run('remove repeated baseline occurrence', lambda: mutate_csv(
            lambda rows: rows.remove(next(r for r in rows if r['id'] == 'p1-i17'))))
        run('ID/page mismatch', lambda: mutate_csv(lambda rows: rows[0].update(page='2')))
        run('PDF hash', lambda: (case / 'velocidade-instantanea.pdf').write_bytes(snapshots['velocidade-instantanea.pdf'] + b'x'))
        run('permission file', lambda: (case / 'PERMISSIONS.md').write_bytes(snapshots['PERMISSIONS.md'] + b'x'))
        run('duplicate JSON key', lambda: (case / 'semantic_reference.json').write_text(
            '{"manifest_id":"036",' + snapshots['semantic_reference.json'].decode('utf-8')[1:], encoding='utf-8'))
        run('duplicate table position', lambda: sem(lambda s: s['tables'][0]['data'][1].update(column=1)))
        run('duplicate blank ID', lambda: sem(lambda s: s['tables'][1]['data'][7].update(id='p5-e01')))
        run('wrong cell/header link', lambda: sem(lambda s: s['tables'][0]['data'][0].update(column_header_id='p2-t02')))
        run('filled intentional blank', lambda: sem(lambda s: s['tables'][1]['data'][5].update(literal='0', latex='0')))
        run('closed interval changed', lambda: sem(lambda s: s['display_formulas']['p3-d01']['ast']['args'][1]['args'][0].update(left_closed=False)))
        run('nested fraction lost', lambda: sem(lambda s: s['display_formulas']['p5-d02']['ast']['args'][1]['args'][0]['args'].__setitem__(0, {'op': 'number', 'literal': '1'})))
        run('silent 2^8 repair', lambda: mutate_csv(lambda rows: next(r for r in rows if r['id'] == 'p2-d03').update(
            expected_latex=next(r for r in rows if r['id'] == 'p2-d03')['expected_latex'].replace('2^8', '2^3'))))
        run('missing display speech', lambda: mutate_json('expectations.json', lambda e: e['speech']['formulas'].pop()))
        run('equation label link', lambda: sem(lambda s: s['equations'][0].update(formula_id='p2-d02')))
        run('missing equation reference', lambda: sem(lambda s: s['equation_references'].pop()))
        run('formula/list item link', lambda: sem(lambda s: s['document_structure']['lists'][0]['items'][0]['contains'].remove('p4-d01')))
        run('table/list item link', lambda: sem(lambda s: s['tables'][1].update(list_item='p5-list01-item2')))
        run('stale comparison', lambda: mutate_csv(lambda rows: rows[0].update(notes='unreported change')))
        # Data-equivalent serializations must remain valid.
        reset()
        for name in ('expectations.json', 'semantic_reference.json'):
            (case / name).write_text(json.dumps(read_json(case / name), ensure_ascii=True, sort_keys=True), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            validate(target)
        reset()
        rows = read_rows((case / 'ground_truth.csv').read_text())
        with (case / 'ground_truth.csv').open('w', encoding='utf-8', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=FIELDS, quoting=csv.QUOTE_ALL, lineterminator='\r\n')
            writer.writeheader()
            writer.writerows(rows)
        with contextlib.redirect_stdout(io.StringIO()):
            validate(target)
    print(json.dumps({'validator_negative_controls': failures,
                      'validator_positive_controls': ['equivalent JSON serialization', 'equivalent CSV serialization'],
                      'output_semantic_controls': 'specifications only; not executed by this validator'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true', help='run controls on temporary copies')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        validate(args.root)
        if args.self_test:
            self_test(args.root)
    except (ValueError, KeyError, TypeError, IndexError, csv.Error, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'INVALID: {error}\n')
