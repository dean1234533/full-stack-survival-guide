"""
Generates: Tutorial_Hell_Escape_Guide.pdf
Amazon Kindle 'Lite' eBook - lead magnet for the Full-Stack Starter Kit
Run: python3 generate_ebook.py
"""

from fpdf import FPDF, XPos, YPos

# ── Palette ─────────────────────────────────────────────────────────────────
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

NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}

GUMROAD = "deanburt.gumroad.com/l/wkiilt"

# ── Base class ───────────────────────────────────────────────────────────────
class Ebook(FPDF):
    chapter_num = 0

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, "Tutorial Hell Ends Here  |  Build-First Developer Guide", align="L")
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"Page {self.page_no() - 1}", align="R",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*BLUE_MID)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        pass

    def rgb(self, t):   self.set_text_color(*t)
    def fill(self, t):  self.set_fill_color(*t)
    def draw(self, t):  self.set_draw_color(*t)

    def chapter_title(self, title):
        self.chapter_num += 1
        self.ln(2)
        # chapter label
        self.set_font("Helvetica", "B", 9)
        self.rgb(BLUE)
        self.cell(0, 6, f"CHAPTER {self.chapter_num}", **NL)
        # title bar
        self.fill(NAVY)
        bar_y = self.get_y()
        self.rect(self.l_margin, bar_y, self.epw, 14, "F")
        self.set_font("Helvetica", "B", 15)
        self.rgb(WHITE)
        self.set_y(bar_y + 1)
        self.cell(0, 12, title, **NL)
        # blue underline
        self.fill(BLUE)
        self.rect(self.l_margin, self.get_y(), self.epw, 2, "F")
        self.ln(6)

    def section(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.rgb(BLUE_DARK)
        self.cell(0, 7, title, **NL)
        self.fill(BLUE_MID)
        self.rect(self.l_margin, self.get_y(), self.epw, 0.5, "F")
        self.ln(4)

    def body(self, text):
        self.set_font("Helvetica", "", 10.5)
        self.rgb(BODY)
        for i, para in enumerate(text.split("\n\n")):
            self.multi_cell(self.epw, 6, para.strip())
            if i < len(text.split("\n\n")) - 1:
                self.ln(3)
        self.ln(3)

    def quote(self, text):
        self.ln(2)
        self.fill(BLUE_PALE)
        self.draw(BLUE_MID)
        self.set_line_width(0.4)
        qy = self.get_y()
        # measure height
        self.set_font("Helvetica", "BI", 11)
        lines = self.multi_cell(self.epw - 12, 6.5, text, dry_run=True, output="LINES")
        h = len(lines) * 6.5 + 10
        self.rect(self.l_margin, qy, self.epw, h, "DF")
        self.fill(BLUE)
        self.rect(self.l_margin, qy, 3, h, "F")
        self.set_xy(self.l_margin + 8, qy + 5)
        self.set_font("Helvetica", "BI", 11)
        self.rgb(NAVY)
        self.multi_cell(self.epw - 12, 6.5, text)
        self.set_y(qy + h + 3)

    def cta_box(self, text):
        """Yellow CTA box at end of each chapter."""
        self.ln(4)
        self.fill(CTA_BG)
        self.draw(CTA_BOR)
        self.set_line_width(0.8)
        cta_y = self.get_y()
        self.set_font("Helvetica", "", 9.5)
        lines = self.multi_cell(self.epw - 16, 5.8, text, dry_run=True, output="LINES")
        h = len(lines) * 5.8 + 20
        self.rect(self.l_margin, cta_y, self.epw, h, "DF")
        # icon label
        self.set_xy(self.l_margin + 6, cta_y + 5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*CTA_BOR)
        self.cell(0, 6, "WANT THE FULL TOOLKIT?", **NL)
        self.set_x(self.l_margin + 6)
        self.set_font("Helvetica", "", 9.5)
        self.rgb(BODY)
        self.multi_cell(self.epw - 12, 5.8, text)
        self.ln(2)
        self.set_x(self.l_margin + 6)
        self.set_font("Helvetica", "B", 9.5)
        self.rgb(BLUE)
        self.cell(0, 6, f"Get it now: {GUMROAD}", **NL)
        self.set_y(cta_y + h + 4)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10.5)
        self.rgb(BODY)
        self.set_x(self.l_margin + 4)
        self.fill(BLUE)
        bx, by = self.get_x(), self.get_y() + 2.5
        self.rect(bx, by, 2, 2, "F")
        self.set_x(self.l_margin + 9)
        self.multi_cell(self.epw - 9, 6, text)
        self.ln(1)


# ── Build ────────────────────────────────────────────────────────────────────
def build_ebook(output="Tutorial_Hell_Escape_Guide.pdf"):
    pdf = Ebook()
    pdf.set_margins(18, 22, 18)
    pdf.set_auto_page_break(True, margin=20)
    pdf.set_title("Tutorial Hell Ends Here")
    pdf.set_author("Dean Burt")

    # ════════════════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.fill(NAVY)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.fill(BLUE)
    pdf.rect(0, 0, 6, 297, "F")
    pdf.rect(0, 291, 210, 6, "F")

    pdf.set_y(50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 8, "A BUILD-FIRST GUIDE FOR SELF-TAUGHT DEVELOPERS", align="C", **NL)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 40)
    pdf.rgb(WHITE)
    pdf.cell(0, 18, "Tutorial Hell", align="C", **NL)

    pdf.fill(BLUE)
    bw = 100
    bx = (210 - bw) / 2
    pdf.rect(bx, pdf.get_y(), bw, 18, "F")
    pdf.set_font("Helvetica", "B", 40)
    pdf.rgb(WHITE)
    pdf.cell(0, 18, "Ends Here.", align="C", **NL)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 13)
    pdf.rgb(BLUE_PALE)
    pdf.multi_cell(0, 7,
        "The self-taught developer's roadmap from watching videos\n"
        "to shipping real apps - in 6 months.",
        align="C")

    pdf.set_y(160)
    pdf.fill(BLUE_DARK)
    pdf.rect(30, 160, 150, 60, "F")
    pdf.set_y(168)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7, "What you will learn:", align="C", **NL)
    pdf.ln(1)
    for item in [
        "Why tutorial hell keeps you stuck - and how to break free",
        "The 6-month build-first roadmap from HTML to deployed app",
        "How to debug like a professional every single time",
        "The AI Co-Pilot Strategy - learn faster, not lazier",
        "Your first step toward shipping something real",
    ]:
        pdf.set_font("Helvetica", "", 9)
        pdf.rgb(WHITE)
        pdf.cell(0, 6.5, f"  +  {item}", align="C", **NL)

    pdf.set_y(240)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(BLUE_PALE)
    pdf.cell(0, 7, "Dean Burt  |  buildwithcode.dev  |  2026", align="C", **NL)
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 9)
    pdf.rgb(MUTED)
    pdf.cell(0, 6,
        "A free preview. The Full-Stack Starter Kit is at " + GUMROAD,
        align="C", **NL)

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 1 - THE TRAP
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("The Tutorial Hell Trap")

    pdf.body(
        "You have probably been here. You find a highly-rated course online, buy it with genuine "
        "excitement, and spend the first evening following along line by line. The code works. The "
        "instructor explains it clearly. You feel, for the first time in a while, like you are "
        "actually making progress.\n\n"
        "Then the course ends. Or you get bored. Or a new, shinier course comes out and the cycle "
        "starts again. You have completed parts of four courses. You have watched maybe two hundred "
        "hours of video. And yet the moment someone asks you to build something from scratch - "
        "anything, even a simple to-do list - you freeze. Nothing comes out.\n\n"
        "That experience is so common it has a name: tutorial hell. And the frustrating truth is "
        "that it is not your fault. The tutorial industry is not designed to make you independent. "
        "It is designed to make you feel productive while keeping you dependent on the next video."
    )

    pdf.quote(
        '"Watching someone else write code is no different from watching someone else do push-ups '
        'and expecting to get stronger. You are consuming, not building."'
    )

    pdf.section("Why the Model is Broken")
    pdf.body(
        "Traditional coding education works like this: watch a concept explained, follow along, "
        "complete a quiz, move to the next module. It feels logical. It mirrors the school system "
        "we all grew up in. But software development does not work like school.\n\n"
        "In school, the goal is to absorb and recall information. In software, the goal is to "
        "solve problems you have never seen before using tools you only partially understand. "
        "No amount of watching prepares you for that moment. Only doing does.\n\n"
        "The developers who get hired - and the ones who build real products - did not finish "
        "more courses than you. They built more things. They broke more things. They spent hours "
        "staring at error messages and coming out the other side with a mental model no tutorial "
        "can give you. That gap between consuming and creating is where real skill is built."
    )

    pdf.section("The One Shift That Changes Everything")
    pdf.body(
        "The fix is not a better course. It is a different philosophy: learn only what you need "
        "to build the thing you are already trying to build.\n\n"
        "Instead of completing a syllabus and then maybe starting a project, you start the project "
        "on day one. When you hit something you do not know, you look it up - in the docs, in a "
        "video, through AI. You learn it in the context of a real problem. It sticks immediately "
        "because it is solving something that actually matters to you right now.\n\n"
        "This is the Build-First approach. It is not a course. It is a mindset. And the rest of "
        "this guide will show you exactly how to apply it over six months."
    )

    pdf.cta_box(
        "This guide gives you the mindset and the roadmap. The Full-Stack Starter Kit gives you "
        "everything else - React, Firebase, and Git cheat sheets, a master debugging flowchart, "
        "AI prompt templates, and the complete developer toolbelt. All in one printable field manual."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 2 - THE ROADMAP
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("The 6-Month Build-First Roadmap")

    pdf.body(
        "One of the most paralysing things about learning to code is not knowing what order to "
        "learn things in. There is an overwhelming amount of content out there and no clear signal "
        "about what actually matters versus what you can safely ignore for now.\n\n"
        "This roadmap gives you that clarity. It is not the only path. But it is a direct, "
        "well-tested path - from no experience at all to a deployed, shareable, full-stack "
        "application - built around the principle that every month should produce something real."
    )

    pdf.section("Month 1 - HTML and CSS: Build Your Foundation")
    pdf.body(
        "Start with the visible web. HTML gives structure to content. CSS makes it look like "
        "something. These are not boring prerequisites - they are the foundation of every single "
        "thing you will build for the rest of your career.\n\n"
        "Focus on semantic HTML, the box model, Flexbox for layout, and basic responsive design. "
        "Skip animations, Grid, and SASS for now. Your milestone: a personal site with at least "
        "three pages. Real content, real layout, nothing copy-pasted."
    )

    pdf.section("Month 2 and 3 - JavaScript: The Engine of Everything")
    pdf.body(
        "JavaScript is where most self-taught developers either break through or give up. It is "
        "worth spending two full months here.\n\n"
        "Month 2 covers the fundamentals: variables, functions, loops, DOM manipulation, and "
        "fetching data from an API. Month 3 goes deeper: ES6+ features like arrow functions, "
        "destructuring, async/await, and the array methods you will use every single day.\n\n"
        "The milestone for Month 3 is a small, self-contained JavaScript app built entirely from "
        "scratch with no tutorial to follow. This is the first real test of the Build-First "
        "approach - and the first time many developers discover they are further along than they thought."
    )

    pdf.section("Month 4 - React: Building Interfaces That Respond")
    pdf.body(
        "React is the most in-demand front-end skill in the job market right now. More "
        "importantly, once you understand it, building interactive interfaces becomes fast, "
        "logical, and almost enjoyable.\n\n"
        "Focus on components, props, state with useState, and side effects with useEffect. "
        "Skip Redux and Next.js for now. Your milestone: rebuild your Month 3 JavaScript app in "
        "React. You will immediately understand why React exists."
    )

    pdf.section("Month 5 - Firebase: Your Backend Without the Backend")
    pdf.body(
        "Firebase lets you add user authentication and a real-time database to your React app "
        "without writing a single line of server code. For a self-taught developer building "
        "their first full-stack app, this is transformative.\n\n"
        "Cover Auth (email and Google sign-in), Firestore for reading and writing data, and "
        "real-time listeners. Milestone: your React app now has login and persistent saved data. "
        "Users can sign up, log in, and see their own content."
    )

    pdf.section("Month 6 - Ship It: The Only Metric That Matters")
    pdf.body(
        "Month 6 is not about learning something new. It is about finishing and shipping what "
        "you have built.\n\n"
        "Deploy on Vercel or Netlify - both are free and take about five minutes. Clean up your "
        "GitHub: write a proper README, remove commented-out code, make it look like something "
        "you are proud of. Write a short post about what you built and what you learned. Share it.\n\n"
        "A deployed project you can show is worth ten unfinished courses. Full stop."
    )

    pdf.quote(
        '"The developers who get hired are not the ones who watched the most videos. '
        'They are the ones who built the most things."'
    )

    pdf.cta_box(
        "The Full-Stack Starter Kit includes the complete month-by-month breakdown with weekly "
        "goals, milestone projects, and the exact tools used at each stage. Stop guessing what "
        "to learn next."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 3 - DEBUGGING
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("Debug Like a Professional")

    pdf.body(
        "Here is something nobody tells you when you are starting out: professional developers "
        "spend a significant portion of their working day debugging. Not because they are bad "
        "at their job - but because building complex software in a world of changing requirements "
        "means things break. Constantly.\n\n"
        "The difference between a junior and a senior developer is rarely how often they "
        "encounter bugs. It is how quickly and methodically they resolve them. Juniors panic "
        "and guess. Seniors follow a process."
    )

    pdf.section("The 4-Step Debugging Process")

    pdf.body("Follow these steps in order. Do not skip ahead. Do not start guessing.")

    for num, (title, detail) in enumerate([
        ("Check the Console",
         "Open DevTools (F12), go to the Console tab, and read every red error message word by word. "
         "Google the exact error text. Most bugs are diagnosed here in under two minutes. If there "
         "is no error message, move to Step 2."),
        ("Check Your Logic and Data",
         "Add console.log() statements around the problem area. Is the data undefined, null, or "
         "the wrong type? Trace it back to where it comes from and fix it at the source. "
         "If the data looks right but the behaviour is wrong, walk through the code line by line "
         "and say it out loud - this technique, called rubber duck debugging, works embarrassingly well."),
        ("Check the UI and CSS",
         "Right-click the element and choose Inspect. Is it rendering but hidden, off-screen, or "
         "zero height? Look for strikethrough rules in DevTools - those are styles being overridden. "
         "A quick trick: add border: 1px solid red to isolate elements and understand your layout."),
        ("Use AI - But Do It Right",
         "Most developers use AI wrong. They paste their entire file and ask 'why doesn't this work?' "
         "That produces generic answers. Instead, give it context: what you are using, what you "
         "expected, what actually happened, and only the relevant broken code. You will get a "
         "mentor-level response instead of a guess."),
    ], 1):
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.rgb(BLUE_DARK)
        pdf.cell(0, 7, f"Step {num}: {title}", **NL)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.rgb(BODY)
        pdf.multi_cell(pdf.epw, 6, detail)
        pdf.ln(3)

    pdf.quote(
        '"If you cannot describe the bug in one sentence, you have not looked closely enough yet."'
    )

    pdf.section("The Golden Rule of Debugging")
    pdf.body(
        "Never guess. Every time you change something without understanding why, you are "
        "introducing a new variable into an already confusing system. One change at a time. "
        "Test after each change. Read the error messages. Follow the process.\n\n"
        "The developers who debug fastest are not smarter than you. They are more systematic "
        "than you. Systematic thinking is a skill, and it is entirely learnable."
    )

    pdf.cta_box(
        "The Full-Stack Starter Kit includes the Master Debugging Flowchart as a full-page "
        "printable - designed to pin above your desk or keep open on a second monitor. "
        "Never panic at a bug again."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 4 - AI CO-PILOT
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("The AI Co-Pilot Strategy")

    pdf.body(
        "We are living through a genuinely unusual moment in the history of software development. "
        "AI coding assistants - tools like Claude, ChatGPT, and GitHub Copilot - can now write "
        "functional code, explain complex concepts, review your work, and help you debug in "
        "real time. For a self-taught developer, this is an extraordinary resource.\n\n"
        "It is also the fastest way to stay permanently junior if you use it wrong."
    )

    pdf.section("The Trap Inside the Tool")
    pdf.body(
        "Here is what most beginners do with AI: they describe what they want to build, "
        "paste the generated code into their project, run it, and move on. It works. They "
        "feel productive. They ship things quickly.\n\n"
        "Then six months later they are in a job interview and someone asks them to write a "
        "useEffect hook from memory. They cannot. They have used it dozens of times but never "
        "once understood it - because the AI always wrote it for them.\n\n"
        "Copy-pasting AI code you do not understand is not productivity. It is debt. "
        "Every line you paste without reading is a gap in your mental model that will surface "
        "at the worst possible moment."
    )

    pdf.section("Use AI as a Mentor, Not an Answer Machine")
    pdf.body(
        "The developers who get the most out of AI are not the ones who use it to avoid thinking. "
        "They are the ones who use it to think better. There is a specific way to prompt AI "
        "that turns it from a code vending machine into a personal senior developer who explains "
        "their reasoning, challenges your assumptions, and helps you build a real mental model.\n\n"
        "Three prompt types cover almost every situation you will encounter:"
    )

    for label, desc in [
        ("The Explain Prompt",
         "When you read code you do not fully understand, ask AI to walk through it line by line "
         "like a mentor - not just what it does, but why it is written that way. Do not move on "
         "until you can explain it back in your own words."),
        ("The Debug Prompt",
         "When something breaks, describe what you expected, what actually happened, and paste "
         "only the relevant broken code. Then ask AI not just to fix it, but to explain the "
         "logic error you made. The act of writing this out often reveals the bug before AI even responds."),
        ("The Refactor Prompt",
         "Once your code works, ask AI to show you a more professional way to write it - and "
         "to explain every change it makes and why. This is how you learn best practices "
         "in the context of code you already understand."),
    ]:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.rgb(BLUE_DARK)
        pdf.cell(0, 7, label, **NL)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.rgb(BODY)
        pdf.multi_cell(pdf.epw, 6, desc)
        pdf.ln(3)

    pdf.quote(
        '"The goal is not to avoid AI. The goal is to use it the way a senior developer does: '
        'as a fast path to understanding, not a shortcut around it."'
    )

    pdf.cta_box(
        "The Full-Stack Starter Kit includes all three AI prompt templates in full - "
        "copy-paste ready, formatted for the exact scenarios you will face every week as "
        "a developer. Plus the Red Line list: three things you must never do with AI."
    )

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 5 - YOUR NEXT STEP
    # ════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("Your Next Step")

    pdf.body(
        "You have been preparing long enough.\n\n"
        "The developers who build careers and ship real products are not the ones who found the "
        "perfect course or waited until they felt ready. They are the ones who opened their "
        "editor and started building before they were ready - and learned everything they needed "
        "along the way.\n\n"
        "You have the roadmap now. You know why tutorial hell exists and how to escape it. You "
        "have a debugging process that will get you unstuck every time. You understand how to "
        "use AI as a mentor rather than a crutch.\n\n"
        "There is only one thing left to do: start."
    )

    pdf.section("The Three Starter Projects")
    pdf.body("Pick one - right now, today - and commit to it:")

    for proj in [
        "A personal site with three pages: Home, About, and a Projects section. Deploy it tonight.",
        "A to-do app in React with Firebase login. Users can sign up, add tasks, and see their "
        "own data. This is a complete full-stack app in a weekend.",
        "Take something you use every day and rebuild a stripped-down version of it. "
        "A simple clone of your notes app, your favourite weather site, anything. "
        "Constraints make you more creative, not less.",
    ]:
        pdf.bullet(proj)

    pdf.ln(4)
    pdf.body(
        "You do not need permission. You do not need to feel ready. You need to open your "
        "editor and write the first line.\n\n"
        "The first line is always the hardest. After that, curiosity takes over."
    )

    pdf.quote(
        '"Don\'t memorize, build. Don\'t finish the course, finish the project."'
    )

    # Final CTA
    pdf.ln(4)
    pdf.fill(NAVY)
    pdf.draw(BLUE)
    pdf.set_line_width(1)
    cta_y = pdf.get_y()
    pdf.rect(pdf.l_margin, cta_y, pdf.epw, 58, "DF")
    pdf.fill(BLUE)
    pdf.rect(pdf.l_margin, cta_y, pdf.epw, 10, "F")
    pdf.set_xy(pdf.l_margin, cta_y + 1)
    pdf.set_font("Helvetica", "B", 10)
    pdf.rgb(WHITE)
    pdf.cell(pdf.epw, 8, "READY TO GO FURTHER?", align="C", **NL)

    pdf.set_xy(pdf.l_margin + 6, cta_y + 13)
    pdf.set_font("Helvetica", "B", 11)
    pdf.rgb(WHITE)
    pdf.cell(pdf.epw - 12, 7, "Get the Full-Stack Developer Starter Kit", align="C", **NL)

    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.rgb(BLUE_PALE)
    pdf.multi_cell(pdf.epw - 12, 5.5,
        "Everything in this guide - and everything you need to actually build: "
        "React Hooks, Firebase CRUD, Git Essentials, AI Prompt Templates, "
        "the Master Debugging Flowchart, and the Developer Toolbelt. "
        "All in one dense, printable field manual.", align="C")

    pdf.ln(3)
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.rgb(BLUE_PALE)
    pdf.cell(pdf.epw - 12, 7, GUMROAD, align="C", **NL)
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.rgb(MUTED)
    pdf.cell(pdf.epw - 12, 6,
        "PS. 30-day money-back guarantee. If you aren't building faster, you get a full refund.",
        align="C", **NL)

    pdf.output(output)
    print(f"  eBook saved: {output}")


if __name__ == "__main__":
    build_ebook("Tutorial_Hell_Escape_Guide.pdf")
