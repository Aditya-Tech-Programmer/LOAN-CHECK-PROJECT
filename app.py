

import streamlit as st
import pandas as pd
import json, uuid, math
from datetime import datetime

st.set_page_config(page_title="LoanCheck  | PythonGuruKool", page_icon="💠", layout="wide")

# Policy values from the LoanCheck brief
MIN_AGE, MAX_AGE, MIN_INCOME, MIN_CIBIL, MAX_FOIR = 21, 60, 25000.0, 650, 50.0
MIN_LOAN, MAX_LOAN = 50000.0, 2500000.0
TENURES = (12, 24, 36, 48, 60)
EMPLOYMENT = ("Salaried", "Self-employed")
BANDS = {
    "Excellent": (750, 900, 11.0),
    "Good": (700, 749, 13.5),
    "Fair": (650, 699, 16.0),
    "Poor": (300, 649, 0.0),
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--cyan:#7cf7c8;--violet:#ffd166;--pink:#ff9f7f}
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{color:#f5f7ff;background:radial-gradient(ellipse at 5% 0%,#174a43 0,transparent 36%),radial-gradient(ellipse at 92% 8%,#5b3d1c 0,transparent 29%),linear-gradient(135deg,#071713,#102923 52%,#101b1b);background-attachment:fixed}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#12362f,#081b19);border-right:1px solid #477568}
[data-testid="stSidebar"] *{color:#f5f7ff}
.block-container{max-width:1450px;padding-top:1.3rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.04em}
.hero{padding:30px 32px;border-radius:28px;margin-bottom:22px;position:relative;overflow:hidden;background:linear-gradient(120deg,rgba(22,91,70,.94),rgba(16,43,39,.91) 58%,rgba(91,60,25,.84));border:1px solid #6ba58c;box-shadow:0 25px 70px #0008,inset 0 1px #ffffff20;transform-style:preserve-3d}
.hero:after{content:"";position:absolute;width:220px;height:220px;border:1px solid #7cf7c855;border-radius:42px;right:8%;top:-120px;transform:rotate(42deg);box-shadow:0 0 50px #7cf7c71c;animation:orbit 12s linear infinite}
.hero:before{content:"";position:absolute;width:120px;height:120px;border:1px solid #ffd16655;border-radius:30px;right:20%;bottom:-82px;transform:rotate(35deg);box-shadow:0 0 45px #ffd16616;animation:floaty 7s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(402deg)}}
@keyframes floaty{0%,100%{translate:0 0}50%{translate:0 -14px}}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}
.eyebrow{color:var(--cyan);font-size:.75rem;font-weight:900;letter-spacing:.18em;text-transform:uppercase}
.bigtitle{text-shadow:0 10px 28px #0007;font-size:clamp(2.3rem,5vw,4rem);font-weight:900;line-height:1.08;margin:.5rem 0;background:linear-gradient(90deg,#fff,#9afaf0 52%,#c0aaff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#bdc9e9;line-height:1.7;max-width:800px}
.pill{display:inline-block;border:1px solid #61f5e755;background:#61f5e711;color:#bafff8;padding:7px 12px;border-radius:999px;margin:5px 5px 0 0;font-size:.78rem;font-weight:800}
.card{padding:20px;border:1px solid #a7baff28;border-radius:21px;background:linear-gradient(145deg,#1c453bd9,#102622ed);box-shadow:0 17px 36px #0005,inset 0 1px #ffffff12;transition:all .25s ease;margin-bottom:15px}
.card:hover{transform:perspective(900px) rotateX(2deg) rotateY(-2deg) translateY(-5px);border-color:#61f5e777;box-shadow:0 25px 45px #0006,0 0 22px #61f5e711}
.metric{min-height:125px;padding:18px;border-radius:19px;border:1px solid #a7baff30;background:linear-gradient(140deg,#20483d,#102722);box-shadow:0 15px 30px #0004,inset 0 1px #ffffff12;transition:.25s}
.metric:hover{transform:perspective(700px) translateY(-5px) rotateX(4deg) rotateY(-1deg);box-shadow:0 22px 38px #0006}
.mlabel{font-size:.72rem;letter-spacing:.12em;color:#aebddd;font-weight:800}
.mvalue{font:800 1.7rem 'Space Grotesk';color:white;margin-top:8px;overflow-wrap:anywhere}
.mfoot{font-size:.78rem;color:#94a5ce;margin-top:4px}
.kicker{font-size:.72rem;letter-spacing:.16em;color:var(--cyan);font-weight:900}
.sectiontitle{font:800 1.55rem 'Space Grotesk';margin:4px 0 14px}
.statusgood,.statusbad,.statuswarn{padding:16px 18px;border-radius:15px;font-weight:900}
.statusgood{background:#36d99a16;border:1px solid #55edaa77;color:#a8ffd3}
.statusbad{background:#ff638516;border:1px solid #ff789877;color:#ffbdcc}
.statuswarn{background:#ffca5c16;border:1px solid #ffca5c77;color:#ffe5a9}
div.stButton>button,div.stFormSubmitButton>button{border:1px solid #8bfff0;border-radius:13px;min-height:3rem;color:#08131d;font-weight:900;background:linear-gradient(100deg,#61f5e7,#aaa0ff 70%,#ff9cd9);box-shadow:0 9px 25px #61f5e728;transition:.2s}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{transform:translateY(-2px) scale(1.01);box-shadow:0 14px 32px #61f5e744}
/* Keep download buttons readable on the dark background */
div.stDownloadButton>button{background:linear-gradient(135deg,#183b35,#172e3a)!important;color:#eafcff!important;border:1px solid #67e8d4!important;border-radius:12px!important;font-weight:800!important;box-shadow:0 8px 22px #0005!important}
div.stDownloadButton>button p,div.stDownloadButton>button span{color:#eafcff!important}
div.stDownloadButton>button:hover{background:linear-gradient(135deg,#20584d,#263b58)!important;border-color:#a7fff2!important;transform:translateY(-2px)}
/* Style native tables and dataframe containers to match the app theme */
[data-testid="stTable"], [data-testid="stDataFrame"], [data-testid="stDataEditor"]{background:#102722!important;color:#f5f7ff!important;border:1px solid #477568!important;border-radius:14px!important;overflow:hidden!important}
[data-testid="stTable"] table{background:#102722!important;color:#f5f7ff!important}
[data-testid="stTable"] th{background:#1a3a34!important;color:#bafff2!important}
[data-testid="stTable"] td{background:#102722!important;color:#f5f7ff!important;border-color:#31534b!important}
[data-testid="stDataFrame"] iframe{color-scheme:dark!important}
[data-testid="stDataFrame"] [data-testid="stToolbar"]{background:#102722!important}
/* Improve all form controls and dropdown menus */
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea{background:#081c18!important;color:white!important;border-color:#7182b85c!important;border-radius:11px!important}
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"]{background:#102722!important;color:#f5f7ff!important}
[data-baseweb="menu"] *,[role="listbox"] *{color:#f5f7ff!important}
label,p,li{color:#e7ecff}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#61f5e7,#a58bff,#ff8dd1)}
[data-testid="stExpander"]{border:1px solid #a7baff30;border-radius:14px;background:#112b25}
hr{border-color:#a7baff24}
.footer{text-align:center;color:#8292bb;font-size:.78rem;padding:26px 0 8px}
</style>
""", unsafe_allow_html=True)

def money(v): return f"₹{v:,.2f}"
def credit_band(score):
    for name, (lo, hi, rate) in BANDS.items():
        if lo <= score <= hi: return name, rate
    return "Poor", 0.0
def emi(principal, annual_rate, months):
    if principal <= 0 or months <= 0: return 0.0
    if annual_rate == 0: return round(principal/months, 2)
    r = annual_rate/1200
    factor = (1+r)**months
    return round(principal*r*factor/(factor-1), 2)
def foir(income, old_emi, new_emi):
    return round((old_emi+new_emi)/income*100, 2) if income > 0 else 0.0
def counter_offer(income, old_emi, rate, months):
    affordable = income*MAX_FOIR/100-old_emi
    if affordable <= 0: return 0.0
    r=rate/1200
    principal=affordable*months if r == 0 else affordable*((1+r)**months-1)/(r*(1+r)**months)
    return float(int(principal//1000)*1000)
def schedule(principal, rate, months):
    r=rate/1200; payment=emi(principal,rate,months); bal=float(principal); rows=[]
    for m in range(1,months+1):
        interest=round(bal*r,2); p=round(payment-interest,2); bal=round(max(0,bal-p),2)
        rows.append({"Month":m,"EMI (₹)":payment,"Interest (₹)":interest,"Principal (₹)":p,"Outstanding (₹)":bal})
    return pd.DataFrame(rows)
def evaluate(a):
    reasons=[]; band, rate=credit_band(a["cibil"])
    if not MIN_AGE <= a["age"] <= MAX_AGE: reasons.append(f"Age must be between {MIN_AGE} and {MAX_AGE}.")
    if a["employment"] not in EMPLOYMENT: reasons.append("Employment must be Salaried or Self-employed.")
    if a["income"] < MIN_INCOME: reasons.append(f"Monthly income must be at least {money(MIN_INCOME)}.")
    if not MIN_LOAN <= a["amount"] <= MAX_LOAN: reasons.append(f"Loan amount must be between {money(MIN_LOAN)} and {money(MAX_LOAN)}.")
    if a["cibil"] < MIN_CIBIL: reasons.append(f"CIBIL score must be at least {MIN_CIBIL}.")
    payment=0.0; debt_ratio=0.0
    if band != "Poor" and a["income"] >= MIN_INCOME:
        payment=emi(a["amount"],rate,a["tenure"]); debt_ratio=foir(a["income"],a["old_emi"],payment)
        if debt_ratio > MAX_FOIR: reasons.append(f"FOIR is {debt_ratio:.2f}%, above the maximum of {MAX_FOIR:.0f}%.")
    initials="".join(ch for ch in a["name"] if ch.isalpha())[:3].upper() or "CUS"
    return {**a,"id":f"PGK-LN-{initials}{a['age']}","band":band,"rate":rate,"emi":payment,"foir":debt_ratio,"reasons":reasons,"eligible":not reasons,"time":datetime.now().strftime("%d %b %Y, %I:%M %p")}

# ---- Required reusable functions from the 12-page project brief ----
def is_valid_age(age): return MIN_AGE <= int(age) <= MAX_AGE
def is_valid_employment(employment_type): return str(employment_type).strip().lower() in {"salaried", "self-employed"}
def is_valid_income(income): return float(income) >= MIN_INCOME
def is_valid_loan_amount(amount): return MIN_LOAN <= float(amount) <= MAX_LOAN
def is_valid_tenure(tenure): return int(tenure) in TENURES
def get_credit_band(score): return credit_band(int(score))[0].lower()
def get_interest_rate(band): return {"excellent":11.0,"good":13.5,"fair":16.0,"poor":0.0}.get(str(band).lower(),0.0)
def calculate_emi(principal, annual_rate, months): return emi(float(principal),float(annual_rate),int(months))
def pass_fail(result): return "PASS" if result else "FAIL"
def total_existing_emi(emis):
    total=0.0
    for value in emis: total += float(value)
    return round(total,2)
def calculate_foir(income, existing_total, new_emi):
    return round((float(existing_total)+float(new_emi))/float(income)*100,2) if float(income)>0 else 0.0
def get_valid_int(prompt, min_value, max_value):
    while True:
        raw=input(prompt).strip()
        if raw.isdigit() and min_value <= int(raw) <= max_value: return int(raw)
        print(f"Invalid input. Enter a value between {min_value} and {max_value}.")
def get_valid_float(prompt, min_value):
    while True:
        try:
            value=float(input(prompt).strip())
            if math.isfinite(value) and value>=min_value: return value
        except ValueError: pass
        print(f"Invalid input. Enter a value greater than or equal to {min_value}.")
def get_valid_choice(prompt, options):
    options={str(x).strip().lower() for x in options}
    while True:
        value=input(prompt).strip().lower()
        if value in options: return value
        print("Invalid choice. Choose one of: "+", ".join(sorted(options)))
def get_valid_tenure(prompt):
    while True:
        raw=input(prompt).strip()
        if raw.isdigit() and int(raw) in TENURES: return int(raw)
        print("Invalid input. Allowed tenures: "+", ".join(map(str,TENURES)))
def collect_existing_emis():
    count=get_valid_int("How many existing loans? ",0,50); values=[]
    for i in range(count): values.append(get_valid_float(f"EMI for loan {i+1}: ",0))
    return values
def create_customer():
    name=input("Full name: ").strip(); age=get_valid_int("Age: ",18,100)
    employment=get_valid_choice("Employment (salaried/self-employed/student): ",["salaried","self-employed","student"])
    income=get_valid_float("Monthly income: ",0); cibil=get_valid_int("CIBIL score: ",300,900)
    existing=collect_existing_emis(); amount=get_valid_float("Loan amount: ",0); tenure=get_valid_tenure("Tenure months: ")
    initials=''.join(ch for ch in name if ch.isalpha())[:3].upper() or "CUS"
    return {"name":name,"age":age,"employment_type":employment,"monthly_income":income,"cibil_score":cibil,"existing_emis":existing,"loan_amount":amount,"tenure":tenure,"application_id":f"PGK-LN-{initials}{age}"}
def print_customer(customer):
    return {**customer,"pan_number":customer.get("pan_number","Not provided")}
def check_eligibility(customer):
    reasons=[]; age=int(customer["age"]); employment=str(customer["employment_type"]).strip().lower()
    income=float(customer["monthly_income"]); score=int(customer["cibil_score"]); amount=float(customer["loan_amount"]); tenure=int(customer["tenure"])
    band=get_credit_band(score); rate=get_interest_rate(band); old=total_existing_emi(customer.get("existing_emis",[]))
    if not is_valid_age(age): reasons.append(f"Age {age} allowed range {MIN_AGE}–{MAX_AGE} se bahar hai")
    if not is_valid_employment(employment): reasons.append("Employment type allowed nahi hai; salaried ya self-employed hona chahiye")
    if not is_valid_income(income): reasons.append(f"Monthly income ₹{income:.2f} minimum ₹{MIN_INCOME:.2f} se kam hai")
    if not is_valid_loan_amount(amount): reasons.append(f"Loan amount ₹{amount:.2f}, ₹{MIN_LOAN:.2f}–₹{MAX_LOAN:.2f} range ke bahar hai")
    if not is_valid_tenure(tenure): reasons.append(f"Tenure {tenure} allowed tenures mein nahi hai")
    if band=="poor": reasons.append(f"CIBIL score {score} 650 se kam hai")
    payment=0.0; ratio=0.0
    if band!="poor" and is_valid_income(income):
        payment=calculate_emi(amount,rate,tenure); ratio=calculate_foir(income,old,payment)
        if ratio>MAX_FOIR: reasons.append(f"FOIR {ratio:.2f}% hai, jo maximum {MAX_FOIR:.0f}% se zyada hai")
    customer.update({"credit_band":band,"interest_rate":rate,"existing_total":old,"emi":payment,"foir":ratio})
    return (len(reasons)==0,reasons)
def max_eligible_amount(income, existing_total, annual_rate, months): return counter_offer(income,existing_total,annual_rate,months)
def emi_schedule(principal, annual_rate, months): return schedule(principal,annual_rate,months).head(6)
def print_report(customer, is_eligible, reasons):
    return {"application_id":customer.get("application_id","PGK-LN-UNKNOWN"),"applicant":customer.get("name","Unknown"),"credit_band":customer.get("credit_band","poor"),"interest_rate":customer.get("interest_rate",0.0),"loan_amount":round(float(customer.get("loan_amount",0)),2),"tenure":int(customer.get("tenure",0)),"monthly_emi":customer.get("emi",0.0),"existing_emis":customer.get("existing_total",0.0),"foir":customer.get("foir",0.0),"status":"APPROVED" if is_eligible else "REJECTED","reasons":list(reasons)}
def print_session_summary(processed, approved, rejected):
    return {"Applications processed":processed,"Approved":approved,"Rejected":rejected}

TEST_APPLICANTS = [
 {"name":"Rohan Mehta","age":32,"employment":"Salaried","income":85000.0,"cibil":780,"old_emi":6500.0,"amount":500000.0,"tenure":36},
 {"name":"Sneha Kulkarni","age":29,"employment":"Salaried","income":60000.0,"cibil":720,"old_emi":20000.0,"amount":800000.0,"tenure":48},
 {"name":"Priya Nair","age":24,"employment":"Self-employed","income":40000.0,"cibil":680,"old_emi":0.0,"amount":300000.0,"tenure":24},
 {"name":"Vikram Joshi","age":63,"employment":"Salaried","income":30000.0,"cibil":700,"old_emi":14000.0,"amount":400000.0,"tenure":60},
 {"name":"Arjun Deshpande","age":27,"employment":"Salaried","income":50000.0,"cibil":640,"old_emi":0.0,"amount":200000.0,"tenure":24},
 {"name":"Kavya Rao","age":22,"employment":"Student","income":15000.0,"cibil":710,"old_emi":0.0,"amount":100000.0,"tenure":12},
]

if "history" not in st.session_state: st.session_state.history=[]
if "last" not in st.session_state: st.session_state.last=None

with st.sidebar:
    st.markdown("## 💠 LOANCHECK DASHBOARD")
    st.markdown("<span class='pill'>PYTHONGURUKOOL FINSERV</span>",unsafe_allow_html=True)
    page=st.radio("NAVIGATION",["🏠 Dashboard","🧮 Eligibility Engine","📊 EMI Studio","🗂️ History","🧪 PDF Test Applicants","🧠 Smart Insights","🧪 Loan Scenario Lab","💡 Affordability Planner","ℹ️ Policy Guide","📋 PDF Requirements Checklist"])
    st.markdown("---")
    st.markdown("### ⚡ Live policy")
    st.write(f"Age: **{MIN_AGE}–{MAX_AGE}** years")
    st.write(f"Minimum income: **{money(MIN_INCOME)}**")
    st.write(f"Minimum CIBIL: **{MIN_CIBIL}**")
    st.write(f"Maximum FOIR: **{MAX_FOIR:.0f}%**")
    st.caption("Educational demo — not a bank sanction.")

st.markdown("""<div class="hero"><div class="eyebrow">✦ SMART LENDING · RISK INTELLIGENCE · INSTANT ANALYTICS</div><div class="bigtitle">LoanCheck</div><div class="sub">A futuristic personal-loan eligibility cockpit. Screen applicants, calculate EMI and FOIR, and generate transparent decision reports inside a premium glassmorphism interface.</div><span class="pill">⚡ Instant scan</span><span class="pill">◈ 3D hover cards</span><span class="pill">📈 EMI intelligence</span><span class="pill">🛡️ Rule-based checks</span></div>""",unsafe_allow_html=True)

if page=="🏠 Dashboard":
    total=len(st.session_state.history); approved=sum(x["eligible"] for x in st.session_state.history); rejected=total-approved
    cols=st.columns(4)
    for col,label,value,foot in zip(cols,["APPLICATIONS","APPROVED","NOT APPROVED","APPROVAL RATE"],[total,approved,rejected,f"{approved/total*100:.1f}%" if total else "0.0%"],["Processed this session","Passed all checks","Requires review","Current session"]):
        with col: st.markdown(f"<div class='metric'><div class='mlabel'>{label}</div><div class='mvalue'>{value}</div><div class='mfoot'>{foot}</div></div>",unsafe_allow_html=True)
    left,right=st.columns([1.2,1])
    with left:
        st.markdown("<div class='card'><div class='kicker'>SYSTEM OVERVIEW</div><div class='sectiontitle'>Your lending command centre</div><p>Capture an applicant profile, run rule-based checks, and review the decision with EMI, FOIR and repayment details.</p><span class='pill'>Age validation</span><span class='pill'>Credit segmentation</span><span class='pill'>Debt burden</span><span class='pill'>Repayment schedule</span></div>",unsafe_allow_html=True)
        st.markdown("<div class='card'><div class='kicker'>WORKFLOW</div><div class='sectiontitle'>Three steps to a decision</div><p><b>01 / Capture</b> — applicant profile and existing obligations.</p><p><b>02 / Evaluate</b> — credit band, EMI and FOIR calculations.</p><p><b>03 / Explain</b> — status, reasons and repayment details.</p></div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'><div class='kicker'>CREDIT MATRIX</div><div class='sectiontitle'>Risk-based interest bands</div>",unsafe_allow_html=True)
        for name,(lo,hi,rate) in BANDS.items():
            st.markdown(f"<p style='display:flex;justify-content:space-between;border-bottom:1px solid #a7baff20;padding:9px 0'><span><b>{name}</b><br><small>CIBIL {lo}–{hi}</small></span><b style='color:#9ff9ef'>{f'{rate:.1f}% p.a.' if rate else 'Not eligible'}</b></p>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    if st.session_state.last:
        r=st.session_state.last
        st.markdown("### Latest decision")
        st.markdown(f"<div class='{'statusgood' if r['eligible'] else 'statusbad'}'>{'✓ APPROVED' if r['eligible'] else '✕ NOT APPROVED'} · {r['name']} · {r['id']}</div>",unsafe_allow_html=True)

elif page=="🧮 Eligibility Engine":
    st.markdown("<div class='kicker'>APPLICATION INTAKE</div><div class='sectiontitle'>Applicant profile & loan request</div>",unsafe_allow_html=True)
    with st.form("application"):
        c1,c2,c3=st.columns(3)
        with c1:
            name=st.text_input("Applicant full name *",placeholder="e.g. Rohan Mehta")
            age=st.number_input("Age (years) *",18,100,28)
            employment=st.selectbox("Employment type *",["Salaried","Self-employed","Student"])
        with c2:
            income=st.number_input("Monthly income (₹) *",0.0,100000000.0,85000.0,step=1000.0)
            cibil=st.slider("CIBIL score *",300,900,780)
            old_emi_text=st.text_input("Existing loan EMIs (₹), comma-separated",value="6500",help="Example: 6500, 12000, 8000. Leave blank if there are no existing loans.")
        with c3:
            amount=st.number_input("Loan amount requested (₹) *",0.0,100000000.0,500000.0,step=10000.0)
            tenure=st.selectbox("Tenure (months) *",TENURES,index=2)
            st.caption("Allowed tenure: 12, 24, 36, 48 or 60 months")
        run=st.form_submit_button("⚡ RUN ELIGIBILITY SCAN",use_container_width=True)
    if run:
        if not name.strip(): st.error("Enter the applicant's full name.")
        elif not all(math.isfinite(v) for v in [income,amount]): st.error("Enter valid numeric values.")
        elif old_emi_text.strip() and any(not part.strip() for part in old_emi_text.split(",")): st.error("Enter existing EMIs as comma-separated numbers, for example 6500, 12000.")
        elif any((not part.strip().replace(".","",1).isdigit()) for part in old_emi_text.split(",") if part.strip()): st.error("Existing EMIs must be valid non-negative numbers separated by commas.")
        else:
            bar=st.progress(0,text="Initializing policy scan…")
            bar.progress(25,text="Validating applicant profile…")
            bar.progress(60,text="Calculating credit band, EMI and FOIR…")
            existing_emi_list=[float(part.strip()) for part in old_emi_text.split(",") if part.strip()]
            old_emi=sum(existing_emi_list)
            applicant={"name":name.strip(),"age":int(age),"employment":employment if employment in EMPLOYMENT else "Student / Other","income":float(income),"cibil":int(cibil),"old_emi":float(old_emi),"existing_emis":existing_emi_list,"amount":float(amount),"tenure":int(tenure)}
            result=evaluate(applicant)
            bar.progress(100,text="Scan complete — decision generated.")
            st.session_state.last=result; st.session_state.history.insert(0,result)
            st.rerun()
    r=st.session_state.last
    if r:
        st.markdown("---")
        st.markdown("<div class='kicker'>DECISION OUTPUT</div><div class='sectiontitle'>Eligibility intelligence report</div>",unsafe_allow_html=True)
        cols=st.columns(4)
        items=[("CREDIT BAND",r["band"],f"CIBIL {r['cibil']}"),("INTEREST RATE",f"{r['rate']:.1f}%" if r["band"]!="Poor" else "N/A","Per annum"),("MONTHLY EMI",money(r["emi"]) if r["emi"] else "Not calculated",f"{r['tenure']} month term"),("FOIR",f"{r['foir']:.2f}%" if r["emi"] else "Not calculated",f"Policy limit {MAX_FOIR:.0f}%")]
        for col,(label,value,foot) in zip(cols,items):
            with col: st.markdown(f"<div class='metric'><div class='mlabel'>{label}</div><div class='mvalue' style='font-size:1.35rem'>{value}</div><div class='mfoot'>{foot}</div></div>",unsafe_allow_html=True)
        st.markdown("")
        if r["eligible"]: st.markdown(f"<div class='statusgood'>✓ APPROVED — {r['name']} meets all configured checks.</div>",unsafe_allow_html=True)
        elif len(r["reasons"])==1 and r["reasons"][0].startswith("FOIR"): st.markdown("<div class='statuswarn'>◈ NOT APPROVED — FOIR threshold exceeded. Review the counter-offer.</div>",unsafe_allow_html=True)
        else: st.markdown("<div class='statusbad'>✕ REJECTED — one or more mandatory checks failed.</div>",unsafe_allow_html=True)
        for reason in r["reasons"]: st.warning(reason)
        if not r["eligible"] and len(r["reasons"])==1 and r["reasons"][0].startswith("FOIR") and r["income"]>=MIN_INCOME and r["band"]!="Poor":
            offer=counter_offer(r["income"],r["old_emi"],r["rate"],r["tenure"])
            if offer>=MIN_LOAN: st.markdown(f"<div class='card'><div class='kicker'>SMART COUNTER-OFFER</div><div class='sectiontitle'>Try a lower loan amount</div><p>Indicative amount within the FOIR limit: <b style='color:#9ff9ef'>{money(offer)}</b> for {r['tenure']} months.</p></div>",unsafe_allow_html=True)
            else: st.info("No counter-offer is available above the minimum loan amount.")
        if r["eligible"]:
            with st.expander("▦ View first six months' repayment schedule",expanded=True):
                st.dataframe(schedule(r["amount"],r["rate"],r["tenure"]).head(6),use_container_width=True,hide_index=True)
        report={k:r[k] for k in ["id","name","age","employment","income","cibil","band","rate","amount","tenure","old_emi","emi","foir","eligible","reasons","time"]}
        st.download_button("⬇️ Download decision report (JSON)",json.dumps(report,indent=2),file_name=f"{r['id']}.json",mime="application/json")

elif page=="📊 EMI Studio":
    st.markdown("<div class='kicker'>REPAYMENT LAB</div><div class='sectiontitle'>EMI Studio — model your monthly payment</div>",unsafe_allow_html=True)
    a,b=st.columns([.85,1.3])
    with a:
        principal=st.number_input("Principal amount (₹)",MIN_LOAN,MAX_LOAN,500000.0,step=25000.0)
        rate=st.selectbox("Annual interest rate (%)",[11.0,13.5,16.0])
        months=st.select_slider("Tenure (months)",options=list(TENURES),value=36)
        payment=emi(principal,rate,months); total=payment*months
        st.markdown(f"<div class='metric'><div class='mlabel'>ESTIMATED MONTHLY EMI</div><div class='mvalue'>{money(payment)}</div><div class='mfoot'>Illustrative calculation</div></div>",unsafe_allow_html=True)
        st.metric("Total interest",money(total-principal)); st.metric("Total repayment",money(total))
    with b:
        df=schedule(principal,rate,months)
        st.markdown("<div class='card'><div class='kicker'>AMORTIZATION TABLE</div><div class='sectiontitle'>Outstanding balance over time</div></div>",unsafe_allow_html=True)
        st.line_chart(df.set_index("Month")[["Outstanding (₹)"]])
        st.dataframe(df.head(6),use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download full EMI schedule (CSV)",df.to_csv(index=False).encode(),file_name="loancheck_emi_schedule.csv",mime="text/csv")

elif page=="🗂️ History":
    st.markdown("<div class='kicker'>SESSION RECORDS</div><div class='sectiontitle'>Application history</div>",unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown("<div class='card'><div class='sectiontitle'>No applications yet</div><p>Run your first scan in Eligibility Engine. Results are stored for this active session.</p></div>",unsafe_allow_html=True)
    else:
        df=pd.DataFrame([{"Application ID":r["id"],"Applicant":r["name"],"Age":r["age"],"Credit band":r["band"],"Loan amount (₹)":r["amount"],"EMI (₹)":r["emi"],"FOIR (%)":r["foir"],"Decision":"APPROVED" if r["eligible"] else "NOT APPROVED","Time":r["time"]} for r in st.session_state.history])
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("⬇️ Export history (CSV)",df.to_csv(index=False).encode(),file_name="loancheck_history.csv",mime="text/csv")
        if st.button("🧹 Clear session history"):
            st.session_state.history=[]; st.session_state.last=None; st.rerun()

elif page=="🧪 PDF Test Applicants":
    st.markdown("<div class='kicker'>REQUIREMENTS VERIFICATION</div><div class='sectiontitle'>All six test applicants from the PDF</div>",unsafe_allow_html=True)
    st.write("Run the six required profiles from the project brief through the same policy logic and inspect the results.")
    if st.button("▶️ Run all six PDF test applicants",use_container_width=True):
        bar=st.progress(0,text="Preparing test desk…"); results=[]
        for i,a in enumerate(TEST_APPLICANTS,1):
            bar.progress(int(i/len(TEST_APPLICANTS)*90),text=f"Checking applicant {i} of {len(TEST_APPLICANTS)}…")
            customer={"name":a["name"],"age":a["age"],"employment_type":a["employment"],"monthly_income":a["income"],"cibil_score":a["cibil"],"existing_emis":[a["old_emi"]] if a["old_emi"] else [],"loan_amount":a["amount"],"tenure":a["tenure"],"application_id":"PGK-LN-"+''.join(x for x in a["name"] if x.isalpha())[:3].upper()+str(a["age"])}
            ok,reasons=check_eligibility(customer); customer["eligible"]=ok; customer["reasons"]=reasons; customer["time"]=datetime.now().strftime("%d %b %Y, %I:%M %p")
            # Compatibility aliases for the existing test-results table; leave the rest of the app unchanged.
            customer["band"]=customer.get("credit_band", "Not calculated")
            customer["rate"]=customer.get("interest_rate", 0.0)
            customer["income"]=customer.get("monthly_income", 0.0)
            customer["old_emi"]=customer.get("existing_total", 0.0)
            customer["amount"]=customer.get("loan_amount", 0.0)
            results.append(customer)
        st.session_state.test_results=results; bar.progress(100,text="Test run complete.")
    if "test_results" in st.session_state:
        rows=[]
        for r in st.session_state.test_results:
            only_foir=(len(r["reasons"])==1 and r["reasons"][0].startswith("FOIR "))
            offer=max_eligible_amount(r["income"],r["old_emi"],r["rate"],r["tenure"]) if only_foir else 0.0
            rows.append({"Applicant":r["name"],"Credit band":r["band"],"Rate":f"{r['rate']:.1f}%" if r["band"]!="Poor" else "—","EMI (₹)":r["emi"] if r["emi"] else "—","Existing EMIs (₹)":r["old_emi"],"FOIR (%)":r["foir"] if r["emi"] else "—","Counter-offer (₹)":offer if offer>=MIN_LOAN else "—","Decision":"APPROVED" if r["eligible"] else ("NOT APPROVED" if only_foir else "REJECTED"),"Reasons":"; ".join(r["reasons"]) if r["reasons"] else "—"})
        df=pd.DataFrame(rows); st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download PDF test results (CSV)",df.to_csv(index=False).encode(),file_name="loancheck_pdf_test_results.csv",mime="text/csv")
        st.download_button("⬇️ Download PDF test results (JSON)",json.dumps(st.session_state.test_results,indent=2),file_name="loancheck_pdf_test_results.json",mime="application/json")
        for r in st.session_state.test_results:
            if r["eligible"]:
                with st.expander(f"{r['name']} — first six months EMI schedule"):
                    st.dataframe(schedule(r["amount"],r["rate"],r["tenure"]).head(6),use_container_width=True,hide_index=True)
        with st.expander("Expected results listed in the brief"): 
            st.markdown("1. **Rohan Mehta** — excellent, 11.0%, approved; 6-month EMI schedule.\n2. **Sneha Kulkarni** — good, 13.5%, FOIR-only failure; counter-offer approximately ₹369,000 for 48 months.\n3. **Priya Nair** — fair, 16.0%, approved.\n4. **Vikram Joshi** — rejected for age and FOIR; no counter-offer because multiple rules fail.\n5. **Arjun Deshpande** — poor CIBIL; EMI/FOIR not calculated.\n6. **Kavya Rao** — employment and income fail; EMI/FOIR not calculated.")
    else:
        st.info("Press the button to run all six named test profiles from the PDF.")


elif page=="🧠 Smart Insights":
    st.markdown("<div class='kicker'>EXPLAINABLE RISK INTELLIGENCE</div><div class='sectiontitle'>Smart applicant insights</div>",unsafe_allow_html=True)
    st.write("A transparent rule-based summary of the latest application. This is a decision-support demo, not an AI credit bureau or bank decision.")
    if not st.session_state.history:
        st.info("Run an application in Eligibility Engine first to unlock personalised insights.")
    else:
        dfh=pd.DataFrame(st.session_state.history)
        selected_id=st.selectbox("Choose an application",[r["id"]+" · "+r["name"] for r in st.session_state.history])
        idx=[r["id"]+" · "+r["name"] for r in st.session_state.history].index(selected_id)
        r=st.session_state.history[idx]
        # transparent 0–100 score based on explicit policy checks
        score=100
        if not MIN_AGE <= r["age"] <= MAX_AGE: score-=25
        if r["employment"] not in EMPLOYMENT: score-=25
        if r["income"] < MIN_INCOME: score-=20
        if r["cibil"] < MIN_CIBIL: score-=30
        if r["amount"] < MIN_LOAN or r["amount"] > MAX_LOAN: score-=15
        if r["emi"] and r["foir"] > MAX_FOIR: score-=25
        score=max(0,score)
        c1,c2,c3=st.columns(3)
        with c1: st.markdown(f"<div class='metric'><div class='mlabel'>RULE-FIT SCORE</div><div class='mvalue'>{score}/100</div><div class='mfoot'>Transparent heuristic, not a credit score</div></div>",unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric'><div class='mlabel'>CREDIT SEGMENT</div><div class='mvalue'>{r['band']}</div><div class='mfoot'>CIBIL {r['cibil']}</div></div>",unsafe_allow_html=True)
        debt_value = f"{r['foir']:.1f}%" if r["emi"] else "N/A"
        with c3: st.markdown(f"<div class='metric'><div class='mlabel'>DEBT BURDEN</div><div class='mvalue'>{debt_value}</div><div class='mfoot'>Policy threshold {MAX_FOIR:.0f}%</div></div>",unsafe_allow_html=True)
        st.markdown("### Findings & next actions")
        insights=[]
        if r["cibil"]>=750: insights.append(("Positive","Strong configured credit band; policy rate is 11.0% p.a."))
        elif r["cibil"]>=700: insights.append(("Review","Good configured credit band; compare affordability before accepting a loan."))
        elif r["cibil"]>=650: insights.append(("Caution","Fair configured credit band has a higher illustrative rate of 16.0% p.a."))
        else: insights.append(("Blocker","CIBIL is below the configured minimum; the app does not calculate EMI/FOIR for poor band."))
        if r["income"]<MIN_INCOME: insights.append(("Income gap",f"Monthly income is below the configured {money(MIN_INCOME)} minimum."))
        if r["emi"] and r["foir"]>MAX_FOIR: insights.append(("Debt burden", "Existing obligations plus the requested EMI exceed the configured FOIR limit. Try the Affordability Planner."))
        elif r["emi"]: insights.append(("Affordability", "FOIR is within the configured limit for this request."))
        if not MIN_AGE<=r["age"]<=MAX_AGE: insights.append(("Age rule",f"Configured eligible age range is {MIN_AGE}–{MAX_AGE}."))
        for tag,msg in insights:
            st.markdown(f"<div class='card'><span class='pill'>{tag}</span><p>{msg}</p></div>",unsafe_allow_html=True)
        st.caption("Score weights are a product-demo heuristic and are not validated lending criteria. Do not use for real credit decisions.")

elif page=="🧪 Loan Scenario Lab":
    st.markdown("<div class='kicker'>WHAT-IF MODELLING</div><div class='sectiontitle'>Loan Scenario Lab</div>",unsafe_allow_html=True)
    st.write("Compare up to three principal/tenure scenarios at the same illustrative interest rate before choosing a request.")
    x1,x2,x3=st.columns(3)
    with x1: base_amount=st.number_input("Scenario A · Loan amount (₹)",MIN_LOAN,MAX_LOAN,500000.0,step=25000.0,key="sc_a")
    with x2: scenario_rate=st.selectbox("Annual rate (%)",[11.0,13.5,16.0],index=0,key="sc_rate")
    with x3: base_tenure=st.selectbox("Scenario A · Tenure",list(TENURES),index=2,key="sc_tenure")
    amounts=[base_amount, max(MIN_LOAN,min(MAX_LOAN,base_amount*0.8)), max(MIN_LOAN,min(MAX_LOAN,base_amount*1.2))]
    tenures=[base_tenure, 24 if base_tenure!=24 else 36, 60 if base_tenure!=60 else 48]
    labels=["A · Requested", "B · 20% lower", "C · Alternate tenure"]
    rows=[]
    for label,amt,months in zip(labels,amounts,tenures):
        pay=emi(amt,scenario_rate,months); total=pay*months
        rows.append({"Scenario":label,"Principal (₹)":amt,"Tenure (months)":months,"Monthly EMI (₹)":pay,"Total interest (₹)":round(total-amt,2),"Total repayment (₹)":round(total,2)})
    dsc=pd.DataFrame(rows)
    st.dataframe(dsc,use_container_width=True,hide_index=True)
    st.bar_chart(dsc.set_index("Scenario")[["Monthly EMI (₹)","Total interest (₹)"]])
    best=dsc.loc[dsc["Monthly EMI (₹)"].idxmin()]
    st.markdown(f"<div class='card'><div class='kicker'>LOWEST MONTHLY EMI</div><div class='sectiontitle'>{best['Scenario']}</div><p>Estimated EMI: <b>{money(best['Monthly EMI (₹)'])}</b>. A longer tenure can reduce EMI while increasing total interest.</p></div>",unsafe_allow_html=True)
    st.download_button("⬇️ Export scenario comparison (CSV)",dsc.to_csv(index=False).encode(),file_name="loancheck_scenario_comparison.csv",mime="text/csv")

elif page=="💡 Affordability Planner":
    st.markdown("<div class='kicker'>PLAN BEFORE YOU BORROW</div><div class='sectiontitle'>Affordability Planner</div>",unsafe_allow_html=True)
    st.write("Estimate a loan amount that fits the configured FOIR cap using monthly income and existing EMIs.")
    a,b=st.columns(2)
    with a:
        plan_income=st.number_input("Monthly take-home income (₹)",min_value=0.0,value=85000.0,step=5000.0,key="plan_income")
        plan_existing=st.number_input("Total existing monthly EMIs (₹)",min_value=0.0,value=6500.0,step=500.0,key="plan_existing")
        plan_cibil=st.selectbox("Credit band for estimate",["Excellent · 11.0%","Good · 13.5%","Fair · 16.0%"],key="plan_band")
        plan_months=st.selectbox("Desired tenure (months)",list(TENURES),index=2,key="plan_tenure")
    with b:
        selected_rate=float(plan_cibil.split("·")[1].replace("%","").strip())
        room=plan_income*MAX_FOIR/100-plan_existing
        max_principal=counter_offer(plan_income,plan_existing,selected_rate,plan_months) if plan_income>0 else 0.0
        st.markdown(f"<div class='metric'><div class='mlabel'>MAXIMUM NEW EMI AT {MAX_FOIR:.0f}% FOIR</div><div class='mvalue'>{money(max(0,room))}</div><div class='mfoot'>After existing EMIs</div></div>",unsafe_allow_html=True)
        st.markdown(f"<div class='metric'><div class='mlabel'>INDICATIVE AFFORDABLE PRINCIPAL</div><div class='mvalue'>{money(max_principal)}</div><div class='mfoot'>{plan_months} months · {selected_rate:.1f}% p.a.</div></div>",unsafe_allow_html=True)
        if plan_income<MIN_INCOME: st.warning(f"Income is below the configured minimum of {money(MIN_INCOME)}.")
        elif room<=0: st.error("Existing EMIs already meet or exceed the configured FOIR allowance.")
        else: st.success("Estimate calculated using the configured FOIR cap. This is not a loan approval.")
    st.caption("This estimate assumes the chosen rate and tenure and does not verify income, employment, CIBIL, identity, or lender-specific rules.")

elif page=="📋 PDF Requirements Checklist":
    st.markdown("<div class='kicker'>SOURCE-BASED AUDIT</div><div class='sectiontitle'>LoanCheck PDF requirements checklist</div>",unsafe_allow_html=True)
    st.write("Checklist based on the supplied 12-page LoanCheck Project Brief. It covers the 7 build phases, the six required test profiles, and interactive app additions.")
    groups = {
      "Phase 1 — Policy setup & intake": ["Named constants for all policy limits", "Allowed tenures stored as tuple", "Allowed employment types stored as set", "Credit interest rates stored in dictionary", "Welcome banner and all applicant fields", "Correct conversions and normalized employment input", "Input types printed with type() in console workflow"],
      "Phase 2 — Basic screening": ["Age 21–60 inclusive", "Employment salaried/self-employed", "Minimum income ₹25,000", "Loan amount ₹50,000–₹25,00,000", "Tenure 12/24/36/48/60", "CIBIL bands and poor-band failure", "PASS/FAIL screening checklist"],
      "Phase 3 — Required reusable functions": ["is_valid_age()", "is_valid_employment()", "is_valid_income()", "is_valid_loan_amount()", "is_valid_tenure()", "get_credit_band()", "get_interest_rate()", "calculate_emi()", "pass_fail()", "Verify EMI(₹5,00,000, 11%, 36) = ₹16,369.36", "Test credit scores 780, 720, 680, 640"],
      "Phase 4 — Customer profile": ["Customer dictionary with all required fields", "create_customer() and print_customer()", "Application ID from first 3 name letters + age", "Safe .get('pan_number', 'Not provided')"],
      "Phase 5 — Debt burden": ["Collect multiple existing EMIs using a loop", "total_existing_emi() uses for loop, not sum()", "calculate_foir() rounds to 2 decimals", "check_eligibility() returns (bool, reasons)", "Calculated values saved back into customer", "Collect all failure reasons; skip EMI/FOIR for poor credit or failed income"],
      "Phase 6 — Validation & multi-applicant desk": ["get_valid_int() with bounds and invalid-input handling", "get_valid_float() supports decimal amounts", "get_valid_choice() normalizes input", "get_valid_tenure() accepts only allowed tenures", "Validate age/CIBIL/employment/income/EMIs/loan/tenure", "Multiple applicants in one session", "Session summary counts processed/approved/rejected"],
      "Phase 7 — Report & counter-offer": ["max_eligible_amount() reverse-calculates principal", "Counter-offer rounded down to nearest ₹1,000", "Counter-offer only for FOIR-only rejection and amount ≥ ₹50,000", "emi_schedule() first six months with EMI/interest/principal/balance", "Approved, FOIR-only and other-rejection report paths", "Poor credit report omits rate/EMI/FOIR", "Money values formatted to 2 decimals"],
      "Six required PDF test applicants": ["Rohan Mehta — 32, salaried, ₹85,000, CIBIL 780, EMI ₹6,500, ₹5,00,000/36", "Sneha Kulkarni — 29, salaried, ₹60,000, CIBIL 720, EMIs ₹12,000 + ₹8,000, ₹8,00,000/48", "Priya Nair — 24, self-employed, ₹40,000, CIBIL 680, no existing EMIs, ₹3,00,000/24", "Vikram Joshi — 63, salaried, ₹30,000, CIBIL 700, EMI ₹14,000, ₹4,00,000/60", "Arjun Deshpande — 27, salaried, ₹50,000, CIBIL 640, no existing EMIs, ₹2,00,000/24", "Kavya Rao — 22, student, ₹15,000, CIBIL 710, no existing EMIs, ₹1,00,000/12"],
      "Interactive dashboard extras": ["Dashboard metrics and credit matrix", "Eligibility form and decision report", "EMI Studio with interest/repayment totals, chart and CSV schedule", "Application history and CSV export", "JSON decision report", "CSV/JSON export of PDF test results", "Animated scan progress", "3D-style glassmorphism UI", "Policy guide and educational disclaimer"]
    }
    count=sum(len(v) for v in groups.values())
    st.markdown(f"<div class='card'><div class='kicker'>REQUIREMENTS MAP</div><div class='sectiontitle'>{count} review items across the PDF and app additions</div><p>This is a review checklist, not a claim that every item has passed an automated test.</p></div>",unsafe_allow_html=True)
    for group, items in groups.items():
      with st.expander(group, expanded=False):
        for item in items: st.markdown(f"- ☑️ {item}")
    

else:
    st.markdown("<div class='kicker'>TRANSPARENT RULES</div><div class='sectiontitle'>Policy guide & validation matrix</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'><div class='sectiontitle'>Eligibility rules</div><p>Every mandatory check must pass for approval. A FOIR-only failure can produce an indicative counter-offer.</p></div>",unsafe_allow_html=True)
    st.table(pd.DataFrame([("Age",f"{MIN_AGE}–{MAX_AGE} years"),("Employment","Salaried or Self-employed"),("Minimum monthly income",money(MIN_INCOME)),("Minimum CIBIL",MIN_CIBIL),("Maximum FOIR",f"{MAX_FOIR:.0f}%"),("Loan amount",f"{money(MIN_LOAN)} to {money(MAX_LOAN)}"),("Tenure options",", ".join(map(str,TENURES))+" months")],columns=["Policy parameter","Configured rule"]))
    st.markdown("### Credit score and interest rate")
    st.table(pd.DataFrame([{"Band":n,"CIBIL range":f"{lo}–{hi}","Interest rate":f"{rate:.1f}% p.a." if rate else "Not eligible"} for n,(lo,hi,rate) in BANDS.items()]))
    st.info("Educational project only. This is not a real bank sanction, credit-bureau check, or financial advice.")

st.markdown("<div class='footer'>PYTHONGURUKOOL FINSERV · LOANCHECK 3D · PYTHON + STREAMLIT<br>Emerald 3D glassmorphism · scenario lab · affordability planner · explainable insights · EMI analytics</div>",unsafe_allow_html=True)
