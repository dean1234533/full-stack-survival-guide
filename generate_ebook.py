"""
Generates: Tutorial_Hell_Escape_Guide.pdf
Amazon KDP - The 6-Month Build-First Developer Blueprint
Run: python3 generate_ebook.py
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
CTA_BG    = (254, 243, 199)
CTA_BOR   = (217, 119,   6)
RED       = (220,  38,  38)
RED_PAL   = (254, 226, 226)

NL      = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}
GUMROAD = "deanburt.gumroad.com/l/wkiilt"


class Ebook(FPDF):
    chapter_num = 0

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8,
            "The 6-Month Build-First Developer Blueprint  |  Dean Burt",
            align="L")
        self.cell(0, 8, f"Page {self.page_no() - 1}", align="R",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*BLUE_MID)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(),
                  210 - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self): pass

    def rgb(self, t):  self.set_text_color(*t)
    def fill(self, t): self.set_fill_color(*t)
    def draw(self, t): self.set_draw_color(*t)

    def chapter_title(self, num_label, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.rgb(BLUE)
        self.cell(0, 6, num_label, **NL)
        self.fill(NAVY)
        by = self.get_y()
        self.rect(self.l_margin, by, self.epw, 13, "F")
        self.fill(BLUE)
        self.rect(self.l_margin, by + 11, self.epw, 2, "F")
        self.set_font("Helvetica", "B", 14)
        self.rgb(WHITE)
        self.set_y(by)
        self.cell(0, 13, "  " + title, **NL)
        self.ln(5)

    def h2(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.rgb(BLUE_DARK)
        self.cell(0, 7, text, **NL)
        self.fill(BLUE_MID)
        self.rect(self.l_margin, self.get_y(), self.epw, 0.5, "F")
        self.ln(4)

    def body(self, text):
        self.set_font("Helvetica", "", 10.5)
        self.rgb(BODY)
        for i, para in enumerate(text.split("\n\n")):
            self.multi_cell(self.epw, 6.2, para.strip())
            if i < len(text.split("\n\n")) - 1:
                self.ln(3)
        self.ln(3)

    def bold_body(self, label, text):
        self.set_font("Helvetica", "B", 10.5)
        self.rgb(NAVY)
        self.cell(0, 6.5, label, **NL)
        self.set_font("Helvetica", "", 10.5)
        self.rgb(BODY)
        self.multi_cell(self.epw, 6.2, text)
        self.ln(2)

    def bullet(self, bold_part, rest=""):
        self.fill(BLUE)
        bx = self.l_margin + 3
        by = self.get_y() + 3
        self.rect(bx, by, 2.5, 2.5, "F")
        self.set_x(self.l_margin + 9)
        if bold_part and rest:
            self.set_font("Helvetica", "B", 10.5)
            self.rgb(NAVY)
            bw = self.get_string_width(bold_part + " ")
            self.cell(bw, 6.5, bold_part + " ")
            self.set_font("Helvetica", "", 10.5)
            self.rgb(BODY)
            self.multi_cell(self.epw - 9 - bw, 6.5, rest)
        else:
            self.set_font("Helvetica", "", 10.5)
            self.rgb(BODY)
            self.multi_cell(self.epw - 9, 6.5, bold_part)
        self.ln(1)

    def quote(self, text):
        self.ln(3)
        self.fill(BLUE_PALE)
        self.draw(BLUE_MID)
        self.set_line_width(0.4)
        qy = self.get_y()
        self.set_font("Helvetica", "BI", 11)
        lines = self.multi_cell(self.epw - 14, 6.5, text,
                                dry_run=True, output="LINES")
        h = len(lines) * 6.5 + 12
        self.rect(self.l_margin, qy, self.epw, h, "DF")
        self.fill(BLUE)
        self.rect(self.l_margin, qy, 4, h, "F")
        self.set_xy(self.l_margin + 9, qy + 6)
        self.set_font("Helvetica", "BI", 11)
        self.rgb(NAVY)
        self.multi_cell(self.epw - 14, 6.5, text)
        self.set_y(qy + h + 4)

    def pain_box(self, items):
        self.ln(3)
        self.fill(RED_PAL)
        self.draw(RED)
        self.set_line_width(0.6)
        bx = self.l_margin
        by = self.get_y()
        self.set_font("Helvetica", "", 9.5)
        total_h = sum(
            len(self.multi_cell(self.epw - 16, 5.8, item,
                                dry_run=True, output="LINES")) * 5.8 + 4
            for item in items
        ) + 14
        self.rect(bx, by, self.epw, total_h, "DF")
        self.fill(RED)
        self.rect(bx, by, 4, total_h, "F")
        self.set_xy(bx + 8, by + 5)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*RED)
        self.cell(0, 5, "DOES THIS SOUND FAMILIAR?", **NL)
        self.ln(1)
        for item in items:
            self.set_x(bx + 8)
            self.set_font("Helvetica", "", 9.5)
            self.rgb(BODY)
            lines = self.multi_cell(self.epw - 14, 5.8,
                                    "x  " + item, **NL)
            self.ln(1)
        self.set_y(by + total_h + 4)

    def cta_box(self, headline, body_text):
        self.ln(5)
        self.fill(CTA_BG)
        self.draw(CTA_BOR)
        self.set_line_width(1)
        cy = self.get_y()
        self.set_font("Helvetica", "", 9.5)
        lines = self.multi_cell(self.epw - 14, 5.8, body_text,
                                dry_run=True, output="LINES")
        h = len(lines) * 5.8 + 26
        self.rect(self.l_margin, cy, self.epw, h, "DF")
        self.set_xy(self.l_margin + 7, cy + 5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*CTA_BOR)
        self.cell(0, 6, headline, **NL)
        self.set_x(self.l_margin + 7)
        self.set_font("Helvetica", "", 9.5)
        self.rgb(BODY)
        self.multi_cell(self.epw - 14, 5.8, body_text)
        self.ln(2)
        self.set_x(self.l_margin + 7)
        self.set_font("Helvetica", "B", 10)
        self.rgb(BLUE)
        self.cell(0, 6, "Get it now -> " + GUMROAD, **NL)
        self.set_y(cy + h + 5)


def build_ebook(output="Tutorial_Hell_Escape_Guide.pdf"):
    pdf = Ebook()
    pdf.set_margins(18, 22, 18)
    pdf.set_auto_page_break(True, margin=22)
    pdf.set_title("The 6-Month Build-First Developer Blueprint")
    pdf.set_author("Dean Burt")

    # ════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.fill(NAVY)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.fill(BLUE)
    pdf.rect(0, 0, 8, 297, "F")
    pdf.rect(202, 0, 8, 297, "F")

    pdf.set_y(30)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7,
        "FOR SELF-TAUGHT DEVELOPERS WHO ARE DONE WATCHING AND READY TO BUILD",
        align="C", **NL)
    pdf.ln(12)

    pdf.set_font("Helvetica", "B", 16)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 9, "THE", align="C", **NL)

    pdf.set_font("Helvetica", "B", 44)
    pdf.rgb(WHITE)
    pdf.cell(0, 19, "6-MONTH", align="C", **NL)

    pdf.set_font("Helvetica", "B", 36)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 16, "BUILD-FIRST", align="C", **NL)

    fw = 160
    fx = (210 - fw) / 2
    pdf.fill(BLUE)
    pdf.rect(fx, pdf.get_y(), fw, 20, "F")
    pdf.set_font("Helvetica", "B", 36)
    pdf.rgb(WHITE)
    pdf.cell(0, 20, "DEVELOPER BLUEPRINT", align="C", **NL)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.rgb(BLUE_PALE)
    pdf.multi_cell(0, 7,
        "How to Escape Tutorial Hell and Start\n"
        "Shipping Real-World Apps.", align="C")

    pdf.set_y(180)
    pdf.fill(BLUE_DARK)
    pdf.rect(25, 180, 160, 72, "F")
    pdf.set_y(187)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 6, "WHAT YOU WILL MASTER:", align="C", **NL)
    pdf.ln(2)
    chapters = [
        "The Build-First Methodology - why it works",
        "The 6-Month Roadmap from zero to deployed app",
        "The Developer's Toolbelt - free tools the pros use",
        "The AI Co-Pilot Strategy - learn 10x faster",
        "The Ship-It Philosophy - stop over-engineering, start launching",
    ]
    for ch in chapters:
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(WHITE)
        pdf.cell(0, 7, f"  >>  {ch}", align="C", **NL)

    pdf.set_y(265)
    pdf.set_font("Helvetica", "B", 9)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 6, "DEAN BURT  |  buildwithcode.dev  |  2026",
             align="C", **NL)

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 1 - THE PAIN
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("CHAPTER 1", "The Tutorial Hell Trap")

    pdf.pain_box([
        "You have watched 200+ hours of coding tutorials and still cannot build anything from scratch.",
        "You finish a course, feel confident, open a blank editor - and freeze completely.",
        "You have started four courses in the last year and finished zero real projects.",
        "You secretly wonder if you are just not built for this.",
    ])

    pdf.ln(3)
    pdf.body(
        "You are not broken. You are not behind. You are a victim of an industry that profits "
        "from your confusion.\n\n"
        "The tutorial industry is not designed to make you independent. It is designed to make "
        "you feel productive while keeping you dependent on the next video, the next course, "
        "the next instructor. Completion bars move. Certificates get issued. And yet the moment "
        "you close the video and open a blank editor - nothing comes out.\n\n"
        "That experience is so common it has a name: tutorial hell. And the brutal truth is "
        "that no amount of watching will get you out of it. Only building will."
    )

    pdf.quote(
        '"Watching someone else write code is no different from watching someone else do push-ups '
        'and expecting to get stronger. You are consuming, not building."'
    )

    pdf.h2("Why the Model is Broken")
    pdf.body(
        "Traditional coding education assumes that understanding comes before doing. "
        "Watch the concept. Follow along. Complete the quiz. Move to the next module. "
        "It feels logical because it mirrors the school system we all grew up in.\n\n"
        "But software development does not work like school. In school, the goal is to absorb "
        "and recall information. In software, the goal is to solve problems you have never "
        "seen before using tools you only partially understand. No amount of watching "
        "prepares you for that moment. Only doing does.\n\n"
        "The developers who get hired - and the ones who build real products - did not finish "
        "more courses than you. They built more things. They broke more things. They spent "
        "hours staring at error messages and came out the other side with a mental model no "
        "tutorial can give you."
    )

    pdf.h2("The Imposter Syndrome Lie")
    pdf.body(
        "Here is something the tutorial industry will never tell you: imposter syndrome in "
        "self-taught developers is almost always caused by the gap between what you have "
        "consumed and what you have built. You know the vocabulary. You can recognise the "
        "patterns. But you have never applied them under pressure on your own.\n\n"
        "That gap does not close by watching more videos. It closes by building. Every project "
        "you finish - no matter how messy, no matter how basic - shrinks the gap. Every bug "
        "you fix alone builds the confidence that a hundred tutorials cannot."
    )

    pdf.cta_box(
        "READY FOR THE FULL SYSTEM?",
        "This guide gives you the mindset. The Full-Stack Developer Starter Kit gives you "
        "the complete toolkit: cheat sheets, AI prompt templates, debugging flowchart, "
        "and the developer toolbelt - everything in one dense, printable field manual."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 2 - THE AHA MOMENT
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("CHAPTER 2", "The Build-First Methodology")

    pdf.body(
        "This book is not a tutorial. It is not a course. It is not a curriculum.\n\n"
        "It is a professional survival guide for the modern self-taught developer - written "
        "by someone who spent a year in tutorial hell, broke out of it, and rebuilt everything "
        "using the one principle that actually works: build first, learn what you need, ship it.\n\n"
        "The Build-First methodology is the missing link that nobody in the tutorial industry "
        "wants you to find, because the moment you find it, you stop needing them."
    )

    pdf.quote(
        '"Don\'t memorize, build. Don\'t finish the course, finish the project. '
        'The project teaches you everything the course was pretending to."'
    )

    pdf.h2("How Build-First Works")
    pdf.body(
        "Instead of completing a syllabus and then maybe starting a project, you start the "
        "project on day one. You pick something real - something you actually want to exist "
        "in the world - and you start building it immediately, even before you know how.\n\n"
        "When you hit something you do not know, you look it up. In the docs. In a quick video. "
        "Through AI. But you learn it in the context of a real problem you are already trying "
        "to solve. It sticks immediately. It has to - because you need it right now.\n\n"
        "This is not a new idea. It is how every senior developer you have ever admired actually "
        "learned. They did not wait until they felt ready. They started before they were ready "
        "and became ready in the process."
    )

    pdf.h2("What This Book Is - And Is Not")

    pdf.bold_body("What this IS:",
        "A structured, opinionated, field-tested roadmap. A reference you keep open on your "
        "second monitor while you build. A system that tells you exactly what to learn, in "
        "what order, using what tools, and why - with no detours, no filler, no theory for "
        "theory's sake.")

    pdf.bold_body("What this is NOT:",
        "Another beginner course. Another hand-holding tutorial. Another list of concepts "
        "to memorize before you start. This guide assumes you are ambitious, you are tired "
        "of 'beginner' content, and you are ready to be treated like a professional.")

    pdf.h2("The One Shift That Changes Everything")
    pdf.body(
        "Stop asking: 'What should I learn next?'\n\n"
        "Start asking: 'What do I need to learn to build this?'\n\n"
        "That one shift - from passive consumer to active builder - is the difference between "
        "a developer who is perpetually almost ready and a developer who ships real products, "
        "gets hired, and builds whatever they want."
    )

    pdf.cta_box(
        "THE FULL-STACK DEVELOPER STARTER KIT",
        "The premium companion to this guide. Every cheat sheet, every prompt template, "
        "every tool recommendation - laid out in a dense, scannable field manual built "
        "to sit next to your keyboard while you work."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 3 - WHAT YOU WILL MASTER
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("CHAPTER 3", "What You Will Master")

    pdf.body(
        "Five pillars. No fluff. Each one is a specific, actionable system - not a concept "
        "to understand, but a tool to use. By the end of this guide, you will have all five."
    )

    pdf.h2("Pillar 1 - The 6-Month Roadmap")
    pdf.body(
        "A clear, month-by-month path from zero experience to a portfolio-ready, deployed, "
        "shareable full-stack application. Every month has a specific focus, a weekly goal, "
        "and a milestone project to build.\n\n"
        "Month 1: HTML and CSS - build a real personal site.\n"
        "Month 2: JavaScript fundamentals - add live interactivity.\n"
        "Month 3: JavaScript deep dive - build your first app from scratch.\n"
        "Month 4: React - rebuild it properly.\n"
        "Month 5: Firebase - add login and real data.\n"
        "Month 6: Ship it - deploy, clean up, share, get hired."
    )
    for item in [
        ("No filler.", "Every month produces something real."),
        ("No detours.", "Skip what you do not need yet."),
        ("No excuses.", "Six months from today, you have a deployed app or you do not."),
    ]:
        pdf.bullet(item[0], item[1])
    pdf.ln(2)

    pdf.h2("Pillar 2 - The Developer's Toolbelt")
    pdf.body(
        "The exact free tools that professional developers use every day - curated, explained, "
        "and prioritised so you spend zero time researching and all your time building."
    )
    for tool, desc in [
        ("VS Code + Extensions:", "The editor. Prettier, ESLint, GitLens, ES7+ snippets."),
        ("Git + GitHub:", "Version control from day one. No exceptions."),
        ("Vercel / Netlify:", "Deploy in five minutes. Free. Automatic on every push."),
        ("Firebase / Supabase:", "Your backend without a backend."),
        ("Figma:", "Plan your UI before you build it. Free."),
        ("Chrome DevTools:", "The debugger that is always open. Learn it inside out."),
    ]:
        pdf.bullet(tool, desc)
    pdf.ln(2)

    pdf.h2("Pillar 3 - The AI Co-Pilot Strategy")
    pdf.body(
        "AI coding tools are the most powerful resource a self-taught developer has ever had. "
        "They are also the fastest way to stay permanently junior if you use them wrong.\n\n"
        "This pillar gives you three specific prompt templates - Explain, Debug, and Refactor - "
        "that turn AI from an answer machine into a personal senior developer who teaches you "
        "while it helps you. You will learn faster and build better code at the same time."
    )
    for item in [
        ("The Explain Prompt:", "AI walks through your code line by line like a mentor."),
        ("The Debug Prompt:", "AI explains the logic error you made - not just the fix."),
        ("The Refactor Prompt:", "AI shows you the professional way and tells you why."),
    ]:
        pdf.bullet(item[0], item[1])
    pdf.ln(2)

    pdf.h2("Pillar 4 - The Master Debugging Flowchart")
    pdf.body(
        "A 4-step decision tree that resolves the vast majority of bugs you will ever encounter. "
        "Professionals follow a process. This is the process.\n\n"
        "Check the console. Check your data. Check the UI. Use AI correctly. "
        "In that order. Every time. Without skipping."
    )

    pdf.h2("Pillar 5 - The Ship-It Philosophy")
    pdf.body(
        "The most dangerous trap in software development is not tutorial hell. "
        "It is the project you have been 'almost finished' with for six months.\n\n"
        "Stop over-engineering. Stop waiting until it is perfect. Stop adding one more feature "
        "before you deploy. Ship the imperfect version. Fix it in public. A deployed project "
        "that is 70% good beats a perfect project that no one can see.\n\n"
        "This chapter gives you the exact deploy process, the README template that gets noticed, "
        "and the mindset shift that turns your project into proof of skill."
    )

    pdf.cta_box(
        "ALL FIVE PILLARS. ONE FIELD MANUAL.",
        "The Full-Stack Developer Starter Kit expands every pillar with full cheat sheets, "
        "code examples, prompt templates, and a complete tool-by-tool breakdown. "
        "Dense. Printable. Built to be used, not collected."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 4 - THE FREEDOM
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("CHAPTER 4", "The Real Goal - Freedom")

    pdf.body(
        "Every self-taught developer I have ever spoken to says the same thing when you ask "
        "them why they want to learn to code. Not for the salary. Not for the job title.\n\n"
        "For the freedom.\n\n"
        "The freedom to build whatever idea they have. The freedom to fix the broken thing "
        "at their company instead of waiting three sprints for an engineer to get to it. "
        "The freedom to launch a product at midnight on a Tuesday because the idea came to "
        "them and they had the skills to act on it immediately.\n\n"
        "That freedom is real. And it is entirely within reach. But it does not come from "
        "finishing another course. It comes from shipping something."
    )

    pdf.quote(
        '"The moment you deploy your first real project, something shifts. '
        'You stop feeling like someone who is learning to code '
        'and start feeling like someone who builds things."'
    )

    pdf.h2("What Freedom Actually Looks Like")
    for item, desc in [
        ("Technical freedom.", "You can build the thing in your head without needing an instructor to guide every step."),
        ("Professional freedom.", "You have a deployed portfolio that proves your skill without a degree or bootcamp certificate."),
        ("Creative freedom.", "You can launch your own product, fix your own problems, and build your own business if you want to."),
        ("Financial freedom.", "You have a skill that is in demand globally, that pays well, and that you can do from anywhere."),
    ]:
        pdf.bullet(item, desc)

    pdf.ln(4)
    pdf.body(
        "None of that requires a computer science degree. None of it requires finishing every "
        "module of every course. It requires building real things, shipping them, and repeating.\n\n"
        "Six months. One project. Shipped and deployed.\n\n"
        "That is all it takes to cross the line from person who is learning to code to person "
        "who builds things. The line is not as far away as the tutorial industry wants you to believe."
    )

    pdf.h2("The AI Co-Pilot Strategy - Full Picture")
    pdf.body(
        "We are living through an extraordinary moment in software development. The AI tools "
        "available to developers today would have seemed impossible five years ago. A self-taught "
        "developer with the right system can now learn and build at a pace that matches - and "
        "sometimes exceeds - developers with formal training.\n\n"
        "But only if you use AI correctly.\n\n"
        "Most developers use AI as a shortcut. They describe what they want, paste the output, "
        "and move on. This works in the short term. In the long term it creates developers who "
        "cannot function without an AI assistant - which is not freedom, it is a new dependency.\n\n"
        "Use the three prompt templates in this guide every single time you interact with AI. "
        "Ask it to explain. Ask it to teach. Ask it to show you the professional way and tell "
        "you why. Within weeks you will notice that you need to ask less, because the AI has "
        "been building your mental model the entire time."
    )

    pdf.cta_box(
        "YOUR FREEDOM STARTS WITH THE RIGHT TOOLS.",
        "The Full-Stack Developer Starter Kit gives you every technical reference you need "
        "in one place - so you spend less time searching and more time building. "
        "React. Firebase. Git. AI prompts. The complete developer toolbelt."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 5 - THE CALL TO ACTION
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("CHAPTER 5", "Take Control - Starting Today")

    pdf.body(
        "You have read this far. That means you are serious.\n\n"
        "Most people who buy books about learning to code put them on a shelf and come back "
        "to them someday. Do not be most people. The only difference between a developer who "
        "ships real products and a developer who is still in tutorial hell five years from now "
        "is what they do in the next twenty-four hours.\n\n"
        "This is your twenty-four hours."
    )

    pdf.h2("Your Action Plan - Right Now")
    for i, (action, detail) in enumerate([
        ("Choose your project.",
         "Not a to-do list. Not a weather app unless you genuinely want to build one. "
         "Something you actually want to exist. A tool for a problem you have. "
         "A portfolio piece you would be proud to show. Pick it in the next five minutes."),
        ("Open your editor.",
         "Create a new folder. Name it after your project. Open VS Code. "
         "Create an index.html file. Write one line of HTML. "
         "You are no longer someone who is thinking about building. You are someone who is building."),
        ("Follow the roadmap.",
         "Month by month. No skipping ahead. No detours. "
         "If you get stuck, follow the debugging flowchart. "
         "If you need to understand something, use the AI prompt templates. "
         "If you need the syntax, open the cheat sheets."),
        ("Ship it.",
         "On month six, deploy it. Write the README. Share it publicly. "
         "This is not optional. Sharing your work is what transforms a project into proof. "
         "Proof is what gets you hired, gets you clients, or gets your product its first users."),
    ], 1):
        pdf.bold_body(f"Step {i}: {action}", detail)

    pdf.quote(
        '"You do not need to feel ready. You do not need to finish the course. '
        'You need to open your editor and write the first line. '
        'Everything else follows from that."'
    )

    pdf.h2("A Note on Failure")
    pdf.body(
        "You will get stuck. Your code will break in ways that make no sense. "
        "You will spend an hour on a bug that turns out to be a missing semicolon. "
        "You will deploy something and immediately spot three things you want to fix.\n\n"
        "This is not failure. This is development.\n\n"
        "Every senior developer you admire has spent hours staring at a broken screen "
        "wondering what is wrong. The only difference between them and where you are now "
        "is that they kept going. They debugged one more time. They pushed one more commit.\n\n"
        "Keep going."
    )

    # Final buy box
    pdf.ln(4)
    pdf.fill(NAVY)
    pdf.draw(BLUE)
    pdf.set_line_width(1.2)
    fy = pdf.get_y()
    pdf.rect(pdf.l_margin, fy, pdf.epw, 64, "DF")
    pdf.fill(BLUE)
    pdf.rect(pdf.l_margin, fy, pdf.epw, 11, "F")
    pdf.set_xy(pdf.l_margin, fy + 1)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(WHITE)
    pdf.cell(pdf.epw, 9,
        "GET THE FULL-STACK DEVELOPER STARTER KIT", align="C", **NL)

    pdf.set_xy(pdf.l_margin + 6, fy + 14)
    pdf.set_font("Helvetica", "B", 12)
    pdf.rgb(WHITE)
    pdf.multi_cell(pdf.epw - 12, 7,
        "Stop collecting tutorials. Take control of your coding career. "
        "Get the complete toolkit today.", align="C")

    pdf.ln(2)
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.rgb(BLUE_PALE)
    pdf.multi_cell(pdf.epw - 12, 5.5,
        "React Hooks + Firebase CRUD + Git Essentials + AI Prompt Templates + "
        "Master Debugging Flowchart + Developer Toolbelt. "
        "All in one dense, printable field manual.", align="C")

    pdf.ln(3)
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.rgb(BLUE_PALE)
    pdf.cell(pdf.epw - 12, 7, GUMROAD, align="C", **NL)

    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.rgb(MUTED)
    pdf.cell(pdf.epw - 12, 6,
        "30-day money-back guarantee. If you are not building faster, you get a full refund.",
        align="C", **NL)

    pdf.output(output)
    print(f"  eBook saved: {output}")


if __name__ == "__main__":
    build_ebook("Tutorial_Hell_Escape_Guide.pdf")
