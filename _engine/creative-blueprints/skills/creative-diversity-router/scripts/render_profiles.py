#!/usr/bin/env python3
"""Render the maintained concept data into linked blueprint/profile references."""
import argparse
import json
from pathlib import Path

ROUTER = Path(__file__).resolve().parents[1]
SKILLS = ROUTER.parent
FIELDS = [
    ('coverage', 'Coverage and layer structure'),
    ('cuts', 'Cut rules and protected holds'),
    ('transitions', 'Transitions and handles'),
    ('broll', 'B-roll entry, exit and return'),
    ('motion', 'Camera, reframing and subject action'),
    ('text', 'Captions and graphic events'),
    ('audio', 'Voice, music and sound design'),
    ('finish', 'Image finish and time treatment'),
    ('ending', 'Reveal, CTA and ending'),
    ('adapt', 'Shorter, longer and timing conflicts'),
    ('reject', 'Reject and verify'),
]


def render(p):
    folder = SKILLS / p['skill'] / 'references'
    stem = p['id']
    source = '../../../research/' + p['ref'] + '/analysis.md'
    contract = '../../creative-diversity-router/references/profile-contract.md'
    lead = f"Profile ID: `{stem}` · Family: `{p['skill']}` · Source: [{p['ref']}]({source}).\n\n"
    note = 'Maintained from `creative-diversity-router/references/profiles.json`; regenerate with its renderer after changing data.\n\n'
    bp = f"# {p['title']} — generalized blueprint\n\n" + lead + note
    bp += f"Read the [editing profile]({stem}-editing-profile.md) and [application contract]({contract}) before adapting. This is a reusable reference, not a produced ad or selected-asset storyboard.\n\n"
    bp += '## Concept and script architecture\n\n' + p['premise'] + '\n\n' + p['script'] + '\n\n'
    bp += '## Keep and vary\n\n**Defining grammar:** ' + p['fixed'] + '\n\n**Adaptable:** ' + p['variable'] + '\n\n'
    bp += '## Beat blueprint\n\nCues are semantic placeholders. Replace them with exact approved words/actions in the target plan. Dwell ranges are proposed seconds for the named shot/module, not source measurements or a total-runtime promise.\n\n'
    bp += '| Slot / communication job | Visible action and style | Placement; enter → leave / return | Proposed dwell; handoff | Why this scene and edit belong |\n|---|---|---|---|---|\n'
    styles = {s[0] for s in p['styles']}
    for b in p['beats']:
        assert len(b) == 7, (stem, b)
        bid, job, visual, style, place, timing, why = b
        assert style in styles, (stem, style)
        bp += f'| {bid} — {job} | {visual} **{style}** | {place} | {timing} | {why} |\n'
    bp += '\n## Required asset roles\n\n' + p['assets'] + '\n\n'
    bp += '## Instantiate and hand off\n\nMap every approved line or silent action to these slots; assign actual selected asset IDs or explicit gaps. Resolve the entry/exit/return cues and all separate picture, overlay, caption and audio events. Save the target editing plan before production; apply the shared contract for Cut Room and current model/editor rules.\n'
    ep = f"# {p['title']} — editing profile\n\n" + lead + note
    ep += f"Use with the [blueprint]({stem}-blueprint.md) and [application contract]({contract}).\n\n"
    ep += '## Observed calibration\n\n' + p['calibration'] + '\n\n'
    boundary = p.get('evidence_boundary', 'the source audit provides observed frames and approximate semantic context. Audio findings were model-assisted; exact mix, word alignment, source tools and performance are unverified. All rules and adjustable ranges below are target direction, not recovered project settings.')
    ep += '**Evidence boundary:** ' + boundary + '\n\n'
    ep += '## Visual styles and where they belong\n\n| Style ID / role | Observable treatment and source route | Placement and allowed purpose |\n|---|---|---|\n'
    for style in p['styles']:
        assert len(style) == 3
        ep += '| ' + ' | '.join(style) + ' |\n'
    for key, title in FIELDS:
        assert p['edit'][key].strip(), (stem,key)
        ep += '\n## ' + title + '\n\n' + p['edit'][key] + '\n'
    return {folder / f'{stem}-blueprint.md': bp, folder / f'{stem}-editing-profile.md': ep}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Validate data and check generated references are current')
    args = parser.parse_args()
    data = json.loads((ROUTER / 'references/profiles.json').read_text())
    concepts = data['concepts']
    assert data['schema_version'] == 1 and concepts
    assert len({p['id'] for p in concepts}) == len(concepts)
    assert len({p['ref'] for p in concepts}) == len(concepts)
    outputs = {}
    for p in concepts:
        assert (SKILLS / p['skill'] / 'SKILL.md').exists()
        assert len({b[0] for b in p['beats']}) == len(p['beats'])
        outputs.update(render(p))
    stale = []
    for path, text in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    if stale:
        raise SystemExit('Stale or missing references: ' + ', '.join(stale))
    print(json.dumps({'concept_variants':len(concepts), 'families':len({p['skill'] for p in concepts}), 'references':len(outputs), 'mode':'checked' if args.check else 'rendered', 'stale':len(stale)}))


if __name__ == '__main__':
    main()
