import re
from datetime import datetime


# =========================================================
# DATE VALIDATION
# =========================================================

def validate_dates(dates):

    errors = []

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y/%m/%d",
        "%Y-%m-%d"
    ]

    for date in dates:

        valid = False

        for fmt in formats:

            try:
                datetime.strptime(date, fmt)
                valid = True
                break

            except ValueError:
                pass

        if not valid:

            errors.append({
                "type": "Invalid Date",
                "message": f"The date '{date}' is not valid."
            })

    return errors


# =========================================================
# EMAIL VALIDATION
# =========================================================

def validate_emails(text):

    errors = []

    # Only check email if an email-like value actually exists.
    possible_emails = re.findall(
        r"\S+@\S+",
        text
    )

    valid_emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if possible_emails and not valid_emails:

        errors.append({
            "type": "Invalid Email",
            "message":
                "An email-like value was detected but it "
                "does not appear to be correctly formatted."
        })

    return errors


# =========================================================
# ACADEMIC RECORD VALIDATION
# =========================================================

def validate_academic_records(entities):

    errors = []
    warnings = []

    records = entities.get(
        "academic_records",
        []
    )

    for index, record in enumerate(
        records,
        start=1
    ):

        maximum = record.get(
            "maximum_marks"
        )

        obtained = record.get(
            "obtained_marks"
        )

        percentage = record.get(
            "percentage"
        )

        year = record.get(
            "year"
        )

        # ---------------------------------------------
        # Check that marks are numeric
        # ---------------------------------------------

        if (
            maximum is None
            or obtained is None
        ):
            continue

        # ---------------------------------------------
        # Obtained cannot exceed maximum
        # ---------------------------------------------

        if obtained > maximum:

            errors.append({
                "type": "Invalid Marks",
                "message":
                    f"Academic record {index}: obtained marks "
                    f"({obtained}) exceed maximum marks "
                    f"({maximum})."
            })

        # ---------------------------------------------
        # Marks cannot be negative
        # ---------------------------------------------

        if maximum < 0 or obtained < 0:

            errors.append({
                "type": "Negative Marks",
                "message":
                    f"Academic record {index}: marks cannot be negative."
            })

        # ---------------------------------------------
        # Calculate expected percentage
        # ---------------------------------------------

        if maximum > 0:

            expected_percentage = (
                obtained / maximum
            ) * 100

            expected_percentage = round(
                expected_percentage,
                2
            )

            # -----------------------------------------
            # Compare with document percentage
            # -----------------------------------------

            if percentage is not None:

                difference = abs(
                    expected_percentage - percentage
                )

                if difference > 1.0:

                    errors.append({
                        "type": "Inconsistent Percentage",
                        "message":
                            f"Academic record {index}"
                            + (
                                f" ({year})"
                                if year
                                else ""
                            )
                            + f": document shows {percentage}%, "
                            f"but {obtained}/{maximum} gives "
                            f"{expected_percentage}%."
                    })

    return errors, warnings


# =========================================================
# CONFLICTING VALUES
# =========================================================

def check_conflicting_values(entities):

    errors = []

    # =================================================
    # INCOME CONSISTENCY
    # =================================================

    income = entities.get(
        "income",
        {}
    )

    monthly = income.get("monthly")
    annual = income.get("annual")

    if (
        monthly is not None
        and annual is not None
    ):

        expected_annual = monthly * 12

        difference = abs(
            expected_annual - annual
        )

        tolerance = max(
            1000,
            annual * 0.05
        )

        if difference > tolerance:

            errors.append({
                "type": "Inconsistent Income",
                "message":
                    f"Monthly income of ₹{monthly:,} "
                    f"implies an annual income of "
                    f"approximately ₹{expected_annual:,}, "
                    f"but the document reports "
                    f"₹{annual:,}."
            })

    # =================================================
    # AGE VALIDATION
    # =================================================

    age = entities.get("age")

    if age is not None:

        if age < 1 or age > 120:

            errors.append({
                "type": "Invalid Age",
                "message":
                    f"The detected age ({age}) is outside "
                    f"the valid range of 1–120 years."
            })

    # =================================================
    # PERCENTAGE RANGE
    # =================================================

    academic_records = entities.get(
        "academic_records",
        []
    )

    for index, record in enumerate(
        academic_records,
        start=1
    ):

        percentage = record.get(
            "percentage"
        )

        if percentage is not None:

            if percentage < 0 or percentage > 100:

                errors.append({
                    "type": "Invalid Percentage",
                    "message":
                        f"Academic record {index}: "
                        f"percentage {percentage}% is outside "
                        f"the valid range of 0–100%."
                })

    return errors


# =========================================================
# REQUIRED INFORMATION
# =========================================================

def check_required_information(
    text,
    intent,
    entities
):

    warnings = []

    text_lower = text.lower()

    # =================================================
    # EDUCATIONAL DOCUMENT
    # =================================================

    if (
        "educational" in intent.lower()
        or "scholarship" in intent.lower()
    ):

        universities = entities.get(
            "universities",
            []
        )

        courses = entities.get(
            "courses",
            []
        )

        academic_records = entities.get(
            "academic_records",
            []
        )

        names = entities.get(
            "names",
            []
        )

        dates = entities.get(
            "dates",
            []
        )

        # ---------------------------------------------
        # STUDENT NAME
        # ---------------------------------------------

        if not names:

            warnings.append({
                "type": "Missing Student Name",
                "message":
                    "A student/applicant name could not "
                    "be confidently detected."
            })

        # ---------------------------------------------
        # UNIVERSITY
        # ---------------------------------------------

        if not universities:

            warnings.append({
                "type": "Missing Institution",
                "message":
                    "No educational institution could "
                    "be confidently detected."
            })

        # ---------------------------------------------
        # COURSE
        # ---------------------------------------------

        if not courses:

            warnings.append({
                "type": "Missing Course",
                "message":
                    "No course or degree could be "
                    "confidently detected."
            })

        # ---------------------------------------------
        # ACADEMIC RECORD
        # ---------------------------------------------

        if not academic_records:

            warnings.append({
                "type": "Missing Academic Record",
                "message":
                    "No academic marks or percentage "
                    "record could be confidently detected."
            })

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        if not dates:

            warnings.append({
                "type": "Missing Date",
                "message":
                    "No application or relevant date "
                    "could be confidently detected."
            })

    return warnings

def check_text_consistency(text):
    """
    Look for repeated labelled fields whose values
    disagree with each other.
    """

    errors = []

    # =================================================
    # NAME CONSISTENCY
    # =================================================

    name_patterns = [
        r"(?:student\s+name|applicant\s+name|name)"
        r"\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,60})"
    ]

    names = []

    for pattern in name_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for name in matches:

            cleaned = name.strip()

            if cleaned:
                names.append(cleaned)

    # Remove duplicates while preserving order
    names = list(
        dict.fromkeys(names)
    )

    # If multiple different names occur,
    # flag a possible inconsistency.
    if len(names) > 1:

        normalized_names = [
            re.sub(
                r"\s+",
                " ",
                name.lower()
            ).strip()
            for name in names
        ]

        if len(set(normalized_names)) > 1:

            errors.append({
                "type": "Conflicting Name",
                "message":
                    "Multiple different applicant/student "
                    "names were detected: "
                    + ", ".join(names)
            })

    # =================================================
    # UNIVERSITY CONSISTENCY
    # =================================================

    university_patterns = [
        r"(?:university|institution)"
        r"\s*[:\-]\s*([A-Za-z][A-Za-z .,&'-]{3,100})"
    ]

    universities = []

    for pattern in university_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for university in matches:

            cleaned = university.strip()

            if cleaned:
                universities.append(
                    cleaned
                )

    universities = list(
        dict.fromkeys(
            universities
        )
    )

    if len(universities) > 1:

        normalized_universities = [
            re.sub(
                r"\s+",
                " ",
                university.lower()
            ).strip()
            for university in universities
        ]

        if len(
            set(normalized_universities)
        ) > 1:

            errors.append({
                "type": "Conflicting Institution",
                "message":
                    "Multiple different institutions "
                    "were detected: "
                    + ", ".join(universities)
            })

    return errors

# =========================================================
# DATE RELATIONSHIP CHECK
# =========================================================

def check_date_relationships(entities):

    warnings = []

    normalized_dates = entities.get(
        "normalized_dates",
        []
    )

    valid_dates = []

    for date in normalized_dates:

        if date:

            try:

                parsed = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                )

                valid_dates.append(
                    parsed
                )

            except ValueError:
                pass

    # We don't call different dates contradictory simply
    # because they are different. Government forms naturally
    # contain many dates.
    #
    # We only flag impossible future dates.

    today = datetime.now()

    for date in valid_dates:

        if date > today:

            warnings.append({
                "type": "Future Date",
                "message":
                    f"The document contains a future date: "
                    f"{date.strftime('%d/%m/%Y')}."
            })

    return warnings


# =========================================================
# OCR QUALITY
# =========================================================

def check_ocr_quality(text):

    warnings = []

    pipe_count = text.count("|")

    if pipe_count > 30:

        warnings.append({
            "type": "OCR Formatting",
            "message":
                "The document contains OCR/table formatting "
                "artifacts. Extracted values should be manually "
                "verified."
        })

    return warnings


# =========================================================
# MAIN VALIDATOR
# =========================================================

def validate_document(
    text,
    entities=None,
    intent="Unknown Intent"
):

    errors = []
    warnings = []

    # -----------------------------------------------------
    # EMPTY DOCUMENT
    # -----------------------------------------------------

    if not text or not text.strip():

        return {
            "status": "Invalid",
            "score": 0,
            "errors": [
                {
                    "type": "Empty Document",
                    "message":
                        "No readable text was found in the document."
                }
            ],
            "warnings": []
        }

    # -----------------------------------------------------
    # SAFETY
    # -----------------------------------------------------

    if entities is None:
        entities = {}

    # -----------------------------------------------------
    # DATE VALIDATION
    # -----------------------------------------------------

    dates = entities.get(
        "dates",
        []
    )

    errors.extend(
        validate_dates(
            dates
        )
    )

    # -----------------------------------------------------
    # EMAIL VALIDATION
    # -----------------------------------------------------

    errors.extend(
        validate_emails(
            text
        )
    )

    # -----------------------------------------------------
    # ACADEMIC SEMANTIC VALIDATION
    # -----------------------------------------------------

    academic_errors, academic_warnings = (
        validate_academic_records(
            entities
        )
    )

    errors.extend(
        academic_errors
    )

    warnings.extend(
        academic_warnings
    )

    # -----------------------------------------------------
    # INCOME / VALUE CONSISTENCY
    # -----------------------------------------------------

    errors.extend(
        check_conflicting_values(
            entities
        )
    )

    errors.extend(
        check_text_consistency(
            text
        )
    )

    # -----------------------------------------------------
    # REQUIRED INFORMATION
    # -----------------------------------------------------

    warnings.extend(
        check_required_information(
            text,
            intent,
            entities
        )
    )

    # -----------------------------------------------------
    # DATE RELATIONSHIPS
    # -----------------------------------------------------

    warnings.extend(
        check_date_relationships(
            entities
        )
    )

    # -----------------------------------------------------
    # OCR QUALITY
    # -----------------------------------------------------

    warnings.extend(
        check_ocr_quality(
            text
        )
    )

    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    score = 100

    # Serious semantic errors
    score -= len(errors) * 20

    # Warnings have smaller impact
    score -= len(warnings) * 5

    score = max(
        0,
        min(
            100,
            score
        )
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    if errors:

        status = "Invalid"

    elif warnings:

        status = "Needs Review"

    else:

        status = "Valid"

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {
        "status": status,
        "score": score,
        "errors": errors,
        "warnings": warnings
    }