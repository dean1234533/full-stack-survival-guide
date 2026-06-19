"""
Generates: FullStack_Field_Manual.pdf
Gumroad Premium Toolkit - dense technical reference
Run: python3 generate_field_manual.py
"""

from fpdf import FPDF, XPos, YPos

NAVY      = (10,  30,  80)
BLUE      = (37,  99, 235)
BLUE_DARK = (29,  78, 216)
BLUE_PALE = (219, 234, 254)
BLUE_MID  = (191, 219, 254)
WHITE     = (255, 255, 255)
BODY      = (30,  41,  59)
MUTED     = (100, 116, 139)
GREEN     = (22, 163,  74)
GREEN_PAL = (220, 252, 231)
RED       = (220,  38,  38)
RED_PAL   = (254, 226, 226)
AMBER     = (217, 119,   6)
AMBER_PAL = (254, 243, 199)
CODE_BG   = (240, 244, 255)

NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}


class Manual(FPDF):
    _section_label = ""

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 10, "F")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*BLUE_PALE)
        self.set_y(1.5)
        self.cell(0, 7, "  FULL-STACK DEVELOPER FIELD MANUAL  |  buildwithcode.dev", align="L")
        self.set_font("Helvetica", "", 7.5)
        self.cell(0, 7, f"{self._section_label}  |  p.{self.page_no()-1}  ",
                  align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_fill_color(*BLUE)
        self.rect(0, 10, 210, 1.5, "F")
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(*NAVY)
        self.rect(0, self.get_y(), 210, 12, "F")
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 10,
            "  Copyright (c) 2026 Dean Burt. Personal use only. Do not redistribute.  "
            "deanburt.gumroad.com/l/wkiilt",
            align="C")

    def rgb(self, t):  self.set_text_color(*t)
    def fill(self, t): self.set_fill_color(*t)

    def section_page(self, label, subtitle=""):
        self._section_label = label.upper()
        self.add_page()
        self.fill(NAVY)
        self.rect(0, 0, 210, 297, "F")
        self.fill(BLUE)
        self.rect(0, 0, 8, 297, "F")
        self.set_y(100)
        self.set_font("Helvetica", "B", 36)
        self.rgb(WHITE)
        self.cell(0, 16, label, align="C", **NL)
        if subtitle:
            self.ln(2)
            self.set_font("Helvetica", "", 14)
            self.rgb(BLUE_PALE)
            self.multi_cell(0, 8, subtitle, align="C")
        self.fill(BLUE)
        sw = 60
        sx = (210 - sw) / 2
        self.rect(sx, self.get_y() + 4, sw, 2, "F")

    def h1(self, text):
        self.ln(3)
        self.fill(NAVY)
        self.rect(self.l_margin, self.get_y(), self.epw, 11, "F")
        self.fill(BLUE)
        self.rect(self.l_margin, self.get_y() + 9, self.epw, 2, "F")
        self.set_font("Helvetica", "B", 13)
        self.rgb(WHITE)
        self.cell(self.epw, 11, "  " + text, **NL)
        self.ln(4)

    def h2(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 10.5)
        self.rgb(BLUE_DARK)
        self.cell(0, 7, text, **NL)
        self.fill(BLUE_MID)
        self.rect(self.l_margin, self.get_y(), self.epw, 0.5, "F")
        self.ln(3)

    def body(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.rgb(BODY)
        self.multi_cell(self.epw, 5.5, text)
        self.ln(2)

    def table_header(self, cols, widths):
        self.fill(NAVY)
        self.set_font("Helvetica", "B", 8.5)
        self.rgb(WHITE)
        for col, w in zip(cols, widths):
            self.cell(w, 8, "  " + col, fill=True, border=0)
        self.ln()

    def table_row(self, cells, widths, idx=0):
        bg = BLUE_PALE if idx % 2 == 0 else WHITE
        self.fill(bg)
        fonts = [("Helvetica", "B", 8), ("Helvetica", "", 8.5), ("Courier", "", 7.5)]
        for i, (cell, w) in enumerate(zip(cells, widths)):
            f = fonts[min(i, len(fonts)-1)]
            self.set_font(f[0], f[1], f[2])
            if i == 0:
                self.rgb(BLUE_DARK)
            elif i == len(cells) - 1:
                self.rgb(NAVY)
            else:
                self.rgb(BODY)
            self.cell(w, 7, "  " + cell, fill=True, border=0)
        self.ln()

    def code_block(self, lines):
        self.fill(CODE_BG)
        h = len(lines) * 5.5 + 6
        self.rect(self.l_margin, self.get_y(), self.epw, h, "F")
        self.set_font("Courier", "", 8.5)
        self.rgb(NAVY)
        for line in lines:
            self.set_x(self.l_margin + 4)
            self.cell(0, 5.5, line, **NL)
        self.ln(3)

    def pro_tip(self, text):
        self.ln(2)
        self.fill(GREEN_PAL)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.6)
        ty = self.get_y()
        self.set_font("Helvetica", "", 8.5)
        lines = self.multi_cell(self.epw - 14, 5.5, text, dry_run=True, output="LINES")
        h = len(lines) * 5.5 + 12
        self.rect(self.l_margin, ty, self.epw, h, "DF")
        self.fill(GREEN)
        self.rect(self.l_margin, ty, 3, h, "F")
        self.set_xy(self.l_margin + 7, ty + 3)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GREEN)
        self.cell(0, 5, "PRO TIP", **NL)
        self.set_x(self.l_margin + 7)
        self.set_font("Helvetica", "", 8.5)
        self.rgb(BODY)
        self.multi_cell(self.epw - 10, 5.5, text)
        self.set_y(ty + h + 3)

    def warning(self, text):
        self.ln(2)
        self.fill(RED_PAL)
        self.set_draw_color(*RED)
        self.set_line_width(0.6)
        ty = self.get_y()
        self.set_font("Helvetica", "", 8.5)
        lines = self.multi_cell(self.epw - 14, 5.5, text, dry_run=True, output="LINES")
        h = len(lines) * 5.5 + 12
        self.rect(self.l_margin, ty, self.epw, h, "DF")
        self.fill(RED)
        self.rect(self.l_margin, ty, 3, h, "F")
        self.set_xy(self.l_margin + 7, ty + 3)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*RED)
        self.cell(0, 5, "RED LINE - NEVER DO THIS", **NL)
        self.set_x(self.l_margin + 7)
        self.set_font("Helvetica", "", 8.5)
        self.rgb(BODY)
        self.multi_cell(self.epw - 10, 5.5, text)
        self.set_y(ty + h + 3)

    def note(self, text):
        self.ln(2)
        self.fill(AMBER_PAL)
        self.set_draw_color(*AMBER)
        self.set_line_width(0.6)
        ty = self.get_y()
        self.set_font("Helvetica", "", 8.5)
        lines = self.multi_cell(self.epw - 14, 5.5, text, dry_run=True, output="LINES")
        h = len(lines) * 5.5 + 10
        self.rect(self.l_margin, ty, self.epw, h, "DF")
        self.fill(AMBER)
        self.rect(self.l_margin, ty, 3, h, "F")
        self.set_xy(self.l_margin + 7, ty + 3)
        self.set_font("Helvetica", "", 8.5)
        self.rgb(BODY)
        self.multi_cell(self.epw - 10, 5.5, text)
        self.set_y(ty + h + 3)


def build_manual(output="FullStack_Field_Manual.pdf"):
    pdf = Manual()
    pdf.set_margins(16, 18, 16)
    pdf.set_auto_page_break(True, margin=18)

    # ════════════════════════════════════════════════════════════════════════
    # COVER
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.fill(NAVY)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.fill(BLUE)
    pdf.rect(0, 0, 8, 297, "F")
    pdf.rect(202, 0, 8, 297, "F")
    pdf.rect(0, 0, 210, 4, "F")
    pdf.rect(0, 293, 210, 4, "F")

    pdf.set_y(38)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7, "PREMIUM DEVELOPER REFERENCE - 2026 EDITION", align="C", **NL)
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 38)
    pdf.rgb(WHITE)
    pdf.cell(0, 17, "FULL-STACK", align="C", **NL)
    pdf.set_font("Helvetica", "B", 38)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 17, "DEVELOPER", align="C", **NL)

    fw = 130
    fx = (210 - fw) / 2
    pdf.fill(BLUE)
    pdf.rect(fx, pdf.get_y(), fw, 18, "F")
    pdf.set_font("Helvetica", "B", 38)
    pdf.rgb(WHITE)
    pdf.cell(0, 18, "FIELD MANUAL", align="C", **NL)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.rgb(BLUE_PALE)
    pdf.multi_cell(0, 7,
        "The complete technical reference for self-taught developers.\n"
        "Print it. Keep it open. Build with it.", align="C")

    pdf.set_y(168)
    pdf.fill(BLUE_DARK)
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.5)
    pdf.rect(26, 168, 158, 78, "DF")
    pdf.set_y(175)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 6, "WHAT'S INSIDE", align="C", **NL)
    pdf.ln(1)
    sections = [
        "The Master Debugging Flowchart",
        "JavaScript ES6+ Cheat Sheet (25 patterns)",
        "React Hooks Cheat Sheet (6 hooks + real patterns)",
        "Firebase Firestore CRUD Cheat Sheet",
        "Git Essentials + Full Undo Toolkit",
        "The AI Co-Pilot Strategy + 3 Prompt Templates",
        "The Developer Toolbelt (free tools that save hours)",
    ]
    for s in sections:
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(WHITE)
        pdf.cell(0, 7, f"  >>  {s}", align="C", **NL)

    pdf.set_y(262)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 6, "Dean Burt  |  buildwithcode.dev  |  deanburt.gumroad.com/l/wkiilt",
             align="C", **NL)
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.rgb(MUTED)
    pdf.cell(0, 5,
        "Copyright (c) 2026 Dean Burt. Personal use only. Do not redistribute.",
        align="C", **NL)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 1 - DEBUGGING
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("The Debugging Flowchart",
                     "The exact 4-step process professionals follow every time something breaks.")
    pdf.add_page()
    pdf._section_label = "DEBUGGING"
    pdf.h1("The Master Debugging Flowchart")
    pdf.body(
        "Follow these steps in order. Do not skip. Do not guess. One methodical pass through "
        "this process will resolve the vast majority of bugs you will ever encounter."
    )

    steps = [
        ("STEP 1", "CHECK THE CONSOLE",
         "Open DevTools (F12) -> Console tab. Read every red error word by word.",
         "Google the EXACT error text in quotes. Most bugs are diagnosed here in under 2 minutes. "
         "Read the line number. Go directly to that line."),
        ("STEP 2", "CHECK YOUR LOGIC AND DATA",
         "Add console.log() at every step around the problem area.",
         "Is the data undefined, null, or the wrong type? Trace it back to the source. "
         "Walk through the logic line by line out loud (rubber duck debugging works)."),
        ("STEP 3", "CHECK THE UI AND CSS",
         "Right-click -> Inspect Element. Look at computed styles.",
         "Struck-through rules = overridden styles. Zero height/width = invisible element. "
         "Quick test: add 'border: 1px solid red' to isolate any element."),
        ("STEP 4", "USE AI - THE RIGHT WAY",
         "Describe context + expected + actual + relevant code only.",
         "Wrong: 'Here is my whole file, why doesn't it work?' "
         "Right: 'I'm using React. I expected X. I got Y. Here is the broken section: [code]'"),
    ]

    for snum, stitle, sdesc, sdetail in steps:
        self_y = pdf.get_y()
        pdf.fill(BLUE_DARK)
        pdf.rect(pdf.l_margin, self_y, 22, 22, "F")
        pdf.set_xy(pdf.l_margin, self_y + 2)
        pdf.set_font("Helvetica", "B", 7)
        pdf.rgb(BLUE_PALE)
        pdf.cell(22, 5, snum, align="C", **NL)
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 6.5)
        pdf.rgb(WHITE)
        pdf.cell(22, 5, stitle, align="C", **NL)

        pdf.fill(BLUE_PALE)
        pdf.rect(pdf.l_margin + 22, self_y, pdf.epw - 22, 22, "F")
        pdf.set_xy(pdf.l_margin + 25, self_y + 3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.rgb(BLUE_DARK)
        pdf.cell(pdf.epw - 28, 6, sdesc, **NL)
        pdf.set_x(pdf.l_margin + 25)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.rgb(BODY)
        pdf.multi_cell(pdf.epw - 28, 5, sdetail)
        pdf.set_y(self_y + 26)

    pdf.ln(2)
    pdf.pro_tip(
        "If you cannot describe the bug in one sentence, you have not looked closely enough yet. "
        "Write the bug description down before you start debugging."
    )
    pdf.warning(
        "Never change multiple things at once. One change, one test. "
        "Each extra variable you introduce makes the bug harder to find, not easier."
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 2 - JAVASCRIPT
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("JavaScript ES6+",
                     "25 must-know patterns. The syntax you will reach for every single day.")
    pdf.add_page()
    pdf._section_label = "JAVASCRIPT ES6+"
    pdf.h1("JavaScript ES6+ Cheat Sheet")

    JS = [
        ("Arrow function",        "Concise function syntax",
         "const greet = (name) => `Hello, ${name}`"),
        ("Destructure object",    "Pull named values out of an object",
         "const { name, age } = user"),
        ("Destructure array",     "Pull values out by position",
         "const [first, second] = items"),
        ("Default params",        "Fallback if argument is undefined",
         "const fn = (x = 0) => x * 2"),
        ("Spread - array",        "Copy or merge arrays",
         "const newArr = [...arr, newItem]"),
        ("Spread - object",       "Copy or merge objects",
         "const newObj = { ...obj, key: val }"),
        ("Rest params",           "Collect remaining args into array",
         "const fn = (first, ...rest) => rest"),
        ("Template literal",      "Embed expressions in strings",
         "const msg = `Hi ${name}, you are ${age}`"),
        ("Optional chaining",     "Safe access - no crash if null",
         "const avatar = user?.profile?.avatar"),
        ("Nullish coalescing",    "Default only if null/undefined",
         'const name = user.name ?? "Anonymous"'),
        ("Async/await",           "Handle promises cleanly",
         "const data = await fetch(url).then(r => r.json())"),
        ("try/catch",             "Handle async errors",
         "try { await fn() } catch (err) { console.log(err) }"),
        ("Array .map()",          "Transform every item",
         "const names = items.map(item => item.name)"),
        ("Array .filter()",       "Keep only matching items",
         "const active = items.filter(item => item.active)"),
        ("Array .find()",         "First matching item",
         "const match = items.find(item => item.id === id)"),
        ("Array .reduce()",       "Accumulate to single value",
         "const total = items.reduce((sum, i) => sum + i.price, 0)"),
        ("Array .some()",         "True if any item matches",
         "const hasAdmin = users.some(u => u.role === 'admin')"),
        ("Array .every()",        "True if all items match",
         "const allDone = tasks.every(t => t.complete)"),
        ("Ternary",               "Inline if/else",
         "const label = isLoggedIn ? 'Welcome' : 'Sign in'"),
        ("Short-circuit &&",      "Render only if truthy",
         "isLoggedIn && <Dashboard />"),
        ("Short-circuit ||",      "Fallback if falsy",
         "const val = input || 'default'"),
        ("Promise.all()",         "Run multiple async calls in parallel",
         "const [a, b] = await Promise.all([fn1(), fn2()])"),
        ("Object.keys/values",    "Iterate over object properties",
         "Object.entries(obj).map(([k, v]) => `${k}: ${v}`)"),
        ("Dynamic key",           "Set object key from variable",
         "const obj = { [fieldName]: value }"),
        ("Computed import",       "Named import from module",
         "import { useState, useEffect } from 'react'"),
    ]

    cw = [38, 42, pdf.epw - 80]
    pdf.table_header(["Concept", "Use When", "Syntax"], cw)
    for i, (concept, use, syntax) in enumerate(JS):
        pdf.table_row([concept, use, syntax], cw, i)

    pdf.ln(3)
    pdf.pro_tip(
        "Master .map(), .filter(), and .find() first - these three cover 80% of all array work "
        "you will do in React. Learn them until you can write them without thinking."
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 3 - REACT
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("React Hooks",
                     "The 6 hooks you need. Real patterns, not just definitions.")
    pdf.add_page()
    pdf._section_label = "REACT HOOKS"
    pdf.h1("React Hooks Cheat Sheet")

    HOOKS = [
        ("useState",    "Store and update local state",
         "const [count, setCount] = useState(0)"),
        ("useEffect",   "Run code on mount, update, or unmount",
         "useEffect(() => { fetchData() }, [id])"),
        ("useContext",  "Read shared data without prop drilling",
         "const user = useContext(UserContext)"),
        ("useRef",      "Access DOM element or persist a value",
         "const inputRef = useRef(null)"),
        ("useMemo",     "Cache expensive calculation result",
         "const total = useMemo(() => calc(items), [items])"),
        ("useCallback", "Cache a function reference",
         "const fn = useCallback(() => doThing(id), [id])"),
    ]

    cw2 = [28, 52, pdf.epw - 80]
    pdf.table_header(["Hook", "Use Case", "Basic Pattern"], cw2)
    for i, row in enumerate(HOOKS):
        pdf.table_row(list(row), cw2, i)

    pdf.h2("useState - Full Pattern")
    pdf.code_block([
        "const [count, setCount] = useState(0);",
        "",
        "setCount(5);                          // set directly",
        "setCount(prev => prev + 1);           // update from previous - use for counters",
        "setUser(prev => ({ ...prev, name: 'Dean' }));  // object - always spread first",
        "setItems(prev => [...prev, newItem]); // array - always spread first",
    ])

    pdf.h2("useEffect - Full Pattern")
    pdf.code_block([
        "useEffect(() => {",
        "  // runs after render when deps change",
        "  const unsub = onSnapshot(collection(db, 'posts'), snap => {",
        "    setPosts(snap.docs.map(d => ({ id: d.id, ...d.data() })));",
        "  });",
        "  return () => unsub();  // cleanup - prevents memory leaks",
        "}, []);  // [] = run once on mount only",
    ])

    pdf.pro_tip(
        "Dependency array rules: [] = run once on mount. [value] = re-run when value changes. "
        "No array at all = run after every render (almost never what you want)."
    )

    pdf.h2("useRef - Access a DOM Element")
    pdf.code_block([
        "const inputRef = useRef(null);",
        "",
        "// attach to element",
        "<input ref={inputRef} />",
        "",
        "// use in event handler",
        "const handleClick = () => inputRef.current.focus();",
    ])

    pdf.warning(
        "Rule of Hooks: only call hooks at the top level of a component. "
        "Never inside loops, conditions, or nested functions. React depends on hooks "
        "being called in the same order every render."
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 4 - FIREBASE
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("Firebase Firestore",
                     "No schema. No migrations. No server. Just data.")
    pdf.add_page()
    pdf._section_label = "FIREBASE FIRESTORE"
    pdf.h1("Firebase Firestore CRUD Cheat Sheet")

    FIREBASE = [
        ("addDoc",      "Create - auto ID",    "addDoc(collection(db,'posts'), { title, uid })"),
        ("setDoc",      "Create - custom ID",  "setDoc(doc(db,'users',uid), { name, email })"),
        ("getDoc",      "Read one document",   "const snap = await getDoc(doc(db,'users',uid))"),
        ("getDocs",     "Read collection",     "const snap = await getDocs(collection(db,'posts'))"),
        ("onSnapshot",  "Real-time listener",  "onSnapshot(collection(db,'posts'), snap => {})"),
        ("updateDoc",   "Update fields only",  "updateDoc(doc(db,'users',uid), { name: 'Dean' })"),
        ("deleteDoc",   "Delete a document",   "deleteDoc(doc(db,'users',uid))"),
        ("query",       "Filter results",      "query(coll, where('uid','==',uid), orderBy('createdAt'))"),
        ("arrayUnion",  "Add to array field",  "updateDoc(ref, { tags: arrayUnion('react') })"),
        ("increment",   "Atomic counter",      "updateDoc(ref, { views: increment(1) })"),
    ]

    cw3 = [26, 32, pdf.epw - 58]
    pdf.table_header(["Method", "Operation", "Example"], cw3)
    for i, row in enumerate(FIREBASE):
        pdf.table_row(list(row), cw3, i)

    pdf.h2("The Standard Write Pattern")
    pdf.code_block([
        "import { addDoc, collection, serverTimestamp } from 'firebase/firestore';",
        "",
        "const handleSubmit = async () => {",
        "  await addDoc(collection(db, 'posts'), {",
        "    title,",
        "    body,",
        "    uid:       auth.currentUser.uid,  // always store the user's uid",
        "    createdAt: serverTimestamp()       // server-side - always use this",
        "  });",
        "};",
    ])

    pdf.h2("Real-Time Listener Pattern")
    pdf.code_block([
        "useEffect(() => {",
        "  const q = query(",
        "    collection(db, 'posts'),",
        "    where('uid', '==', auth.currentUser.uid),",
        "    orderBy('createdAt', 'desc')",
        "  );",
        "  const unsub = onSnapshot(q, snap => {",
        "    setPosts(snap.docs.map(d => ({ id: d.id, ...d.data() })));",
        "  });",
        "  return () => unsub();",
        "}, []);",
    ])

    pdf.pro_tip(
        "Always store the user's uid on every document you create. "
        "Then use Firestore Security Rules to enforce that users can only "
        "read and write documents where uid == request.auth.uid."
    )
    pdf.warning(
        "Never trust AI-generated Firestore security rules without testing edge cases. "
        "Always test: unauthenticated access, wrong user access, and missing field access."
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 5 - GIT
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("Git Essentials",
                     "10 commands cold. The full undo toolkit. Never lose work again.")
    pdf.add_page()
    pdf._section_label = "GIT ESSENTIALS"
    pdf.h1("Git Essentials Cheat Sheet")

    GIT = [
        ("git init",             "Start a new local repository in the current folder"),
        ("git add .",            "Stage all changed files ready to commit"),
        ("git commit -m 'msg'",  "Save a snapshot - describe what changed and why"),
        ("git push origin main", "Upload commits to GitHub"),
        ("git pull origin main", "Download and merge latest changes from GitHub"),
        ("git branch name",      "Create a new branch"),
        ("git checkout name",    "Switch to an existing branch"),
        ("git merge name",       "Merge branch 'name' into your current branch"),
        ("git status",           "See staged, changed, and untracked files"),
        ("git log --oneline",    "View commit history, one line per commit"),
    ]

    cw4 = [55, pdf.epw - 55]
    pdf.table_header(["Command", "What It Does"], cw4)
    for i, row in enumerate(GIT):
        pdf.table_row(list(row), cw4, i)

    pdf.h2("The Undo Toolkit")

    UNDO = [
        ("git restore .",         "Discard all unstaged changes (permanent)"),
        ("git reset HEAD~1",      "Undo last commit - keep changes staged"),
        ("git reset --hard HEAD~1","Undo last commit AND discard all changes"),
        ("git revert <hash>",     "New commit that safely undoes a past commit"),
        ("git stash",             "Shelve all changes to switch branches cleanly"),
        ("git stash pop",         "Restore most recently stashed changes"),
        ("git checkout <hash>",   "View repo at a past commit (read-only)"),
        ("git diff",              "See all unstaged changes line by line"),
    ]

    pdf.table_header(["Command", "What It Undoes / Does"], cw4)
    for i, row in enumerate(UNDO):
        pdf.table_row(list(row), cw4, i)

    pdf.pro_tip(
        "Commit small and often. A commit is a save point - you cannot lose work you have committed. "
        "Good commit message format: verb + what changed. "
        "Example: 'Add login form validation' not 'Update stuff'."
    )
    pdf.warning(
        "git reset --hard is permanent. It destroys uncommitted work with no recovery. "
        "If unsure, use git stash instead - it is always reversible."
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 6 - AI CO-PILOT
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("The AI Co-Pilot Strategy",
                     "Use AI to think better. Not to avoid thinking.")
    pdf.add_page()
    pdf._section_label = "AI CO-PILOT STRATEGY"
    pdf.h1("The AI Co-Pilot Strategy")

    pdf.body(
        "AI coding tools are the most powerful resource a self-taught developer has ever had. "
        "They are also the fastest way to stay permanently junior if you use them wrong. "
        "These three prompt templates turn AI from an answer machine into a personal mentor."
    )

    pdf.h2("The Golden Rule")
    pdf.note(
        "Copy-pasting AI code you do not understand is not productivity - it is debt. "
        "Every line you paste without reading is a gap in your mental model that will surface "
        "at the worst possible moment: in an interview, in production, or when you need to "
        "build something similar on your own. Senior developers use AI to move faster. "
        "Junior developers use AI to avoid thinking. The difference is the habit, not the tool."
    )

    pdf.h2("Prompt Template 1 - The Explain Prompt")
    pdf.body("Use this when you read code you do not fully understand.")
    pdf.code_block([
        "I am a self-taught developer learning [React / Firebase / JS].",
        "Explain this code to me like a mentor, not a documentation page.",
        "Walk through it line by line. Tell me:",
        "  1. What each part does and WHY it is written that way.",
        "  2. Any pattern or concept I should learn properly.",
        "  3. What I would need to change if [X requirement changed].",
        "",
        "[paste your code here]",
    ])

    pdf.h2("Prompt Template 2 - The Debug Prompt")
    pdf.body("Use this when something breaks. Writing context often reveals the bug before AI responds.")
    pdf.code_block([
        "I am debugging a problem in my [React / Firebase / JS] app.",
        "Do NOT just fix it. Explain the logic error I made.",
        "",
        "Expected: [what you expected to happen]",
        "Actual:   [what actually happened / paste error message]",
        "",
        "Here is the relevant code (not the whole file):",
        "[paste only the broken section]",
        "",
        "Walk me through why it is broken and what the correct mental model is.",
    ])

    pdf.h2("Prompt Template 3 - The Refactor Prompt")
    pdf.body("Use this after your code works. Getting it working is 50% of the job.")
    pdf.code_block([
        "My code works but I want to write it like a professional.",
        "Show me a more senior way to write this using best practices.",
        "",
        "For each change you make:",
        "  1. Tell me what pattern or principle you are applying.",
        "  2. Explain WHY it is better, not just that it is better.",
        "  3. Flag anything I should learn more about.",
        "",
        "[paste your working code here]",
    ])

    pdf.h2("The Red Line - Never Do These With AI")

    for i, (rule, detail) in enumerate([
        ("Never copy-paste code you cannot explain line by line.",
         "If you cannot walk someone through it, you do not own it. "
         "Paste it, run it, then spend five minutes reading it until you can."),
        ("Never trust AI-generated auth or database logic without checking.",
         "AI confidently writes Firestore security rules and auth flows with critical vulnerabilities. "
         "Always read it. Always test unauthenticated access and edge cases."),
        ("Never use AI to avoid the error message.",
         "Read the error first. Google it. Form a hypothesis. Then use AI. "
         "The debugging instinct you build from that process is what separates developers "
         "who can work anywhere from those who cannot function without an assistant."),
    ]):
        pdf.warning(f"{rule} {detail}")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 7 - TOOLBELT
    # ════════════════════════════════════════════════════════════════════════
    pdf.section_page("The Developer Toolbelt",
                     "The free tools professional developers actually use.")
    pdf.add_page()
    pdf._section_label = "DEVELOPER TOOLBELT"
    pdf.h1("The Developer Toolbelt")

    TOOLS = [
        ("VS Code",     "Code editor",      "Free",
         "The industry standard. Install Prettier, ESLint, GitLens, and ES7+ snippets."),
        ("Git + GitHub","Version control",  "Free",
         "Every project, from day one. No exceptions. Commit early and often."),
        ("Vercel",      "Deployment",       "Free",
         "Connect your GitHub repo and your app deploys automatically on every push."),
        ("Netlify",     "Deployment",       "Free",
         "Alternative to Vercel. Drag-and-drop deploy for static sites."),
        ("Firebase",    "Backend-as-service","Free tier",
         "Auth + Firestore database. Enough for most apps with no server required."),
        ("Supabase",    "Backend-as-service","Free tier",
         "Open-source Firebase alternative with a full PostgreSQL database."),
        ("Figma",       "Design/wireframes", "Free",
         "Plan your UI before you build it. Figma Community has free templates for everything."),
        ("Postman",     "API testing",       "Free",
         "Test any API endpoint before wiring it into your app. Saves hours of debugging."),
        ("Chrome DevTools","Debugging",      "Built-in",
         "F12. Learn the Console, Network, and Elements tabs inside out."),
        ("ESLint",      "Code quality",     "Free",
         "Catches errors before you run the code. Install the VS Code extension."),
        ("Prettier",    "Code formatting",  "Free",
         "Auto-formats your code on save. Consistent style, zero mental overhead."),
        ("React DevTools","React debugging", "Free browser ext.",
         "Inspect component trees, state, and props in real time in the browser."),
    ]

    cw5 = [26, 24, 18, pdf.epw - 68]
    pdf.table_header(["Tool", "Category", "Cost", "Why You Need It"], cw5)
    for i, row in enumerate(TOOLS):
        pdf.table_row(list(row), cw5, i)

    pdf.ln(3)
    pdf.pro_tip(
        "VS Code extensions to install on day one: Prettier (auto-format on save), "
        "ESLint (catch errors before running), GitLens (see git blame inline), "
        "ES7+ React Snippets (type 'rafce' to generate a full React component)."
    )

    pdf.h2("The Recommended Stack for Your First Full-Stack App")
    pdf.code_block([
        "Frontend:   React (Vite)         -> npx create vite@latest my-app --template react",
        "Styling:    Tailwind CSS          -> npm install -D tailwindcss",
        "Backend:    Firebase (Firestore)  -> npm install firebase",
        "Auth:       Firebase Auth         -> included in firebase package",
        "Deploy:     Vercel                -> vercel.com -> import GitHub repo -> done",
        "",
        "Total cost: FREE",
    ])

    pdf.output(output)
    print(f"  Field Manual saved: {output}")


if __name__ == "__main__":
    build_manual("FullStack_Field_Manual.pdf")
