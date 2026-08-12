import re
from datetime import datetime


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    """Clean OCR/document text while preserving useful structure."""

    if not text:
        return ""

    # Normalize Windows line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove obvious OCR noise characters
    text = text.replace("�", " ")

    # Normalize repeated spaces but preserve newlines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


# =========================================================
# DATE EXTRACTION
# =========================================================

def extract_dates(text):
    """Extract common date formats."""

    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2}\b",
        r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
        r"\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b"
    ]

    dates = []

    for pattern in patterns:
        dates.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )

    return list(dict.fromkeys(dates))


# =========================================================
# DATE NORMALIZATION
# =========================================================

def normalize_date(date_string):
    """Convert a detected date into YYYY-MM-DD when possible."""

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d %B %Y",
        "%d %b %Y"
    ]

    for fmt in formats:

        try:
            date_object = datetime.strptime(
                date_string,
                fmt
            )

            return date_object.strftime(
                "%Y-%m-%d"
            )

        except ValueError:
            pass

    return None


# =========================================================
# MONEY EXTRACTION
# =========================================================

def extract_money(text):
    """Extract monetary values."""

    patterns = [
        r"(?:₹|rs\.?|inr)\s?[\d,]+(?:\.\d+)?",
        r"[\d,]+(?:\.\d+)?\s*(?:₹|rs\.?|inr)"
    ]

    money = []

    for pattern in patterns:

        money.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )

    return list(dict.fromkeys(money))


# =========================================================
# NUMERIC VALUES
# =========================================================

def extract_numbers(text):
    """Extract useful numeric values."""

    numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        text
    )

    return numbers


# =========================================================
# EMAIL EXTRACTION
# =========================================================

def extract_emails(text):
    """Extract email addresses."""

    pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    return re.findall(
        pattern,
        text
    )


# =========================================================
# PHONE NUMBER EXTRACTION
# =========================================================

def extract_phone_numbers(text):
    """Extract Indian-style phone numbers."""

    pattern = (
        r"(?<!\d)"
        r"(?:\+91[\s-]?)?"
        r"[6-9]\d{9}"
        r"(?!\d)"
    )

    return re.findall(
        pattern,
        text
    )


# =========================================================
# AGE EXTRACTION
# =========================================================

def extract_age(text):
    """Extract explicitly stated age."""

    patterns = [
        r"\bage\s*[:\-]?\s*(\d{1,3})\b",
        r"(\d{1,3})\s*years?\s*old"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            age = int(
                match.group(1)
            )

            if 1 <= age <= 120:
                return age

    return None


# =========================================================
# INCOME EXTRACTION
# =========================================================

def extract_income_values(text):
    """Extract monthly and annual income values."""

    monthly = None
    annual = None

    monthly_patterns = [
        r"monthly\s+income\s*[:\-]?\s*"
        r"(?:₹|rs\.?|inr)?\s*([\d,]+)",

        r"monthly\s+salary\s*[:\-]?\s*"
        r"(?:₹|rs\.?|inr)?\s*([\d,]+)"
    ]

    annual_patterns = [
        r"annual\s+income\s*[:\-]?\s*"
        r"(?:₹|rs\.?|inr)?\s*([\d,]+)",

        r"yearly\s+income\s*[:\-]?\s*"
        r"(?:₹|rs\.?|inr)?\s*([\d,]+)"
    ]

    for pattern in monthly_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            monthly = int(
                match.group(1).replace(",", "")
            )

            break

    for pattern in annual_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            annual = int(
                match.group(1).replace(",", "")
            )

            break

    return {
        "monthly": monthly,
        "annual": annual
    }


# =========================================================
# PERCENTAGE EXTRACTION
# =========================================================

def extract_percentages(text):
    """Extract percentage values."""

    pattern = r"\b\d+(?:\.\d+)?\s*%"

    percentages = re.findall(
        pattern,
        text
    )

    return list(
        dict.fromkeys(percentages)
    )


# =========================================================
# MARKS EXTRACTION
# =========================================================

def extract_marks(text):
    """
    Extract explicit marks written as obtained/maximum.

    Small values such as 1/1 are ignored because they are
    commonly OCR artifacts or form numbering.
    """

    marks = []

    pattern = (
        r"\b"
        r"(\d+(?:\.\d+)?)"
        r"\s*/\s*"
        r"(\d+(?:\.\d+)?)"
        r"\b"
    )

    matches = re.findall(
        pattern,
        text
    )

    for obtained, maximum in matches:

        try:

            obtained_value = float(obtained)
            maximum_value = float(maximum)

            # Ignore tiny values that are unlikely
            # to represent academic marks.
            if maximum_value <= 10:
                continue

            if (
                maximum_value > 0
                and 0 <= obtained_value <= maximum_value
            ):

                marks.append({
                    "obtained": obtained_value,
                    "maximum": maximum_value
                })

        except ValueError:
            pass

    return marks


# =========================================================
# ACADEMIC RECORD EXTRACTION
# =========================================================

def extract_academic_records(text):
    """
    Extract academic records from both:

    1. Structured forms:
       500.00 466.00 93.20

    2. Labelled documents:
       Maximum Marks: 600
       Obtained Marks: 386
       Percentage: 80%
    """

    records = []

    # =================================================
    # FORMAT 1: LABELLED ACADEMIC INFORMATION
    # =================================================

    maximum_match = re.search(
        r"maximum\s+marks\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        text,
        flags=re.IGNORECASE
    )

    obtained_match = re.search(
        r"obtained\s+marks\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        text,
        flags=re.IGNORECASE
    )

    percentage_match = re.search(
        r"percentage\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*%",
        text,
        flags=re.IGNORECASE
    )

    year_match = re.search(
        r"(?:academic\s+year|year)\s*[:\-]?\s*(20\d{2})",
        text,
        flags=re.IGNORECASE
    )

    if maximum_match and obtained_match:

        maximum = float(
            maximum_match.group(1)
        )

        obtained = float(
            obtained_match.group(1)
        )

        percentage = None

        if percentage_match:
            percentage = float(
                percentage_match.group(1)
            )

        year = None

        if year_match:
            year = int(
                year_match.group(1)
            )

        if (
            maximum > 0
            and obtained >= 0
        ):

            record = {
                "year": year,
                "maximum_marks": maximum,
                "obtained_marks": obtained
            }

            if percentage is not None:
                record["percentage"] = percentage

            records.append(record)

    # =================================================
    # FORMAT 2: TABLE-STYLE ACADEMIC RECORD
    # =================================================

    table_pattern = (
        r"\b"
        r"(20\d{2})"
        r"[^\n]{0,80}?"
        r"(\d+(?:\.\d+)?)"
        r"\s+"
        r"(\d+(?:\.\d+)?)"
        r"\s+"
        r"(\d+(?:\.\d+)?)"
    )

    matches = re.findall(
        table_pattern,
        text
    )

    for year, maximum, obtained, percentage in matches:

        try:

            maximum_value = float(maximum)
            obtained_value = float(obtained)
            percentage_value = float(percentage)

            # Avoid impossible records
            if (
                maximum_value <= 0
                or obtained_value < 0
                or obtained_value > maximum_value
                or percentage_value < 0
                or percentage_value > 100
            ):
                continue

            record = {
                "year": int(year),
                "maximum_marks": maximum_value,
                "obtained_marks": obtained_value,
                "percentage": percentage_value
            }

            # Avoid duplicates
            duplicate = any(
                r.get("year") == record["year"]
                and r.get("maximum_marks") == record["maximum_marks"]
                and r.get("obtained_marks") == record["obtained_marks"]
                for r in records
            )

            if not duplicate:
                records.append(record)

        except ValueError:
            pass

    return records


# =========================================================
# UNIVERSITY EXTRACTION
# =========================================================

def extract_universities(text):
    """Extract university/institution names."""

    universities = []

    pattern = (
        r"\b[A-Z][A-Za-z&.,' -]{3,100}"
        r"\b(?:University|UNIVERSITY)\b"
    )

    matches = re.findall(
        pattern,
        text
    )

    for university in matches:

        cleaned = university.strip()

        if cleaned not in universities:
            universities.append(
                cleaned
            )

    # OCR often produces uppercase university names
    lines = text.splitlines()

    for line in lines:

        if "UNIVERSITY" in line.upper():

            cleaned = line.strip()

            if (
                len(cleaned) > 5
                and cleaned not in universities
            ):
                universities.append(
                    cleaned
                )

    return universities


# =========================================================
# COURSE / DEGREE EXTRACTION
# =========================================================

def extract_courses(text):
    """Extract common degree/course names."""

    courses = []

    course_patterns = [
        r"\bMASTER OF [A-Z][A-Z ]+\b",
        r"\bBACHELOR OF [A-Z][A-Z ]+\b",
        r"\bM\.?A\.?\b",
        r"\bM\.?COM\.?\b",
        r"\bM\.?SC\.?\b",
        r"\bM\.?TECH\.?\b",
        r"\bB\.?A\.?\b",
        r"\bB\.?COM\.?\b",
        r"\bB\.?SC\.?\b",
        r"\bB\.?TECH\.?\b",
        r"\bMBA\b",
        r"\bMCA\b",
        r"\bBCA\b",
        r"\bLLB\b",
        r"\bLLM\b",
        r"\bPHD\b"
    ]

    for pattern in course_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            cleaned = match.strip()

            if cleaned not in courses:
                courses.append(
                    cleaned
                )

    return courses


# =========================================================
# CERTIFICATE / ID NUMBERS
# =========================================================

def extract_identification_numbers(text):
    """
    Extract long numeric identifiers.

    These are returned separately because they should
    NOT be confused with marks, dates or money.
    """

    numbers = re.findall(
        r"\b\d{8,20}\b",
        text
    )

    return list(
        dict.fromkeys(numbers)
    )


# =========================================================
# NAME-LIKE VALUES
# =========================================================

def extract_names(text):
    """
    Extract likely person names from common labelled fields.

    OCR can make this imperfect, so these values should
    be treated as candidates rather than guaranteed names.
    """

    names = []

    patterns = [
        r"(?:name|student name|applicant name)"
        r"\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,60})",

        r"(?:father'?s name|mother'?s name)"
        r"\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,60})"
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            cleaned = match.strip()

            if cleaned:
                names.append(
                    cleaned
                )

    return list(
        dict.fromkeys(names)
    )


# =========================================================
# DOCUMENT KEYWORDS
# =========================================================

def detect_document_keywords(text):
    """Detect important document concepts."""

    text_lower = text.lower()

    categories = {

        "education": [
            "university",
            "college",
            "student",
            "course",
            "degree",
            "marks",
            "percentage",
            "academic"
        ],

        "scholarship": [
            "scholarship",
            "financial assistance",
            "financial aid",
            "fee concession",
            "income certificate"
        ],

        "identity": [
            "aadhaar",
            "aadhar",
            "passport",
            "voter",
            "driving licence",
            "driving license"
        ],

        "income": [
            "income",
            "salary",
            "annual income",
            "monthly income"
        ]
    }

    detected = {}

    for category, keywords in categories.items():

        found = []

        for keyword in keywords:

            if keyword in text_lower:
                found.append(
                    keyword
                )

        detected[category] = found

    return detected


# =========================================================
# MAIN ENTITY EXTRACTION
# =========================================================

def extract_entities(text):
    """
    Extract structured information for the
    semantic validation engine.
    """

    cleaned = clean_text(
        text
    )

    dates = extract_dates(
        cleaned
    )

    return {

        # Basic entities
        "dates": dates,

        "normalized_dates": [
            normalize_date(date)
            for date in dates
        ],

        "money": extract_money(
            cleaned
        ),

        "emails": extract_emails(
            cleaned
        ),

        "phone_numbers": extract_phone_numbers(
            cleaned
        ),

        "age": extract_age(
            cleaned
        ),

        "income": extract_income_values(
            cleaned
        ),

        # Academic information
        "percentages": extract_percentages(
            cleaned
        ),

        "marks": extract_marks(
            cleaned
        ),

        "academic_records": extract_academic_records(
            cleaned
        ),

        "universities": extract_universities(
            cleaned
        ),

        "courses": extract_courses(
            cleaned
        ),

        # Identification information
        "identification_numbers":
            extract_identification_numbers(
                cleaned
            ),

        "names": extract_names(
            cleaned
        ),

        # Document classification clues
        "document_keywords":
            detect_document_keywords(
                cleaned
            )
    }