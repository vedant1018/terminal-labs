#!/usr/bin/env python3
"""Create isolated, deterministic teaching data. Never overwrite a prior attempt."""
import hashlib
import re
import shlex
import sys
from pathlib import Path


def make_data(student_id):
    h = hashlib.sha256(student_id.encode()).hexdigest()
    event = 'EV' + h[:6].upper()
    token = 'REG' + h[6:12].upper()
    room = 'Hall-' + str(1 + int(h[12:14], 16) % 8)
    branch = ['east', 'west', 'north'][int(h[14:16], 16) % 3]
    ticket = 'TK' + h[16:22].upper()
    files = {
      'identity.txt': f'LAB_ID={student_id}\nEVENT={event}\nTOKEN={token}\nROOM={room}\n',
      '.welcome': 'Hidden does not mean encrypted. The leading dot affects ordinary listings.\n',
      'maze/gate/desk/location.txt': 'You reached the event help desk.\n',
      'practice/original.txt': f'Welcome to event {event}.\nDoors open at 09:00.\n',
      'practice/reading.txt': '\n'.join(f'Line {n}: event preparation step {n}' for n in range(1,13)) + '\n',
      'practice/sample.log': 'INFO ready\nERROR badge missing\nINFO waiting\nERROR door blocked\nINFO fixed\nERROR printer offline\n',
      'practice/empty.txt': '',
      'practice/labels.txt': 'ERROR\nerror\nERROR ERROR\nINFO\n',
      'practice/wildcards/notice-a.txt': 'First notice\n',
      'practice/wildcards/notice-b.txt': 'Second notice\n',
      'practice/wildcards/notice.csv': 'name,status\n',
      'practice/wildcards/.notice-secret.txt': 'A hidden text file\n',
      'practice/wildcards/old/notice-c.txt': 'A nested notice\n',
      'practice/registrations.txt': f'{token} CONFIRMED\nREGOTHER WAITLIST\n{token} ARRIVED\nREGOTHER ARRIVED\n{token} BADGE_ISSUED\n',
      f'records/{branch}/box/brief-{event}.txt': f'Event: {event}\nAssigned room: {room}\nAll registrations are fictional.\n',
      'records/archive/brief-OLD.txt': 'This is an old event.\n',
      'records/other/readme.txt': 'Use the filename to identify the assigned event brief.\n',
      'rescue/.dispatch': f'EVENT={event}\nTICKET={ticket}\nLocate the file named approved-{event}.txt under rescue/inbox.\nUse rescue/system.log for the error report.\nRemove ONLY rescue/discard/{ticket}.tmp.\n',
      f'rescue/inbox/{branch}/Final Notices/approved-{event}.txt': f'APPROVED\nEvent {event}\nRoom {room}\nDoors open at 09:00.\n',
      f'rescue/inbox/archive/draft-{event}.txt': f'DRAFT - do not submit\nEvent {event}\n',
      'rescue/inbox/other/approved-OTHER.txt': 'APPROVED\nDifferent event\n',
      f'rescue/discard/{ticket}.tmp': 'Disposable duplicate designated by dispatch.\n',
      'rescue/discard/KEEP.tmp': 'Required recovery record. Preserve me.\n',
      'rescue/discard/notes.txt': 'Required coordinator notes. Preserve me.\n',
    }
    count = 4 + int(h[22:24],16) % 3
    logs = []
    for n in range(1, count+1):
        logs += [f'{n:02d}:00 EVENT={event} INFO checkpoint-{n}',
                 f'{n:02d}:01 EVENT=OTHER ERROR unrelated-{n}',
                 f'{n:02d}:02 EVENT={event} ERROR fault-{h[24:28]}-{n}']
    logs += [f'20:00 EVENT={event} INFO finished']
    files['rescue/system.log'] = '\n'.join(logs) + '\n'
    return files


def create(student_id, destination):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', student_id):
        raise ValueError('Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    destination.mkdir(parents=True, exist_ok=False)
    for relative, content in make_data(student_id).items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    return destination


if __name__ == '__main__':
    student_id = input('Enter the lab ID assigned by your instructor (not your email): ').strip()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', student_id):
        sys.exit('Invalid ID. Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    destination = Path(__file__).resolve().parent.parent / 'lab-work' / ('lab1-' + student_id)
    try:
        create(student_id, destination)
    except FileExistsError:
        print('This attempt already exists. Your work has been preserved.')
    print('\nEnter your lab folder with this exact command:')
    print('cd ' + shlex.quote(str(destination)))
    print('\nThen run: pwd')
