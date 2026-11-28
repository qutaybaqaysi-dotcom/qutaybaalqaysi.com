"""Read the IPTC/XMP caption fields from a Lightroom export and print them as JSON.

Usage: python3 tools/caption.py image.jpg
Title comes from IPTC Title; year, medium and size come from the
Description (Caption) lines written in Lightroom: title, year, medium, size.
"""
import html, json, re, sys
from PIL import Image

def xmp_text(x, tag):
    m = re.search(r'<%s>(.*?)</%s>' % (tag, tag), x, re.S)
    if not m:
        return ''
    li = re.findall(r'<rdf:li[^>]*>(.*?)</rdf:li>', m.group(1), re.S)
    return html.unescape(li[0] if li else m.group(1)).strip()

def caption(path):
    x = Image.open(path).info.get('xmp', b'')
    x = x.decode('utf-8', 'replace') if isinstance(x, bytes) else x
    lines = [l.strip() for l in xmp_text(x, 'dc:description').splitlines() if l.strip()]
    return {
        'artist': xmp_text(x, 'dc:creator'),
        'title': xmp_text(x, 'dc:title') or (lines[0] if lines else ''),
        'year': lines[1] if len(lines) > 1 else '',
        'medium': lines[2] if len(lines) > 2 else '',
        'size': lines[3] if len(lines) > 3 else '',
        'description_title': lines[0] if lines else '',
    }

if __name__ == '__main__':
    print(json.dumps(caption(sys.argv[1]), indent=2, ensure_ascii=False))
