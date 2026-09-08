#!/usr/bin/env python3
"""Read-only feedback on a student lab folder; not proof of independent work."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
from setup import make_data

root = Path.cwd()
try:
    identity = dict(line.split('=',1) for line in (root/'identity.txt').read_text().splitlines())
    lab_id, event = identity['LAB_ID'], identity['EVENT']
    original = make_data(lab_id)
except (OSError, ValueError, KeyError):
    sys.exit('Start this checker from your lab root (the folder containing identity.txt).')

results = []
def check(label, condition):
    results.append(bool(condition))
    print(('PASS  ' if condition else 'CHECK ') + label)
def read(relative):
    try: return (root/relative).read_text()
    except (OSError, UnicodeError): return None

check('Workspace: drafts and submission directories exist', (root/'work/drafts').is_dir() and (root/'work/submission').is_dir())
check('Copy and rename: announcement revised.txt has the original content', read('work/drafts/announcement revised.txt') == original['practice/original.txt'])
check('Touch: empty.txt exists and is empty', (root/'work/drafts/empty.txt').is_file() and read('work/drafts/empty.txt') == '')
check('Move: delivery.txt is in submission and absent from drafts', read('work/submission/delivery.txt') == original['practice/original.txt'] and not (root/'work/drafts/delivery.txt').exists())
check('Delete: disposable folder removed and keep.txt preserved', not (root/'work/disposable').exists() and read('work/keep.txt') == '')
check('Journal: exactly two lines with your ID and the stage', read('work/journal.txt') == f'{lab_id}\nStage: investigation\n')
check('Redirection experiment: final scratch text is replacement', read('work/scratch.txt') == 'replacement\n')
expected_records = ''.join(line+'\n' for line in original['practice/registrations.txt'].splitlines() if identity['TOKEN'] in line)
check('Search: own registration records saved', read('work/submission/my-records.txt') == expected_records)
sample_errors = ''.join(line+'\n' for line in original['practice/sample.log'].splitlines() if 'ERROR' in line)
check('Pipes: all sample errors saved', read('work/submission/sample-errors.txt') == sample_errors)
check('Pipes: latest two matching records saved', read('work/submission/latest-two.txt') == ''.join(sample_errors.splitlines(keepends=True)[-2:]))
rescue_source = next(p for p in original if p.startswith('rescue/inbox/') and p.endswith(f'approved-{event}.txt'))
check('Rescue: correct approved announcement copied', read('work/submission/rescue/announcement final.txt') == original[rescue_source])
errors = ''.join(line+'\n' for line in original['rescue/system.log'].splitlines() if f'EVENT={event} ' in line and 'ERROR' in line)
check('Rescue: error report has only this event and all its errors', read('work/submission/rescue/errors.txt') == errors)
count_text = read('work/submission/rescue/error-count.txt')
check('Rescue: count file contains the number only', count_text is not None and count_text.strip() == str(len(errors.splitlines())))
check('Rescue: latest three matching records saved', read('work/submission/rescue/latest-three.txt') == ''.join(errors.splitlines(keepends=True)[-3:]))
discard = next(p for p in original if p.startswith('rescue/discard/TK'))
check('Rescue: only the designated disposable file removed', not (root/discard).exists() and read('rescue/discard/KEEP.tmp') == original['rescue/discard/KEEP.tmp'] and read('rescue/discard/notes.txt') == original['rescue/discard/notes.txt'])
check('Original evidence files preserved', all(read(p) == text for p,text in original.items() if p != discard))
print(f'\n{sum(results)}/{len(results)} file checks passed. Paper observations and explanations are checked separately.')
sys.exit(0 if all(results) else 1)
