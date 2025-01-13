desc_db_system="""
        "Dapat mengakses PostgreSql untuk kebutuhan proses technical",
        "Ensure SQL queries are optimized and avoid unsafe operations like 'DROP' or 'TRUNCATE' unless explicitly allowed.",
        "Selalu gunakan query SIMILAR TO dan lower/upper case  dan lakukan pada setiap column yang ada di table untuk mencari data",
        The following is the metadata description for a detail database columns:

        Tables: users_dt
        Description: Contains information about users and their profiles.
        users_dt: use public.users_dt
        Columns:
        id: Unique identifier for the user.
        first_name: User's first name.
        last_name: User's last name.
        full_name: Full name of the user.
        country: Country where the user is located.
        city: City where the user resides.
        phone_number: User's contact number.
        email: User's email address.
        created_at: Timestamp of when the user was created.
        Relations:
        Foreign Key Relationship:
        Source Table: public.transactions_dt
        Source Column: ref_id_user
        Target Table: public.users_dt
        Target Column: id

        Tables Name: products_ms
        Description: Contains information about product and their descriptions.
        products_ms: use public.products_ms
        Columns:
        id: Unique identifier for the product.
        product_name: name of product
        product_description: description of the product
        formula: formula for calculate premium ex. "object_pertanggungan * rate_premi"
        rate_premi: rate premi for calculate premium ex. "0.07%"
        created_at: Timestamp indicating when the transaction was created.
        Foreign Key Relationship:
        Source Table: public.transactions_dt
        Source Column: ref_id_product
        Target Table: public.products_ms
        Target Column: id

        Tables Name: transactions_dt
        Description: Contains information about detail transactions.
        transactions_dt: use public.transactions_dt
        Columns:
        id: Unique identifier for the transaction.
        ref_id_user: Reference to the user involved in the transaction.
        ref_id_product: Reference to the product insured in the transaction.
        nominal_object_insured: Value of the object being insured.
        premium: Amount of premium paid for the insurance.
        policy_number: Unique identifier for the insurance policy.
        created_at: Timestamp indicating when the transaction was created.
        Foreign Key Relationship:
        Source Table: public.transactions_dt
        Source Column: ref_id_product
        Target Table: public.products_ms
        Target Column: id

        Tables Name: claims_dt
        Description: Contains information about detail claimed policy.
        transactions_dt: use public.claims_dt
        Columns:
        claim_number: Unique identifier for the transaction claim, typically a sequential number or code.
        policy_number: Unique identifier for the insurance policy associated with the claim.
        description: Detailed explanation of the claim, describing the incident or reason for the claim.
        surveyor: Name of the person or agent responsible for assessing the claim.
        status_claim: Numerical representation of the claim status (e.g., 1 for "Proses", 2 for "Selesai", 3 for "Ditolak").
        status_claim_desc: Textual description of the claim status, providing additional context (e.g., "Proses", "Selesai", "Ditolak").
        created_at: Timestamp indicating when the claim was first recorded in the system.
        update_at: Timestamp indicating the last time the claim's details were updated.

        Foreign Key Relationship:
        Source Table: public.claims_dt
        Source Column: policy_number
        Target Table: public.transactions_dt
        Target Column: policy_number
        """