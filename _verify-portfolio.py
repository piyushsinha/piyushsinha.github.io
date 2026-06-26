#!/usr/bin/env python3
"""Ad-hoc verification for piyushsinha.com copy rewrite."""

import yaml
import re
import sys
import os

BASE = "/Users/piyush/Library/Mobile Documents/com~apple~CloudDocs/Piyush/Github/piyushsinha/piyushsinha.github.io"
errors = []
passes = 0

def check(name, condition, detail=""):
    global passes
    if condition:
        passes += 1
        print(f"  ✓ {name}")
    else:
        errors.append(name)
        print(f"  ✗ {name} {detail}")

# ── 1. YAML validation ─────────────────────────────────────────────
print("\n[1] _data/case_studies.yml")
yml_path = os.path.join(BASE, "_data", "case_studies.yml")
with open(yml_path) as f:
    data = yaml.safe_load(f)

check("YAML parses without error", data is not None)
check("Has 10 entries (8 case studies + intro deck + keynote)", len(data) == 10)

# Verify all embed URLs preserved
for entry in data:
    if 'embed_url' in entry:
        check(f"Embed URL preserved for {entry['id']}", 
              'pubembed' in entry['embed_url'])

# Verify case study titles match new copy
expected_titles = {
    'agoda-5mm': "The $5MM Question Nobody Was Asking",
    'xendit-golive': "From 30 Days to 14: Rebuilding Trust at Sign-Up",
    'agoda-hidden-behaviors': "What Users Do When They Think No One's Watching",
    'brankas-tap': "Teaching 15 Countries to Trust a New Kind of Bank",
    'agoda-booking-form': "The Booking Form That Never Stopped Improving",
    'agoda-hcd': "Turning a 5,000-Person Company Into Researchers",
    'xendit-xendesign': "One Design System, Four Companies, Half the Cost",
    'uxhh-bangkok': "The Bar Where Bangkok's Designers Actually Talk to Each Other",
}

for entry in data:
    if entry.get('type') == 'case-study' and entry['id'] in expected_titles:
        check(f"Title correct for {entry['id']}", 
              entry['title'] == expected_titles[entry['id']],
              f"got: {entry['title']}")

# Verify Before/Bet/Proof structure in outcomes (uses <strong> HTML tags)
for entry in data:
    if entry.get('type') == 'case-study':
        outcome = entry.get('outcome', '')
        has_before = '<strong>Before:</strong>' in outcome or '**Before:**' in outcome
        has_bet = '<strong>The bet:</strong>' in outcome or '**The bet:**' in outcome
        has_proof = '<strong>The proof:</strong>' in outcome or '**The proof:**' in outcome
        check(f"Before/Bet/Proof structure for {entry['id']}", 
              has_before and has_bet and has_proof,
              f"missing: before={has_before}, bet={has_bet}, proof={has_proof}")

# Verify company names & domains preserved
for entry in data:
    if entry.get('type') == 'case-study':
        check(f"Company name preserved for {entry['id']}", 
              entry.get('company', '') != '',
              f"got: {entry.get('company')}")
        check(f"Domain tag preserved for {entry['id']}", 
              entry.get('domain', '') != '',
              f"got: {entry.get('domain')}")

# ── 2. About page validation ───────────────────────────────────────
print("\n[2] about/index.html")
about_path = os.path.join(BASE, "about", "index.html")
with open(about_path) as f:
    about = f.read()

# Front matter unchanged
check("Front matter has layout: default", 'layout: default' in about)
check("Front matter title unchanged", '"Piyush Sinha - About"' in about or "'Piyush Sinha - About'" in about)
check("Front matter permalink unchanged", 'permalink: /about/' in about)

# New content present
check("New opening paragraph present", "I didn't set out to run design organizations" in about)
check("Old intro paragraph removed", "Design and product leader with 14+ years building and scaling functions across high-growth" not in about)

# Framing sentences present
check("PouchNATION framing", "A platform business spread across five regions doesn't fail" in about)
check("Appsynth framing", "Eighteen designers, four major clients, zero shared process" in about)
check("Brankas framing", "Open finance is a hard sell when people don't trust banks" in about)
check("aamzng framing", "I built a consultancy for the clients other consultancies turn down" in about)
check("Xendit framing", "Merchants were quitting before they ever processed a single payment" in about)
check("Agoda framing", "Agoda had never had a researcher" in about)
check("SimpleRelevance framing", "A three-person UX team, a dashboard nobody liked" in about)

# Community section updated
check("Community text updated", "Ten years ago, Bangkok's designers didn't really talk to each other" in about)
check("UX Happy Hour founder line preserved", "Founder — UX Happy Hour Bangkok" in about)

# Resume link preserved
check("Resume download link preserved", "drive.google.com/file/d/1Y5Fd-FNKKhOT_TBbQVKR0XwdPiwo8Fxv/view" in about)

# HTML structure intact
check("No unclosed <p> tags", about.count('<p') == about.count('</p>'))
check("No unclosed <ul> tags", about.count('<ul') == about.count('</ul>'))
check("No unclosed <li> tags", about.count('<li') == about.count('</li>'))
check("No unclosed <div> tags", about.count('<div') == about.count('</div>'))
check("No unclosed <section> tags", about.count('<section') == about.count('</section>'))

# ── 3. Connect page validation ─────────────────────────────────────
print("\n[3] connect/index.html")
connect_path = os.path.join(BASE, "connect", "index.html")
with open(connect_path) as f:
    connect = f.read()

# Front matter unchanged
check("Front matter has layout: default", 'layout: default' in connect)
check("Front matter permalink unchanged", 'permalink: /connect/' in connect)

# Heading changed
check("Heading is 'Let's Talk'", "Let's Talk" in connect)
check("Old heading 'Connect' removed from h1", '<h1>Connect</h1>' not in connect)

# New opening line present
check("New opening line present", "easiest message you'll send all week" in connect)

# Links preserved
check("LinkedIn link preserved", 'linkedin.com/in/itspiyushsinha' in connect)
check("X/Twitter link preserved", 'twitter.com/piyushsinha' in connect)
check("LunchClub link preserved", 'lunchclub.com/?invite_code=piyushs4' in connect)

# New content
check("Work enquiries bullet", "Work enquiries" in connect)
check("Mentorship bullet with ADPList note", "stepped away from ADPList" in connect)
check("Talk shop bullet", "Just want to talk shop" in connect)
check("Facebook/Instagram note", "close friends and family only" in connect)

# Email obfuscation script preserved
check("Email obfuscation script preserved", 'email-link' in connect and 'mailto:' in connect)

# HTML structure intact
check("No unclosed <p> tags", connect.count('<p') == connect.count('</p>'))
check("No unclosed <li> tags", connect.count('<li') == connect.count('</li>'))
check("No unclosed <div> tags", connect.count('<div') == connect.count('</div>'))

# ── 4. Home page (no changes expected) ─────────────────────────────
print("\n[4] index.html (unchanged verification)")
index_path = os.path.join(BASE, "index.html")
with open(index_path) as f:
    index = f.read()

check("Hero text already updated", "I build the teams — and the products" in index)
check("Impact section already updated", "I saved Agoda $5MM a year" in index)
check("About paragraph already updated", "building the function before the function existed" in index)
check("CTA section already updated", "Want to build something that actually works" in index)

# ── 5. Liquid template compatibility ───────────────────────────────
print("\n[5] Liquid template compatibility")
work_path = os.path.join(BASE, "work", "index.html")
with open(work_path) as f:
    work = f.read()

check("Work page renders outcome with replace filter", 
      "item.outcome" in work and "replace" in work,
      "outcome rendering may not handle multi-line strings")

# ── Summary ────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"Results: {passes} passed, {len(errors)} failed")
if errors:
    print(f"FAILURES:\n" + "\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
else:
    print("All checks passed.")
    sys.exit(0)
