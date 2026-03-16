import re


def parse_query_constraints(query: str):

    query = query.lower()

    # detect degree
    degree = "phd" if "phd" in query or "doctor" in query else None

    # detect funding intent
    funding_keywords = ["scholarship", "funding", "stipend", "grant"]
    funding_required = any(k in query for k in funding_keywords)

    # detect potential field keywords
    stop_words = ["phd", "program", "programs", "university", "scholarship", "funding", "in", "for", "with"]

    tokens = re.findall(r"[a-zA-Z]+", query)

    field_keywords = [
        w for w in tokens
        if w not in stop_words and len(w) > 3
    ]

    return {
        "degree": degree,
        "funding_required": funding_required,
        "field_keywords": field_keywords
    }


def is_field_relevant(program: str, keywords):

    if not program:
        return False

    text = program.lower()

    for k in keywords:
        if k in text:
            return True

    return False


def compute_quality_score(result):

    score = 0

    if result.get("phd_program") and result["phd_program"] != "Not found":
        score += 3

    if result.get("funding") and result["funding"] != "Not found":
        score += 2

    if result.get("application_link") and result["application_link"] != "Not found":
        score += 1

    if result.get("application_deadline") and result["application_deadline"] != "Not found":
        score += 1

    if result.get("requirements") and result["requirements"] != "Not found":
        score += 1

    return score


def validate_and_rank_results(results, query):

    constraints = parse_query_constraints(query)

    validated = []
    seen = set()

    for r in results:

        university = r.get("university")
        program = r.get("phd_program")

        if not university or university == "Not found":
            continue

        if not program or program == "Not found":
            program = "PhD Program"
            r["phd_program"] = program

        # check field relevance
        if constraints["field_keywords"]:
            if not is_field_relevant(program, constraints["field_keywords"]):
                continue

        # funding filter
        if constraints["funding_required"]:
            funding = r.get("funding", "").lower()

            if funding == "not found":
                continue

        key = (university.lower(), program.lower())

        if key in seen:
            continue

        seen.add(key)

        score = compute_quality_score(r)

        if score < 2:
            continue

        r["score"] = score

        validated.append(r)

    validated = sorted(validated, key=lambda x: x["score"], reverse=True)

    return validated