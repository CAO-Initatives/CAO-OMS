#!/usr/bin/env python3
from pathlib import Path
import re, sys, hashlib
ROOT=Path(__file__).resolve().parent
INDEX=ROOT/'index.html'; OMS=ROOT/'oms.html'
def check(name,ok): print(('PASS' if ok else 'FAIL')+': '+name); return ok
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
r=[]
r += [check('index.html exists',INDEX.exists()),check('oms.html exists',OMS.exists())]
if not all(r):sys.exit(2)
i=INDEX.read_text(encoding='utf-8');o=OMS.read_text(encoding='utf-8')
tests=[
('OMS login page identified','CAO OMS Sign In' in i),('OMS application identified','CAO Operations Management System (OMS)' in o),('v1.4.0 output identified','v1.4.0' in o),('Gateway URL present','https://cao-oms-gateway.vercel.app' in i and 'https://cao-oms-gateway.vercel.app' in o),('Login endpoint present','/api/login' in i),('State endpoint present','/api/state' in o),('Operation endpoint present','/api/operation' in o),('Shared password removed','SITE_PASSWORD' not in i and 'CAO-OMS-2026!' not in i),('Legacy access flag removed','cao_oms_gate_access' not in i),('Session storage used','sessionStorage' in i and 'sessionStorage' in o),('Sign Out present',bool(re.search(r'Sign Out',o,re.I))),('Sync states present',all(x.lower() in o.lower() for x in ['Connected','Sync pending','Synced','Unsynced'])),('User Guide present','User Guide' in o),('User Guide updated','Authentication required' in o and 'shared canonical' in o),('No private key in index','BEGIN PRIVATE KEY' not in i and 'BEGIN RSA PRIVATE KEY' not in i),('No private key in OMS','BEGIN PRIVATE KEY' not in o and 'BEGIN RSA PRIVATE KEY' not in o),('Dashboard retained','Dashboard' in o),('Weekly Brief retained','Weekly Brief' in o),('CAO Visibility retained','CAO Visibility' in o),('Calendars retained','Calendars' in o),('Cadence retained','Cadence (RoB)' in o),('SOPs retained','SOPs' in o),('Deliverables retained','Deliverables' in o),('People retained','People' in o),('Notifications retained','Notifications' in o)]
for n,v in tests:r.append(check(n,v))
print('\nSHA256 index.html',sha(INDEX));print('SHA256 oms.html  ',sha(OMS))
f=sum(not x for x in r);print(f'\nSUMMARY: {len(r)-f} passed, {f} failed');sys.exit(1 if f else 0)
