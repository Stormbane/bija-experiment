"""Build a stratified 36-probe subset from soul_probes.yml.

4 probes per domain × 9 domains = 36 total. Deterministic: takes the first
4 of each domain in declared order. Used for phase 1 signal indication
while inference speed is PyTorch-SDPA-limited.
"""

import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
FULL = ROOT / "data" / "probes" / "soul_probes.yml"
SUBSET = ROOT / "data" / "probes" / "soul_probes_subset.yml"

N_PER_DOMAIN = 4

probes = yaml.safe_load(open(FULL, encoding="utf-8"))

by_domain = defaultdict(list)
for p in probes:
    by_domain[p["domain"]].append(p)

subset = []
for domain, items in by_domain.items():
    subset.extend(items[:N_PER_DOMAIN])

# Keep original ordering: sort by ID to preserve intuitive order
subset.sort(key=lambda p: p["id"])

print(f"Full: {len(probes)} probes across {len(by_domain)} domains")
print(f"Subset: {len(subset)} probes ({N_PER_DOMAIN} per domain)")
print()
for p in subset:
    print(f"  {p['id']:<6} [{p['domain']:<18}] {p['probe'][:80]}")

with open(SUBSET, "w", encoding="utf-8") as f:
    yaml.dump(
        subset,
        f,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=120,
    )
print(f"\nwrote {SUBSET.relative_to(ROOT)}")
