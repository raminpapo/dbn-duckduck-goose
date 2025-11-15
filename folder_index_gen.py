#!/usr/bin/env python3
"""
Generate folder indices and global documentation
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class FolderIndexGenerator:
    def __init__(self, repo_root, docs_dir="docs"):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / docs_dir
        self.global_keywords = defaultdict(list)

    def get_all_folders(self):
        """Get all folders in docs directory"""
        folders = set()
        for item in self.docs_dir.rglob('*'):
            if item.is_dir() and not item.name.startswith('.'):
                rel_path = item.relative_to(self.docs_dir)
                if str(rel_path) != '.':
                    folders.add(rel_path)

        # Add root
        folders.add(Path('.'))
        return sorted(folders)

    def create_folder_index(self, folder_path):
        """Create index.md for a folder"""
        full_path = self.docs_dir / folder_path if folder_path != Path('.') else self.docs_dir

        # Get direct children
        files = []
        subdirs = []

        for item in full_path.iterdir():
            if item.name.startswith('.'):
                continue

            if item.is_file() and item.suffix == '.md':
                if not item.name.endswith('_kw.md') and item.name not in ['index.md', 'doc.md', 'sub.md']:
                    files.append(item.name)
            elif item.is_dir():
                subdirs.append(item.name)

        # Create index.md
        index_content = f"""# {folder_path if folder_path != Path('.') else 'Root'} - Index

## Overview
{'Root directory of the repository' if folder_path == Path('.') else f'Documentation for {folder_path} directory'}

"""

        if subdirs:
            index_content += "## Subdirectories\n\n"
            for subdir in sorted(subdirs):
                index_content += f"- [{subdir}/]({subdir}/index.md)\n"
            index_content += "\n"

        if files:
            index_content += "## Files\n\n"
            for file in sorted(files):
                # Remove _docs.md suffix if present
                display_name = file.replace('_docs.md', '')
                index_content += f"- [{display_name}]({file})\n"
            index_content += "\n"

        index_content += f"""---
*Generated: {datetime.now().isoformat()}*
"""

        index_file = full_path / "index.md"
        with open(index_file, 'w') as f:
            f.write(index_content)

        return index_file

    def create_folder_doc(self, folder_path):
        """Create doc.md for a folder"""
        full_path = self.docs_dir / folder_path if folder_path != Path('.') else self.docs_dir

        # Map folder names to descriptions
        folder_descriptions = {
            '.': 'Root directory containing main configuration and entry point files',
            '.github': 'GitHub-specific configuration files',
            '.github/workflows': 'GitHub Actions CI/CD workflow definitions',
            '.vscode': 'Visual Studio Code editor configuration',
            'etc': 'Example files and supplementary resources',
            'handlers': 'HTTP request handlers for API endpoints',
            'handlers/js': 'JavaScript files for chart customization',
            'livedata': 'Live data streaming client components',
            'middleware': 'HTTP middleware for logging, CORS, and database access',
            'middleware/sql': 'SQL query templates for DuckDB operations',
            'sdk': 'Internal SDK types and utilities',
        }

        folder_str = str(folder_path)
        description = folder_descriptions.get(folder_str, f"Contains files and components for {folder_str}")

        doc_content = f"""# {folder_path if folder_path != Path('.') else 'Root'} - Documentation

## Purpose

{description}

## Contents

This directory contains the following components:

"""

        # Analyze files in this directory
        files = []
        for item in full_path.iterdir():
            if item.is_file() and not item.name.startswith('.') and not item.name.endswith(('.md', '.log')):
                # Get original file from repo
                if folder_path == Path('.'):
                    orig_file = self.repo_root / item.name.replace('_docs.md', '').replace('_kw.md', '')
                else:
                    orig_file = self.repo_root / folder_path / item.name.replace('_docs.md', '').replace('_kw.md', '')

                if not orig_file.exists():
                    continue

                files.append({
                    'name': item.name,
                    'path': orig_file,
                    'rel_path': orig_file.relative_to(self.repo_root)
                })

        if files:
            for file_info in sorted(files, key=lambda x: x['name']):
                # Try to determine file purpose
                fname = str(file_info['rel_path'])
                purpose = self.get_file_purpose(fname)
                if purpose:
                    doc_content += f"- **{file_info['rel_path']}**: {purpose}\n"

        doc_content += f"""

## Related Documentation

- [Folder Index](index.md)
- [Keyword Index](sub.md)

---
*Generated: {datetime.now().isoformat()}*
"""

        doc_file = full_path / "doc.md"
        with open(doc_file, 'w') as f:
            f.write(doc_content)

        return doc_file

    def get_file_purpose(self, filename):
        """Get human-readable purpose for a file"""
        purposes = {
            'main.go': 'Main application entry point, initializes web server and live data client',
            'go.mod': 'Go module definition with dependencies',
            'go.sum': 'Go module dependency checksums',
            'README.md': 'Project documentation and usage guide',
            'LICENSE.txt': 'MIT License text',
            'Dockerfile': 'Docker container image definition',
            'Taskfile.yml': 'Task automation and build configuration',
            '.gitignore': 'Git ignore patterns',
            '.dockerignore': 'Docker ignore patterns',
            '.vscode/launch.json': 'VS Code debugger configuration',
            '.github/workflows/docker.yml': 'GitHub Actions workflow for Docker builds',
            '.github/workflows/go.yml': 'GitHub Actions workflow for Go builds',
            'handlers/registry.go': 'HTTP route registration and OpenAPI setup',
            'handlers/get_charts.go': 'Chart generation endpoints',
            'handlers/get_last_trades.go': 'Last trades API endpoints (JSON/CSV/Excel)',
            'handlers/get_ohlcv.go': 'OHLCV candlestick data endpoints',
            'livedata/client.go': 'Databento live stream client implementation',
            'livedata/config.go': 'Live data client configuration',
            'middleware/cors.go': 'CORS middleware for cross-origin requests',
            'middleware/db.go': 'Database connection middleware',
            'middleware/logger.go': 'Structured logging middleware',
            'middleware/util.go': 'Middleware utility functions',
            'sdk/types.go': 'Custom type definitions and data structures',
        }

        return purposes.get(filename, '')

    def collect_keywords_from_folder(self, folder_path):
        """Collect all keywords from a folder's _kw.md files"""
        full_path = self.docs_dir / folder_path if folder_path != Path('.') else self.docs_dir
        keywords = {}

        for kw_file in full_path.glob('*_kw.md'):
            try:
                with open(kw_file, 'r') as f:
                    content = f.read()

                # Simple parsing of keywords
                current_keyword = None
                current_letter = None

                for line in content.split('\n'):
                    if line.startswith('## ') and len(line) == 4:  # Letter header
                        current_letter = line[3]
                    elif line.startswith('### '):  # Keyword
                        current_keyword = line[4:].strip()
                        if current_letter and current_keyword:
                            if current_letter not in keywords:
                                keywords[current_letter] = []
                            keywords[current_letter].append({
                                'keyword': current_keyword,
                                'file': kw_file.name.replace('_kw.md', '')
                            })
            except:
                pass

        return keywords

    def create_folder_sub(self, folder_path):
        """Create sub.md (keyword aggregation) for a folder"""
        full_path = self.docs_dir / folder_path if folder_path != Path('.') else self.docs_dir

        # Collect keywords from this folder and subfolders
        keywords = self.collect_keywords_from_folder(folder_path)

        # Recursively collect from subfolders
        for item in full_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                sub_folder = folder_path / item.name if folder_path != Path('.') else Path(item.name)
                sub_keywords = self.collect_keywords_from_folder(sub_folder)

                # Merge keywords
                for letter, kw_list in sub_keywords.items():
                    if letter not in keywords:
                        keywords[letter] = []
                    keywords[letter].extend(kw_list)

        # Create sub.md
        sub_content = f"""# {folder_path if folder_path != Path('.') else 'Root'} - Keyword Index

## Overview
Aggregated keywords from all files in this directory and subdirectories.

"""

        if keywords:
            for letter in sorted(keywords.keys()):
                sub_content += f"## {letter}\n\n"
                # Deduplicate keywords
                seen = set()
                for kw_info in keywords[letter]:
                    kw_key = kw_info['keyword']
                    if kw_key not in seen:
                        seen.add(kw_key)
                        sub_content += f"### {kw_info['keyword']}\n"
                        sub_content += f"**Source**: {kw_info['file']}\n\n"
        else:
            sub_content += "*No keywords found*\n\n"

        sub_content += f"""---
*Generated: {datetime.now().isoformat()}*
"""

        sub_file = full_path / "sub.md"
        with open(sub_file, 'w') as f:
            f.write(sub_content)

        return sub_file

    def generate_all_folder_docs(self):
        """Generate index.md, doc.md, sub.md for all folders"""
        folders = self.get_all_folders()

        print(f"Generating folder documentation for {len(folders)} folders...")

        for folder in folders:
            print(f"  Processing {folder}...")
            self.create_folder_index(folder)
            self.create_folder_doc(folder)
            self.create_folder_sub(folder)

        print(f"Created documentation for {len(folders)} folders")
        return len(folders) * 3  # 3 files per folder

# Main execution
if __name__ == "__main__":
    gen = FolderIndexGenerator("/home/user/dbn-duckduck-goose")
    docs_created = gen.generate_all_folder_docs()

    print(f"\nFolder documentation generation complete!")
    print(f"Total folder docs created: {docs_created}")
