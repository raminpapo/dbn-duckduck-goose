# repo_book_gen.py - Documentation

## File Metadata
- **File Path**: `repo_book_gen.py`
- **File Type**: text
- **File Size**: 15,561 bytes
- **Language**: python
- **Last Modified**: 2025-11-15T20:34:36.636354

## Original Source

```python
#!/usr/bin/env python3
"""
World's Best Repo Book Generator
Generates comprehensive documentation for entire repository
"""

import os
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
import subprocess
import re

class RepoBookGenerator:
    def __init__(self, repo_root, docs_dir="docs"):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / docs_dir
        self.repo_fingerprint = None
        self.file_map = {}
        self.docs_created = []
        self.errors = []
        self.total_words = 0
        self.total_bytes = 0
        self.progress_log = []

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

    def classify_file(self, filepath):
        """Classify file as text, binary, or large"""
        try:
            size = filepath.stat().st_size

            # Check size
            if size > 100 * 1024 * 1024:  # > 100MB
                return "very_large", size

            # Check MIME type
            mime_type, _ = mimetypes.guess_type(str(filepath))
            if mime_type and mime_type.startswith('image/'):
                return "binary_image", size

            # Try to read as text
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    f.read(100)  # Try reading first 100 bytes
                return "text", size
            except:
                return "binary", size

        except Exception as e:
            return "error", 0

    def scan_repository(self):
        """Scan and classify all files"""
        print("Scanning repository...")

        self.repo_fingerprint = self.get_git_sha()

        for item in self.repo_root.rglob('*'):
            if '.git' in item.parts or 'docs' in item.parts:
                continue

            if item.is_file():
                rel_path = item.relative_to(self.repo_root)
                file_type, size = self.classify_file(item)

                self.file_map[str(rel_path)] = {
                    'path': str(rel_path),
                    'size': size,
                    'type': file_type,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }

        print(f"Found {len(self.file_map)} files")
        return len(self.file_map)

    def generate_file_docs(self, filepath):
        """Generate _docs.md and _kw.md for a single file"""
        try:
            rel_path = Path(filepath)
            file_info = self.file_map.get(str(rel_path))

            if not file_info:
                return False

            # Determine output paths
            if rel_path.parent == Path('.'):
                docs_path = self.docs_dir
            else:
                docs_path = self.docs_dir / rel_path.parent

            docs_path.mkdir(parents=True, exist_ok=True)

            # Read file content
            full_path = self.repo_root / rel_path

            if file_info['type'] == 'binary_image':
                content = f"Binary image file: {rel_path.name}\nSize: {file_info['size']} bytes\nType: Image"
                keywords = []
            elif file_info['type'] != 'text':
                content = f"Binary file: {rel_path.name}\nSize: {file_info['size']} bytes"
                keywords = []
            else:
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    keywords = self.extract_keywords(content, rel_path)
                except Exception as e:
                    self.errors.append(f"Failed to read {rel_path}: {e}")
                    return False

            # Generate docs file
            docs_md = self.create_docs_content(rel_path, content, file_info)
            docs_file = docs_path / f"{rel_path.name}_docs.md"

            with open(docs_file, 'w', encoding='utf-8') as f:
                f.write(docs_md)

            self.docs_created.append(str(docs_file.relative_to(self.repo_root)))
            self.total_words += len(docs_md.split())
            self.total_bytes += len(docs_md.encode('utf-8'))

            # Generate keywords file
            if keywords or file_info['type'] == 'text':
                kw_md = self.create_keywords_content(rel_path, keywords, content)
                kw_file = docs_path / f"{rel_path.name}_kw.md"

                with open(kw_file, 'w', encoding='utf-8') as f:
                    f.write(kw_md)

                self.docs_created.append(str(kw_file.relative_to(self.repo_root)))
                self.total_bytes += len(kw_md.encode('utf-8'))

            # Log progress
            self.progress_log.append({
                'file': str(rel_path),
                'docs_created': 2 if keywords or file_info['type'] == 'text' else 1,
                'bytes': file_info['size'],
                'status': 'success'
            })

            return True

        except Exception as e:
            self.errors.append(f"Error processing {filepath}: {e}")
            self.progress_log.append({
                'file': str(filepath),
                'status': 'error',
                'error': str(e)
            })
            return False

    def extract_keywords(self, content, filepath):
        """Extract keywords from file content"""
        keywords = set()

        # Extract function/method names
        func_pattern = r'func\s+(\w+)|def\s+(\w+)|function\s+(\w+)|class\s+(\w+)'
        for match in re.finditer(func_pattern, content):
            for group in match.groups():
                if group:
                    keywords.add(group)

        # Extract type names (Go structs, interfaces)
        type_pattern = r'type\s+(\w+)\s+(struct|interface)'
        for match in re.finditer(type_pattern, content):
            keywords.add(match.group(1))

        # Extract constants and variables
        const_pattern = r'(const|var)\s+(\w+)'
        for match in re.finditer(const_pattern, content):
            keywords.add(match.group(2))

        # Extract imports/packages
        import_pattern = r'import\s+["\']([^"\']+)["\']|from\s+(\w+)\s+import'
        for match in re.finditer(import_pattern, content):
            for group in match.groups():
                if group:
                    parts = group.split('/')
                    if parts:
                        keywords.add(parts[-1])

        return sorted(list(keywords))

    def create_docs_content(self, filepath, content, file_info):
        """Create comprehensive documentation content for a file"""

        # Detect language
        ext = filepath.suffix
        lang_map = {
            '.go': 'go',
            '.py': 'python',
            '.js': 'javascript',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.md': 'markdown',
            '.txt': 'text',
            '.sql': 'sql',
            '.sh': 'bash',
        }
        lang = lang_map.get(ext, 'text')

        docs = f"""# {filepath.name} - Documentation

## File Metadata
- **File Path**: `{filepath}`
- **File Type**: {file_info['type']}
- **File Size**: {file_info['size']:,} bytes
- **Language**: {lang}
- **Last Modified**: {file_info['modified']}

## Original Source

"""

        if file_info['type'] == 'text' and len(content) < 500000:
            docs += f"""```{lang}
{content}
```

"""
        elif file_info['type'] == 'text':
            docs += f"""**Note**: File is very large ({file_info['size']:,} bytes). Showing first 100KB:

```{lang}
{content[:100000]}
... (truncated)
```

"""
        else:
            docs += f"""**Note**: Binary file, content not displayed.

"""

        # Add analysis sections
        if file_info['type'] == 'text':
            docs += self.analyze_file_content(filepath, content, lang)

        docs += f"""
---
*Generated by World's Best Repo Book Generator v1.0*
*Generated: {datetime.now().isoformat()}*
"""

        return docs

    def analyze_file_content(self, filepath, content, lang):
        """Analyze and document file content"""
        analysis = """
## High-Level Overview

"""

        lines = content.split('\n')
        line_count = len(lines)

        if lang == 'go':
            analysis += self.analyze_go_file(content, lines)
        elif lang == 'python':
            analysis += self.analyze_python_file(content, lines)
        elif lang == 'javascript':
            analysis += self.analyze_js_file(content, lines)
        elif lang in ['yaml', 'yml']:
            analysis += self.analyze_yaml_file(content, lines)
        elif lang == 'markdown':
            analysis += f"This is a Markdown documentation file with {line_count} lines.\n\n"
        else:
            analysis += f"This file contains {line_count} lines of {lang} code.\n\n"

        return analysis

    def analyze_go_file(self, content, lines):
        """Analyze Go source file"""
        analysis = f"This is a Go source file with {len(lines)} lines.\n\n"

        # Find package
        pkg_match = re.search(r'package\s+(\w+)', content)
        if pkg_match:
            analysis += f"**Package**: `{pkg_match.group(1)}`\n\n"

        # Find imports
        imports = re.findall(r'import\s+(?:\(([^)]+)\)|"([^"]+)")', content)
        if imports:
            analysis += "**Imports**:\n"
            for imp_group in imports:
                for imp in imp_group:
                    if imp.strip():
                        for line in imp.split('\n'):
                            line = line.strip().strip('"')
                            if line:
                                analysis += f"- `{line}`\n"
            analysis += "\n"

        # Find types
        types = re.findall(r'type\s+(\w+)\s+(struct|interface)', content)
        if types:
            analysis += "**Types Defined**:\n"
            for type_name, type_kind in types:
                analysis += f"- `{type_name}` ({type_kind})\n"
            analysis += "\n"

        # Find functions
        funcs = re.findall(r'func\s+(?:\([\w\s\*]+\)\s+)?(\w+)\s*\(', content)
        if funcs:
            analysis += f"**Functions/Methods**: {len(funcs)} defined\n\n"

        return analysis

    def analyze_python_file(self, content, lines):
        """Analyze Python source file"""
        analysis = f"This is a Python source file with {len(lines)} lines.\n\n"

        # Find imports
        imports = re.findall(r'(?:from\s+[\w\.]+\s+)?import\s+([^\n]+)', content)
        if imports:
            analysis += f"**Imports**: {len(imports)} import statements\n\n"

        # Find classes
        classes = re.findall(r'class\s+(\w+)', content)
        if classes:
            analysis += f"**Classes**: {', '.join(classes)}\n\n"

        # Find functions
        funcs = re.findall(r'def\s+(\w+)\s*\(', content)
        if funcs:
            analysis += f"**Functions/Methods**: {len(funcs)} defined\n\n"

        return analysis

    def analyze_js_file(self, content, lines):
        """Analyze JavaScript source file"""
        analysis = f"This is a JavaScript source file with {len(lines)} lines.\n\n"

        # Find functions
        funcs = re.findall(r'function\s+(\w+)|const\s+(\w+)\s*=\s*(?:\([^)]*\)|[\w]+)\s*=>', content)
        if funcs:
            func_names = [f[0] or f[1] for f in funcs if f[0] or f[1]]
            analysis += f"**Functions**: {len(func_names)} defined\n\n"

        return analysis

    def analyze_yaml_file(self, content, lines):
        """Analyze YAML configuration file"""
        analysis = f"This is a YAML configuration file with {len(lines)} lines.\n\n"

        # Find top-level keys
        top_keys = re.findall(r'^(\w+):', content, re.MULTILINE)
        if top_keys:
            analysis += f"**Top-level configuration keys**: {', '.join(set(top_keys))}\n\n"

        return analysis

    def create_keywords_content(self, filepath, keywords, content):
        """Create keywords index file"""

        kw_md = f"""# {filepath.name} - Keywords Index

"""

        if not keywords:
            kw_md += """*No keywords extracted*

"""
            return kw_md

        # Group by first letter
        grouped = {}
        for kw in keywords:
            first_letter = kw[0].upper()
            if first_letter not in grouped:
                grouped[first_letter] = []
            grouped[first_letter].append(kw)

        for letter in sorted(grouped.keys()):
            kw_md += f"## {letter}\n\n"
            for kw in sorted(grouped[letter]):
                kw_md += f"### {kw}\n"
                kw_md += f"**Type**: Identifier\n"
                kw_md += f"**File**: [{filepath}]({filepath.name}_docs.md)\n"

                # Try to find context
                context = self.find_keyword_context(kw, content)
                if context:
                    kw_md += f"**Context**: {context}\n"

                kw_md += "\n"

        kw_md += f"""---
*Generated by World's Best Repo Book Generator v1.0*
*Generated: {datetime.now().isoformat()}*
"""

        return kw_md

    def find_keyword_context(self, keyword, content):
        """Find context for a keyword in content"""
        patterns = [
            (rf'func\s+{keyword}\s*\(', 'Function'),
            (rf'type\s+{keyword}\s+struct', 'Struct type'),
            (rf'type\s+{keyword}\s+interface', 'Interface type'),
            (rf'const\s+{keyword}\s*=', 'Constant'),
            (rf'var\s+{keyword}\s', 'Variable'),
            (rf'class\s+{keyword}', 'Class'),
            (rf'def\s+{keyword}\s*\(', 'Function'),
        ]

        for pattern, description in patterns:
            if re.search(pattern, content):
                return description

        return None

# Main execution
if __name__ == "__main__":
    gen = RepoBookGenerator("/home/user/dbn-duckduck-goose")

    # Scan repository
    file_count = gen.scan_repository()
    print(f"Repository fingerprint: {gen.repo_fingerprint}")

    # Process all files
    print("\nGenerating documentation for all files...")
    processed = 0
    for filepath in sorted(gen.file_map.keys()):
        if gen.generate_file_docs(filepath):
            processed += 1
            if processed % 5 == 0:
                print(f"Processed {processed}/{file_count} files...")

    print(f"\nGeneration complete!")
    print(f"Files processed: {processed}/{file_count}")
    print(f"Docs created: {len(gen.docs_created)}")
    print(f"Total words: {gen.total_words:,}")
    print(f"Total bytes: {gen.total_bytes:,}")
    print(f"Errors: {len(gen.errors)}")

    # Save progress log
    progress_file = gen.docs_dir / ".progress.log"
    with open(progress_file, 'w') as f:
        json.dump(gen.progress_log, f, indent=2)

    print(f"\nProgress log saved to {progress_file}")

    # Print summary
    summary = {
        "repo_source": str(gen.repo_root),
        "repo_fingerprint": gen.repo_fingerprint,
        "files_scanned": file_count,
        "docs_created": len(gen.docs_created),
        "words_estimated": gen.total_words,
        "bytes_written": gen.total_bytes,
        "errors": gen.errors
    }

    print("\n" + "="*60)
    print("SUMMARY:")
    print(json.dumps(summary, indent=2))
    print("="*60)

```


## High-Level Overview

This is a Python source file with 474 lines.

**Imports**: 9 import statements

**Classes**: RepoBookGenerator

**Functions/Methods**: 14 defined


---
*Generated by World's Best Repo Book Generator v1.0*
*Generated: 2025-11-15T20:34:43.930025*
