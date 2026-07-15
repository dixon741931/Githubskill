"""Verify Shopify collections + product_type for the desk-first shop structure.

Usage:
    python scripts/hermes-verify-collections.py

Reads SHOPIFY_API_KEY from /d/my_bot/.env, probes the live store,
and writes a JSON report to %TEMP%/hermes-verify-collections.json.
"""
import os, sys, json, requests

try:
    from dotenv import load_dotenv  # optional
    load_dotenv('/d/my_bot/.env')
except Exception:
    pass

API_KEY = os.environ.get('SHOPIFY_API_KEY')
if not API_KEY:
    for p in ['/d/my_bot/.env']:
        if os.path.exists(p):
            with open(p, encoding='utf-8-sig') as fh:
                for line in fh:
                    line=line.strip()
                    if line.startswith('SHOPIFY_API_KEY='):
                        API_KEY=line.split('=',1)[1].strip().strip('"').strip("'")
                        break
            if API_KEY:
                break

if not API_KEY:
    print('NO_API_KEY')
    sys.exit(1)

SHOP = 'dbd9ub-8a.myshopify.com'
BASE = f'https://{SHOP}/admin/api/2024-01'
HEADERS = {'X-Shopify-Access-Token': API_KEY}

# Update these when the classification changes.
EXPECTED_TYPE_BY_HANDLE_PREFIX = {
    "clay-arch-mouse-pad": "Desk Mats",
    "greige-travertine-mouse-pad": "Desk Mats",
    "sage-line-art-desk-mat": "Desk Mats",
    "terracotta-dune-desk-mat": "Desk Mats",
    "cushioned-ergo-mouse-mat": "Desk Mats",
    "ultimate-office-enhancer-mouse-pad": "Desk Mats",
    "rawlins-leather-desk-pads": "Desk Mats",
    "leather-mouse-pad": "Desk Mats",
    "oat-minimalist-desk-mat": "Desk Mats",
    "leather-coaster-circular-set-4": "Desk Accessories",
    "leather-journal": "Desk Accessories",
    "lifetime-valet-tray": "Desk Accessories",
    "deskmate-wooden-headphone-organizer": "Desk Accessories",
    "silvershield-airpods-max-stand": "Desk Accessories",
    "sleekhead-desktop-headphone-holder": "Desk Accessories",
    "unite-desk-organizer": "Desk Accessories",
    "cozy-cabin": "Desk Lighting",
    "readease-portable-desk-lamp": "Desk Lighting",
    "sleek-touch-led-desk-lamp": "Desk Lighting",
    "spracht-flex-charge": "Charging Station",
    "lunarglow-wireless-charger": "Charging Station",
    "magnetic-6-pack-cable-clip": "Cable Management",
    "sleek-under-desk-cable-organizer": "Cable Management",
    "clay-horizon": "Wall Art",
    "dried-botanical-study": "Wall Art",
    "plaster-arch-textured-relief": "Wall Art",
    "terracotta-vessels-still-life": "Wall Art",
    "tonal-fields-color-field": "Wall Art",
    "quiet-night-earplugs": "Sleep",
    "soothing-jellyfish-led-mood-lamp": "Sleep",
    "titanium-gear-fidget-ring": "Desk Toys",
}

EXPECTED_COLLECTION_BY_TYPE = {
    "Desk Mats": 314864173135,
    "Desk Accessories": 314864205903,
    "Desk Lighting": 314864238671,
    "Charging Station": 314864271439,
    "Cable Management": 314864304207,
    "Wall Art": 314864336975,
    "Sleep": 314864369743,
    "Desk Toys": 314864402511,
}


def paginate(url, params, headers):
    out = []
    while url:
        r = requests.get(url, params=params, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        key = 'products' if 'products' in data else 'collects'
        chunk = data.get(key, [])
        out.extend(chunk)
        link = r.headers.get('Link', '')
        url = None
        params = None
        if 'rel="next"' in link:
            urls = [u.strip().split(';')[0].strip('<>') for u in link.split(',') if 'rel="next"' in u]
            if urls:
                url = urls[0]
    return out


def main():
    products = paginate(f'{BASE}/products.json', {'limit': 250}, HEADERS)
    collects = paginate(f'{BASE}/collects.json', {'limit': 250}, HEADERS)

    by_pid = {}
    for c in collects:
        by_pid.setdefault(c['product_id'], []).append(c['collection_id'])

    ok = 0
    fail = 0
    rows = []
    for p in products:
        pid = p['id']
        expected_type = None
        for prefix, t in EXPECTED_TYPE_BY_HANDLE_PREFIX.items():
            if p['handle'] == prefix or p['handle'].startswith(prefix):
                expected_type = t
                break
        expected_cid = EXPECTED_COLLECTION_BY_TYPE.get(expected_type)
        actual_type = (p.get('product_type') or '').strip()
        actual_cids = by_pid.get(pid, [])
        type_ok = actual_type == expected_type
        coll_ok = expected_cid in actual_cids if expected_cid else False
        if type_ok and coll_ok:
            ok += 1
        else:
            fail += 1
            rows.append({
                'pid': pid,
                'handle': p['handle'],
                'expected_type': expected_type,
                'actual_type': actual_type,
                'expected_cid': expected_cid,
                'actual_cids': actual_cids,
            })

    print('live_products', len(products))
    print('type_ok', ok, 'type_fail', fail)
    for row in rows:
        print('FAIL', row)

    counts = {}
    for cid in EXPECTED_COLLECTION_BY_TYPE.values():
        counts[cid] = sum(1 for arr in by_pid.values() if cid in arr)
    print('collection counts:', counts)
    print('overall', 'pass' if fail == 0 else f'issues:{fail}')

    out = os.path.join(os.environ.get('TEMP', '/tmp'), 'hermes-verify-collections.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({
            'overall': 'pass' if fail == 0 else 'issues',
            'ok': ok,
            'fail': fail,
            'live_products': len(products),
            'fails': rows,
            'collection_counts': {str(k): v for k, v in counts.items()},
        }, f, ensure_ascii=False, indent=2)
    print('report', out)


if __name__ == '__main__':
    main()
