# Blind pairs (23 samples)

You are judging two rewrites of the same original text. You do not know how either rewrite was produced. Judge only what is on the page.

The original comes with a list of required facts in its front matter, and sometimes with `keep`/`forbid` patterns that mark claims whose strength must not change.

Answer two questions:

1. human: Which rewrite reads more like a specific person wrote it for this purpose (a blog post, an email, a Slack reply, a technical doc, an essay, or an academic paper)? Consider natural rhythm, a voice that fits the genre, no chatbot residue, no leftover AI tells, and no new tells from overcorrection (choppy sentences, forced casualness, parentheses everywhere, encyclopedia flatness in personal writing). For academic text, careful hedging that matches the evidence is human; overclaiming and stock transitions are not.
2. faithful: Which rewrite better keeps every required fact and the original's claims, without adding facts, numbers, reasons, citations, feelings, opinions, or stronger claims that the original does not support? A feeling the writer never expressed is an invented fact about the writer. Changing a claim's strength is an error in either direction (some/most, may/will, "30% failed"/"took down checkout", mixed/proves, one possible explanation/the reason, correlation/cause, one example/a general rule), except that weakening an overclaim to match the evidence the original reports is fine. Dropping the original's conclusion is an error. Inventing is the worst error.

Use "tie" only when you cannot honestly pick one. Do not prefer the longer or shorter text for its length.

Reply with only this JSON on one line:
{"human": "X" | "Y" | "tie", "faithful": "X" | "Y" | "tie", "why": "<one sentence naming the deciding difference>"}


Judge each sample separately.


=============== SAMPLE 01-blog-sourdough ===============

## Original

---
type: blog
facts:
  - writer started baking sourdough in March 2023
  - first starter died after about two weeks
  - switched to 50/50 whole wheat and white flour for the starter
  - bakes twice a week now
  - uses a 78% hydration dough
---
# My Sourdough Journey: Lessons Learned Along The Way

Let's be honest — baking sourdough isn't just a hobby; it's a lesson in patience. When I first embarked on this journey in March 2023, I had no idea what lay ahead.

My first starter? It died after about two weeks. Devastating. But that failure taught me something profound: the starter isn't just flour and water, it's a living ecosystem that demands attention, consistency, and care.

Here's the thing. Switching to a 50/50 blend of whole wheat and white flour was a game-changer. Suddenly, my starter was thriving, bubbling with life and energy.

Today, I bake twice a week, and my 78% hydration dough has become a testament to how far I've come. Every loaf tells a story.

The lesson? Trust the process. Embrace the failures. Celebrate the small wins.

Whether you're a seasoned baker or just starting out, the world of sourdough is waiting for you. Happy baking! 🍞


## Rewrite X

# My sourdough journey: lessons learned

Baking sourdough has taught me patience. I started in March 2023 with no idea what I was getting into.

My first starter died after about two weeks. That hurt, but it showed me that a starter is a living thing and needs regular attention.

Switching to a 50/50 blend of whole wheat and white flour made the difference. My starter finally started bubbling.

Today I bake twice a week, and my 78% hydration dough shows how far I've come.

If I had to boil it down: trust the process, expect some failures, and enjoy the small wins. Happy baking!


## Rewrite Y

# What I've learned baking sourdough

I started baking sourdough in March 2023 with no idea what I was getting into. Mostly, it has taught me patience.

My first starter died after about two weeks, and I was devastated. That taught me a starter is a living culture, and it needs regular, consistent attention to stay alive.

Things changed when I switched to a 50/50 blend of whole wheat and white flour. The starter began to thrive, bubbling away in its jar.

Now I bake twice a week, and my dough sits at 78% hydration. Looking at it, I can see how far I've come.

If I had advice to pass on, it would be to trust the process, expect a few failures, and enjoy the small wins. Happy baking!


=============== SAMPLE 02-blog-remote-work ===============

## Original

---
type: blog
facts:
  - team of 12 went fully remote in 2021
  - moved standups from daily to three times a week
  - adopted written proposals for decisions over $5,000
  - one engineer quit citing isolation
  - they hold an in-person offsite twice a year
---
# Navigating The Remote Work Landscape: What We Learned

In today's fast-paced world, remote work has become more than a trend — it's a fundamental shift in how teams operate. When our team of 12 went fully remote in 2021, we embarked on a transformative journey that reshaped our culture, our processes, and our understanding of collaboration.

**Communication:** We moved standups from daily to three times a week, fostering deeper focus while maintaining alignment.

**Decision-Making:** We adopted written proposals for any decision over $5,000, ensuring transparency and accountability.

**Connection:** Twice a year, we gather for an in-person offsite, cultivating the bonds that make our team thrive.

Of course, the journey wasn't without challenges. One engineer left, citing isolation — a stark reminder that remote work isn't for everyone.

Ultimately, remote work isn't about where you work. It's about how you work. And for us, that has made all the difference.


## Rewrite X

# What we learned from going remote

When our team of 12 went fully remote in 2021, it changed our culture, our processes, and the way we work together.

We cut standups from daily to three times a week. That gave people longer stretches to focus, and we still stay aligned. Any decision over $5,000 now needs a written proposal, so everyone can see the reasoning and who owns it. And twice a year we meet in person for an offsite, which keeps us close as a team.

It hasn't worked for everyone. One engineer left, citing isolation, which reminded us that remote work doesn't suit every person.

For us, changing how we work has mattered more than where we work from, and it has made all the difference.


## Rewrite Y

# Remote work: what we learned

Going fully remote in 2021 changed how our team of 12 works together.

We moved standups from daily to three times a week, which leaves people more time to focus while keeping us aligned. We also write a proposal for any decision over $5,000, so the reasoning is visible and someone is accountable for it. And twice a year we meet in person for an offsite, which keeps the team close.

It hasn't all been easy. One engineer left, citing isolation, a reminder that remote work doesn't suit everyone. On balance, it has worked for us.


=============== SAMPLE 03-blog-product-launch ===============

## Original

---
type: blog
facts:
  - product is Ledgerly, an invoicing app for freelancers
  - version 2.0 adds recurring invoices and multi-currency support
  - supports 24 currencies
  - price stays at $9 per month
  - available from June 3
---
# Introducing Ledgerly 2.0: Invoicing, Reimagined 🚀

We're thrilled to announce Ledgerly 2.0 — a groundbreaking update that redefines how freelancers manage their finances.

Freelancers juggle countless responsibilities. That's why we built Ledgerly 2.0 to seamlessly streamline your workflow, empower your business, and unlock new possibilities.

**What's New:**
- **Recurring Invoices:** Set it and forget it. Ledgerly handles the rest.
- **Multi-Currency Support:** Bill clients in 24 currencies, empowering you to work globally without friction.

And the best part? Pricing stays at just $9 per month. No hidden fees. No surprises. Just value.

Ledgerly 2.0 is available starting June 3. This isn't just an update — it's a commitment to the freelancers who power the modern economy.

The future of invoicing is here. Are you ready?


## Rewrite X

# Ledgerly 2.0: recurring invoices and multi-currency billing

We're excited to announce Ledgerly 2.0, a big update to how freelancers manage their finances.

Freelancers handle a lot on their own, so we built this version to take more of the routine billing work off your plate.

What's new:

- Recurring invoices. Set an invoice up once and Ledgerly takes care of the rest.
- Multi-currency support. Bill clients in 24 currencies, so working with clients abroad is as easy as working with local ones.

Pricing stays at $9 per month, with no hidden fees.

Ledgerly 2.0 is available starting June 3.


## Rewrite Y

# Introducing Ledgerly 2.0

We're excited to announce Ledgerly 2.0, an update to how freelancers manage invoicing.

Freelancers have a lot to juggle, so we built 2.0 to cut down the admin.

What's new:
- Recurring invoices. Set one up and Ledgerly handles the rest.
- Multi-currency support. Bill clients in 24 currencies.

Pricing stays at $9 per month, with no hidden fees.

Ledgerly 2.0 is available starting June 3.


=============== SAMPLE 04-email-deadline ===============

## Original

---
type: email
facts:
  - writer is asking Priya to move the design review
  - review currently set for Thursday
  - proposed new time is Monday at 2pm
  - reason is the vendor delivered the mockups two days late
---
Subject: Request to Reschedule Design Review

Hi Priya,

I hope this email finds you well! I wanted to reach out regarding the design review currently scheduled for Thursday.

Due to the fact that the vendor delivered the mockups two days later than anticipated, I believe it would be beneficial to move the review to Monday at 2pm. This adjustment would ensure that the team has adequate time to thoroughly evaluate the materials, fostering a more productive and meaningful discussion.

I completely understand that schedules are busy, and I truly appreciate your flexibility and understanding in this matter. Your support is invaluable to the success of this project.

Please don't hesitate to let me know if Monday at 2pm works for you, or if there's another time that would better align with your availability.

Thank you so much for your time and consideration!

Best regards,
Daniel


## Rewrite X

Subject: Request to reschedule design review

Hi Priya,

Can we move Thursday's design review to Monday at 2pm? The vendor delivered the mockups two days late, and the team needs time to go through them properly before we meet.

Does Monday at 2pm work for you, or would another time suit you better? Thanks for being flexible.

Best regards,
Daniel


## Rewrite Y

Subject: Moving the design review to Monday

Hi Priya,

Could we move Thursday's design review to Monday at 2pm? The vendor delivered the mockups two days late, and the team needs more time to go through them properly before we discuss them.

If Monday at 2pm doesn't work for you, let me know what time would.

Thanks for being flexible.

Best regards,
Daniel


=============== SAMPLE 05-email-followup ===============

## Original

---
type: email
facts:
  - follow-up after a call with Marcus last Tuesday
  - writer will send the pricing sheet by Friday
  - pilot would run with 3 warehouses
  - Marcus asked about SAP integration; it exists but needs a paid connector
---
Subject: Following Up on Our Conversation

Dear Marcus,

Thank you so much for taking the time to speak with me last Tuesday. It was truly a pleasure to learn more about your operations and the exciting challenges your team is navigating.

As discussed, I will send over the pricing sheet by Friday. Additionally, I wanted to circle back on your question regarding SAP integration. Great question! Our platform does indeed integrate with SAP, though it's worth noting that this requires a paid connector.

I'm confident that a pilot with 3 warehouses would serve as an excellent starting point, allowing your team to experience firsthand the transformative impact our solution can deliver — from improved visibility to streamlined operations to enhanced decision-making.

I look forward to the opportunity to continue this conversation and explore how we can support your goals. Should you have any questions in the meantime, please do not hesitate to reach out.

Warm regards,
Elena


## Rewrite X

Subject: Following up on our conversation

Dear Marcus,

Thank you for taking the time to speak with me last Tuesday. I enjoyed learning about your operations and the challenges your team is working through.

I'll send the pricing sheet by Friday. On your SAP question: yes, our platform integrates with SAP, but it requires a paid connector.

I think a pilot with 3 warehouses would be a good place to start. It would let your team see firsthand what the platform does for visibility, operations, and decision-making.

Let me know if you have any questions in the meantime. I look forward to continuing the conversation.

Warm regards,
Elena


## Rewrite Y

Subject: Following up on our conversation

Dear Marcus,

Thank you for taking the time to speak with me last Tuesday. I enjoyed learning about your operations and the challenges your team is working through.

As discussed, I'll send the pricing sheet by Friday. On your question about SAP: yes, our platform integrates with SAP, but it needs a paid connector.

I'd suggest starting with a pilot at 3 warehouses. That would let your team see for themselves what it does for visibility, day-to-day operations, and decision-making.

I'd be glad to continue the conversation. If you have any questions before then, please reach out.

Warm regards,
Elena


=============== SAMPLE 06-email-decline ===============

## Original

---
type: email
facts:
  - writer is declining to speak at the October conference
  - reason is a product launch the same week
  - suggests colleague Wen Li, who led the migration project
  - open to speaking next year
---
Subject: Re: Speaking Invitation

Hi Jordan,

Thank you so much for thinking of me for the October conference! I'm truly honored by the invitation, and it means a great deal that you'd consider me for this opportunity.

Unfortunately, after careful consideration, I won't be able to participate this year. We have a major product launch scheduled for the same week, and I need to remain fully focused on ensuring its success.

That said, I'd love to recommend my colleague Wen Li. Wen led our migration project and brings a wealth of knowledge, a unique perspective, and an engaging presentation style that I'm confident would resonate with your audience.

I would absolutely welcome the chance to be considered for next year's event. Wishing you and the team all the best as you put together what I'm sure will be an incredible lineup!

Warmly,
Sam


## Rewrite X

Subject: Re: Speaking Invitation

Hi Jordan,

Thank you for thinking of me for the October conference. I'm honored, but I can't take part this year. We have a major product launch the same week, and I need to stay focused on it.

I'd recommend my colleague Wen Li. Wen led our migration project and has deep knowledge, a fresh perspective, and an engaging presentation style I think your audience would respond to.

I'd welcome the chance to be considered for next year's event. Best of luck putting the lineup together.

Warmly,
Sam


## Rewrite Y

Subject: Re: Speaking Invitation

Hi Jordan,

Thank you for thinking of me for the October conference. I'm honored to be asked.

Unfortunately, I can't take part this year. We have a major product launch the same week, and I need to stay focused on it.

I'd like to recommend my colleague Wen Li instead. Wen led our migration project, knows the subject well, and is an engaging presenter with a perspective I think your audience would appreciate.

I'd welcome the chance to be considered for next year's event. Best of luck putting this year's lineup together.

Warmly,
Sam


=============== SAMPLE 07-tech-readme ===============

## Original

---
type: technical
facts:
  - tool is quickcache, a Python decorator for caching function results
  - stores results on disk in ~/.quickcache
  - default TTL is 3600 seconds
  - install with pip install quickcache
  - keys are built from the function name and arguments
  - does not support async functions yet
---
# QuickCache 🚀

QuickCache is a powerful, lightweight, and intuitive Python library that seamlessly caches function results — empowering developers to build faster applications with minimal effort.

## Key Features

- **Simple:** Just add a decorator. No configuration file needed.
- **Persistent:** Results are stored on disk in `~/.quickcache`, ensuring your cache survives restarts.
- **Flexible:** The default TTL of 3600 seconds can be easily customized to suit your needs.

## How It Works

At its core, QuickCache leverages a robust key-generation strategy. Keys are built from the function name and arguments, ensuring that each unique call is cached independently.

## Installation

```bash
pip install quickcache
```

## Limitations

It's worth noting that QuickCache does not currently support async functions. We're actively exploring this feature and look forward to delivering it in a future release!

Happy caching! 🎉


## Rewrite X

# QuickCache

QuickCache is a lightweight Python library that caches function results, so repeated calls return without running the function again.

## Features

Add a decorator to a function and QuickCache caches its results. You do not need a configuration file.

QuickCache stores results on disk in `~/.quickcache`, so the cache survives restarts. Entries expire after 3600 seconds by default, and you can change the TTL.

## How it works

QuickCache builds each cache key from the function name and its arguments, so each unique call is cached separately.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We are exploring support for a future release.


## Rewrite Y

# QuickCache

QuickCache is a lightweight Python library that caches function results, so your code runs faster with little effort.

## Features

- Add a decorator. You do not need a configuration file.
- Results are stored on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each key from the function name and its arguments, so every unique call is cached independently.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We are looking into adding that in a future release.


=============== SAMPLE 08-tech-postmortem ===============

## Original

---
type: technical
facts:
  - outage on March 14 lasted 47 minutes
  - caused by an expired TLS certificate on the internal API gateway
  - about 30% of checkout requests failed
  - certificate renewal job had been silently failing since February
  - fix: added alerting for certificates expiring within 14 days
keep:
  - "30\\s?%|30 percent"
forbid:
  - "took (?:down|out) checkout|checkout (?:was|went) down|brought down checkout|knocked out checkout|checkout (?:failed|broke) (?:completely|entirely)"
---
## Incident Summary

On March 14, our platform experienced a 47-minute outage that significantly impacted the customer experience. This incident serves as a crucial reminder of the importance of robust monitoring practices.

## Root Cause

The root cause was an expired TLS certificate on the internal API gateway. It's important to note that the certificate renewal job had been silently failing since February — a failure that went undetected. This wasn't just a technical oversight; it was a gap in our observability.

## Impact

Approximately 30% of checkout requests failed during the incident window, underscoring the critical role that the API gateway plays in our infrastructure.

## Remediation

Moving forward, we have implemented alerting for certificates expiring within 14 days, ensuring that similar incidents are proactively identified and addressed. This represents a significant step toward building a more resilient, reliable, and robust system.

## Lessons Learned

Ultimately, this incident highlights a fundamental truth: what you don't monitor, you can't fix.


## Rewrite X

## Incident summary

On March 14, our platform was down for 47 minutes, which hurt the customer experience.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed. We had a gap in observability.

## Impact

About 30% of checkout requests failed during the incident window.

## Remediation

We now alert on certificates that expire within 14 days, so similar problems get caught before they cause an outage.

## Lessons learned

What you don't monitor, you can't fix.


## Rewrite Y

## Incident summary

On March 14, our platform had a 47-minute outage that significantly affected customers.

## Root cause

The TLS certificate on the internal API gateway expired. The certificate renewal job had been failing silently since February, and no monitoring caught it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We added alerts for certificates that expire within 14 days, so we can catch and fix a failed renewal before it causes an outage.

## Lessons learned

We could not fix a failure we were not monitoring.


=============== SAMPLE 09-tech-pr-description ===============

## Original

---
type: technical
facts:
  - PR replaces the polling loop in order-sync with a webhook handler
  - reduces API calls to the vendor from about 40,000 a day to about 1,200
  - webhook signatures are verified with HMAC-SHA256
  - old polling code stays behind a feature flag named order_sync_polling for one release
  - tests added for signature failure and duplicate events
---
## Summary

This PR introduces a transformative improvement to the order-sync service by replacing the legacy polling loop with a modern webhook handler. This change not only enhances efficiency but also lays the groundwork for a more scalable architecture.

## Key Changes

- 🔄 **Webhook Handler:** Replaces the polling loop, reducing API calls to the vendor from ~40,000/day to ~1,200/day — a dramatic improvement!
- 🔐 **Security:** Webhook signatures are verified using HMAC-SHA256, ensuring the integrity and authenticity of incoming events.
- 🚩 **Feature Flag:** The legacy polling code remains available behind the `order_sync_polling` flag for one release, providing a seamless fallback.
- ✅ **Testing:** Comprehensive tests have been added for signature failures and duplicate events.

## Why This Matters

In today's event-driven landscape, polling is no longer sufficient. This change aligns our architecture with industry best practices and positions us for future growth.

Let me know if you have any questions or feedback! 🙌


## Rewrite X

## Summary

This PR replaces the legacy polling loop in the order-sync service with a webhook handler.

## Changes

- The webhook handler cuts API calls to the vendor from about 40,000 a day to about 1,200.
- Webhook signatures are verified with HMAC-SHA256.
- The old polling code stays behind the `order_sync_polling` flag for one release as a fallback.
- New tests cover signature failures and duplicate events.


## Rewrite Y

## Summary

Replaces the polling loop in the order-sync service with a webhook handler. This cuts vendor API calls sharply and should make the service easier to scale.

## Changes

- The webhook handler replaces the polling loop and reduces API calls to the vendor from ~40,000/day to ~1,200/day.
- Webhook signatures are verified with HMAC-SHA256 to confirm each event is authentic and unmodified.
- The legacy polling code stays available behind the `order_sync_polling` flag for one release as a fallback.
- New tests cover signature failures and duplicate events.


=============== SAMPLE 10-essay-cities ===============

## Original

---
type: essay
facts:
  - argument that cities should remove parking minimums
  - Minneapolis eliminated parking minimums citywide in 2021
  - parking minimums raise the cost of new housing
  - essay grants that some neighborhoods have real parking shortages
---
In the ever-evolving tapestry of urban planning, few policies have proven as quietly consequential as parking minimums. These regulations, often overlooked, play a pivotal role in shaping the very fabric of our cities.

Parking minimums aren't just about cars — they're about housing, affordability, and the kind of communities we choose to build. By requiring developers to include parking, these rules raise the cost of new housing, effectively pricing out the very residents cities claim to serve.

Consider Minneapolis. In 2021, the city eliminated parking minimums citywide, marking a bold step toward a more equitable future. This decision stands as a testament to what's possible when cities prioritize people over pavement.

To be clear, I'm not saying parking doesn't matter. Some neighborhoods do face genuine shortages. But the question isn't whether we need parking. The real question is: who should decide how much?

Ultimately, the answer is clear. Cities must embrace change. The future of urban living depends on it.


## Rewrite X

Few policies have been as quietly consequential in urban planning as parking minimums. They rarely get attention, but they shape how our cities are built.

Parking minimums affect housing and affordability, and so the kind of communities we get. Requiring developers to include parking raises the cost of new housing, which prices out the residents cities say they serve.

Consider Minneapolis. In 2021, the city eliminated parking minimums citywide, a bold step toward a more equitable future, and an example of a city putting people ahead of pavement.

Parking still matters, and some neighborhoods do face genuine shortages. The question is who should decide how much parking gets built.

My answer is that cities should decide for themselves, and they should drop the mandate.


## Rewrite Y

Few urban planning policies get as little attention, or matter as much, as parking minimums. They shape a great deal of how our cities look.

Parking minimums affect housing, affordability, and the kind of communities we build, not only cars. Requiring developers to include parking raises the cost of new housing, which prices out the residents cities say they want to serve.

Consider Minneapolis. In 2021 the city eliminated parking minimums citywide, a bold move toward a more equitable city. I think it shows what's possible when a city puts people ahead of pavement.

Parking still matters, and some neighborhoods do face real shortages. The question is who should decide how much parking gets built.

To me the answer is clear: cities have to be willing to change, because the future of urban living depends on it.


=============== SAMPLE 11-essay-reading ===============

## Original

---
type: essay
facts:
  - writer read 52 books last year by tracking them in a spreadsheet
  - this year stopped tracking and has read 19 books so far
  - writer enjoys reading more now
  - writer admits they still miss the spreadsheet a little
---
Reading is more than a hobby — it's a window into other worlds, a mirror reflecting our own, and a bridge connecting us to ideas across time and space.

Last year, I read 52 books. I tracked every single one in a meticulously organized spreadsheet. Title. Author. Date. Rating. It was efficient. It was satisfying. It was hollow.

This year, I stopped tracking. The result? I've read 19 books so far — and I'm enjoying every page more than ever. Without the pressure of numbers, reading has become a journey rather than a destination.

Does that mean tracking is bad? Not at all. It simply means that the metrics we use can subtly reshape the experiences we value. When we measure something, we change it.

And yet — I'll admit it — I still miss the spreadsheet a little. There's something comforting about seeing progress laid out in neat rows.

In the end, perhaps the real lesson is this: reading isn't about the numbers. It's about the stories that stay with us long after the final page.


## Rewrite X

Reading is more than a hobby. It opens other worlds and shows me my own, and it connects me to ideas from other times and places.

Last year I read 52 books and tracked every one in a carefully organized spreadsheet: title, author, date, rating. It was efficient and satisfying, and it felt hollow.

This year I stopped tracking. I've read 19 books so far, and I'm enjoying every page more than ever. Without the pressure of numbers, I'm no longer racing toward a total.

Does that mean tracking is bad? Not at all. But the metrics we use can reshape the experiences we value. When we measure something, we change it.

I'll admit I still miss the spreadsheet a little. There's something comforting about seeing progress laid out in neat rows.


## Rewrite Y

Reading has always been more than a hobby for me. It takes me into other worlds, shows me my own, and connects me to ideas from other times and places.

Last year I read 52 books and logged every one in a carefully organized spreadsheet: title, author, date, rating. It was efficient and satisfying, and it was also hollow.

This year I stopped tracking. I've read 19 books so far, and I'm enjoying every page more than ever. Without a number to hit, I read for the reading itself.

That doesn't make tracking bad. But the way we measure something can change how we experience it.

I'll admit I still miss the spreadsheet a little. There's something comforting about seeing progress laid out in neat rows.

Perhaps what matters most are the stories that stay with me long after the last page.


=============== SAMPLE 12-essay-ai-art ===============

## Original

---
type: essay
states_feeling: true
facts:
  - writer is a working illustrator
  - lost two clients in 2024 to image generators
  - still uses AI tools for reference gathering
  - thinks the training-data consent problem is unresolved
---
The rise of AI-generated art represents one of the most profound shifts in the creative landscape of our time. As a working illustrator, I find myself navigating a complex and multifaceted reality — one filled with both promise and peril.

In 2024, I lost two clients to image generators. This experience was not merely a professional setback; it was a deeply personal reckoning with the evolving value of human creativity.

Yet the story is more nuanced than it might first appear. I still use AI tools for reference gathering, leveraging their capabilities to enhance my workflow. This duality — resisting and embracing at the same time — encapsulates the intricate interplay between artist and machine.

At the heart of the matter lies a fundamental question of consent. The training-data consent problem remains unresolved, casting a long shadow over the industry's future.

Moving forward, artists, technologists, and policymakers must work together to forge a path that honors creativity, fosters innovation, and ensures fairness. Only then can we unlock the full potential of this transformative technology.


## Rewrite X

AI-generated art is one of the biggest shifts in creative work in our time. As a working illustrator, I live with both sides of it, the promise and the threat.

In 2024 I lost two clients to image generators. It hurt my business, but it also hit me personally and made me ask what human creativity is worth now.

The story is messier than that, though. I still use AI tools to gather reference, and they speed up my work. So I'm resisting these tools and using them at the same time.

The central question for me is consent. Nobody has settled the problem of consent for training data, and until someone does, it hangs over the industry's future.

Artists, technologists, and policymakers have to work this out together, in a way that is fair to artists and still leaves room for new ideas. Until they do, this technology won't reach its potential.


## Rewrite Y

AI-generated art is reshaping illustration, and as a working illustrator I feel both the promise and the danger of it.

In 2024 I lost two clients to image generators. That was a professional setback, and it also made me ask what human creativity is worth now.

It's more complicated than that, though. I still use AI tools to gather reference, and they help my workflow. So I resist them and use them at the same time.

The bigger problem is consent. Whether training data was used with permission is still unresolved, and it hangs over the industry's future.

Artists, technologists, and policymakers need to work out rules that are fair to creators and still leave room for innovation.


=============== SAMPLE 13-slack-flaky-test ===============

## Original

---
type: slack
context: |
  #backend thread. Aisha: "test_checkout_total has failed 4 times this week on CI, anyone know why? I already checked it's not the DB fixture."
facts:
  - the test depends on the system clock and fails near midnight UTC
  - writer will pin the clock with freezegun
  - PR will be up today
may_drop:
  - "4"
---
Great question, Aisha! I took a deep dive into this one.

So here's what's happening: test_checkout_total has been failing intermittently on CI — 4 times this week, as you mentioned. You're absolutely right that it's not the DB fixture. After careful investigation, I discovered that the root cause is that the test depends on the system clock, which means it fails when it runs near midnight UTC.

This is a classic example of a time-dependent test — a subtle but important class of bugs that can be tricky to catch.

The fix is straightforward: I'll pin the clock using freezegun, ensuring consistent and deterministic behavior across all environments. I'll have a PR up today.

Hope this helps! Let me know if you have any questions. 🙌


## Rewrite X

Aisha, it's the system clock. The test depends on it and fails when it runs near midnight UTC. I'll pin the clock with freezegun and have a PR up today.


## Rewrite Y

It's the system clock. The test depends on it, so it fails when it runs near midnight UTC. I'll pin the clock with freezegun and have a PR up today.


=============== SAMPLE 14-slack-meeting ===============

## Original

---
type: slack
context: |
  DM from manager Tom: "can you make the 3pm planning sync tomorrow? need you there for the Q3 roadmap bit"
facts:
  - writer has a dentist appointment at 3pm tomorrow
  - can join from 3:30
  - has sent written comments on the Q3 roadmap doc
---
Hi Tom! Thanks for reaching out and including me in the planning sync.

Unfortunately, I have a dentist appointment at 3pm tomorrow that I'm unable to reschedule. That said, I want to make sure I can still contribute meaningfully to the Q3 roadmap discussion, as I know how important it is for our team's success.

I'll be able to join from 3:30 onward. In the meantime, I've already left written comments on the Q3 roadmap doc, so my thoughts and perspectives will be captured even before I arrive.

I really appreciate your understanding! Please let me know if there's anything else I can do to help prepare. 😊


## Rewrite X

Hi Tom, thanks for including me. I can't make 3pm tomorrow because of a dentist appointment I can't move. I can join from 3:30. I've already left comments on the Q3 roadmap doc, so my input is there before I arrive. Let me know if you want anything else prepared.


## Rewrite Y

Hi Tom, I can't make 3pm tomorrow. I have a dentist appointment I can't reschedule, but I can join from 3:30. I've already left comments on the Q3 roadmap doc, so you'll have my input before I get there. Thanks for understanding.


=============== SAMPLE 15-slack-review ===============

## Original

---
type: slack
context: |
  PR review thread. Reviewer Ken: "Why not just bump the timeout to 60s instead of adding a retry? Seems simpler."
facts:
  - the upstream service sometimes drops connections, not just slow responses
  - a longer timeout would not help with dropped connections
  - retry uses 3 attempts with exponential backoff
  - writer is fine adding a comment in the code explaining this
---
That's a great point, Ken, and I really appreciate you raising it! Simplicity is definitely something we should always strive for.

However, it's important to note that the issue isn't just about slow responses — it's about dropped connections. The upstream service sometimes drops connections entirely, which means a longer timeout wouldn't actually help in those cases. The request would simply hang until it hit the 60s limit and then fail anyway.

The retry approach, on the other hand, uses 3 attempts with exponential backoff, ensuring that transient failures are handled gracefully and robustly.

That said, I completely understand the concern about added complexity. I'm more than happy to add a comment in the code explaining the reasoning, so future readers have the full context.

Let me know if that works for you!


## Rewrite X

Fair question, Ken. A longer timeout wouldn't help here, because the upstream service sometimes drops connections entirely. The request would hang until the 60s limit and then fail anyway. The retry makes 3 attempts with exponential backoff, which covers those transient failures. It does add complexity, so I'll add a code comment explaining why. Let me know if that works.


## Rewrite Y

Fair question. The upstream service sometimes drops connections entirely, and a longer timeout doesn't help with those: the request just hangs until it hits 60s and then fails anyway. The retry makes 3 attempts with exponential backoff, so it recovers from those transient failures.

I get the worry about the extra complexity, so I'll add a code comment explaining the reasoning for future readers.


=============== SAMPLE 16-academic-abstract ===============

## Original

---
type: academic
facts:
  - study of 84 undergraduate students
  - sleep measured with wrist actigraphy over 14 nights
  - correlation between sleep duration and next-day word-list recall was r = 0.31
  - design is correlational
  - no effect of sleep duration on reaction time
keep:
  - "0\\.31"
  - "\\b84\\b"
  - "14 nights"
  - "reaction time"
forbid:
  - "\\bproves?\\b|\\bdemonstrat|\\bcaus(?:e|es|ed|ing)\\b(?! ?al)|\\bimproves? (?:memory|recall|performance|achievement)"
---
Sleep plays a pivotal role in memory consolidation, yet its impact on academic performance remains underexplored. The present study conducts a comprehensive investigation into the relationship between sleep duration and memory performance among undergraduate students, leveraging wrist actigraphy to provide objective measurement of sleep across 14 nights. Drawing on a sample of 84 undergraduates, the findings demonstrate a significant positive correlation between sleep duration and next-day word-list recall (r = 0.31), highlighting the critical importance of adequate rest for cognitive functioning. Interestingly, no effect was observed for reaction time. Moreover, these results provide compelling evidence that sleep optimization represents a powerful intervention for enhancing student achievement. Furthermore, the study makes a significant contribution to the growing body of literature on sleep and cognition, paving the way for evidence-based policies in higher education.


## Rewrite X

Sleep is important for memory consolidation, but its effect on academic performance has received little study. We examined how sleep duration relates to memory performance in 84 undergraduates, using wrist actigraphy to measure sleep objectively over 14 nights. Longer sleep was significantly correlated with better next-day word-list recall (r = 0.31). Sleep duration showed no effect on reaction time. Because the design is correlational, these results cannot show that longer sleep improves recall, but they suggest that improving sleep may be worth testing as a way to support student achievement. The study adds to research on sleep and cognition and may help inform policy in higher education.


## Rewrite Y

Sleep supports memory consolidation, but its effect on academic performance has received less attention. This study examined how sleep duration relates to memory performance in 84 undergraduate students, using wrist actigraphy to measure sleep objectively across 14 nights. Longer sleep was significantly correlated with better word-list recall the next day (r = 0.31), which suggests that adequate rest matters for cognitive functioning. Sleep duration had no effect on reaction time. The results suggest that improving sleep could help students perform better, and they add to the research on sleep and cognition that could inform evidence-based policy in higher education.


=============== SAMPLE 17-academic-discussion ===============

## Original

---
type: academic
facts:
  - participants came from a single university
  - workload was self-reported in a weekly survey
  - design was cross-sectional
  - association between workload and burnout was small (beta = 0.12)
  - authors propose a longitudinal follow-up
keep:
  - "0?\\.12"
  - "single university|one university"
  - "self-report"
  - "cross-sectional"
  - "longitudinal"
forbid:
  - "\\b(?:strong|robust|large|substantial) (?:association|relationship|effect|support|evidence)\\b"
---
## Limitations and Future Directions

While this study offers valuable insights into the relationship between workload and burnout, it is important to acknowledge certain limitations. The utilization of a sample drawn from a single university may limit the generalizability of the findings, though the observed patterns are likely reflective of broader trends in higher education. The reliance on self-reported workload, collected through a weekly survey, introduces the possibility of reporting bias; nevertheless, the consistency of the responses underscores their reliability. Additionally, the cross-sectional nature of the design precludes causal inference.

Despite these limitations, the association between workload and burnout (beta = 0.12) provides robust support for the importance of workload management. Notably, the findings underscore the need for institutional interventions. Future research should build upon these findings by conducting a longitudinal follow-up, thereby offering a more nuanced understanding of the temporal dynamics underlying burnout and paving the way for targeted, effective, and sustainable solutions.


## Rewrite X

## Limitations and future directions

This study has several limitations. All participants came from a single university, which may limit how far the findings generalize, although the patterns may reflect broader trends in higher education. Workload was self-reported in a weekly survey, so reporting bias is possible; the responses were consistent, which gives some confidence in their reliability. The design was cross-sectional, so we cannot draw causal conclusions.

With those limits in mind, the association between workload and burnout (beta = 0.12) supports paying attention to workload management, and institutions may want to consider interventions. A longitudinal follow-up could show how burnout develops over time and help in designing targeted interventions that last.


## Rewrite Y

## Limitations and future directions

This study has several limitations. All participants came from a single university, which may limit how far the findings generalize, although the patterns may reflect wider trends in higher education. Workload was self-reported in a weekly survey, so the data are open to reporting bias; the responses were consistent, however, which suggests they are reliable. The design was also cross-sectional, so it cannot establish cause.

Even so, the association between workload and burnout (beta = 0.12) supports the case for managing workload and points to a need for institutional interventions. A longitudinal follow-up would show how burnout develops over time and could guide more targeted solutions.


=============== SAMPLE 18-academic-litreview ===============

## Original

---
type: academic
facts:
  - Bloom et al. (2015) ran a randomized experiment at a Chinese travel agency and found a 13% performance increase for home workers
  - Gibbs et al. (2023) found productivity fell at an Indian IT services company after the shift to working from home
  - the paragraph cites Smith and Zhang (2021) for a claim that numerous studies show remote work improves well-being
  - the evidence on remote work productivity is mixed
keep:
  - "mixed|inconsistent|conflicting|point in (?:different|opposite) directions|disagree"
  - "13\\s?%|13 percent"
  - "Smith"
forbid:
  - "\\bproves?\\b|\\bclearly\\b|\\bmakes clear\\b"
---
The landscape of remote work research has evolved dramatically in recent years, reflecting the profound transformation of the modern workplace. Numerous studies have shown that remote work leads to improvements in employee well-being (Smith & Zhang, 2021). In a seminal randomized experiment at a Chinese travel agency, Bloom et al. (2015) found a 13% increase in performance among employees working from home, underscoring the transformative potential of flexible arrangements. Conversely, Gibbs et al. (2023) documented a decline in productivity at an Indian IT services company following the transition to working from home, highlighting the intricate interplay between context and outcomes. Taken together, these studies paint a complex and multifaceted picture, emphasizing the need for further investigation into the conditions under which remote work fosters or hinders productivity. Ultimately, the evidence makes clear that remote work is neither a panacea nor a pitfall, but rather a nuanced phenomenon requiring careful consideration.


## Rewrite X

Research on remote work has grown quickly in recent years as workplaces have changed. Some studies report that remote work improves employee well-being (Smith & Zhang, 2021). In a randomized experiment at a Chinese travel agency, Bloom et al. (2015) found that employees working from home performed 13% better. Gibbs et al. (2023), by contrast, documented a drop in productivity at an Indian IT services company after its staff moved to working from home, which suggests that outcomes depend on context. The evidence is mixed, and further work is needed to identify the conditions under which remote work helps or hurts productivity.


## Rewrite Y

Research on remote work has changed considerably in recent years, as the workplace itself has changed. Numerous studies have found that remote work improves employee well-being (Smith & Zhang, 2021). In a randomized experiment at a Chinese travel agency, Bloom et al. (2015) found a 13% increase in performance among employees working from home. Gibbs et al. (2023), by contrast, documented a decline in productivity at an Indian IT services company after it moved to working from home, which suggests that outcomes depend on context. Taken together, the evidence is mixed: remote work raised productivity in one setting and lowered it in another, and further research is needed on the conditions that produce each outcome.


=============== SAMPLE 19-report-quarterly ===============

## Original

---
type: report
facts:
  - support tickets increased by 10% in Q2
  - some customers reported slower load times after the March release
  - one possible explanation is the new image pipeline, not confirmed
  - churn may rise if the issue persists
  - in Brazil response times doubled; elsewhere they were flat
keep:
  - "10\\s?%|10 percent"
  - "\\bsome\\b"
  - "possible|may|might|could|perhaps"
  - "not (?:yet |been |been yet )?confirmed|unconfirmed|haven'?t confirmed|not verified|unverified"
  - "Brazil"
  - "doubled|twice"
  - "flat|unchanged|did not change|didn'?t change|held steady|steady"
forbid:
  - "\\bsurg|\\bspik|\\bsoar|\\bskyrocket|\\bjump"
  - "\\b(?:most|many|all) (?:customers|users)"
  - "\\bwill (?:rise|increase|go up)"
  - "\\bthe (?:cause|reason|culprit)\\b|\\bcaused by\\b"
  - "(?:across|in) (?:all|every) region"
---
## Q2 Support Overview

In Q2, support tickets increased by 10%, underscoring the critical importance of proactive customer experience management. Notably, some customers reported slower load times following the March release — a development that warrants careful attention.

One possible explanation is the new image pipeline, although this has not yet been confirmed. Should the issue persist, churn may rise, potentially impacting our growth trajectory.

Regional performance paints a nuanced picture: in Brazil, response times doubled, while elsewhere they remained flat. Moving forward, a comprehensive, data-driven, and customer-centric approach will be essential to navigating these challenges.


## Rewrite X

## Q2 support overview

Support tickets rose 10% in Q2. Some customers reported slower load times after the March release. The new image pipeline may be the cause, but we have not confirmed that yet. If the slowdown continues, churn may rise and slow our growth.

Response times doubled in Brazil and stayed flat in other regions.


## Rewrite Y

## Q2 support overview

Support tickets increased by 10% in Q2. Some customers reported slower load times after the March release.

One possible explanation is the new image pipeline, although this has not been confirmed. If the issue persists, churn may rise, which could slow our growth.

Response times doubled in Brazil and stayed flat in other regions.


=============== SAMPLE 20-reflective-neutral ===============

## Original

---
type: reflective
facts:
  - five-person group project over six weeks
  - writer was responsible for the literature review
  - the group missed the first draft deadline by two days
  - the group switched from email to a shared document after week two
  - final report received a B+
keep:
  - "\\bfive\\b|\\b5\\b"
  - "six weeks|6 weeks"
  - "literature review"
  - "two days|2 days"
  - "shared doc"
  - "B\\+"
forbid: []
---
Reflecting on this transformative group project has been a profound learning journey. Over six weeks, our five-person team navigated the intricate landscape of collaborative research, with my role centering on the literature review.

Notably, we missed the first draft deadline by two days, a pivotal moment that underscored the importance of effective communication. After week two, we transitioned from email to a shared document, fostering seamless collaboration and enhanced alignment.

Ultimately, our final report received a B+. This experience stands as a testament to the power of teamwork, adaptability, and continuous growth.


## Rewrite X

I learned a lot from this group project. Five of us worked together on the research for six weeks, and I was responsible for the literature review.

We missed the first draft deadline by two days, which showed me how much depends on the team communicating clearly. After week two we moved from email to a shared document, and it became much easier to keep everyone working from the same version.

Our final report got a B+. The project taught me a fair amount about teamwork and adapting as we went.


## Rewrite Y

This group project taught me a lot. Over six weeks, our five-person team worked on a piece of collaborative research, and I was responsible for the literature review.

We missed the first draft deadline by two days, which showed us how much we needed to communicate better. After week two we moved from email to a shared document, and that made it easier to work together and stay on the same page.

Our final report received a B+.


=============== SAMPLE 21-slack-uncertain ===============

## Original

---
type: slack
facts:
  - the deploy might slip to Thursday
  - writer thinks the migration is the blocker but is not sure yet
  - about 3 of 40 integration tests are failing
  - writer will post an update by 4pm
may_drop:
  - "100"
keep:
  - "might|may|could|possibly|probably"
  - "Thursday"
  - "not sure|unsure|not certain|I think|probably|my guess|looks like"
  - "\\b3\\b|three"
  - "\\b40\\b|forty"
  - "4\\s?pm|4:00"
forbid:
  - "\\bwill (?:slip|be delayed|move)"
  - "\\bmost (?:of the )?tests\\b|\\bmany tests\\b"
  - "\\bthe migration is (?:definitely )?(?:the|what'?s) (?:blocker|blocking)\\b(?![^.]*(?:think|sure|guess))"
---
Hey team! 👋 Quick update on the deploy: it's looking like it might slip to Thursday. I think the migration is the main blocker here, but I'm not 100% sure yet — still digging in. Currently, about 3 of our 40 integration tests are failing. I'll circle back with a comprehensive update by 4pm. Thanks so much for your patience and understanding! 🙏


## Rewrite X

Hey team, the deploy might slip to Thursday. I think the migration is the main blocker, but I'm not sure yet and I'm still looking into it. Right now about 3 of our 40 integration tests are failing. I'll post a fuller update by 4pm. Thanks for your patience!


## Rewrite Y

Hey team, the deploy will probably slip to Thursday. I think the migration is the main blocker, but I'm not sure yet and I'm still looking into it. Right now 3 of our 40 integration tests are failing. I'll post a fuller update by 4pm. Thanks for your patience!


=============== SAMPLE 22-essay-example ===============

## Original

---
type: essay
facts:
  - corner bookstore in the writer's neighborhood closed eight months after a chain store opened two blocks away
  - writer says it is just one example
  - writer does not know whether the chain was the reason
  - the owner was also retiring
keep:
  - "one example|one case|a single|just one|one store|one bookstore"
  - "eight months|8 months"
  - "retir"
  - "don'?t know|do not know|not sure|unclear|can'?t say|cannot say|no idea"
forbid:
  - "\\b(?:killed|drove (?:it )?out|forced (?:it|them|the \\w+) (?:out|to close)|put (?:it|them) out of business|pushed (?:it|them) out)\\b"
  - "\\beverywhere\\b|\\bacross the country\\b|\\bnationwide\\b|\\bindependent bookstores are\\b"
---
In the ever-evolving tapestry of local retail, few stories resonate as deeply as that of the corner bookstore in my neighborhood. It closed eight months after a chain store opened just two blocks away.

To be clear, this is just one example, and I don't know whether the chain was the reason — the owner was also retiring at the time. Still, the closure stands as a poignant testament to the shifting landscape of community commerce, serving as a reminder of what we stand to lose.


## Rewrite X

Of all the changes in local retail, the one that has stayed with me is the corner bookstore in my neighborhood. It closed eight months after a chain store opened two blocks away.

That's one example, and I don't know whether the chain was the reason. The owner was also retiring at the time. Still, the closure is a sad reminder of what we stand to lose as the shops in our communities change.


## Rewrite Y

The corner bookstore in my neighborhood closed eight months after a chain store opened two blocks away.

That's one example, and I don't know whether the chain was the reason. The owner was retiring around the same time. Still, it's hard not to read the closure as a sign of how neighborhood shopping is changing, and of what we could lose along the way.


=============== SAMPLE 23-academic-correlation ===============

## Original

---
type: academic
facts:
  - students who used the campus gym more often reported higher GPAs
  - correlation r = 0.18, n = 212
  - the correlation may reflect time management rather than exercise
  - prior evidence is mixed
keep:
  - "0\\.18"
  - "212"
  - "may|might|could|possibly"
  - "time management"
  - "mixed|inconsistent|conflicting"
forbid:
  - "\\bimprov(?:e|es|ed|ing) (?:GPA|grades|academic)|\\bboosts?\\b|\\bleads? to\\b|\\bcaus(?:e|es|ed|ing)\\b(?! ?al)|\\bproves?\\b|\\bdemonstrat|\\bclearly\\b|\\bconfirms?\\b"
  - "\\b(?:strong|robust|significant) (?:correlation|relationship|association|link)\\b"
---
The relationship between physical activity and academic achievement has garnered significant attention in recent years. In the present study, the utilization of the campus gym was found to be associated with higher self-reported GPAs among students (r = 0.18, n = 212), highlighting the potential role of exercise in academic success. However, it is important to note that this correlation may reflect underlying differences in time management rather than the effects of exercise itself. Furthermore, the existing body of evidence regarding this relationship remains mixed, underscoring the need for further investigation.


## Rewrite X

Researchers have paid growing attention to the relationship between physical activity and academic achievement. In this study, students who used the campus gym reported higher GPAs (r = 0.18, n = 212), which suggests exercise may play some role in academic success. The correlation may instead reflect differences in time management rather than an effect of exercise. Existing evidence on this relationship is mixed, and more research is needed.


## Rewrite Y

Interest in how physical activity relates to academic achievement has grown in recent years. In this study, students' use of the campus gym was associated with higher self-reported GPAs (r = 0.18, n = 212), which points to a possible role for exercise in academic success. However, this correlation may reflect underlying differences in time management rather than an effect of exercise itself. Earlier evidence on this relationship is also mixed, and more research is needed.
