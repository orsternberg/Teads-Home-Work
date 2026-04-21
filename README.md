# Teads-Home-Work

BIA Prioritization Tool

# My Approach
My approach was to move beyond simple spreadsheets by building a weighted scoring engine. Instead of only looking at RTO, I engineered a model that automatically calculates priority based on:

- Technical Constraints: Process Status and RTO.

- Risk Factors: Single Point of Failure (SPOF) and Systemic Dependencies.

- Business Urgency: Time-Criticality markers.

By automating this with Python, I ensured that recovery rankings are objective, repeatable, and scalable—avoiding the human error and subjectivity found in manual BIA assessments.

-----------------------------------------

# AI-Agentic Workflow
To enhance the analysis, I utilized Claude to act as a GRC Analyst. I developed a custom "BIA Analyst Skill" to ensure the AI applies the same GRC standards every time it reads the data.

How I used the AI:

- Skill Setup: I attached a custom skill to the AI, instructing it to prioritize systemic risk (hub dependencies and critical departments) rather than just looking at RTO.

- Data Integration: The agent reads directly from the BIA_-_2026.xlsx - Exersize.csv file attached to this repository.

- Prompt Used: "Hi, based on this skill, read the excel file and Generate a short summary of business impact and Suggest a recovery priority."

Why I did this:

I used an AI agent to perform a qualitative "sanity check" on the data. While my Python script handles the mathematical ranking, the AI agent provides the contextual business impact. This two-layer approach allows me to identify not just what to recover first, but why it matters to the business operations.

-------------------------------------------------

Critique of the Agent’s Approach
While the agent’s approach correctly uses foundational metrics like 'Process Status' and 'RTO', it remains reductive. By failing to integrate 'Time-Criticality,' 'SPOF,' and 'Systemic Dependencies,' the agent treats each process as an isolated entity. My weighted scoring model is superior because it considers the "blast radius" of failures across the entire infrastructure, ensuring that infrastructure fragility is prioritized alongside recovery time.
