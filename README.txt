Product Requirements Document (PRD): Ramsey
1. Overview
Ramsey is a smart, WhatsApp-based grocery shopping assistant that simplifies online shopping by combining natural language interaction, AI-powered product suggestions, and direct integration with supermarket carts. The MVP will target users in Israel and integrate with Shufersal, Israel’s largest grocery chain.

2. Problem Statement
Online grocery platforms are often clunky, slow, and unintuitive for users who just want to “get their list done.” Ramsey offers a frictionless alternative: users interact via WhatsApp to build their list, see AI-optimized selections, customize, and submit to checkout—all in a few clicks.

3. Target Audience
Busy individuals who shop weekly online

People frustrated with existing grocery site UX

Users seeking price-conscious but reliable recommendations

Users comfortable with WhatsApp and mobile-first experiences

4. Key Features (MVP)
🟢 WhatsApp Bot
Natural language commands:

“Add milk”

“Remove toothpaste”

“Show my list”

Trigger LLM generation with phrases like “I’m ready” or “Create my order”

Language: Hebrew + English

🧠 LLM Product List Generator (Gemini)
Interprets the user’s shopping list

Matches each item with the most fitting product at Shufersal

Uses memory from previous orders for personalization

If tie between items → select the cheapest

🔍 Smart Scraper / Browser Automation
Headless browser or scraping tool (e.g., Playwright, Selenium)

Navigates Shufersal site and finds real-time product matches

Supports memory via DB to avoid re-scraping known products

🖥️ Dynamic Web UI (React)
Mobile-first experience

Opens via a magic link sent on WhatsApp

Lets user:

Review LLM selections

View price, image, brand, and future metadata

Swap items for similar/cheaper alternatives

Submit order

🛒 Cart Finalization
When user confirms, generate a Shufersal checkout link with pre-filled cart

5. Architecture Overview
Frontend: React (hosted on Vercel or similar)

Backend: Python (FastAPI or Flask)

Scraper: Python w/ Playwright or Selenium (headless mode)

LLM Integration: Gemini API

WhatsApp: WhatsApp Business API (Twilio or direct)

Database: PostgreSQL or Firebase (storing lists, phone numbers, history, and product mappings)

Hosting: Cloud-based (AWS/Azure)

6. User Flow
User opens WhatsApp and starts chatting with Ramsey

Adds/removes items from shopping list in natural language

When ready → says “I’m done” / “Create my order”

LLM maps items to real products using scraper/browser automation

A link to a dynamic web UI is sent via WhatsApp

User reviews + edits list

Clicks “Submit”

Gets redirected to Shufersal checkout page with cart pre-filled

7. Monetization Plan
Model: Token-based or Subscription (TBD in MVP)

Entry Plan:

First 1-3 orders free

Invite-based referral system for free tokens

Optionally explore B2B partnerships with supermarkets post-MVP

8. Language Support
Hebrew & English toggle

Default based on WhatsApp device language

9. Metrics for Success (MVP)
🛒 % of users who successfully reach cart checkout

🕒 Average time from first message → completed order

💬 Engagement rate (messages per session)

💰 Token usage and conversion rate

📈 Retention after 1st order

10. Risks & Open Questions
Risk / Unknown	Mitigation
Anti-scraping measures from Shufersal	Use rotating proxies and delay-based scraping
WhatsApp approval time for Business API	Use Twilio or fallback chatbot for MVP
Cart pre-fill structure changes	Build scraper to auto-adapt and detect structure shifts
Gemini cost/API limitations	Add caching + lightweight fallback model
Need for login?	Use phone number only + temporary session tokens

11. Future Roadmap (Post-MVP)
Multi-supermarket support (Rami Levi, Victory)

Smart budget constraints (“Stay under 300₪”)

Auto-predict items you forgot (e.g. milk, eggs)

Scheduled recurring lists

Payments within the UI