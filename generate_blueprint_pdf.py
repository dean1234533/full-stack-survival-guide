"""
Developer Blueprint PDF Generator
Run:  python3 generate_blueprint_pdf.py
Output: Developer_Blueprint.pdf
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ── Blue colour palette ------------------------------------------------------
NAVY      = (10,  30,  80)     # deep navy   - title bg / dark elements
BLUE      = (37,  99, 235)     # blue-600    - accent / headings
BLUE_DARK = (29,  78, 216)     # blue-700    - darker accent
BLUE_PALE = (219, 234, 254)    # blue-100    - light fills / alt rows
BLUE_MID  = (191, 219, 254)    # blue-200    - box borders
WHITE     = (255, 255, 255)
BODY      = (30,  41,  59)     # slate-800   - body text
MUTED     = (100, 116, 135)    # slate-500   - captions
PAGE_BG   = (248, 250, 255)    # near-white with blue tint

NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}

# ── Content ------------------------------------------------------------------
MONTHS = [
    {
        "num": "01", "title": "HTML & CSS",
        "learn": [
            "Semantic HTML - header, main, section, article, footer",
            "The box model - margin, padding, border",
            "Flexbox for layout and alignment",
            "Responsive design with media queries",
        ],
        "skip":    "CSS Grid, SASS, animations - not yet.",
        "project": "A personal site with 3+ real pages. No Lorem Ipsum.",
    },
    {
        "num": "02", "title": "JavaScript Fundamentals",
        "learn": [
            "Variables (let / const), functions, loops",
            "Arrays and objects",
            "DOM selection and event listeners",
            "fetch() API - pull data from a free public API",
        ],
        "skip":    "TypeScript, frameworks, class-based OOP.",
        "project": "A live widget added to your site - weather, quotes, a form.",
    },
    {
        "num": "03", "title": "JavaScript Deep Dive",
        "learn": [
            "Arrow functions, template literals, ternary operators",
            "Destructuring, spread / rest operators",
            "Promises, async/await, try/catch",
            "Array methods: .map()  .filter()  .reduce()  .find()",
        ],
        "skip":    "Design patterns, algorithms - that is interview prep, not building.",
        "project": "A self-contained JS app built from scratch, no tutorials.",
    },
    {
        "num": "04", "title": "React",
        "learn": [
            "JSX and component structure",
            "Props and state with useState",
            "useEffect for data fetching and side effects",
            "Conditional rendering and list rendering with .map()",
        ],
        "skip":    "Redux, Next.js, advanced patterns - foundations first.",
        "project": "Rebuild your Month 3 app in React.",
    },
    {
        "num": "05", "title": "Firebase",
        "learn": [
            "Firebase project setup and SDK config",
            "Auth: email/password and Google sign-in",
            "Firestore: read, write, update, delete documents",
            "Real-time listeners with onSnapshot",
        ],
        "skip":    "Cloud Functions, advanced security rules - get it working first.",
        "project": "Add login and persistent data to your React app.",
    },
    {
        "num": "06", "title": "Ship It",
        "learn": [
            "Deploy on Vercel or Netlify (both free)",
            "Write a proper GitHub README",
            "Write one short post about what you built",
            "Share it - LinkedIn, Reddit, anywhere",
        ],
        "skip":    "Nothing. Do all of it.",
        "project": "Your finished, live, shareable project.",
    },
]

DEBUG_STEPS = [
    (
        "Check the Console",
        [
            "Open DevTools (F12) and click the Console tab.",
            "Is there a red error message?",
            "  YES -> Read it carefully. Google the EXACT error text. Fix it, do not guess.",
            "  NO  -> Move to Step 2.",
        ],
    ),
    (
        "Check Your Logic and Data",
        [
            "Add console.log() before and after the broken area.",
            "Is the data undefined, null, or the wrong type?",
            "  YES -> Trace back to where the data comes from. Fix the source.",
            "  NO  -> Walk through the code line by line. Say it out loud.",
        ],
    ),
    (
        "Check the UI and CSS",
        [
            "Is the element visible but misplaced, or not showing at all?",
            "Right-click -> Inspect Element. Look for overridden (struck-through) styles.",
            "Quick test: add  border: 1px solid red;  to isolate a layout issue.",
        ],
    ),
    (
        "Use AI - But Do It Right",
        [
            "WRONG: Paste your whole file and say 'why doesn't this work?'",
            "RIGHT: Give it context:",
            "  - I am using [React / Firebase / plain JS]",
            "  - I expected [X] to happen",
            "  - Instead I got [Y]",
            "  - Here is the relevant code: [paste only the broken part]",
        ],
    ),
]

SYNTAX_ROWS = [
    ["JS ES6+",   "Arrow function",       "const greet = (n) => `Hello ${n}`"],
    ["JS ES6+",   "Destructure object",   "const { name, age } = user"],
    ["JS ES6+",   "Destructure array",    "const [first, second] = items"],
    ["JS ES6+",   "Spread operator",      "const arr2 = [...arr, newItem]"],
    ["JS ES6+",   "Optional chaining",    "user?.profile?.avatar"],
    ["JS ES6+",   "Nullish coalescing",   "const n = user.name ?? 'Anon'"],
    ["JS ES6+",   "Async / await",        "const d = await fetch(url).then(r=>r.json())"],
    ["JS ES6+",   ".map()",               "items.map(item => item.name)"],
    ["JS ES6+",   ".filter()",            "items.filter(item => item.active)"],
    ["JS ES6+",   ".find()",              "items.find(item => item.id === id)"],
    ["React",     "useState",             "const [val, setVal] = useState('')"],
    ["React",     "Update prev state",    "setCount(prev => prev + 1)"],
    ["React",     "useEffect on mount",   "useEffect(() => { fetch() }, [])"],
    ["React",     "useEffect on change",  "useEffect(() => { fetch() }, [id])"],
    ["React",     "Conditional render",   "isLoggedIn && <Dashboard />"],
    ["React",     "Ternary render",       "isOn ? <On /> : <Off />"],
    ["Firebase",  "Sign up",              "createUserWithEmailAndPassword(auth,e,p)"],
    ["Firebase",  "Sign in",              "signInWithEmailAndPassword(auth,e,p)"],
    ["Firebase",  "Sign out",             "signOut(auth)"],
    ["Firebase",  "Auth state listener",  "onAuthStateChanged(auth, user => {})"],
    ["Firebase",  "Add document",         "addDoc(collection(db,'posts'), data)"],
    ["Firebase",  "Set document",         "setDoc(doc(db,'users',uid), data)"],
    ["Firebase",  "Real-time listener",   "onSnapshot(collection(db,'posts'), cb)"],
    ["Firebase",  "Update fields",        "updateDoc(doc(db,'users',uid), {name})"],
    ["Firebase",  "Delete document",      "deleteDoc(doc(db,'users',uid))"],
]


# ── PDF class ----------------------------------------------------------------
class Blueprint(FPDF):

    def __init__(self):
        super().__init__()
        # top margin large enough to clear the running header
        self.set_margins(left=20, top=28, right=20)
        self.set_auto_page_break(auto=True, margin=22)

    # ── colour helpers -------------------------------------------------------
    def rgb(self, t):   self.set_text_color(*t)
    def fill(self, t):  self.set_fill_color(*t)
    def draw(self, t):  self.set_draw_color(*t)

    # ── running header (all pages except title page) -------------------------
    def header(self):
        if self.page_no() == 1:
            return
        # thin blue top bar
        self.fill(BLUE)
        self.rect(0, 0, 210, 8, "F")
        # guide title
        self.set_y(1)
        self.set_font("Helvetica", "B", 8)
        self.rgb(WHITE)
        self.cell(0, 6, "The 6-Month Build-First Developer Blueprint", align="C")
        # reset to content area
        self.set_y(12)
        self.set_line_width(0.2)
        self.draw(BLUE_MID)
        self.line(20, 12, 190, 12)
        self.ln(4)

    # ── footer ---------------------------------------------------------------
    def footer(self):
        self.set_y(-13)
        self.set_line_width(0.2)
        self.draw(BLUE_MID)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(1)
        self.set_font("Helvetica", "I", 8)
        self.rgb(MUTED)
        self.cell(0, 6, f"Page {self.page_no()}", align="C")

    # ── section heading ------------------------------------------------------
    def h1(self, text):
        self.ln(3)
        # full-width blue band
        self.fill(BLUE)
        self.rect(20, self.get_y(), self.epw, 10, "F")
        self.set_font("Helvetica", "B", 13)
        self.rgb(WHITE)
        # indent text inside band
        self.set_x(24)
        self.cell(self.epw - 4, 10, text, **NL)
        self.ln(4)

    # ── sub heading ----------------------------------------------------------
    def h2(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.rgb(BLUE)
        self.cell(0, 7, text, **NL)
        # underline
        y = self.get_y()
        self.fill(BLUE_MID)
        self.rect(20, y, self.epw, 0.5, "F")
        self.ln(3)

    def sub_heading(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 9)
        self.rgb(BLUE_DARK)
        self.cell(0, 6, text, **NL)
        self.ln(1)

    # ── body text ------------------------------------------------------------
    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.rgb(BODY)
        for i, para in enumerate(text.split("\n\n")):
            self.multi_cell(self.epw, 5.5, para.strip())
            if i < len(text.split("\n\n")) - 1:
                self.ln(3)
        self.ln(2)

    # ── bullet --------------------------------------------------------------
    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.rgb(BODY)
        self.set_x(24)
        self.fill(BLUE)
        # small filled square as bullet
        bx, by = self.get_x(), self.get_y() + 1.8
        self.rect(bx, by, 2, 2, "F")
        self.set_x(28)
        self.multi_cell(self.epw - 8, 5.8, text)

    # ── label + value --------------------------------------------------------
    def kv(self, label, value):
        # label on its own line (bold), value indented on the next line
        self.set_x(24)
        self.set_font("Helvetica", "B", 10)
        self.rgb(BLUE_DARK)
        self.cell(0, 5.5, label, **NL)
        self.set_x(30)
        self.set_font("Helvetica", "", 10)
        self.rgb(BODY)
        self.multi_cell(self.epw - 10, 5.5, value)
        self.ln(2)

    # ── highlighted note box ------------------------------------------------
    def note_box(self, text):
        self.ln(2)
        # measure text height first by doing a dry run
        self.set_font("Helvetica", "I", 10)
        # draw box
        pad = 4
        bx = 20
        by = self.get_y()
        bw = self.epw
        # draw background + border
        self.fill(BLUE_PALE)
        self.draw(BLUE)
        self.set_line_width(0.5)
        # We'll draw the rect after writing to know the height, so write first
        # then come back - use a simpler fixed padding approach
        self.set_xy(bx + pad, by + pad)
        self.rgb(BLUE_DARK)
        self.multi_cell(bw - pad * 2, 5.5, text)
        text_end_y = self.get_y()
        bh = text_end_y - by + pad
        # draw rect behind text (it draws on top visually but PDF layers stack)
        # Instead: draw rect first, rewrite text
        self.rect(bx, by, bw, bh, "DF")
        self.set_xy(bx + pad, by + pad)
        self.set_font("Helvetica", "I", 10)
        self.rgb(BLUE_DARK)
        self.multi_cell(bw - pad * 2, 5.5, text)
        self.ln(4)

    # ── month card ----------------------------------------------------------
    def month_card(self, num, title, learn, skip, project):
        if self.get_y() > 220:
            self.add_page()

        # header bar with month number
        card_y = self.get_y()
        self.fill(NAVY)
        self.rect(20, card_y, self.epw, 9, "F")
        self.set_font("Helvetica", "B", 10)
        self.rgb(BLUE_PALE)
        self.set_xy(24, card_y + 1)
        self.cell(14, 7, f"M{num}")
        self.rgb(WHITE)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, title, **NL)
        self.ln(2)

        # learn items
        self.set_font("Helvetica", "B", 9)
        self.rgb(BLUE)
        self.set_x(24)
        self.cell(0, 5, "What to learn:", **NL)
        for item in learn:
            self.bullet(item)

        self.ln(1)
        self.kv("Skip:", skip)
        self.kv("Project:", project)
        self.ln(3)

    # ── debug step ----------------------------------------------------------
    def debug_step(self, num, title, lines):
        if self.get_y() > 230:
            self.add_page()

        step_y = self.get_y()

        # circle with number
        cx, cy = 26, step_y + 4
        self.fill(BLUE)
        self.ellipse(cx - 4, cy - 4, 8, 8, "F")
        self.set_font("Helvetica", "B", 9)
        self.rgb(WHITE)
        self.set_xy(cx - 3, cy - 3.5)
        self.cell(6, 7, str(num), align="C")

        # title to the right of circle
        self.set_xy(34, step_y)
        self.set_font("Helvetica", "B", 11)
        self.rgb(NAVY)
        self.cell(0, 8, title, **NL)

        # detail lines
        for line in lines:
            self.set_x(34)
            self.set_font("Courier", "", 9)
            self.rgb(BODY)
            self.multi_cell(self.epw - 14, 5.2, line)

        self.ln(5)

        # connector dot
        if num < 4:
            self.fill(BLUE_MID)
            self.rect(25.5, self.get_y() - 1, 1, 4, "F")

    # ── table header --------------------------------------------------------
    def table_header(self, headers, widths):
        self.fill(NAVY)
        self.rgb(WHITE)
        self.set_font("Helvetica", "B", 9)
        for h, w in zip(headers, widths):
            self.cell(w, 8, "  " + h, border=0, fill=True)
        self.ln()


# ── Build the PDF -----------------------------------------------------------
def build_pdf(output="Developer_Blueprint.pdf"):
    pdf = Blueprint()

    # ========================================================================
    # TITLE PAGE
    # ========================================================================
    pdf.add_page()

    # navy header block
    pdf.fill(NAVY)
    pdf.rect(0, 0, 210, 90, "F")

    # blue accent stripe
    pdf.fill(BLUE)
    pdf.rect(0, 90, 210, 5, "F")

    # title text
    pdf.set_y(20)
    pdf.set_font("Helvetica", "B", 30)
    pdf.rgb(WHITE)
    pdf.cell(0, 13, "The 6-Month", align="C", **NL)
    pdf.cell(0, 13, "Build-First Developer", align="C", **NL)

    pdf.set_font("Helvetica", "B", 30)
    pdf.fill(BLUE)
    # highlight the word Blueprint
    bw = 90
    bx = (210 - bw) / 2
    pdf.rect(bx, pdf.get_y(), bw, 13, "F")
    pdf.rgb(WHITE)
    pdf.cell(0, 13, "Blueprint", align="C", **NL)

    pdf.ln(3)
    pdf.set_font("Helvetica", "", 12)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7, "For self-taught developers who are done watching", align="C", **NL)
    pdf.cell(0, 7, "and ready to build.", align="C", **NL)

    # what's inside panel
    pdf.set_y(106)
    pdf.fill(BLUE_PALE)
    pdf.draw(BLUE_MID)
    pdf.set_line_width(0.4)
    pdf.rect(30, 106, 150, 64, "DF")

    pdf.set_y(111)
    pdf.set_font("Helvetica", "B", 11)
    pdf.rgb(NAVY)
    pdf.cell(0, 7, "What's inside this guide:", align="C", **NL)
    pdf.ln(1)

    contents = [
        "Reality check - why tutorial-hell is keeping you stuck",
        "Month-by-month plan: HTML to deployed app",
        "A 4-step debugging flowchart",
        "Syntax cheat sheet: JS, React & Firebase",
        "A call to action that gets you building today",
    ]
    for item in contents:
        pdf.set_font("Helvetica", "", 10)
        pdf.rgb(BODY)
        pdf.cell(0, 8, item, align="C", **NL)

    # philosophy banner
    pdf.set_y(182)
    pdf.fill(BLUE)
    pdf.rect(20, 182, 170, 16, "F")
    pdf.set_y(186)
    pdf.set_font("Helvetica", "BI", 11)
    pdf.rgb(WHITE)
    pdf.cell(0, 8,
             '"Don\'t memorize, build. Don\'t finish the course, finish the project."',
             align="C", **NL)

    pdf.set_y(208)
    pdf.set_font("Helvetica", "", 9)
    pdf.rgb(MUTED)
    pdf.cell(0, 6, "buildwithcode.dev  |  2026", align="C", **NL)

    # ========================================================================
    # LICENCE PAGE
    # ========================================================================
    pdf.add_page()

    # centred navy header block
    pdf.fill(NAVY)
    pdf.rect(0, 0, 210, 40, "F")
    pdf.fill(BLUE)
    pdf.rect(0, 40, 210, 3, "F")

    pdf.set_y(12)
    pdf.set_font("Helvetica", "B", 18)
    pdf.rgb(WHITE)
    pdf.cell(0, 10, "Licence & Copyright Notice", align="C", **NL)
    pdf.set_font("Helvetica", "", 10)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7, "Please read before using this guide.", align="C", **NL)

    pdf.set_y(58)

    # copyright line
    pdf.set_font("Helvetica", "B", 13)
    pdf.rgb(NAVY)
    pdf.cell(0, 9, "Copyright (c) 2026 Dean Burt. All rights reserved.", align="C", **NL)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.rgb(BODY)
    pdf.multi_cell(
        pdf.epw, 6,
        "This PDF and all content within it is the sole intellectual property of Dean Burt "
        "(buildwithcode.dev). Purchasing this guide grants you a single-user personal licence only.",
        align="C"
    )
    pdf.ln(6)

    # permitted / not permitted boxes side by side
    col_w = (pdf.epw - 6) / 2

    # --- Permitted ---
    lx = pdf.l_margin
    by = pdf.get_y()
    pdf.fill(BLUE_PALE)
    pdf.set_draw_color(*BLUE_MID)
    pdf.set_line_width(0.5)
    pdf.rect(lx, by, col_w, 68, "DF")

    pdf.set_xy(lx + 4, by + 4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(BLUE_DARK)
    pdf.cell(col_w - 8, 7, "What you MAY do", **NL)
    permitted = [
        "Read and use this guide for your\npersonal learning and development.",
        "Print a single copy for personal use.",
        "Reference ideas and concepts in your\nown original work with attribution.",
        "Share the Gumroad purchase link\nwith others (not the file itself).",
    ]
    for item in permitted:
        pdf.set_x(lx + 4)
        pdf.set_font("Helvetica", "B", 9)
        pdf.rgb(BLUE)
        pdf.cell(5, 6, "+")
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(BODY)
        pdf.multi_cell(col_w - 14, 6, item)
        pdf.ln(1)

    # --- Not Permitted ---
    rx = lx + col_w + 6
    pdf.fill((255, 240, 240))
    pdf.set_draw_color(220, 38, 38)
    pdf.rect(rx, by, col_w, 68, "DF")

    pdf.set_xy(rx + 4, by + 4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 20, 20)
    pdf.cell(col_w - 8, 7, "What you may NOT do", **NL)
    not_permitted = [
        "Share, resell, or distribute this\nfile in any form.",
        "Upload it to file-sharing sites,\ncourses, or group chats.",
        "Reproduce substantial portions\nwithout written permission.",
        "Claim this content as your own\nor rebrand it.",
    ]
    for item in not_permitted:
        pdf.set_x(rx + 4)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(220, 38, 38)
        pdf.cell(5, 6, "x")
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(BODY)
        pdf.multi_cell(col_w - 14, 6, item)
        pdf.ln(1)

    pdf.set_y(by + 74)
    pdf.ln(4)

    # legal paragraph
    pdf.set_font("Helvetica", "", 9)
    pdf.rgb(MUTED)
    pdf.multi_cell(
        pdf.epw, 5.5,
        "Unauthorised reproduction, distribution, or resale of this material - in whole or in part, "
        "in any format - is strictly prohibited and may constitute copyright infringement under the "
        "Copyright, Designs and Patents Act 1988 (UK) and equivalent international law. "
        "Violation may result in legal action.",
        align="C"
    )

    pdf.ln(6)

    # contact line
    pdf.fill(BLUE)
    pdf.rect(20, pdf.get_y(), pdf.epw, 0.4, "F")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(NAVY)
    pdf.cell(0, 6, "Questions? Permissions?  buildwithcode.dev", align="C", **NL)
    pdf.set_font("Helvetica", "", 9)
    pdf.rgb(MUTED)
    pdf.cell(0, 6, "deanburt1308@gmail.com", align="C", **NL)

    # ========================================================================
    # PAGE 2 - INTRODUCTION
    # ========================================================================
    pdf.add_page()
    pdf.h1("The Truth About Coding")

    pdf.body(
        "You're not broken. You're not behind. You're overwhelmed - and that's by design.\n\n"
        "The tutorial industry profits from your confusion. Courses are built to keep you "
        "watching, not shipping. You've probably started three courses, finished zero, and "
        "feel guilty about it. Stop.\n\n"
        "Here's the truth: you don't need to finish the course. You need to finish the project.\n\n"
        "Nobody learned to swim by watching videos. Nobody landed a dev job by completing every "
        "module. The developers getting hired - and the ones building real businesses - learned "
        "by breaking things, fixing them, and building again.\n\n"
        "Burnout hits when you're consuming without creating. The fix is not a better course. "
        "It's a narrower focus and a real project to aim at.\n\n"
        "This guide gives you exactly that: a 6-month roadmap, a debugging process, and the "
        "syntax you'll actually use. Nothing more. Now close the tutorial and open your editor."
    )

    pdf.note_box(
        'Core philosophy: "Don\'t memorize, build. Don\'t finish the course, finish the project."'
    )

    pdf.h2("Why Tutorial-Hell Keeps You Stuck")
    for label, desc in [
        ("Passive learning:", "Watching code being written is not the same as writing it."),
        ("No end state:",     "Courses don't ship - projects do."),
        ("Scope creep:",      "One video leads to five. Five leads to a new course."),
        ("False progress:",   "Completion percentage is not the same as capability."),
    ]:
        pdf.kv(label, desc)

    # ========================================================================
    # PAGE 3 - ROADMAP OVERVIEW
    # ========================================================================
    pdf.add_page()
    pdf.h1("The 6-Month Roadmap")

    pdf.body(
        "You do not need to learn everything. You need to build something real. "
        "Follow this plan in order. Each month has one project - finish the project, then move on."
    )

    # summary table
    cw = [18, 46, 50, pdf.epw - 114]
    pdf.table_header(["Mo.", "Focus", "Milestone Project", "Key Skills"], cw)

    summary = [
        ("01", "HTML & CSS",        "Static personal site",        "Flexbox, box model, responsive"),
        ("02", "JS Fundamentals",   "Live widget on your site",    "DOM, events, fetch API"),
        ("03", "JS Deep Dive",      "Self-built JS app",           "ES6+, async/await, array methods"),
        ("04", "React",             "Rebuild app in React",        "Hooks, components, props"),
        ("05", "Firebase",          "Login + real-time data",      "Auth, Firestore, onSnapshot"),
        ("06", "Ship It",           "Deployed live project",       "Vercel/Netlify, README, share"),
    ]
    for idx, (mo, focus, proj, skills) in enumerate(summary):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)
        pdf.rgb(BODY)
        pdf.set_font("Helvetica", "B", 9)
        pdf.rgb(BLUE)
        pdf.cell(cw[0], 7, f"  {mo}", border=0, fill=True)
        pdf.set_font("Helvetica", "B", 9)
        pdf.rgb(NAVY)
        pdf.cell(cw[1], 7, focus, border=0, fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(BODY)
        pdf.cell(cw[2], 7, proj, border=0, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(MUTED)
        pdf.cell(cw[3], 7, skills, border=0, fill=True)
        pdf.ln()

    pdf.ln(6)

    # ========================================================================
    # PAGES 4-5 - MONTH BY MONTH DETAIL
    # ========================================================================
    pdf.h1("Month-by-Month Breakdown")
    pdf.ln(2)

    for m in MONTHS:
        pdf.month_card(
            m["num"], m["title"], m["learn"], m["skip"], m["project"]
        )

    # ========================================================================
    # PAGE - DEBUGGING FLOWCHART
    # ========================================================================
    pdf.add_page()
    pdf.h1("The Debugger's Flowchart")

    pdf.body(
        "When something breaks - and it will - follow these four steps in order. "
        "Do not skip ahead to AI. Work through each step first."
    )
    pdf.ln(2)

    for i, (title, lines) in enumerate(DEBUG_STEPS, 1):
        pdf.debug_step(i, title, lines)

    pdf.note_box(
        "Golden rule: if you cannot explain the bug in one sentence, "
        "you have not looked closely enough yet."
    )

    # ========================================================================
    # PAGE - SYNTAX CHEAT SHEET
    # ========================================================================
    pdf.add_page()
    pdf.h1("Essential Syntax Cheat Sheet")
    pdf.body("The patterns you will use every single day. Save this page.")

    cw2 = [22, 48, pdf.epw - 70]
    pdf.table_header(["Category", "Concept", "Syntax / Code"], cw2)

    current_cat = ""
    for idx, (cat, concept, code) in enumerate(SYNTAX_ROWS):
        if pdf.get_y() > 260:
            pdf.add_page()
            pdf.table_header(["Category", "Concept", "Syntax / Code"], cw2)

        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)

        pdf.set_font("Helvetica", "B", 8)
        pdf.rgb(BLUE)
        pdf.cell(cw2[0], 6.5, "  " + (cat if cat != current_cat else ""),
                 border=0, fill=True)
        if cat != current_cat:
            current_cat = cat

        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(BODY)
        pdf.cell(cw2[1], 6.5, concept, border=0, fill=True)

        pdf.set_font("Courier", "", 7.5)
        pdf.rgb(NAVY)
        pdf.cell(cw2[2], 6.5, code, border=0, fill=True)
        pdf.ln()

    # ========================================================================
    # PAGE - REACT HOOKS CHEAT SHEET
    # ========================================================================
    pdf.add_page()
    pdf.h1("React Hooks Cheat Sheet")
    pdf.body(
        "Hooks are the engine of modern React. Stop memorising the docs - "
        "understand what each hook is FOR and you will never forget it."
    )

    REACT_HOOKS = [
        ("useState",    "Store and update any local value",
         "const [count, setCount] = useState(0)"),
        ("useEffect",   "Run code on mount, update, or unmount",
         "useEffect(() => { fetchData() }, [id])"),
        ("useContext",  "Read shared data without prop drilling",
         "const user = useContext(UserContext)"),
        ("useRef",      "Access a DOM element or persist a value",
         "const inputRef = useRef(null)"),
        ("useMemo",     "Cache an expensive calculation result",
         "const total = useMemo(() => calc(items), [items])"),
        ("useCallback", "Cache a function so it does not re-create",
         "const fn = useCallback(() => doThing(id), [id])"),
    ]

    cw_hooks = [32, 56, pdf.epw - 88]
    pdf.table_header(["Hook", "Use Case", "Example"], cw_hooks)
    for idx, (hook, use, example) in enumerate(REACT_HOOKS):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)
        pdf.set_font("Helvetica", "B", 8)
        pdf.rgb(BLUE)
        pdf.cell(cw_hooks[0], 7, "  " + hook, border=0, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(BODY)
        pdf.cell(cw_hooks[1], 7, use, border=0, fill=True)
        pdf.set_font("Courier", "", 7.5)
        pdf.rgb(NAVY)
        pdf.cell(cw_hooks[2], 7, example, border=0, fill=True)
        pdf.ln()

    pdf.ln(5)
    pdf.h2("The Two Patterns You Will Use Every Day")

    pdf.sub_heading("useState - update based on previous value")
    pdf.set_font("Courier", "", 9)
    pdf.rgb(NAVY)
    pdf.fill((240, 244, 255))
    pdf.rect(20, pdf.get_y(), pdf.epw, 22, "F")
    pdf.set_x(24)
    pdf.cell(0, 6, "const [items, setItems] = useState([]);", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "setItems(prev => [...prev, newItem]);  // always use prev for arrays", **NL)
    pdf.ln(4)

    pdf.sub_heading("useEffect - fetch on mount, clean up on unmount")
    pdf.set_font("Courier", "", 9)
    pdf.rgb(NAVY)
    pdf.fill((240, 244, 255))
    pdf.rect(20, pdf.get_y(), pdf.epw, 28, "F")
    pdf.set_x(24)
    pdf.cell(0, 6, "useEffect(() => {", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "  const unsub = onSnapshot(collection(db,'posts'), snap => {", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "    setPosts(snap.docs.map(d => ({ id: d.id, ...d.data() })));", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "  });", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "  return () => unsub();   // cleanup prevents memory leaks", **NL)
    pdf.set_x(24)
    pdf.cell(0, 6, "}, []);  // [] = run once on mount", **NL)
    pdf.ln(4)

    pdf.note_box(
        "Rule of hooks: only call hooks at the top level of a component. "
        "Never inside loops, conditions, or nested functions."
    )

    # ========================================================================
    # PAGE - FIREBASE CRUD CHEAT SHEET
    # ========================================================================
    pdf.add_page()
    pdf.h1("Firebase Firestore CRUD Cheat Sheet")
    pdf.body(
        "Firebase handles your backend so you can focus on building. "
        "No schema. No migrations. No server. Just data."
    )

    pdf.h2("Why 'No Schema' Is a Superpower")
    pdf.body(
        "Traditional databases need you to define every column before you store anything. "
        "Firestore does not. You can store any shape of data in any document at any time. "
        "That means you build faster, iterate freely, and never run a migration script again. "
        "Just push the data and Firestore figures out the rest."
    )

    FIREBASE_CRUD = [
        ("addDoc",    "Create (auto ID)",   "addDoc(collection(db,'posts'), { title, body, uid })"),
        ("setDoc",    "Create (custom ID)", "setDoc(doc(db,'users',uid), { name, email })"),
        ("getDoc",    "Read one doc",       "const snap = await getDoc(doc(db,'users',uid))"),
        ("getDocs",   "Read collection",    "const snap = await getDocs(collection(db,'posts'))"),
        ("onSnapshot","Real-time listen",   "onSnapshot(collection(db,'posts'), snap => {})"),
        ("updateDoc", "Update fields",      "updateDoc(doc(db,'users',uid), { name: 'Dean' })"),
        ("deleteDoc", "Delete a doc",       "deleteDoc(doc(db,'users',uid))"),
        ("query",     "Filter results",     "query(collection(db,'posts'), where('uid','==',uid))"),
    ]

    cw_fb = [26, 30, pdf.epw - 56]
    pdf.table_header(["Method", "Operation", "Example"], cw_fb)
    for idx, (method, op, example) in enumerate(FIREBASE_CRUD):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)
        pdf.set_font("Helvetica", "B", 8)
        pdf.rgb(BLUE)
        pdf.cell(cw_fb[0], 7, "  " + method, border=0, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(BODY)
        pdf.cell(cw_fb[1], 7, op, border=0, fill=True)
        pdf.set_font("Courier", "", 7.5)
        pdf.rgb(NAVY)
        pdf.cell(cw_fb[2], 7, example, border=0, fill=True)
        pdf.ln()

    pdf.ln(5)
    pdf.h2("The Pattern You Will Use in Every App")
    pdf.set_font("Courier", "", 8.5)
    pdf.rgb(NAVY)
    pdf.fill((240, 244, 255))
    code_y = pdf.get_y()
    pdf.rect(20, code_y, pdf.epw, 52, "F")
    for line in [
        "import { addDoc, collection, serverTimestamp } from 'firebase/firestore';",
        "",
        "const handleSubmit = async () => {",
        "  await addDoc(collection(db, 'posts'), {",
        "    title,",
        "    body,",
        "    uid:       auth.currentUser.uid,",
        "    createdAt: serverTimestamp()     // server-side timestamp, always",
        "  });",
        "};",
    ]:
        pdf.set_x(24)
        pdf.cell(0, 5.5, line, **NL)

    pdf.ln(4)
    pdf.note_box(
        "Auth + Firestore together: always store the user's uid on every document. "
        "Use Firestore Security Rules to make sure users can only read and write their own data."
    )

    # ========================================================================
    # PAGE - GIT CHEAT SHEET
    # ========================================================================
    pdf.add_page()
    pdf.h1("Git Cheat Sheet - 10 Commands You Need")
    pdf.body(
        "Git is non-negotiable. Every developer uses it. "
        "You do not need to know everything - you need to know these ten commands cold."
    )

    GIT_COMMANDS = [
        ("git init",              "Start a new local repository in the current folder"),
        ("git add .",             "Stage all changed files ready for a commit"),
        ("git commit -m 'msg'",   "Save a snapshot with a message describing what changed"),
        ("git push origin main",  "Upload your commits to GitHub"),
        ("git pull origin main",  "Download and merge the latest changes from GitHub"),
        ("git branch name",       "Create a new branch called 'name'"),
        ("git checkout name",     "Switch to an existing branch"),
        ("git merge name",        "Merge branch 'name' into your current branch"),
        ("git status",            "See which files are staged, changed, or untracked"),
        ("git log --oneline",     "View recent commit history, one line per commit"),
    ]

    cw_git = [52, pdf.epw - 52]
    pdf.table_header(["Command", "What It Does"], cw_git)
    for idx, (cmd, desc) in enumerate(GIT_COMMANDS):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)
        pdf.set_font("Courier", "B", 8)
        pdf.rgb(NAVY)
        pdf.cell(cw_git[0], 7, "  " + cmd, border=0, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(BODY)
        pdf.cell(cw_git[1], 7, desc, border=0, fill=True)
        pdf.ln()

    pdf.ln(5)
    pdf.h2("Undo - The Commands That Save You")

    UNDO_CMDS = [
        ("git restore .",
         "Discard all unstaged changes in your working directory"),
        ("git reset HEAD~1",
         "Undo the last commit but keep your changes staged"),
        ("git reset --hard HEAD~1",
         "Undo the last commit AND discard all changes (cannot be undone)"),
        ("git revert <hash>",
         "Create a new commit that undoes a specific past commit safely"),
        ("git stash",
         "Temporarily shelve all changes so you can switch branches cleanly"),
        ("git stash pop",
         "Restore your most recently stashed changes"),
    ]

    cw_undo = [52, pdf.epw - 52]
    pdf.table_header(["Command", "What It Undoes"], cw_undo)
    for idx, (cmd, desc) in enumerate(UNDO_CMDS):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        pdf.fill(bg)
        pdf.set_font("Courier", "B", 8)
        pdf.rgb(NAVY)
        pdf.cell(cw_undo[0], 7, "  " + cmd, border=0, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.rgb(BODY)
        pdf.cell(cw_undo[1], 7, desc, border=0, fill=True)
        pdf.ln()

    pdf.ln(4)
    pdf.note_box(
        "Commit early and often. A commit is a save point. "
        "You cannot lose work you have committed. Make small, focused commits with clear messages."
    )

    # ========================================================================
    # PAGE - AI CO-PILOT STRATEGY
    # ========================================================================
    pdf.add_page()
    pdf.h1("The AI Co-Pilot Strategy")
    pdf.body(
        "Mastering the tool without losing the skill.\n\n"
        "AI coding assistants are the most powerful tool a self-taught developer has ever had access to. "
        "They are also the fastest way to stay permanently junior if you use them wrong."
    )

    # Golden Rule
    pdf.h2("The Golden Rule")
    pdf.body(
        "Copy-pasting AI code you do not understand is not productivity - it is debt. "
        "Every line you paste without reading is a gap in your mental model that will surface "
        "at the worst possible moment: in an interview, in production, or the next time you need "
        "to build something similar on your own. "
        "Senior developers use AI to move faster. Junior developers use AI to avoid thinking. "
        "The difference is not the tool - it is the habit."
    )

    # 3-Step Framework
    pdf.h2("The 3-Step AI Prompting Framework")
    pdf.body(
        "These three prompt templates turn AI from an answer machine into a mentor. "
        "Use them every time."
    )

    pdf.sub_heading("Step 1: The Explain Prompt")
    pdf.body(
        "Use this when you read code you do not fully understand. "
        "Never move on until you can explain it back in your own words."
    )

    # Explain prompt code block
    pdf.set_font("Courier", "", 8)
    pdf.rgb(NAVY)
    pdf.fill((240, 244, 255))
    explain_lines = [
        'I am a self-taught developer learning [React / Firebase / JS].',
        'Explain this code to me like a mentor, not a documentation page.',
        'Walk through it line by line. Tell me:',
        '  1. What each part does and WHY it is written that way.',
        '  2. Any pattern or concept I should learn properly.',
        '  3. What I would need to change if [X requirement changed].',
        '',
        '[paste your code here]',
    ]
    block_h = len(explain_lines) * 5.5 + 6
    pdf.rect(20, pdf.get_y(), pdf.epw, block_h, "F")
    for line in explain_lines:
        pdf.set_x(24)
        pdf.cell(0, 5.5, line, **NL)
    pdf.ln(3)

    pdf.sub_heading("Step 2: The Debug Prompt")
    pdf.body(
        "Use this when you hit an error. Force yourself to give context - "
        "the act of writing it out often reveals the bug before AI even responds."
    )

    debug_lines = [
        'I am debugging a problem in my [React / Firebase / JS] app.',
        'Do NOT just fix it. Explain the logic error I made.',
        '',
        'Here is what I expected to happen:',
        '[describe expected behaviour]',
        '',
        'Here is what is actually happening:',
        '[describe actual behaviour / paste error message]',
        '',
        'Here is the relevant code (not the whole file):',
        '[paste only the broken section]',
        '',
        'Walk me through why it is broken and what the correct mental model is.',
    ]
    block_h2 = len(debug_lines) * 5.5 + 6
    pdf.fill((240, 244, 255))
    pdf.rect(20, pdf.get_y(), pdf.epw, block_h2, "F")
    for line in debug_lines:
        pdf.set_x(24)
        pdf.cell(0, 5.5, line, **NL)
    pdf.ln(3)

    pdf.sub_heading("Step 3: The Refactor Prompt")
    pdf.body(
        "Use this after your code works. Getting it working is 50% of the job. "
        "The other 50% is writing it so that a professional would not wince reading it."
    )

    refactor_lines = [
        'My code works but I want to write it like a professional.',
        'Show me a more senior way to write this using best practices.',
        '',
        'For each change you make:',
        '  1. Tell me what pattern or principle you are applying.',
        '  2. Explain WHY it is better, not just that it is better.',
        '  3. Flag anything I should learn more about.',
        '',
        '[paste your working code here]',
    ]
    block_h3 = len(refactor_lines) * 5.5 + 6
    pdf.fill((240, 244, 255))
    pdf.rect(20, pdf.get_y(), pdf.epw, block_h3, "F")
    for line in refactor_lines:
        pdf.set_x(24)
        pdf.cell(0, 5.5, line, **NL)
    pdf.ln(5)

    # Red Line List
    pdf.h2("The Red Line - Never Do These With AI")

    RED_LINES = [
        (
            "Never copy-paste code you cannot explain line by line.",
            "If you cannot walk someone through it, you do not own it. "
            "Paste it, run it, then spend five minutes reading it until you do."
        ),
        (
            "Never trust AI-generated database or auth logic without checking.",
            "AI will confidently write Firestore security rules or auth flows that have "
            "critical vulnerabilities. Always read it. Always test edge cases. "
            "Security is the one place where 'it looks right' is not good enough."
        ),
        (
            "Never use AI to avoid the error message.",
            "When something breaks, read the error first. Google it. Form a hypothesis. "
            "Then use AI. The debugging instinct you build from that process is "
            "what separates developers who can work anywhere from developers who "
            "cannot function without an assistant."
        ),
    ]

    for i, (rule, detail) in enumerate(RED_LINES):
        # Red number badge
        pdf.fill((220, 38, 38))
        bx = 20
        by = pdf.get_y() + 1
        pdf.rect(bx, by, 6, 6, "F")
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(bx + 0.5, by - 0.5)
        pdf.cell(5, 7, str(i + 1), border=0)
        # Rule text
        pdf.set_xy(30, pdf.get_y())
        pdf.set_font("Helvetica", "B", 10)
        pdf.rgb(NAVY)
        pdf.multi_cell(pdf.epw - 10, 5.5, rule)
        pdf.set_x(30)
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(BODY)
        pdf.multi_cell(pdf.epw - 10, 5.5, detail)
        pdf.ln(3)

    pdf.note_box(
        "The goal is not to avoid AI. The goal is to use it the way a senior developer does: "
        "as a fast path to understanding, not a shortcut around it."
    )

    # ========================================================================
    # FINAL PAGE - CALL TO ACTION
    # ========================================================================
    pdf.add_page()
    pdf.h1("Stop Watching. Start Building.")

    pdf.body(
        "You've been preparing long enough.\n\n"
        "The developers who get jobs and ship real products are not the ones who "
        "finished the most courses. They are the ones who built the most things. "
        "Every bug you fix teaches you more than any tutorial will.\n\n"
        "Your next step is not another video."
    )

    pdf.h2("Pick one right now and start today:")
    for action in [
        "Build a personal site and deploy it today",
        "Build a to-do app in React with Firebase login",
        "Take something you use every day and rebuild a version of it",
    ]:
        pdf.bullet(action)

    pdf.ln(6)
    pdf.body(
        "You do not need permission. You do not need to feel ready. "
        "You need to open your editor and write the first line."
    )

    # closing banner
    pdf.ln(4)
    by = pdf.get_y()
    pdf.fill(NAVY)
    pdf.rect(20, by, pdf.epw, 34, "F")
    pdf.fill(BLUE)
    pdf.rect(20, by, 5, 34, "F")

    pdf.set_y(by + 7)
    pdf.set_font("Helvetica", "B", 14)
    pdf.rgb(WHITE)
    pdf.cell(0, 9, "Don't memorize, build.", align="C", **NL)
    pdf.cell(0, 9, "Don't finish the course, finish the project.", align="C", **NL)
    pdf.ln(1)
    pdf.set_font("Helvetica", "BI", 12)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 8, "Now go ship something.", align="C", **NL)

    pdf.output(output)
    print(f"\n  Done - PDF saved as: {output}\n")


if __name__ == "__main__":
    build_pdf("Developer_Blueprint.pdf")
