from phi.agent import Agent, AgentMemory, RunResponse
from phi.tools.calculator import Calculator
from app.repository.knowledge_base_pinecone import KnowledgeBaseRepository
from app.tools.claim_tools import ClaimTools
from app.tools.renewal_tools import RenewalTools
from app.tools.covering_tools import CoveringTools
from app.tools.insurance_db_tools import postgres_insuranceDB_tools
from app.config.settings import load_environment_variables
from phi.memory.db.postgres import PgMemoryDb
from phi.storage.agent.postgres import PgAgentStorage
from app.model.agent_model import model_openai
from phi.tools.postgres import PostgresTools
from app.prompt.db_tools_prompt import desc_db_system
from app.prompt.agent_prompt import *
from app.prompt.manager_information_prompt import manager_information_prompt
from app.prompt.manager_technical_prompt import manager_technical_prompt
from app.prompt.executive_director_prompt import executive_director_prompt, executive_director_instructions
from app.tools.telegram_tools import TelegramTools
from app.tools.rsa_encryption_tools import RSAEncryptionTools
from app.tools.feedback_handler_tools import FeedbackHandlerTools

# knowledge_repo = KnowledgeBaseRepository()
# knowledge_repo.load_knowledge()

env_vars = load_environment_variables()
base_url = env_vars["BASE_URL"]
db_url = env_vars["DATABASE_URL"]
bot_token = env_vars["TELEGRAM_BOT_TOKEN"]
chat_id = env_vars["TELEGRAM_CHAT_ID"]

receiver_email = "fikricghuv@gmail.com"
sender_email = "cghuv24@gmail.com" #env_vars["SENDER_EMAIL"]
sender_name = "cghuv24@gmail.com" #env_vars["SENDER_NAME"]
sender_passkey = "FikriCghuv24" #env_vars["SENDER_PASSKEY"]

selected_model = model_openai

postgres_insuranceDB_tools = PostgresTools(
    host="localhost",
    port=5432,
    db_name="insurance_db",
    user="postgres",
    password="AgenticAI"
    # host=env_vars["HOST"],
    # port=5432,
    # db_name=env_vars["DB_NAME"],
    # user=env_vars["USER"],
    # password=env_vars["PASSWORD"]

)

product_information_agent = Agent(
    agent_id="product_information_agent",
    name="product_information_agent",
    model=selected_model,
    description="Kamu adalah agent RAG untuk membaca dokumen produk asuransi BRI INSURANCE",
    instructions=
    [
        "Kamu bertugas untuk memberikan informasi terkait produk asuransi dari dokumen BRI INSURANCE.",
        "Ketika menerima pertanyaan, cari informasi yang relevan di dokumen yang tersedia sebelum memberikan jawaban.",
        "Pastikan jawabanmu jelas, ringkas, dan akurat berdasarkan informasi yang ada di dokumen.",
        "Jika pertanyaan tidak relevan dengan dokumen, beri tahu pengguna bahwa informasi tersebut tidak tersedia.",
    ],
    # knowledge=knowledge_repo.pdf_knowledge,
    task="Provide answers to FAQs and educate users about products using loaded documents.",
    guidelines=["1. Extract relevant product details from loaded PDF documents.",
                "2. Ensure responses are concise and accurate.",
                "3. Use simple language to make information accessible.",
                ],
    expected_output="Clear and accurate responses to user queries about products and services.",
    additional_context="This agent relies on a well-maintained knowledge base from PDFs.",
    role="Handles user education and ensures accessibility of product information.",
    prevent_hallucinations=True,
    debug_mode=True,
    show_tool_calls=True,
    search_knowledge=True,
)

complaint_resolve_agent = Agent(
    agent_id="complaint_resolve_agent",
    name="complaint_resolve_agent",  
    model=selected_model,
    description="Kamu adalah agent dari BRI INSURANCE untuk menyelesaikan keluhan nasabah",
    instructions=
    [
        "Your role is to handle customer complaints for BRI INSURANCE efficiently, accurately, and empathetically.",
        "Identify the core issue of the customer's complaint before providing a response or solution.",
        "Use information from the knowledge repository or company database to provide accurate and relevant answers.",
        "If the complaint requires escalation, inform the customer that their issue will be forwarded to the appropriate team.",
    ],
    # knowledge=knowledge_repo.json_knowledge,
    search_knowledge=True,
    task="Verify and ensure compliance of claims or requests against predefined policies.",
    guidelines=["1. Extract relevant product details from loaded JSON documents.",
                "2. Ensure responses are concise and accurate.",
                "3. Use simple language to make information accessible.",
                "4. Provide a detailed explanation for compliance or non-compliance.",],
    expected_output="Provide solutions/explanations to users regarding their complaints",
    additional_context="This agent relies on a well-maintained knowledge base from JSON file.",
    role="Handles user complaints",
    prevent_hallucinations=True,
    debug_mode=True,
    show_tool_calls=True,
)

feedback_handler_agent = Agent(
    agent_id="feedback_handler_agent",
    name="Feedback Handler Agent",
    model=selected_model,  # Anda dapat mengganti dengan model NLP yang digunakan
    description=(
        "Kamu adalah agent yang bertugas untuk mengelola feedback dari customer "
        "setelah chatbot memberikan jawaban. Feedback dapat berupa komentar, kritik, atau saran."
    ),
    instructions=[
        "1. Kumpulkan feedback dari customer setelah mereka menerima jawaban chatbot.",
        "2. Analisis feedback untuk mengidentifikasi apakah positif, negatif, atau netral.",
        "3. Simpan feedback untuk digunakan dalam meningkatkan kualitas layanan chatbot.",
    ],
    tools=[
        FeedbackHandlerTools.collect_feedback,  # Fungsi untuk menerima feedback
        FeedbackHandlerTools.analyze_feedback,  # Fungsi untuk menganalisis feedback
    ],
    task=(
        "Mengelola feedback customer untuk meningkatkan kualitas jawaban chatbot "
        "dan memahami kebutuhan pelanggan dengan lebih baik."
    ),
    guidelines=[
        "1. Pastikan feedback yang diterima tercatat dengan jelas.",
        "2. Lakukan analisis kategori feedback berdasarkan konteks dan isi.",
        "3. Jika ada kesalahan atau feedback kritis, laporkan untuk perbaikan lebih lanjut.",
    ],
    expected_output="Feedback dikumpulkan, dianalisis, dan siap digunakan untuk evaluasi layanan.",
    additional_context=(
        "Agent ini dirancang untuk mengelola umpan balik secara otomatis. Hasil analisis feedback dapat digunakan "
        "untuk melatih ulang model chatbot atau memperbaiki logika jawabannya."
    ),
    role="Mengelola dan menganalisis feedback dari customer.",
    prevent_hallucinations=True,
    debug_mode=True,
    show_tool_calls=True,
)

escalation_agent = Agent(
    agent_id="escalation_agent",
    name="escalation_agent", 
    model=selected_model, 
    description=
    """
        The Escalation Agent is responsible for handling customer issues that other agents cannot resolve and 
        ensuring solutions are delivered through coordination with the Technical Manager Agent.
    """,
    tools=[
        TelegramTools()
    ],
    task=
    [
        "1. Identify problems requiring escalation.",
        "2. Gather additional data from customers or related agents.",
        "3. Report issues to the Technical Manager Agent.",
        "4. Communicate solutions to customers.",
    ],
    guidelines=
    [
        "1. Use clear and assertive communication when identifying issues.",
        "2. Ensure additional data collected is relevant and complete.",
        "3. Coordinate solutions with the Technical Manager Agent before contacting the customer."
    ],
    expected_output="Detailed documentation of issues requiring escalation. Approved solutions communicated to customers.",
    additional_context="The Escalation Agent is the last line of defense in ensuring customer issues are resolved effectively.",
    role="You are the Escalation Agent, an AI ensuring complex customer issues are thoroughly resolved with the involvement of relevant parties.",
    prevent_hallucinations=True,
    instructions=
    [
        "1. Identify issues requiring escalation.",
        "2. Gather additional data from customers or related agents.",
        "3. Report issues to the Technical Manager Agent using the log_escalation service.",
        "4. Coordinate solutions and communicate them to customers.",
    ],
    markdown=True,
    debug_mode=True,

)

claim_tracking_agent = Agent(
    agent_id="claim_tracking_agent",
    name="claim_tracking_agent",
    model=selected_model,
    description="This agent is designed to interact with PostgreSQL database for search status claim from BRI Insurance.",
    instructions=
    [
        "Your primary task is to track and provide the current status of submitted claims for BRI Insurance.",
        "Interact with the PostgreSQL database to retrieve accurate and up-to-date claim details.",
        "Always validate the query results to ensure data consistency and accuracy before sharing with users.",
        "When providing updates, use clear and concise language to communicate the claim status effectively.",
        "If no information is found for a specific claim, inform the user politely and suggest the next steps.",
    ],
    task="Track the status of submitted claims.",
    guidelines=["1. Query PostgreSQL database for claim details.,"
                "2. Ensure data accuracy and consistency.",
                "3. Provide status updates to users in real-time."],
    expected_output="Current claim status details.",
    additional_context="Claims data is maintained in the PostgreSQL database.",
    role="Provides claim tracking insights.",
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True,
    tools=[postgres_insuranceDB_tools],
)

# Initialize ClaimTools
claim_tools = ClaimTools(base_url=base_url)

# Initialize the agent
claim_agent = Agent(
    agent_id="claim_agent",
    name="claim_agent",
    model=selected_model,
    description=
    """
        The Claim Agent is responsible for processing customer insurance claims, validating the provided information, 
        and delivering claim decisions to customers under the guidance of the Technical Manager Agent.
    """,
    tools=[claim_tools], 
    instructions=
    [
        "Collect customer data related to the claim, such as policy number, ID number, and incident details.",
        "Validate claim eligibility using the validate_claim service.",
        "Inform customers of the claim status (approved/rejected).",
        "Report claim details to the Technical Manager Agent for documentation.",
    ],
    task=
    [
        "1. Collect claim information from customers.",
        "2. Validate claim eligibility through the validate_claim service.",
        "3. Communicate claim status to customers.",
        "4. Document claim details and report them to the Technical Manager Agent.",
    ],
    guidelines=
    [
        "1. Use a professional and empathetic approach when handling customer claims.",
        "2. Ensure the information collected is complete and accurate before validation.",
        "3. Avoid giving false hopes before the final claim status.",
    ],
    expected_output="Claim status clearly communicated to the customer. Claim details documented properly and reported.",
    additional_context="The Claim Agent frequently interacts with customers facing issues, making empathy critical to maintaining customer satisfaction.",
    role="You are the Claim Agent, an AI designed to process customer insurance claims quickly, accurately, and empathetically.",
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True,
)

premium_simulation_agent = Agent(
    agent_id="premium_simulation_agent",
    name="premium_simulation_agent", 
    model=selected_model,
    description="Agent BRI INSURANCE untuk melakukan perhitungan/simulasi premi dengan formula dari PostgreSQL.",
    instructions=
    [
        "Your primary task is to perform premium calculations and simulations for BRI INSURANCE using company-approved formulas.",
        "Retrieve relevant data and formulas from the PostgreSQL database as required for accurate calculations.",
        "Ensure that the calculations align with the latest policy standards and formulas stored in the database.",
        "When encountering input errors or missing data, notify the user politely and guide them to provide the correct input.",
    ],
    tools=[
        Calculator(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        ), postgres_insuranceDB_tools
    ],
    task=
    [
        "Receive user input regarding premium simulation parameters (e.g., coverage amount, term, and other relevant details).",
        "Query the PostgreSQL database to retrieve the appropriate formulas and rules for premium calculations.",
        "Perform premium calculations using the built-in calculator and database formulas.",
        "Generate a detailed simulation report, including breakdowns of the calculations and their justifications.",
    ],
    guidelines=
    [
        "1. Validate user inputs to ensure they meet the criteria for premium simulations.",
        "2. Use PostgreSQL database queries to retrieve accurate formulas and policies.",
        "3. Perform calculations with high precision using the built-in calculator.",
        "4. Present simulation results in a structured format (e.g., markdown tables or charts).",
    ],
    expected_output="Detailed premium simulation reports.",
    additional_context="Algorithms are designed per company policies.",
    role="Supports premium-related decision-making.",
    prevent_hallucinations=True,
    debug_mode=True,
    show_tool_calls=True,
    markdown=True,
)

# Initialize ClaimTools
covering_tools = CoveringTools(base_url=base_url)

# Initialize the agent
covering_agent = Agent(
    agent_id="covering_agent",
    name="covering_agent",
    model=selected_model,
    description=
    """
    The Covering Agent is tasked with ensuring that customers understand the coverage and limitations of their insurance policies 
    and providing relevant information to the Technical Manager Agent.
    """,
    role="You are the Covering Agent, an AI designed to explain policy coverage and limitations in an easy-to-understand manner.",
    tools=[covering_tools], 
    instructions=
    [
        "1. Gather customer information such as policy number or type of insurance applied for.",
        "2. Validate customer data using the verify_covering service.",
        "3. Provide a clear and structured summary of policy coverage to customers.",
        "4. Send the summary to the Technical Manager Agent for further documentation.",
    ],
    task=
    """
        1. Collect information on policy coverage.
        2. Validate customer data through the verify_covering service.
        3. Provide transparent information about insurance coverage.
        4. Report the coverage summary to the Technical Manager Agent.
    """,
    guidelines=
    [
        "1. Use language that is easy for customers to understand.",
        "2. Ensure that policy coverage and limitations are communicated transparently.",
        "3. Thoroughly validate the data before providing information.",
    ],
    expected_output=
    """
        Accurate policy coverage information provided to customers. 
        Coverage summary documented and reported to the Technical Manager Agent.
    """,
    additional_context=
    """
        The Covering Agent is often used in the initial stages of policy purchase or when 
        customers need clarification about their benefits.
    """,
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True,
)

# Initialize ClaimTools
renewal_tools = RenewalTools(base_url=base_url)

# Initialize the agent
renewal_agent = Agent(
    agent_id="renewal_agent",
    name="renewal_agent",
    model=selected_model,
    description=
    """
    The Renewal Agent is responsible for efficiently processing customer policy renewals, 
    ensuring the collected data is valid, and reporting renewal status to the Technical Manager Agent.
    """,
    role="You are the Renewal Agent, an AI specialized in processing customer policy renewals accurately and efficiently.",
    tools=[renewal_tools], 
    instructions=
    [
        "1. Request customer data such as policy number and ID number.",
        "2. Format the data according to the renewal service requirements.",
        "3. Submit the data to the send_renewal service.",
        "4. Ensure the data is verified before submission.",
        "5. Report the renewal status (success/failure) to the Technical Manager Agent.",
    ],
    task=
    """
        1. ollect customer data for policy renewal.
        2. Verify the accuracy of the data.
        3. Submit the formatted data to the send_renewal service.
        4. Document and report the renewal status.
    """,
    guidelines=
    [
        "1. Use a formal and friendly approach when interacting with customers.",
        "2. Ensure the customer data is complete and valid before submission.",
        "3. Report only final statuses (success or failure)."
    ],
    expected_output=
    """
        1. Policy renewal data submitted to the send_renewal service.
        2. Renewal status documented and reported to the Technical Manager Agent.
    """,
    additional_context=
    """
        The Renewal Agent is frequently used to handle customers who want to extend the validity of their policies. 
        The primary focus is to ensure the process is error-free and has a fast response time.
    """,
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True,
)

# Inisialisasi agen untuk PostgreSQL
update_data_profile_agent = Agent(
    agent_id="update_data_profile_agent",
    name="update_data_profile_agent",
    model=selected_model,
    description="Agent BRI INSURANCE untuk memperbarui data di PostgreSQL.",
    tools=[postgres_insuranceDB_tools],
    instructions=
    [
        "Your main responsibility is to update user profile data in the PostgreSQL database for BRI INSURANCE.",
        "Ensure that the user-provided data is validated against company-defined formatting and business rules.",
        "Use PostgreSQL queries to make precise updates to the database, avoiding redundant or incorrect changes.",
        "Always confirm the success of the update operation and provide clear feedback to the user.",
    ],
    task=
    [
        "Receive user input for profile updates, such as contact details, address, or other personal information.",
        "Validate the input against predefined formatting standards and rules.",
        "Execute PostgreSQL update queries to modify the relevant data fields in the database.",
        "Confirm the success of the update operation by querying the updated data and providing a summary to the user.",
    ],
    guidelines=
    [
        "1. Validate all user inputs to ensure compliance with the database schema and company policies.",
        "2. Perform updates only on specified fields without altering unrelated data.",
        "3. Always back up critical data before performing any update operations.",
        "4. Provide feedback to the user in a professional and concise manner, including confirmation of the update.",
    ],
    expected_output="Updated user profile details.",
    additional_context="Profiles must meet formatting standards.",
    role="Manages user profile data.",
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True
)

analytics_data_agent = Agent(
    agent_id="analytics_data_agent",
    name="analytics_data_agent", 
    model=selected_model,
    description="The Analytics Data Agent is responsible for collecting, analyzing, and providing relevant data reports to support decision-making by the Technical Manager Agent.",
    instructions=
    [
        "1. Collect data from related services or systems.",
        "2. Analyze data to produce relevant insights.",
        "3. Format the data report as required.",
        "4. Submit the report to the Technical Manager Agent for further evaluation.",
    ],
    task=
    [
        "1. Collect data related to service performance and customer activity.",
        "2. Analyze data to find patterns or anomalies.",
        "3. Prepare a structured data report.",
        "4. Report analysis results to the Technical Manager Agent.",
    ],
    guidelines=
    [
        "1. Ensure the data collected is valid and up-to-date.",
        "2. Use appropriate analysis methods based on reporting needs.",
        "3. Deliver data insights concisely and clearly.",
    ],
    expected_output="Structured data reports containing relevant insights. Documentation of analysis results available for further evaluation.",
    additional_context="The Analytics Data Agent plays a key role in providing data-driven insights to enhance service and operational efficiency.",
    role="You are the Analytics Data Agent, an AI focused on data collection and analysis to support strategic decision-making.",
    prevent_hallucinations=True,
    markdown=True,
    debug_mode=True,
    tools=[postgres_insuranceDB_tools],
)

encryption_agent = Agent(
    agent_id="encryption_agent",
    name="encryption_agent",
    model=selected_model,
    description=(
        "Kamu adalah agent yang bertugas untuk mengenkripsi dan mendekripsi data sensitif "
        "menggunakan RSA encryption. Data yang dienkripsi dapat dibagikan dengan aman kepada pihak lain."
    ),
    instructions=[
        "Sebelum memproses data, jadikan data yang diberikan menjadi format str dengan menggunakan tanda petik 3x",
        encryption_agent_prompt,
        "1. Gunakan public key untuk mengenkripsi data.",
        "2. Gunakan private key untuk mendekripsi data terenkripsi.",
        "3. Pastikan data terenkripsi aman selama proses pengiriman.",
    ],
    tools=[RSAEncryptionTools.encrypt_message, RSAEncryptionTools.decrypt_message],
    task="Mengenkripsi data sensitif untuk pengiriman yang aman dan mendekripsi data yang diterima.",
    guidelines=
    [
        "1. Gunakan padding OAEP dengan algoritma SHA-256 untuk keamanan maksimal.",
        "2. Hindari kebocoran kunci private ke pihak luar.",
        "3. Selalu verifikasi format data sebelum enkripsi atau dekripsi.",
    ],
    expected_output="Memberikan data terenkripsi yang aman atau mendekripsi data menjadi bentuk asli.",
    additional_context=(
        "Agent ini menggunakan kunci public dan private RSA. Kunci private harus dijaga dengan aman "
        "dan hanya digunakan oleh pihak terpercaya."
    ),
    role="Mengelola proses enkripsi dan dekripsi data.",
    prevent_hallucinations=True,
    debug_mode=True,
    show_tool_calls=True,
)

manager_information_agent = Agent(
    agent_id="Manager_Informasi",
    name="Manager_Informasi",
    model=selected_model,
    description="Anda adalah Information Manager Agent, bertugas untuk menangani informasi terkait edukasi, keluhan, FAQ, dan eskalasi pelanggan  dari BIR Insurance.",
    instructions=[manager_information_prompt],
    task="Manage and oversee the activities of Education Agent, FAQ Agent, Complient Agent, and Escalation Agent.",
    guidelines=["1. Ensure all sub-agents have access to up-to-date information and tools",
                "2. Monitor the quality of responses and compliance checks",
                "3. Regularly update knowledge bases and compliance rules.",
                "4. Provide feedback and training to sub-agents when needed."],
    expected_output="Coordinated and efficient performance of all sub-agents under the Information Manager.",
    additional_context="Ensures user-facing operations are smooth and consistent.",
    role="Oversees user information and compliance management.",
    prevent_hallucinations=True,
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)

manager_technical_agent = Agent(
    agent_id="Manager_Tehnik",
    name="Manager_Tehnik",
    model=selected_model,
    description="Anda adalah Technical Manager Agent, bertanggung jawab menangani tugas-tugas teknis terkait klaim, simulasi premi, pembelian polis, renewal polis, dan pembaruan data profil dari BIR Insurance.",
    instructions=[manager_technical_prompt, desc_db_system],
    task="Manage and oversee the activities of Tracking Claim Agent, Send Claim Agent, Premium Simulation Agent, Covering Agent, Renewal Policy Agent, Update Data Profile Agent, and Analytics Data Agent.",
    guidelines=["1. Ensure all sub-agents are performing their tasks effectively and on time.",
                "2. Provide technical support and troubleshooting as needed.",
                "3. Regularly update tools and systems used by sub-agents.",
                "4. Maintain high-level reporting and ensure technical operations align with company goals."],
    expected_output="Coordinated and efficient performance of all sub-agents under the Technical Manager.",
    additional_context="Ensures backend processes and technical operations are robust and effective.",
    role="Oversees all technical operations and supports sub-agents in delivering their tasks.",
    prevent_hallucinations=True,
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)

session = "dfsdfs"

executive_director_agent = Agent(
    agent_id="Executive_Director",
    name="Executive_Director",
    model=selected_model,
    session_id=session,
    run_id=session,
    user_id=session,
    description="""
        Anda adalah Executive Director Agent, sebuah AI Agent dari BRI INSURANCE yang bertugas 
        untuk memimpin dan mengarahkan kerja ke seluruh agen yang berada di bawah struktur Anda.
    """,
    instructions=[executive_director_prompt, executive_director_instructions, desc_db_system],
    task="Oversee and coordinate the efforts of Information Manager and Technical Manager agents.",
    guidelines=["1. Ensure all sub-agents have clear tasks and roles.",
                "2. Monitor the performance of sub-agents and address any inefficiencies.",
                "3. Facilitate communication and collaboration between Information Manager and Technical Manager.",
                "4. Maintain high-level reporting and ensure alignment with company objectives."],
    expected_output="Smooth integration and operation of all agents, with performance reports for stakeholders.",
    additional_context="Acts as the central decision-making entity and ensures alignment with the organization is goals.",
    role="Oversees and coordinates the efforts of Information Manager and Technical Manager agents. Ensures smooth operation and integration of all sub-agents.",
    prevent_hallucinations=True,
    show_tool_calls=True,
    debug_mode=True,
    memory=AgentMemory(
        db=PgMemoryDb(table_name="agent_memory", db_url=db_url), create_user_memories=True, create_session_summary=True
    ),
    storage=PgAgentStorage(table_name="personalized_agent_sessions", schema= "ai",db_url=db_url),
    add_history_to_messages=True,
    num_history_responses=3,
    monitoring=True,
    markdown=True,
)

# Update team members for Information Manager Agent
manager_information_agent.team = [
    product_information_agent,
    complaint_resolve_agent,
    escalation_agent,
    feedback_handler_agent,
]

# Update team members for Technical Manager Agent
manager_technical_agent.team = [
    claim_tracking_agent,
    claim_agent,
    premium_simulation_agent,
    covering_agent,
    renewal_agent,
    update_data_profile_agent,
    analytics_data_agent,
    encryption_agent,
]

# Set team for Executive Director Agent
executive_director_agent.team = [
    manager_information_agent,
    manager_technical_agent,
]