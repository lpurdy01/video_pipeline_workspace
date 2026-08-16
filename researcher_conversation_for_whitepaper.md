ChatGPT Plus





verification-compiler-levi-purdy-research-preview-draft-5-20-2026-v0-alpha.pdf
PDF
I want collaborators or interest in this project, is there anyone in my university that I should send this to? 

Thought for 31s
Assuming you mean UW–Madison: yes. I’d send this to a small, targeted set first, and I’d frame it as a program verification / software engineering systems project, not primarily as “LLMs for certification.”

Your draft’s strongest hook is: a deterministic artifact graph + query compiler for requirements/code/test evidence, where LLMs are only a development pre-screen and humans remain the certification endpoint 

. That maps pretty well onto UW–Madison CS.

Best first contacts
1. Tej Chajed — strongest first send
He works in systems verification, including proving real systems meet specifications, and UW’s CS announcement describes his focus as systems verification. This is probably the cleanest fit for the “verification compiler” architecture. 

2. Adithya Murali — also very strong
His research focus is program verification and synthesis, and his own page says he wants to democratize software verification so non-experts can verify code. That is extremely close to your project’s “bounded verification query packages” idea. 

3. Aws Albarghouthi — strong if you emphasize AI + verification
His CV says his group works on program synthesis/verification and safe/secure AI agents. He may be a good fit for the model-unit / AI-agent angle, especially if you want someone who can push back hard on whether the LLM role is technically defensible. 

4. madPL group generally
UW–Madison’s madPL group explicitly lists interests in program verification, program synthesis, language design, and software security. If you do not know the best individual, sending to one faculty member and asking whether this is appropriate for madPL is reasonable. 

5. Thomas Reps — maybe as a senior “is there prior art I’m missing?” contact
He has deep relevance to graph reachability, program analysis, slicing, dependence graphs, and incremental computation. I would not lead with “collaborate?” to him; I’d ask for a pointer or 20-minute sanity check if you can get one. 

Secondary contacts, depending on angle
Yea-Seul Kim could be relevant for the reviewer-interface / uncertainty / VRM visualization / human-in-the-loop side. Her research sits at HCI, visualization, and data science, and UW CS described her work as making data and uncertainty more comprehensible to people. 

Xiangru Xu is less directly matched to the compiler architecture, but relevant if you pivot Stage 2 toward autonomous systems / drones / safety-critical controls. His lab works on safety of autonomous systems and drone/scaled-car testbeds. 

My recommendation
Send first to Tej Chajed and Adithya Murali, probably separately. They are the two cleanest fits. I’d attach a 1–2 page teaser, not the whole 34-page draft yet, because the current draft itself says “not for distribution,” and it still has self-reported citation/coverage issues on page 2. That is fine internally, but for first contact you want the idea to land before the rough edges do.

A good subject line would be:

Potential research fit: continuous verification compiler for requirements/code/test evidence

The message should ask for one of three things: “Is this in-scope for your group?”, “Is there a student who might be interested?”, or “Who at UW–Madison would you point me toward?”


Caude identified 


UW-Madison faculty most likely to be interested (verified current as of early 2025):

Name	Area	Page
Aws Albarghouthi	Program synthesis, formal verification, ML correctness	cs.wisc.edu
Adithya Murali	ML-assisted verification, program synthesis (joined Jan 2025)	muraliadithya.github.io
Loris D'Antoni	Formal verification/synthesis, program analysis	UW-Madison CS
Somesh Jha	Formal methods, adversarial ML, software security	pages.cs.wisc.edu/~jha
Ben Liblit	Program analysis, automated bug detection, software reliability	pages.cs.wisc.edu/~liblit
Closest match to your paper: Albarghouthi (verification + ML correctness) and Murali (ML-assisted verification) are the strongest fit. The madPL group coordinates most of this work — reaching out through that group is a reasonable entry point.

On affiliation: listing "Student, University of Wisconsin–Madison" is standard and correct even for independent work — it identifies your institutional context without implying the university sponsored the research.

Please rank the top 5 best contacts and figure out how I could get a flat mailer to them. I want their attention, so will email them, but I don't expect that to work. A snail mail is much more impactful.

Thought for 44s
Yeah — but I’d adjust Claude’s list before you spend postage. Loris D’Antoni and Ben Liblit should probably not get UW–Madison mailers: Loris appears to now be at UCSD, and Ben Liblit’s own page says he is no longer affiliated with UW–Madison. 
 

Your project is best framed as: CI-integrated evidence packaging + requirements/code/test trace verification, with LLMs as non-certifying prescreen reviewers and deterministic graph traversal as the qualifiable core. That is the strongest, least hand-wavy version of the paper. 


My ranked top 5
1. Aws Albarghouthi
Best overall fit. He works on program synthesis and verification, and his current page explicitly mentions interest in AI agent construction and correctness. That is almost directly aligned with your “model units inside a structured verification architecture” idea. 

Mailer address:

Prof. Aws Albarghouthi
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall 7647
1205 University Avenue
Madison, WI 53706

His office/email are listed on the UW CS faculty page as Morgridge Hall 7647 and aws@cs.wisc.edu. 

2. Adithya Murali
Best “new faculty who might actually engage” fit. His page says he works on formal methods, program verification, program synthesis, and “democratizing software verification” for non-experts. Your bounded verification-query idea fits that motivation extremely well. 

Mailer address:

Prof. Adithya Murali
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall 6532
1205 University Avenue
Madison, WI 53706

UW CS lists him as Assistant Professor, adithyamurali@cs.wisc.edu, Morgridge Hall 6532. 

3. Somesh Jha
Best for the security / adversarial ML / formal-methods credibility angle. He is senior, very high-impact, and works at the intersection of security, formal methods, adversarial ML, and privacy. He may be less likely to personally collaborate, but a positive pointer from him would carry weight. 

Mailer address:

Prof. Somesh Jha
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall
1205 University Avenue
Madison, WI 53706

I’d email him rather than rely on mail only, since I did not find a clean current office-room listing in the quick search.

4. Thomas Reps
Best “prior art / architecture sanity check” contact. Reps is probably not the best “collaborator” target because he is emeritus/retired, but he is one of the strongest people anywhere for program analysis, slicing, dataflow analysis, model checking, symbolic abstraction, and graph-based program analysis. That maps to the artifact-graph/compiler part of your idea. 

Mailer address:

Prof. Thomas Reps
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall
1205 University Avenue
Madison, WI 53706

For him, I’d send a shorter note asking: “Is there prior work I should study before taking this further?” not “do you want to collaborate?”

5. Tej Chajed — with a caveat
Technically maybe one of the closest fits, administratively weird. His page says he works on “using AI to enable formal verification at scale,” which is very close to your direction. But it also says he is now a Research Scientist at Theorem and “was” an assistant professor at UW–Madison, while some UW course pages still list UW teaching/office info. So I would email him, but I would not make him one of the physical UW mailers unless you confirm he is still receiving UW faculty mail. 

Potential UW mailer if you decide to try:

Tej Chajed
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall 7572
1205 University Avenue
Madison, WI 53706

But again: this one is a bit risky. Email is safer.

How I’d send the physical mailers
Use a 9×12 flat envelope so nothing is folded. Send three UW mailers first: Aws, Adithya, Somesh. Maybe Reps as a fourth. I would skip physical mail to Tej until you verify where he wants mail.

The department/CDIS public mailing address is:

School of Computer, Data & Information Sciences
1205 University Avenue
Madison, WI 53706 

For each envelope, put the professor’s name and room number above that address. That should route through campus mail / reception. The CS contacts page also lists CS reception in the 3rd-floor administrative suite at Morgridge Hall, so the building has a normal admin routing point. 

What to put in the mailer
Do not send the whole 34-page draft first. Send something that looks intentional:

One-page cover letter.

Two-page research teaser / abstract.

One clean architecture figure, ideally the artifact graph / dual-mode reviewer endpoint figure.

QR code to full PDF, GitHub repo, or private Google Drive folder.

Optional: one sentence saying “full draft is rough; citation audit and Stage 2 prototype are in progress.”

The physical packet should feel like: “This is a serious student/researcher asking for a targeted pointer,” not “unsolicited manuscript dump.”

My top move: email all five, then mail only Aws + Adithya + Somesh + Reps. Use the email to say, “I also mailed a one-page summary because this is easier to evaluate visually than as a cold email.”


I'm totally ok sending mailers to people outside of uw madison, we just will want to try and find their best address. If they aren't a uw madison collaborator then they might be a good industry connection.

Do we need to reconsider any of the contacts considering this? 

Also I would like a personalized message (make sure it is correct, and doesn't sound like AI ) make it like I in a rushed form typed it up as to why I was contacting them, let me know if any of their content I need to be faimliar with so I can mention it. Have sometihng about how I found them / why I chose them. 

I want the hook, and why they are being sent this to be personalized

Thought for 27s
Yes — allowing non-UW contacts does change the ranking. I would move Loris D’Antoni back into the top 5, and I would keep Tej Chajed high even though he is now industry-adjacent via Theorem. I would not prioritize Ben Liblit for a physical mailer: he is relevant, but his own page says he is no longer affiliated with UW, and I do not see a good public mailing path for him. 

Your project’s core hook is not “LLM certifies code.” It is: a deterministic verification-query compiler that packages requirements/code/test evidence into bounded review units, where LLM review is only a development pre-screen and human review remains the certification endpoint. That distinction is exactly what makes it defensible. 


Revised top 5
Rank	Contact	Why they get a mailer	Best physical mailing path
1	Aws Albarghouthi	Program verification/synthesis + AI/correctness angle. Best UW anchor.	UW–Madison CS, Morgridge Hall 7647
2	Adithya Murali	New UW faculty, program verification/synthesis, likely more reachable.	UW–Madison CS, Morgridge Hall 6532
3	Loris D’Antoni	Very strong fit for synthesis/verification + “software people can trust”; now UCSD, still madPL lineage.	UCSD CSE, Office 3214
4	Tej Chajed	Systems verification + “AI to enable formal verification at scale”; excellent industry bridge.	His page still lists Morgridge 7572; I’d email first before mailing.
5	Somesh Jha	Formal methods/security/adversarial ML; good for the “LLM is an untrusted component inside a constrained system” framing.	UW–Madison CS general Morgridge address unless you confirm room.
For Loris, his UCSD page gives a clean mailing address: Computer Science and Engineering, UCSD, Office 3214, 3235 Voigt Dr, La Jolla, CA 92093. 

For Tej, his personal page says he is a Research Scientist at Theorem and works on using AI to enable formal verification at scale, but it still lists his UW email and Morgridge Hall 7572. I would not invent a Theorem physical address; use email first, or mail to the UW room if you’re comfortable with the ambiguity. 

For Aws and Adithya, UW CS lists their Morgridge offices, and Morgridge Hall’s public address is 1205 University Avenue, Madison, WI 53706. 
 

Mailer addresses
Aws Albarghouthi
Prof. Aws Albarghouthi
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall 7647
1205 University Avenue
Madison, WI 53706

Adithya Murali
Prof. Adithya Murali
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall 6532
1205 University Avenue
Madison, WI 53706

Loris D’Antoni
Prof. Loris D’Antoni
Computer Science and Engineering
University of California San Diego
Office 3214
3235 Voigt Dr
La Jolla, CA 92093

Tej Chajed
Tej Chajed
Morgridge Hall 7572
1205 University Avenue
Madison, WI 53706

Somesh Jha
Prof. Somesh Jha
Department of Computer Sciences
University of Wisconsin–Madison
Morgridge Hall
1205 University Avenue
Madison, WI 53706

For Somesh, I would try to confirm the room before printing, but the general Morgridge route should still route through the department.

What you should skim before mentioning them
For Aws, skim his homepage/research overview and be familiar with the phrase “automated verification and synthesis.” Do not pretend you know his whole publication history.
For Adithya, skim his homepage and UW announcement; the key phrasing is program verification/synthesis and making verification more usable/non-expert-accessible. 

For Loris, skim his homepage. The safest personal hook is his stated mission: “make it easier for people to build software they can trust,” plus his connection to madPL. 

For Tej, skim his homepage and maybe his systems verification course page. Your connection is “AI to enable formal verification at scale” plus systems verification. 

For Somesh, skim his homepage and, optionally, the recent “Agent Security is a Systems Problem” paper. That paper’s framing — model as untrusted component, system-level invariants — is very close to the way your architecture treats LLMs. 

Here are draft notes you can use as cover letters or email bodies. I intentionally kept them a bit imperfect and human-sounding — not polished grant-proposal voice.

AWS ALBARGHOUTHI

Professor Albarghouthi,

I’m a UW–Madison engineering grad student working outside the normal research-lab path, and I’m trying to find the right person to sanity-check a project I’ve been developing.

I found you through the UW PL / formal methods side, and your work on automated verification and synthesis looked like one of the closest matches I could find. The thing I’m sending is a rough research preview for what I’m calling a “Verification Compiler.” The basic idea is to treat requirements, source code, tests, static analysis outputs, and review records as an artifact graph, then deterministically compile that graph into bounded verification query packages.

The LLM part is not meant to certify anything. That is actually the part I am trying to be careful about. The LLM is only a development-cycle pre-screen. The more important part, in my mind, is the deterministic graph traversal / evidence packaging layer, because that is the part that could eventually be reviewable, testable, and maybe qualifiable. Human reviewers would still be the certification endpoint.

I’m contacting you because I think this sits near program verification, synthesis, and correctness tooling, but I am not yet sure if I’m framing it in the right research language. If this is in-scope for your group, I’d be very interested in a short conversation. If not, even a pointer to the right person or paper trail would be useful.

I included a short summary rather than just sending the whole draft cold. The draft is still rough and I’m actively cleaning up the citations / claims, but I think the architecture might be worth discussing before I build the Stage 2 prototype.

Thank you,
Levi Purdy

ADITHYA MURALI

Professor Murali,

I’m a UW–Madison engineering grad student, and I’m looking for feedback or possible collaborators on a verification project I’ve been working on independently.

I found your page after looking through UW people working on program verification and synthesis. Your interest in making verification more usable / accessible is why I’m sending this to you specifically. My project is not trying to replace formal verification with an LLM. It’s more of a structure for turning messy engineering evidence into small, reviewable verification tasks.

The short version is: build an artifact graph linking requirements, code units, tests, analysis results, physical test evidence, and review records. Then deterministically compile that graph into bounded verification query packages. During development, LLMs can pre-screen those packages and produce structured pass/fail/uncertain results. For any serious certification use, humans still review the same evidence package and their result is the only one that counts.

What I’m trying to figure out is whether this is a useful bridge between real embedded/safety-critical software practice and the program verification world. I come from embedded/UAV/power systems work, so I’m seeing this from the engineering-process side more than from the PL theory side.

I’d be grateful for a short meeting, or even just a pointer if there is an obvious line of prior work I should be reading before I take the prototype further.

Thank you,
Levi Purdy

LORIS D’ANTONI

Professor D’Antoni,

I’m a UW–Madison engineering grad student working on an independent research idea, and I’m trying to get it in front of a few people who are close enough to tell me whether I’m onto something or just rediscovering known work.

I found your work through the UW/madPL connection and then through your UCSD page. The line that stood out to me was the goal of making it easier for people to build software they can trust. That is basically the problem I’m trying to attack, but from the engineering evidence side rather than from only the code side.

The project is a rough architecture I’m calling a Verification Compiler. It treats requirements, code, tests, analysis outputs, datasheets, and review records as an artifact graph. A deterministic compiler pass walks that graph and produces bounded verification query packages. Those packages can be reviewed by an LLM during development, or by a human reviewer for a formal pass. The LLM output is explicitly not certification evidence — it is a pre-screen signal.

The part I think may be interesting is the separation between the deterministic evidence/query compiler and the probabilistic reviewer endpoint. I’m trying to make the useful AI part fit inside a structure that still looks auditable and defensible to safety-critical software people.

I’m sending this because your work seems close to the trust/synthesis/verification side, and because I suspect you would know quickly whether this framing is useful or naive. If you have time for a short conversation or can point me toward relevant prior work, I’d really appreciate it.

Thank you,
Levi Purdy

TEJ CHAJED

Tej,

I’m a UW–Madison engineering grad student, and I’m sending this because your page says you’re working on using AI to enable formal verification at scale. That is probably the closest one-sentence match I found to what I’m trying to do, even though my angle is more engineering-process / certification-evidence than theorem proving directly.

The project is a rough research preview for something I’m calling a Verification Compiler. The idea is to take the artifact graph that safety-critical software teams already sort of maintain — requirements, code units, tests, analysis results, physical test evidence, review records — and compile it into bounded verification query packages.

The LLM is not the certifier in this architecture. It is a development-cycle reviewer endpoint. The deterministic part is the graph traversal, query assembly, invariant checking, and evidence logging. A human can review the exact same generated package later, and for certification that human verdict is the only one that matters.

I’m contacting you because I think the real question is whether this kind of structured decomposition is a plausible way to make AI useful in verification without pretending the model itself is trustworthy. I’d be very interested in any feedback, especially if there is prior work from systems verification that I should read before building the Stage 2 prototype.

Thank you,
Levi Purdy

SOMESH JHA

Professor Jha,

I’m a UW–Madison engineering grad student working independently on a software verification architecture, and I’m trying to get it in front of a few people who can challenge the security / trust assumptions.

I found your work through the formal methods and security side, and especially because of the way your recent agent-security framing treats the model as an untrusted component and pushes guarantees into the surrounding system. That is very close to the design instinct in this project.

The project is called the Verification Compiler. It builds a graph of requirements, code, tests, analysis outputs, and evidence records, then deterministically compiles that graph into bounded verification query packages. LLMs can review those packages during development, but their output is explicitly not certification evidence. The system treats them as useful but fallible reviewers. The auditable part is the deterministic evidence packaging, graph coverage, invariant enforcement, and human review path.

I’m sending this to you because I think the biggest risk is not just “LLMs hallucinate,” but whether the surrounding architecture actually constrains the failure modes well enough to be useful. If you think this is the wrong framing, I would rather find that out early. If it is adjacent to anything your group cares about, I’d be very interested in a short conversation or a pointer.

Thank you,
Levi Purdy

My opinion: send the physical packet to Aws, Adithya, Loris, and Somesh first. Email Tej with the same packet and ask whether UW mail still reaches him before sending a flat mailer.


Can you extend the consideration to any of the cited sources in the paper. reading Rearson's book was a big foundation of me starting to think about how DO178 workflows could interact / be agumented by the agentic coding I was practicing. 

Also there are m-dashes — in the letters. That is a dead giveaway of AI and is generally unfationable. I want these to look like I didn't spend a bunch of time writing the personal things, just a message, not too well formatted or correct. What you wrote is techincally nice, but we can be a little more brief

Thought for 26s
Yes, I’d reconsider the list. Once non-UW people are allowed, I’d add Leanna Rierson and Corina Păsăreanu into the serious-contact pool.

Rierson is not just a citation. Her book is basically the practical DO-178C backbone for your paper, and it is credible to say that reading it pushed you toward the “DO-178 workflow plus agentic coding” idea. Her book is described as a practical guide to aviation software and DO-178C compliance, and her background includes FAA software and avionics certification work. 
 Your draft specifically leans on Rierson for independence, reviewer qualification, DO-330 framing, and DAL-scaled independence requirements. 


Revised priority list
Leanna Rierson
Best practitioner-source contact. Not necessarily a “collaborator,” but if she responds, the feedback would be gold. I would not send a physical mailer until you find a real current business address. The book affiliation I found is Digital Safety Consulting, Wichita, Kansas, but not a full mailing address. 

Aws Albarghouthi
Still the best UW academic match. Program verification, synthesis, and AI correctness. Send UW mailer.

Adithya Murali
Strong UW fit, likely more reachable as newer faculty, especially if framed around making verification usable.

Corina Păsăreanu
Very strong cited-source-adjacent fit. Her work includes model checking, symbolic execution, compositional verification, autonomy, and security. CMU lists her at CMU Silicon Valley, Building 23, Moffett Field, CA 94035. 

Loris D’Antoni or Tej Chajed
I’d pick Loris for academic synthesis/verification and Tej for the “AI for formal verification at scale” angle. Tej is maybe the more exciting fit, but his physical address is fuzzier.

I would bump Somesh Jha to honorable mention unless you want a security/trust critique specifically. He is high value, but less directly tied to your paper’s seed.

What to know before mentioning them
For Rierson, know that her book is the practical source that made the DO-178C workflow feel like a structured information-processing system. Mentioning that is authentic and specific.

For Corina Păsăreanu, skim her work on assume-guarantee/compositional verification. Your paper already cites assume-guarantee reasoning as a lineage for decomposing large verification problems into local checks. 


For Haolin Jin and Huaming Chen, authors of the overcorrection paper, I would not put them in the top mailer group, but they are worth emailing later. Their paper is directly relevant because it finds LLMs can misclassify correct code as non-compliant in requirement conformance judgment, which supports your “LLM as pre-screen only” stance. 

Shorter, less polished notes
I kept these intentionally less formal. No em dashes.

LEANNNA RIERSON

Dr. Rierson,

I’m a UW-Madison engineering grad student and I wanted to send you this because your DO-178C book was one of the main reasons I started thinking about this project.

I work around embedded and safety-critical-ish systems, and I’ve also been using agentic coding tools a lot. Reading your book made me start seeing the DO-178C workflow as a structured evidence and review problem, not just a paperwork problem. That is what led to this “Verification Compiler” idea.

The basic idea is to build a graph of requirements, code, tests, analysis outputs, and review evidence, then compile that into small review packages. LLMs can pre-screen during development, but they do not certify anything. The human review path is still the real endpoint.

I’m not assuming this is correct yet. I’m sending it because your book is the foundation I kept coming back to, and I’d be very interested if you think this framing is useful, naive, or already covered somewhere I should be reading.

Thank you,
Levi Purdy

CORINA PASAREANU

Dr. Păsăreanu,

I’m a UW-Madison engineering grad student working on an independent verification project, and I wanted to send this because your work on compositional verification seems close to the part I’m trying to reason through.

The project is a rough architecture I’m calling a Verification Compiler. It builds an artifact graph from requirements, code, tests, analysis results, and review evidence, then turns that graph into bounded review packages.

The LLM part is not meant to prove or certify anything. It is more like a development pre-screen. The thing I care about more is whether the graph decomposition and evidence package are structured enough that a human or tool can review each unit cleanly.

I found your work through assume-guarantee and compositional verification references. I’m trying to understand whether that analogy is actually fair, or if I’m stretching it too far.

If you have time for a short pointer or know a better prior-work trail, I’d really appreciate it.

Thank you,
Levi Purdy

AWS ALBARGHOUTHI

Professor Albarghouthi,

I’m a UW-Madison engineering grad student and I’m trying to find the right person to sanity check a verification project I’ve been developing.

I found you through UW program verification / synthesis work. This seemed close enough that I wanted to send a short preview instead of just guessing from the outside.

The idea is a “Verification Compiler.” It takes requirements, code, tests, analysis outputs, and review records as a graph, then compiles that into small verification review packages. LLMs can review those during development, but they are not the certifier. The deterministic graph/query compiler is the part I think matters.

I’m coming at this from embedded systems and DO-178C process thinking, not from PL theory, so I’m trying to figure out if this is a reasonable research framing or if I’m missing obvious prior work.

Thank you,
Levi Purdy

ADITHYA MURALI

Professor Murali,

I’m a UW-Madison engineering grad student and I wanted to send you a rough research preview because your work looked close to the “make verification more usable” side of what I’m trying to do.

The project is called a Verification Compiler. The short version is that it builds a graph of requirements, code, tests, analysis outputs, and evidence records, then compiles that into small review packages.

An LLM can pre-screen those during development, but it is not the certification endpoint. A human can review the same package later. I’m trying to keep the AI part useful but not trusted.

I’m coming from embedded/UAV/power systems work, so I may be using different language than the verification community would. If this is near your area, I’d be interested in a short conversation or even just a pointer to what I should read first.

Thank you,
Levi Purdy

LORIS D’ANTONI

Professor D’Antoni,

I’m a UW-Madison engineering grad student and I found your work through the UW/madPL connection. Your “software people can trust” framing seemed close enough to what I’m doing that I wanted to send this.

I’m working on a rough architecture called a Verification Compiler. It treats requirements, code, tests, analysis outputs, and review evidence as a graph, then compiles that graph into bounded review packages.

The LLM is only a development pre-screen. The human review path stays the real endpoint. The part I’m interested in is whether this makes verification evidence easier to package, review, and keep current in CI.

I’m not sure if this is framed correctly yet, but I’d really value a pointer if there is prior work I should know before I build the next prototype.

Thank you,
Levi Purdy

TEJ CHAJED

Tej,

I’m a UW-Madison engineering grad student and I found your page while looking for people working on AI and formal verification at scale.

I’m working on a rough project called a Verification Compiler. It builds a graph of requirements, code, tests, analysis results, and evidence, then compiles that into small review packages.

The LLM part is not trusted. It can pre-screen during development, but for any serious use the human review path is still the real endpoint. The deterministic graph traversal and evidence packaging is the part I’m trying to make rigorous.

This is coming from embedded systems and DO-178C workflow thinking more than theorem proving directly. If this is adjacent to your work, I’d be interested in any quick feedback or pointers.

Thank you,
Levi Purdy

For the mailers, I’d send physical packets to Aws, Adithya, Corina, and Loris first. For Rierson, I’d email first or use a professional contact route, because I would not trust “Digital Safety Consulting, Wichita, Kansas” as enough for a flat mailer without a confirmed address.


can you do some address research on the ones we don't have mailing addresses for yet?

Thought for 35s
Yes. I found a few more usable routes, but I’d be conservative about anything that looks like a personal/home address. For this kind of outreach, I’d only use public institutional, company, publisher, or conference-provided addresses.

Your paper leans heavily on DO-178C workflow, tool qualification, reviewer independence, and compositional decomposition, so the extra address work should focus on Rierson, Corina Păsăreanu, Dimitra Giannakopoulou, Tej Chajed, and Somesh Jha. The strongest direct source-contact is still Rierson because your draft cites her book for the independence / DO-330 framing and your actual project seed came from reading it. 


Best new address findings
1. Leanna Rierson
I did not find a trustworthy public street address for her or Digital Safety Consulting. The public sources consistently identify her as “Digital Safety Consulting, Wichita, Kansas, USA,” but they do not give a mail-ready address. Her book bio says she is an independent consultant in safety-critical software and avionics, and that she spent nine years at the FAA, including as chief scientific and technical advisor for aircraft computer software. 

Best physical route: publisher forwarding attempt

Leanna Rierson
c/o CRC Press / Taylor & Francis
Two Peninsula Executive Center
2385 Executive Center Drive
Suite 320
Boca Raton, FL 33431

Taylor & Francis lists that as the current CRC Press Boca Raton office. 

I’d mark this as medium-low confidence. It may not reach her, but it is legitimate and not creepy. I would write “Please forward to author if possible” on the envelope or cover note.

Better move: email/contact first if you can find a professional channel, then ask where to send a short printed packet.

2. Corina S. Păsăreanu
This one is solid.

Corina S. Păsăreanu
Carnegie Mellon University Silicon Valley
Building 23, MS 23-11
Moffett Field, CA 94035

CMU ECE lists her as a Senior Research Scientist, gives MS 23-11, and gives the CMU Silicon Valley Building 23 address. 

This is a good mailer candidate. Her work is probably the cleanest cited-source connection for the assume-guarantee / compositional verification side of your paper. Your draft explicitly uses that as a lineage for graph traversal and bounded query decomposition. 


3. Dimitra Giannakopoulou
I would not use an old NASA address unless you decide you are fine with lower odds. She appears to now be at Amazon / AWS. Amazon Science lists her as a Senior Principal Scientist, and LinkedIn search results show her in AWS’s Automated Reasoning Group. 

I did not find a clean public mail address for her at AWS. I would treat her as email / LinkedIn only unless you later find an official AWS Automated Reasoning mailing route.

Could use, but I would not prioritize:

Dimitra Giannakopoulou
c/o Amazon Web Services / Automated Reasoning Group
Seattle, WA

That is not mail-ready. I would not print that.

4. Tej Chajed
Best currently supported address remains:

Tej Chajed
Morgridge Hall 7572
1205 University Avenue
Madison, WI 53706

His personal page says he is now a Research Scientist at Theorem, but still lists chajed@wisc.edu and Morgridge Hall 7572. 

This is medium confidence. The page itself says he moved to industry, so I would email first and ask, “Does UW mail still reach you?” If you send anyway, it is not unreasonable because he still publishes that address.

5. Somesh Jha
I found enough to improve the mailer, but not a room number I fully trust. His personal page gives:

Somesh Jha
Lubar Professor
Computer Sciences Department
University of Wisconsin
Madison, WI 53706

It also gives his phone and email, but no room. 

Best mailer format:

Prof. Somesh Jha
Department of Computer Sciences
University of Wisconsin-Madison
Morgridge Hall
1205 University Avenue
Madison, WI 53706

UW CS faculty search snippets also associate him with UW CS and Morgridge Hall, but I would leave the room blank rather than guess. 

Extra cited-source people I’d maybe add later
Haolin Jin and Huaming Chen
Their paper is very relevant because it supports your “LLM pre-screen only” position. The arXiv page says they find LLMs can misclassify correct implementations as non-compliant, and that explanation-heavy prompts can increase misjudgment rates. 

But I only found arXiv contact routing, not a physical address. I’d email them, not mail.

Jamieson Cobleigh
Cited through assume-guarantee reasoning. I found older UMass / paper affiliations, not a current reliable address. Not a top mailer.

Dimitra Giannakopoulou
Very relevant intellectually, especially because of NASA + compositional verification + requirements/formal methods, but current physical mail route is bad. Email/LinkedIn only.

Practical mailing list now
I’d physically mail these first:

Aws Albarghouthi - UW Morgridge 7647

Adithya Murali - UW Morgridge 6532

Corina Păsăreanu - CMU Silicon Valley, Building 23, MS 23-11

Loris D’Antoni - UCSD CSE, Office 3214

Somesh Jha - UW Morgridge general

Leanna Rierson via CRC Press - only as a publisher-forwarding attempt

For Rierson, I’d make the packet especially brief and personal. She is the one where the “your book is what made this click for me” hook is real and probably the best chance of getting attention.


