"""Package the explicitly requested Flwers session and references for laptop transfer."""
from pathlib import Path
import hashlib, json, shutil, zipfile, gzip, xml.etree.ElementTree as ET

workspace = Path(__file__).resolve().parent.parent
repo = Path(__file__).resolve().parent
project = Path('C:/Users/Collin/Downloads/FLWERS SET NOV 2026 for collin Project/FLWERS SET NOV 2026 for collin Project')
downloads = Path('C:/Users/Collin/Downloads')
release = workspace / 'flwers-release-assets'
release.mkdir(exist_ok=True)
(repo / 'artifacts').mkdir(exist_ok=True)
allowed_prefixes = ('Flwers', 'Flwers-', 'Every', 'Figure', 'Tongue', 'TT ', 'SAA ', 'Remaining Songs', 'Helix Ableton')
selected = [p for p in workspace.iterdir() if p.is_file() and (
    p.suffix.lower() in ('.hlx', '.hls') or
    (p.suffix.lower() in ('.txt', '.json') and p.name.startswith(allowed_prefixes)) or
    p.name in ('analyze_remaining_songs.py', 'analyze_tongue_tied.py', 'build-simple-helix.cjs'))]
for source in selected:
    target = repo / 'artifacts' / source.name
    shutil.copyfile(source, target)

small_project = repo / 'Ableton' / 'FLWERS SET NOV 2026 for collin Project'
small_project.mkdir(parents=True, exist_ok=True)
for name in ('FLWERS SET NOV 2026 for collin.als', 'FLWERS SET NOV 2026 - Helix Snapshots CC69.als', 'Stop after Song and Go To Next Locator V1.1 AbletonDrummer.amxd'):
    shutil.copyfile(project / name, small_project / name)
history = small_project / 'Historical - CC67 bug'
history.mkdir(exist_ok=True)
shutil.copyfile(project / 'FLWERS SET NOV 2026 - Helix Snapshots Test.als', history / 'FLWERS SET NOV 2026 - Helix Snapshots Test.als')

def hashfile(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(8*1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

manifest = []
def pack(files, prefix, base, root):
    groups, group, size = [], [], 0
    for path in files:
        length = path.stat().st_size
        if group and size + length > 1_400_000_000:
            groups.append(group); group, size = [], 0
        group.append(path); size += length
    if group:
        groups.append(group)
    for number, group in enumerate(groups, 1):
        target = release / f'{prefix}-part-{number:02d}.zip'
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
            for source in group:
                arcname = (Path(root) / source.relative_to(base)).as_posix()
                archive.write(source, arcname)
                manifest.append({'archive': target.name, 'path': arcname, 'bytes': source.stat().st_size, 'sha256': hashfile(source)})
        with zipfile.ZipFile(target) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f'CRC verification failed: {bad}')
        print(f'Packed and verified {target.name}: {target.stat().st_size:,} bytes, {len(group)} files', flush=True)

pack(sorted(p for p in project.rglob('*') if p.is_file()), 'Flwers-Ableton-Project', project, project.name)
references = [downloads / name for name in (
    "Tongue Tied Gtr Parts Solo'd.wav", 'tongue tied MSTR02 (CD 16b44.1k).wav',
    "Fade Gtr Parts Solo'd.wav", 'Fade FULL PRACTICE TRACK.wav',
    "Better Than This Gtr Parts Solo'd.wav", 'Better Than This FULL PRACTICE TRACK.wav',
    "Nothing at All Collins Parts Solo'd.wav", 'Nothing at All FULL PRACTICE TRACK.wav')]
pack(references, 'Flwers-Tone-References', downloads, 'Tone References')
(repo / 'release-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
checks = '\n'.join(f'{hashfile(p)}  {p.name}' for p in sorted(release.glob('*.zip'))) + '\n'
(release / 'SHA256SUMS.txt').write_text(checks, encoding='utf-8')
(repo / 'RELEASE-SHA256SUMS.txt').write_text(checks, encoding='utf-8')

root = ET.fromstring(gzip.decompress((project / 'FLWERS SET NOV 2026 - Helix Snapshots CC69.als').read_bytes()))
refs = []
for ref in root.iter('FileRef'):
    relative = ref.find('RelativePath')
    if relative is not None and relative.get('Value'):
        val = relative.get('Value')
        resolved = project / val.replace('\\', '/')
        refs.append({'relativePath': val, 'exists': resolved.exists()})
(repo / 'ableton-relative-path-audit.json').write_text(json.dumps(refs, indent=2), encoding='utf-8')
print(f'Copied {len(selected)} workspace artifacts; archived {len(manifest)} project/reference files.', flush=True)
print(f'Relative FileRefs checked: {len(refs)}; missing: {sum(not r["exists"] for r in refs)}', flush=True)
