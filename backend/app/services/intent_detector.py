def detect_intent(text):

    text = text.lower()

    if "passport" in text:
        return "Passport Renewal"

    elif "driving license" in text:
        return "Driving License"

    elif "aadhaar" in text:
        return "Aadhaar Update"

    elif "voter" in text:
        return "Voter ID"

    elif "birth certificate" in text:
        return "Birth Certificate"

    elif "scholarship" in text:
        return "Scholarship Application"

    else:
        return "Unknown Intent"