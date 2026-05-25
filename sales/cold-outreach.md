# Cold outreach — the demo-led motion

You have no warm network and no reviews. So you don't pitch — you **show**. The
move that beats everything else from a cold start: re-skin the agent to the
prospect's own business, record a 60-90 second video of it catching and booking
a lead, and send them that. The demo *is* your credibility.

This is high-personalization, low-volume. 10-20 great touches/day beats 500 blasts
— and blasting also breaks anti-spam law (CAN-SPAM/CASL) and torches your sender
reputation. Don't.

## Step 1 — Build a target list (30 min/day)

- Search Google Maps for "{service} {city}" (e.g. "house cleaning Austin").
- Prioritize businesses that **have a website with a contact form or "we'll get
  back to you"** — that's the leaking funnel you fix. Bonus signal: you fill out
  their form yourself and get a slow/no reply. That's your opening line.
- Capture: business name, owner name if findable, site, the lead form, niche.
- Tools that help (free tiers): Google Maps, the business's own site, LinkedIn.

## Step 2 — Re-skin the agent (~15 min per prospect)

1. Copy `configs/sample_home_services.json` → `configs/<prospect>.json`.
2. Fill in their real name, services, hours, service area, tone.
3. Run the scenario demo with their config:
   `python -m lead_agent.cli -c configs/<prospect>.json -s configs/sample_scenario.json`
   (tweak the scenario messages to fit their service).
4. Screen-record it (Loom free tier, or OBS). 60-90 seconds, no intro fluff:
   show a "customer" messaging in and walking out with a booked appointment.

## Step 3 — The first-touch message

Lead with the result and the personalized proof. Keep it short.

**Email / form / DM:**

> Subject: caught a lead for {Business} in 45 seconds
>
> Hi {Name} — I filled out your contact form yesterday as a test and didn't hear
> back. That's the gap I help local {niche} businesses close.
>
> I built a quick demo using *your* services: an AI assistant that replies to
> every new lead instantly, qualifies them, and books the job on your calendar —
> 24/7. 90-second video here: {Loom link}
>
> If it's useful, I can have it live on your site this week. Worth a 15-minute
> call? — {Your name}

**Why it works:** it opens with a real observation (their slow form), shows a
tailored working demo (not a slide), and asks for a small next step.

## Step 4 — Follow-up sequence (no reply ≠ no)

- **+3 days:** "Quick follow-up — here's the actual number: if you get ~{X} leads
  a month and lose even a third to slow follow-up, that's ~${Y} walking out the
  door. The demo I sent plugs that. Open to a quick look?"
- **+5 days:** one-liner with a different angle (a 1-line testimonial once you
  have one, or a specific feature: "it also texts you a summary of every lead").
- **+7 days:** soft close — "Should I close the loop on this, or is timing just
  off?"

Stop at 3-4 touches. Move on; revisit in 60 days.

## Step 5 — The call → close

15 minutes. Confirm their lead volume + what a job is worth (fills in the ROI
math), show the demo live, propose the **2-week pilot** ($500-$1k) to de-risk it.
Pilot → setup → retainer.

## Channels, in priority order for cold start

1. **Personalized email / their own contact form** (you're demonstrating the
   exact channel you fix — meta, and it lands).
2. **Instagram/Facebook DM** for visual local businesses (med spas, cleaners).
3. **LinkedIn** for professional services (law, accounting, B2B).
4. **Local FB groups / subreddits** — answer "how do I stop missing leads"
   questions with genuine help, mention you build this. Don't spam; add value.

## Volume + tracking

- 10-20 personalized touches/day. Track in a simple sheet: prospect, channel,
  demo sent, replies, calls, status.
- Target funnel to first cash: ~150-250 quality touches → ~10-20 replies →
  ~3-6 calls → 1-2 pilots/setups. That's your $330-and-then-some.
- The agent makes step 2 fast, which is the only reason this volume is feasible
  solo. That speed is the leverage you said you didn't have.
