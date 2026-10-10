#!/usr/bin/env python3
"""Conservative QA release policy: never interprets static warnings as proved defects."""
from __future__ import annotations
import argparse, json, pathlib
from datetime import datetime, timezone

STATES = ('BLOCKED','HOLD_FOR_REVIEW','READY_FOR_STAGING')

def evaluate(static: dict, game: dict|None=None, approvals: dict|None=None) -> dict:
    approvals=approvals or {}
    findings=static.get('findings', [])
    confirmed=[x for x in findings if x.get('review')=='confirmed']
    blocked_findings=[x for x in confirmed if x.get('severity') in ('major','critical')]
    candidates=[x for x in findings if x.get('review','candidate') not in ('confirmed','rejected')]
    coverage=static.get('autopilot',{}).get('coverage','UNKNOWN')
    all_tests=(game or {}).get('tests',[])
    failed=[x for x in all_tests if x.get('status') in ('FAIL','ERROR')]
    passed=[x for x in all_tests if x.get('status')=='PASS']
    unsupported=[x for x in all_tests if x.get('status') in ('NOT_RUN','SKIPPED','OBSERVED')]
    reasons=[]
    if blocked_findings: reasons.append(f'{len(blocked_findings)} confirmed major/critical issue(s)')
    if failed: reasons.append(f'{len(failed)} failed functional/browser test(s)')
    if blocked_findings or failed:state='BLOCKED'
    else:
        if static.get('quality_gate')=='INCOMPLETE' or coverage!='STATIC_ONLY':
            reasons.append('Static archive coverage incomplete or unknown')
        if candidates:reasons.append(f'{len(candidates)} unreviewed static candidate(s)')
        if not game or not passed:reasons.append('No evidenced passing functional tests')
        if unsupported:reasons.append(f'{len(unsupported)} unsupported or unexecuted game checks')
        if approvals.get('human_qa_approval') is not True:reasons.append('Human QA approval required')
        if approvals.get('security_privacy_review') is not True:reasons.append('Security/privacy review required')
        if approvals.get('deployment_target_verified') is not True:reasons.append('Staging/deployment target verification required')
        state='HOLD_FOR_REVIEW' if reasons else 'READY_FOR_STAGING'
    return {'schema':'alexqa.release_gate.v1','generated_at':datetime.now(timezone.utc).isoformat(),
            'source':static.get('name','unknown'),'static_gate':static.get('quality_gate','UNKNOWN'),
            'coverage':coverage,'decision':state,'reasons':reasons,
            'metrics':{'candidates_unreviewed':len(candidates),'confirmed_major_critical':len(blocked_findings),
                       'functional_pass':len(passed),'functional_fail':len(failed),'functional_not_run':len(unsupported)},
            'human_approvals':approvals,
            'disclaimer_en':'READY_FOR_STAGING is permission to try a controlled staging rollout, NOT production certification.',
            'disclaimer_ru':'READY_FOR_STAGING разрешает только контролируемое тестовое развёртывание, НЕ является сертификатом качества.'}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--static',type=pathlib.Path,required=True)
    p.add_argument('--game',type=pathlib.Path)
    p.add_argument('--approvals',type=pathlib.Path)
    p.add_argument('--output',type=pathlib.Path)
    args=p.parse_args(argv)
    s=json.loads(args.static.read_text(encoding='utf-8'))
    g=json.loads(args.game.read_text(encoding='utf-8')) if args.game else None
    a=json.loads(args.approvals.read_text(encoding='utf-8')) if args.approvals else None
    r=evaluate(s,g,a);print(json.dumps(r,ensure_ascii=False,indent=2))
    if args.output: args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return 2 if r['decision']=='BLOCKED' else (1 if r['decision']=='HOLD_FOR_REVIEW' else 0)
if __name__=='__main__':raise SystemExit(main())
