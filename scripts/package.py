"""Deliver sources and evidence reports, excluding credentials and runtime user records."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='../tech-selection-agent.zip')
    args = parser.parse_args()
    target = Path(args.output).resolve()
    files = [ROOT / p for p in ('README.md', '技术选型项目交付说明.md', 'pyproject.toml', 'uv.lock', 'requirements.lock.txt', '.env.example',
                                '.gitignore', '.dockerignore', 'Dockerfile', 'docker-compose.yml')]
    for folder in ('src', 'scripts', 'tests', 'evaluation', 'docs', 'reports'):
        files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and
                     p.suffix not in {'.pyc', '.sqlite', '.db'})
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path, 'tech-selection-agent/' + path.relative_to(ROOT).as_posix())
    with ZipFile(target) as archive:
        assert archive.testzip() is None
        assert all('/.env' not in name or name.endswith('.env.example') for name in archive.namelist())
    manifest = {'archive': target.name, 'files': len(files), 'bytes': target.stat().st_size,
                'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    target.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
