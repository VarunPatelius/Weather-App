from country_list import countries_for_language


countries = dict(countries_for_language("en"))


def countrylist():
    set = []

    for key, value in countries.items():
        set.append(f"{key} - {value}")

    return set


def countryconvert(ISO):
    return countries[ISO]
