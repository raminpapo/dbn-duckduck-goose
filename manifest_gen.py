#!/usr/bin/env python3
"""
Generate manifest.json with metadata and checksums
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess

class ManifestGenerator:
    def __init__(self, repo_root, docs_dir="docs"):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / docs_dir

    def get_git_sha(self):
        """Get current git commit SHA"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if result.returncode == 0 else "no-git-sha"
        except:
            return "no-git-sha"

    def get_git_remote(self):
        """Get git remote URL"""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"

    def calculate_sha256(self, filepath):
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except:
            return "error"

    def scan_repo_files(self):
        """Scan all files in repository (excluding .git and docs)"""
        repo_files = []

        for item in self.repo_root.rglob('*'):
            if '.git' in item.parts or 'docs' in item.parts:
                continue

            if item.is_file():
                rel_path = item.relative_to(self.repo_root)
                repo_files.append({
                    'path': str(rel_path),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })

        return sorted(repo_files, key=lambda x: x['path'])

    def scan_docs_files(self):
        """Scan all generated documentation files"""
        docs_files = []
        total_bytes = 0

        for item in self.docs_dir.rglob('*'):
            if item.is_file() and item.suffix in ['.md', '.json', '.log']:
                rel_path = item.relative_to(self.docs_dir)
                size = item.stat().st_size
                checksum = self.calculate_sha256(item)

                docs_files.append({
                    'path': str(rel_path),
                    'size': size,
                    'checksum': checksum,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })

                total_bytes += size

        return sorted(docs_files, key=lambda x: x['path']), total_bytes

    def estimate_words(self):
        """Estimate total words in documentation"""
        total_words = 0

        for md_file in self.docs_dir.rglob('*.md'):
            try:
                with open(md_file, 'r') as f:
                    content = f.read()
                    total_words += len(content.split())
            except:
                pass

        return total_words

    def generate_manifest(self):
        """Generate complete manifest.json"""
        print("Generating manifest.json...")

        repo_files = self.scan_repo_files()
        docs_files, total_bytes = self.scan_docs_files()
        total_words = self.estimate_words()

        manifest = {
            "generator": {
                "name": "World's Best Repo Book Generator",
                "version": "1.0",
                "generated_at": datetime.now().isoformat()
            },
            "repository": {
                "name": "dbn-duckduck-goose",
                "description": "Golang Web Service Example using Databento and DuckDB",
                "remote_url": self.get_git_remote(),
                "commit_sha": self.get_git_sha(),
                "scan_timestamp": datetime.now().isoformat()
            },
            "statistics": {
                "repo_files_count": len(repo_files),
                "repo_folders_count": len(set(os.path.dirname(f['path']) for f in repo_files)),
                "docs_files_count": len(docs_files),
                "docs_md_files": len([f for f in docs_files if f['path'].endswith('.md')]),
                "total_bytes_written": total_bytes,
                "estimated_word_count": total_words
            },
            "repository_files": repo_files,
            "documentation_files": docs_files,
            "file_map": {
                "per_file_docs": sorted([str(f['path']) for f in docs_files if f['path'].endswith('_docs.md')]),
                "per_file_keywords": sorted([str(f['path']) for f in docs_files if f['path'].endswith('_kw.md')]),
                "folder_indices": sorted([str(f['path']) for f in docs_files if f['path'].endswith('index.md')]),
                "folder_docs": sorted([str(f['path']) for f in docs_files if f['path'].endswith('doc.md')]),
                "folder_keywords": sorted([str(f['path']) for f in docs_files if f['path'].endswith('sub.md')])
            },
            "global_files": {
                "index": "index.md",
                "keywords": "keywords.md",
                "comprehensive_book": "comprehensive_book.md",
                "verification_report": "verification_report.md",
                "manifest": "manifest.json",
                "readme": "README.md"
            }
        }

        manifest_file = self.docs_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"  Created {manifest_file}")
        print(f"  Repository files: {len(repo_files)}")
        print(f"  Documentation files: {len(docs_files)}")
        print(f"  Total bytes: {total_bytes:,}")
        print(f"  Estimated words: {total_words:,}")

        return manifest

# Main execution
if __name__ == "__main__":
    gen = ManifestGenerator("/home/user/dbn-duckduck-goose")
    manifest = gen.generate_manifest()

    print("\nManifest generation complete!")
