def detect_intent(text):

    if not text:
        return "Unknown Intent"

    text_lower = text.lower()

    # ---------------------------------------------
    # SCHOLARSHIP / EDUCATIONAL APPLICATION
    # ---------------------------------------------

    scholarship_keywords = [
        "scholarship",
        "student scholarship",
        "financial assistance",
        "financial aid",
        "fee concession",
        "educational assistance",
        "income certificate",
        "student application"
    ]

    education_keywords = [
        "university",
        "college",
        "course",
        "student",
        "semester",
        "admission",
        "academic",
        "marks",
        "percentage",
        "degree",
        "master of arts",
        "bachelor",
        "cbse",
        "education"
    ]

    scholarship_score = sum(
        1
        for keyword in scholarship_keywords
        if keyword in text_lower
    )

    education_score = sum(
        1
        for keyword in education_keywords
        if keyword in text_lower
    )

    # If scholarship-specific terms exist
    if scholarship_score >= 1:
        return "Scholarship Application"

    # If several educational indicators exist
    if education_score >= 3:
        return "Educational Application"

    # ---------------------------------------------
    # PASSPORT
    # ---------------------------------------------

    passport_keywords = [
        "passport",
        "passport application",
        "passport renewal"
    ]

    if any(
        keyword in text_lower
        for keyword in passport_keywords
    ):
        return "Passport Application"

    # ---------------------------------------------
    # DRIVING LICENSE
    # ---------------------------------------------

    driving_keywords = [
        "driving licence",
        "driving license",
        "learner licence",
        "learner license",
        "rto"
    ]

    if any(
        keyword in text_lower
        for keyword in driving_keywords
    ):
        return "Driving License"

    # ---------------------------------------------
    # AADHAAR
    # ---------------------------------------------

    aadhaar_keywords = [
        "aadhaar",
        "aadhar",
        "uidai"
    ]

    if any(
        keyword in text_lower
        for keyword in aadhaar_keywords
    ):
        return "Aadhaar Update"

    # ---------------------------------------------
    # VOTER ID
    # ---------------------------------------------

    voter_keywords = [
        "voter id",
        "voter identity",
        "election commission",
        "elector"
    ]

    if any(
        keyword in text_lower
        for keyword in voter_keywords
    ):
        return "Voter ID"

    # ---------------------------------------------
    # BIRTH CERTIFICATE
    # ---------------------------------------------

    birth_keywords = [
        "birth certificate",
        "date of birth certificate",
        "municipal corporation"
    ]

    if any(
        keyword in text_lower
        for keyword in birth_keywords
    ):
        return "Birth Certificate"

    return "Unknown Intent"