"""
Dummy data generator for Contoso Financial Services.

Generates realistic activity events from two sources:
  1. Celonis Task Mining (desktop + browser captures)
  2. Microsoft Work IQ (Copilot agent signals)

Covers 8 loan origination cases with 4 different analysts,
two process variants (with/without Copilot), and a mix of
applications (SAP, Outlook, SharePoint, Word, Excel, Teams).
"""

from __future__ import annotations
import random
import uuid
from datetime import datetime, timedelta

ANALYSTS = [
    {"id": "sarah.chen@contoso.com", "name": "Sarah Chen"},
    {"id": "james.miller@contoso.com", "name": "James Miller"},
    {"id": "priya.patel@contoso.com", "name": "Priya Patel"},
    {"id": "marcus.johnson@contoso.com", "name": "Marcus Johnson"},
]

LOAN_CASES = [
    {"case_id": "LOAN-4872", "applicant": "John Smith", "amount": "$245,000", "type": "Mortgage"},
    {"case_id": "LOAN-4873", "applicant": "Emily Davis", "amount": "$180,000", "type": "Mortgage"},
    {"case_id": "LOAN-4874", "applicant": "Robert Wilson", "amount": "$52,000", "type": "Auto"},
    {"case_id": "LOAN-4875", "applicant": "Maria Garcia", "amount": "$320,000", "type": "Mortgage"},
    {"case_id": "LOAN-4876", "applicant": "David Lee", "amount": "$15,000", "type": "Personal"},
    {"case_id": "LOAN-4877", "applicant": "Jennifer Brown", "amount": "$410,000", "type": "Mortgage"},
    {"case_id": "LOAN-4878", "applicant": "Michael Taylor", "amount": "$28,000", "type": "Auto"},
    {"case_id": "LOAN-4879", "applicant": "Lisa Anderson", "amount": "$195,000", "type": "Mortgage"},
]


def _ts(base: datetime, offset_sec: int) -> str:
    return (base + timedelta(seconds=offset_sec)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_variant_a(case: dict, analyst: dict, base_time: datetime):
    """Full hybrid path: human desktop work + Copilot agent steps."""
    cid = case["case_id"]
    uid = analyst["id"]
    applicant = case["applicant"]
    tm_events = []
    wiq_events = []

    # Phase 1: Create Sales Order in SAP (human, desktop)
    t = 0
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "SAP GUI",
        "tabTitle": f"VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > input#orderType",
        "context": {"elementType": "input", "elementId": "orderType"},
    })
    t += random.randint(25, 45)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Element changed", "application": "SAP GUI",
        "tabTitle": f"VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > input#customerID",
        "context": {"elementType": "input", "elementId": "customerID"},
    })
    t += random.randint(15, 30)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "SAP GUI",
        "tabTitle": f"VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > button#save",
        "context": {"elementType": "button", "elementId": "save"},
    })

    # Phase 2: Review loan application email (human, browser)
    t += random.randint(20, 50)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "Outlook",
        "url": "https://outlook.office.com/mail/inbox",
        "tabTitle": f"Loan App {cid} - {applicant}", "userId": uid, "caseId": cid,
    })
    t += random.randint(30, 60)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Copy to clipboard", "application": "Outlook",
        "url": "https://outlook.office.com/mail/inbox",
        "tabTitle": f"Loan App {cid} - {applicant}", "userId": uid, "caseId": cid,
        "clipboardText": f"Annual income: $87,000...",
    })
    t += random.randint(15, 30)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "SharePoint",
        "url": f"https://contoso.sharepoint.com/docs/Credit_Report_{cid.split('-')[1]}.xlsx",
        "tabTitle": f"Credit_Report_{cid.split('-')[1]}.xlsx", "userId": uid, "caseId": cid,
    })
    t += random.randint(20, 40)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "SharePoint",
        "url": f"https://contoso.sharepoint.com/docs/Credit_Report_{cid.split('-')[1]}.xlsx",
        "tabTitle": f"Credit_Report_{cid.split('-')[1]}.xlsx", "userId": uid, "caseId": cid,
        "domPath": "body > div#grid > cell.R2C5",
    })

    # Phase 3: AI Credit Risk Assessment (agent, Work IQ)
    t += random.randint(30, 60)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "copilot.invoke", "copilotUsed": True,
        "appHost": "Microsoft Word", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"Loan_Summary_{cid.split('-')[1]}.docx",
        "copilotPrompt": f"Summarize the credit risk assessment for applicant {applicant} on loan {cid}",
    })
    t += random.randint(5, 12)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "copilot.toolCall", "copilotUsed": True,
        "appHost": "Microsoft Word", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"Loan_Summary_{cid.split('-')[1]}.docx",
        "pluginName": "RAG_search",
        "copilotPrompt": f"credit score history {applicant}",
    })
    t += random.randint(4, 10)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "copilot.completion", "copilotUsed": True,
        "appHost": "Microsoft Word", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"Loan_Summary_{cid.split('-')[1]}.docx",
        "copilotResponse": f"Risk assessment: Medium. FICO {random.randint(680, 780)}. DTI ratio {random.randint(28, 42)}%. Recommendation: Approve with conditions.",
    })

    # Phase 4: Draft & Send approval email (hybrid — agent drafts, human sends)
    t += random.randint(25, 55)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "copilot.invoke", "copilotUsed": True,
        "appHost": "Microsoft Outlook", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"RE: Loan App {cid} - Approval",
        "copilotPrompt": f"Draft an approval email to the branch manager for loan {cid} ({applicant}, {case['amount']})",
    })
    t += random.randint(3, 8)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "copilot.completion", "copilotUsed": True,
        "appHost": "Microsoft Outlook", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"RE: Loan App {cid} - Approval",
        "copilotResponse": f"Dear Manager, Based on the credit risk assessment, I recommend approving loan {cid} for {applicant}...",
    })
    t += random.randint(30, 70)
    wiq_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "actionType": "click", "copilotUsed": False,
        "actorType": "HUMAN",
        "appHost": "Microsoft Outlook", "userPrincipalName": uid, "caseId": cid,
        "resourceTitle": f"RE: Loan App {cid} - Approval",
    })

    return tm_events, wiq_events


def _generate_variant_b(case: dict, analyst: dict, base_time: datetime):
    """Manual-only path: no Copilot involvement — longer cycle time."""
    cid = case["case_id"]
    uid = analyst["id"]
    applicant = case["applicant"]
    tm_events = []

    # Phase 1: Create Sales Order in SAP
    t = 0
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "SAP GUI",
        "tabTitle": "VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > input#orderType",
        "context": {"elementType": "input"},
    })
    t += random.randint(30, 55)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Element changed", "application": "SAP GUI",
        "tabTitle": "VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > input#customerID",
    })
    t += random.randint(20, 40)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "SAP GUI",
        "tabTitle": "VA01 - Create Sales Order", "userId": uid, "caseId": cid,
        "domPath": "body > sap-frame > button#save",
    })

    # Phase 2: Review email (takes longer without AI help)
    t += random.randint(40, 80)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "Outlook",
        "url": "https://outlook.office.com/mail/inbox",
        "tabTitle": f"Loan App {cid} - {applicant}", "userId": uid, "caseId": cid,
    })
    t += random.randint(40, 90)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Copy to clipboard", "application": "Outlook",
        "url": "https://outlook.office.com/mail/inbox",
        "tabTitle": f"Loan App {cid} - {applicant}", "userId": uid, "caseId": cid,
    })
    t += random.randint(20, 40)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "SharePoint",
        "url": f"https://contoso.sharepoint.com/docs/Credit_Report_{cid.split('-')[1]}.xlsx",
        "tabTitle": f"Credit_Report_{cid.split('-')[1]}.xlsx", "userId": uid, "caseId": cid,
    })
    t += random.randint(30, 60)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Element changed", "application": "SharePoint",
        "tabTitle": f"Credit_Report_{cid.split('-')[1]}.xlsx", "userId": uid, "caseId": cid,
    })

    # Phase 3: Manual credit risk analysis in Excel (human, much slower)
    t += random.randint(60, 120)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "Excel",
        "tabTitle": f"Risk_Calculator.xlsx", "userId": uid, "caseId": cid,
    })
    t += random.randint(90, 180)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Element changed", "application": "Excel",
        "tabTitle": f"Risk_Calculator.xlsx", "userId": uid, "caseId": cid,
    })
    t += random.randint(60, 120)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "Excel",
        "tabTitle": f"Risk_Calculator.xlsx", "userId": uid, "caseId": cid,
    })

    # Phase 4: Manual email composition (human, also slower)
    t += random.randint(30, 60)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Activated tab", "application": "Outlook",
        "url": "https://outlook.office.com/mail/compose",
        "tabTitle": f"New Message - Loan App {cid}", "userId": uid, "caseId": cid,
    })
    t += random.randint(120, 240)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Element changed", "application": "Outlook",
        "url": "https://outlook.office.com/mail/compose",
        "tabTitle": f"New Message - Loan App {cid}", "userId": uid, "caseId": cid,
    })
    t += random.randint(15, 30)
    tm_events.append({
        "event_id": str(uuid.uuid4())[:8], "timestamp": _ts(base_time, t),
        "eventType": "Left click", "application": "Outlook",
        "url": "https://outlook.office.com/mail/compose",
        "tabTitle": f"New Message - Loan App {cid}", "userId": uid, "caseId": cid,
        "domPath": "body > button#send",
    })

    return tm_events, []


def generate_contoso_data(seed: int = 42) -> tuple[list[dict], list[dict]]:
    """
    Generate all dummy events for Contoso Financial Services.

    Returns (task_mining_events, work_iq_events).
    ~62% of cases use Variant A (with Copilot), ~38% use Variant B (manual).
    """
    random.seed(seed)
    base = datetime(2026, 3, 28, 8, 30, 0)

    all_tm: list[dict] = []
    all_wiq: list[dict] = []

    variant_assignment = [
        ("A", ANALYSTS[0], LOAN_CASES[0]),  # Sarah  → Copilot
        ("A", ANALYSTS[1], LOAN_CASES[1]),  # James  → Copilot
        ("B", ANALYSTS[2], LOAN_CASES[2]),  # Priya  → Manual
        ("A", ANALYSTS[3], LOAN_CASES[3]),  # Marcus → Copilot
        ("B", ANALYSTS[0], LOAN_CASES[4]),  # Sarah  → Manual (she uses both)
        ("A", ANALYSTS[1], LOAN_CASES[5]),  # James  → Copilot
        ("A", ANALYSTS[2], LOAN_CASES[6]),  # Priya  → Copilot (she also uses both)
        ("B", ANALYSTS[3], LOAN_CASES[7]),  # Marcus → Manual
    ]

    for i, (variant, analyst, case) in enumerate(variant_assignment):
        case_base = base + timedelta(minutes=i * 15 + random.randint(0, 5))

        if variant == "A":
            tm, wiq = _generate_variant_a(case, analyst, case_base)
        else:
            tm, wiq = _generate_variant_b(case, analyst, case_base)

        all_tm.extend(tm)
        all_wiq.extend(wiq)

    all_tm.sort(key=lambda e: e["timestamp"])
    all_wiq.sort(key=lambda e: e["timestamp"])

    return all_tm, all_wiq
