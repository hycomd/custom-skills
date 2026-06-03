#!/usr/bin/env python3
"""
embed-images.py — Post-process HTML to replace image placeholders with base64 data URIs.

Usage:
    python embed-images.py <html-file> [--content-dir <dir>] [--max-size <bytes>]

Placeholders in HTML:
    __IMG__:relative/path/to/image.png__
    __IMG__:https://example.com/image.png__

Placeholders can appear in:
    - <img src="__IMG__:path__">
    - <img src="__IMG__:url__">

This script:
    1. Reads the HTML file
    2. Finds all __IMG__:... placeholders
    3. For each: reads the image file (or downloads), base64-encodes, builds data URI
    4. Replaces placeholders with data URIs
    5. Writes the updated HTML back (in-place)
"""

import sys
import os
import re
import base64
import json
import urllib.request
import urllib.parse
import tempfile

PLACEHOLDER_RE = re.compile(r'__IMG__:(.+?)__')
MAX_SIZE_DEFAULT = 10 * 1024 * 1024  # 10 MB

MIME_MAP = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp',
    '.ico': 'image/x-icon',
    '.avif': 'image/avif',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
}


def guess_mime(path_or_url):
    """Guess MIME type from file extension in path or URL."""
    # Strip query string and fragment
    clean = urllib.parse.urlparse(path_or_url).path
    _, ext = os.path.splitext(clean.lower())
    return MIME_MAP.get(ext, 'image/png')


def encode_local(path, max_size):
    """Read a local file and return (data_uri, size_bytes) or None if failed."""
    if not os.path.isfile(path):
        return None
    size = os.path.getsize(path)
    if size > max_size:
        print(f"  SKIP (too large): {path} ({size} bytes)", file=sys.stderr)
        return None
    with open(path, 'rb') as f:
        data = f.read()
    mime = guess_mime(path)
    b64 = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{b64}', size


def encode_remote(url, max_size):
    """Download a URL and return (data_uri, size_bytes) or None if failed."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'html-standalone/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read(max_size + 1)
            if len(data) > max_size:
                print(f"  SKIP (too large): {url} ({len(data)} bytes)", file=sys.stderr)
                return None
        mime = guess_mime(url)
        # Try to get MIME from Content-Type header
        ct = resp.headers.get('Content-Type', '')
        if ct and ct.startswith('image/'):
            mime = ct.split(';')[0].strip()
        b64 = base64.b64encode(data).decode('ascii')
        return f'data:{mime};base64,{b64}', len(data)
    except Exception as e:
        print(f"  FAIL (download): {url} — {e}", file=sys.stderr)
        return None


def process(html_path, content_dir=None, max_size=MAX_SIZE_DEFAULT):
    """Process HTML file, replace image placeholders with data URIs."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    placeholders = PLACEHOLDER_RE.findall(html)
    if not placeholders:
        print("No image placeholders found.")
        return

    # Deduplicate
    seen = {}
    for ref in placeholders:
        if ref not in seen:
            seen[ref] = None

    print(f"Found {len(seen)} unique image(s) to embed:")
    total_bytes = 0
    embedded = 0
    failed = 0

    for ref in seen:
        is_url = ref.startswith('http://') or ref.startswith('https://')

        if is_url:
            print(f"  [remote] {ref}")
            result = encode_remote(ref, max_size)
        else:
            # Resolve relative to content_dir
            if content_dir and not os.path.isabs(ref):
                full_path = os.path.join(content_dir, ref)
            else:
                full_path = ref
            full_path = os.path.normpath(full_path)
            print(f"  [local]  {ref} -> {full_path}")
            result = encode_local(full_path, max_size)

        if result:
            data_uri, size = result
            seen[ref] = data_uri
            total_bytes += size
            embedded += 1
            print(f"           OK ({size:,} bytes)")
        else:
            failed += 1

    # Replace placeholders
    def replacer(m):
        ref = m.group(1)
        if seen[ref]:
            return seen[ref]
        # Keep original reference if encoding failed
        return m.group(0)

    html = PLACEHOLDER_RE.sub(replacer, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    out_size = os.path.getsize(html_path)
    print(f"\nDone: {embedded} embedded, {failed} failed")
    print(f"Image data: {total_bytes:,} bytes raw -> {out_size:,} bytes HTML total")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

    html_path = args[0]
    content_dir = None
    max_size = MAX_SIZE_DEFAULT

    i = 1
    while i < len(args):
        if args[i] == '--content-dir' and i + 1 < len(args):
            content_dir = args[i + 1]
            i += 2
        elif args[i] == '--max-size' and i + 1 < len(args):
            max_size = int(args[i + 1])
            i += 2
        else:
            i += 1

    if not os.path.isfile(html_path):
        print(f"Error: file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    process(html_path, content_dir, max_size)


if __name__ == '__main__':
    main()
