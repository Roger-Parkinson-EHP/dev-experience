License Corporation
AI Policy [v 1.0]

│ Page 1

LICENSE CORPORATION

POLICY FOR USE OF ARTIFICIAL INTELLIGENCE IN
SOFTWARE DEVELOPMENT

Effective Date: August 14, 2025
Version: 1.0

*

1.  PURPOSE

The purpose of this policy is to establish expectations and guidelines for the appropriate use of
artificial intelligence (AI) in software development activities at License Corporation, including the
use  of  Generative  AI  (GAI)  tools.  This  policy  aims  to  ensure  that  AI  technology  is  deployed
responsibly and is used in a lawful and ethical manner to enhance productivity, efficiency, and
decision-making while complying with applicable law and respecting privacy, confidentiality, and
data security.

This policy applies to all employees, independent contractors, consultants, and third-party vendors
who  develop,  review,  or  maintain  code  for  License  Corporation  (collectively,  “Personnel”).  It
covers  all  AI  technologies  used  in  software  development,  including  Large  Language  Models,
machine learning systems, and AI-powered development tools.

2.  CONTRACTUAL OBLIGATIONS AND COMPLIANCE

Personnel  are  reminded  that  their  use  of  AI  tools  must  comply  with  their  existing  contractual
obligations to License Corporation. Employees are bound by the Confidentiality and Proprietary
Rights  provisions  set  forth  in  Section  9  of  the  Employment  Agreement,  which  prohibits  the
disclosure  of  Confidential  Information  to  third  parties.  Independent  Contractors  are  similarly
bound  by  the  Confidential  Information  provisions  in  Section  8  of  the  Independent  Contractor
Agreement, which requires protection of all Confidential Information and Work Product.

The unauthorized input of Company materials, code, or information into AI platforms constitutes
a  breach  of  these  contractual  obligations.  Personnel  should  note  that  under  the  Inventions
provisions  (Section  10  of  the  Employment  Agreement  and  Section  11  of  the  Independent
Contractor Agreement), any work product created during engagement with License Corporation
belongs  exclusively  to  the  Company.  However,  code  generated  primarily  by  AI  tools  may  not
qualify for intellectual property protection, potentially jeopardizing our competitive advantage.

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354
License Corporation
AI Policy [v 1.0]

3.  DEFINITIONS

│ Page 2

For  purposes  of  this  policy,  “Generative  AI”  or  “GAI”  refers  to  artificial  intelligence  systems
capable of creating new content, such as code, based on the data they have been trained on. These
systems use machine learning algorithms to analyze existing data and generate novel outputs in
response to user prompts.

“Vibe Coding” refers to the practice of developing software entirely through AI prompts without
understanding, reviewing, or manually writing code. This practice involves delegating cognitive
responsibility  to  AI  systems  and  accepting  their  output  without  critical  evaluation  or
comprehension.

“AI-Powered IDE” means any Integrated  Development Environment that incorporates  artificial
intelligence features for code suggestion, completion, or generation.

4.  GENERAL PRINCIPLES

License  Corporation  recognizes  that  AI  tools  can  provide  valuable  assistance  in  software
development when used appropriately. However, we are dedicated to upholding ethical standards
and protecting our intellectual property  rights. Personnel must ensure that their use of AI tools
respects fundamental principles of code quality, security, and confidentiality.

The Company believes in transparency regarding AI usage. Personnel must be able to explain and
understand all code they submit, regardless of whether AI tools assisted in its creation. We actively
seek to prevent the introduction of vulnerabilities, inefficiencies, or legal liabilities that may arise
from uncritical acceptance of AI-generated code.

5.  APPROVED AI TOOLS AND CONFIGURATION

Personnel may only use AI tools that have been explicitly approved by the Company. The current
list of approved platforms includes OpenAI (ChatGPT, GPT-4), Google Gemini, and Perplexity
AI.  These  platforms  may  be  used  subject  to  proper  configuration  and  within  the  constraints
outlined in this policy.

Before using any approved AI tool, Personnel must disable all settings that allow the platform to
train on user data. This includes turning off options such as “Improve the model for everyone” or
similar data collection features. Personnel must use only Company email addresses when creating
accounts for approved AI platforms and must never use personal accounts for work-related queries.

The following AI-powered  IDEs  are strictly prohibited: Windsurf, Trae (trae.ai), and  any other
“vibe-coding” IDEs that expose code repositories to AI services or enable writing entire features

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354
License Corporation
AI Policy [v 1.0]

│ Page 3

through AI. Trae presents particular security concerns due to its connection to ByteDance, creating
risks of international data exposure.

Cursor is the only AI-powered IDE approved for use, subject to the requirement that AI assistance
must remain at or under 50% per task. Traditional IDEs such as VS Code and Xcode are approved
without restriction. AI assistant plugins integrated into traditional IDEs (such as GitHub Copilot
in VS Code) are permitted, as these maintain appropriate boundaries between AI assistance and
human code ownership. The distinction is that AI-powered IDEs facilitate complete delegation of
coding  tasks,  while  integrated  assistants  in  traditional  IDEs  maintain  developer  control  and
ownership.

6.  PROHIBITED PRACTICES

The practice of Vibe Coding is strictly prohibited. Personnel must not generate entire functions,
modules, or significant code blocks through AI prompts without understanding and substantially
modifying the output. This prohibition extends to submitting any code that the developer cannot
explain in detail or debug independently.

Personnel  are  prohibited  from  inputting  any  Confidential  Information,  as  defined  in  their
respective agreements, into AI platforms. This includes but is not limited to complete source code
files, system architecture details, database schemas, API implementations, proprietary algorithms,
client configurations, or any information related to our white label partnerships. Even abstracting
or modifying such information before input does not make this practice acceptable.

The exposure of any information that  could be  considered  a trade secret  under the  Company’s
agreements immediately destroys its protected status and may subject the individual to personal
liability under the indemnification provisions of their agreement.

7.  ACCEPTABLE USE GUIDELINES

AI assistance must not exceed fifty percent (50%) per task. This means that for any given feature,
function,  or  code  component,  Personnel  must  write  or  substantially  modify  at  least  half  of  the
implementation. AI should serve as a tool to enhance productivity, not as a replacement for human
expertise and judgment. The use of AI to write entire features is strictly prohibited as it eliminates
code ownership and accountability.

Appropriate  uses  of  AI  include  seeking  syntax  assistance  for  common  programming  patterns,
researching  documentation  for  publicly  available  libraries,  understanding  error  messages,
generating small utility functions of ten lines or fewer, and learning new programming concepts.
Personnel may use AI to help refactor code they have personally written, provided they understand
and can explain all changes.

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354
License Corporation
AI Policy [v 1.0]

│ Page 4

When  using  AI  tools,  Personnel  should  formulate  specific,  narrow  queries  that  do  not  reveal
proprietary  information.  Queries  should  focus  on  general  programming  concepts  and  publicly
available information. Personnel must never paste entire files, large code blocks, or any code that
reveals our business logic or architectural decisions.

8.  CODE QUALITY AND REVIEW REQUIREMENTS

All code, whether AI-assisted or not, must meet License Corporation’s quality standards. Before
submitting any code, Personnel must thoroughly review every line for accuracy, efficiency, and
security. They must test all functionality, ensure no AI-specific artifacts or comments remain, and
verify compliance with company coding standards.

Personnel must be prepared to explain any portion of their code during review. The inability to
explain code implementation details will be considered evidence of Vibe Coding and may result
in disciplinary action. Code reviewers are instructed to flag suspicious patterns that may indicate
excessive AI reliance.

9.  MONITORING AND ENFORCEMENT

License Corporation reserves the right to monitor the use of AI tools to ensure compliance with
this policy. This monitoring may include reviewing code contributions for AI artifacts, auditing
development practices, and examining account activity on approved AI platforms. The Company
maintains the right to blacklist any software deemed to pose security risks.

Violations of this policy will be addressed through progressive discipline. First offenses will result
in written warnings and mandatory retraining. Second offenses will lead to suspension and final
warnings. Third offenses or severe violations will result in termination of employment or contract.
Personnel  who  cannot  comply  with  these  restrictions  will  not  be  permitted  to  participate  in
development cycles.

Severe violations include any action that exposes trade secrets, Confidential Information, client
data, or system architecture to AI platforms. Such violations will result in immediate termination
and may trigger legal action for breach of confidentiality. Personnel may be held personally liable
for damages under the indemnification provisions of their agreements. The use of prohibited tools,
particularly those with foreign ownership that could compromise data sovereignty, constitutes a
severe violation.

10.  INTELLECTUAL PROPERTY CONSIDERATIONS

Personnel  must  understand  that  code  generated  primarily  by  AI  tools  may  not  be  eligible  for
copyright  protection  and  could  inadvertently  incorporate  others’  intellectual  property.  This

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354
License Corporation
AI Policy [v 1.0]

│ Page 5

uncertainty  could  compromise  License  Corporation’s  ability  to  protect  its  software  assets  and
maintain its competitive advantage.

All work product, regardless of AI assistance levels, remains the exclusive property of License
Corporation  under  the  Work  Product  and  Inventions  provisions  of  Personnel  agreements.
However, the Company’s ability to enforce these rights may be compromised if the work product
is substantially AI-generated.

11.  REPORTING AND COMPLIANCE

Personnel  have  an  affirmative  obligation  to  report  any  accidental  exposure  of  Confidential
Information to AI platforms, suspected policy violations by others, or any circumstances where AI
tools  generate  concerning  or  unexpected  outputs.  Reports  should  be  submitted  immediately  to
legal@licensecorporation.com

Personnel must complete mandatory AI security training before using any approved AI tools and
must attend quarterly updates on best practices. Annual certification and policy acknowledgment
are required for continued access to AI tools.

12.  AMENDMENTS

AI technology and applicable laws are rapidly evolving. This policy may be amended from time
to time to address technological changes, emerging threats, or legal requirements. The Company
will  provide  notice  of  material  changes,  and  continued  use  of  AI  tools  following  such  notice
constitutes acceptance of the amended policy.

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354

License Corporation
AI Policy [v 1.0]

│ Page 6

ACKNOWLEDGMENT

I acknowledge that I have received and read License Corporation’s Policy for Use of Artificial
Intelligence in Software Development. I understand and agree to abide by its terms. I acknowledge
that violation of this policy may constitute a breach of my Employment Agreement or Independent
Contractor Agreement and may result in termination and legal action.

I understand that this policy supplements but does not replace my obligations under my existing
agreements with License Corporation, including all provisions related to Confidential Information,
Work Product, and Inventions.

Signature: ______________________________

Name: _________________________________

Title: __________________________________

Date: __________________________________

Docusign Envelope ID: 231875A1-E60F-4ECD-917B-7058DFAF3354Roger Parkinson12/22/2025Consultant

