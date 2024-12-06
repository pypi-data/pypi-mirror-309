def indicator_predictor(indicator_terms, observation):
    if indicator_terms is None:
        return 0

    total_value = 0
    for indicator_term in indicator_terms:

        indicator_value = linear_predictor(
            indicator_term["terms"],
            indicator_term["intercept"],
            observation)
        
        if (indicator_term["type"] == "multiple"):
            checks = []
            for term in indicator_term['indicators']:
                checks.append(check_single_indicator(term, observation))
            
            if all(checks):
                total_value += indicator_value
        else:
            if check_single_indicator(indicator_term, observation):
                total_value += indicator_value

    return total_value

def check_single_indicator(term, observation):
    check_value = get_check_value(term, observation)

    if (term["type"] == "greater_than_value"):
        if check_value > term['threshold']:
            return True

    if (term["type"] == "greater_or_equal_than_value"):
        if check_value >= term['threshold']:
            return True

    if (term["type"] == "smaller_or_equal_than_value"):
        if check_value <= term['threshold']:                
            return True

    if (term["type"] == "greater_than_variable"):
        for lag in term['threshold']:
            for variable in term['threshold'][lag]:
                threshold = observation[lag][variable]

        if check_value > threshold:                
            return True

def get_check_value(term, observation):
    # Get check_variable
    lag = list(term['variable'].keys())[0]
    variable = term['variable'][lag][0]

    check_value = observation[lag][variable]
    
    return check_value

def linear_predictor(terms, intercept, observation):

    prod = 0

    if intercept:
        prod += intercept

    if terms is None:
        return prod

    # print(observation)
    for term in terms:
        value = term["param"]
        for lag in term["variables"].keys():
            for var in term["variables"][lag]:
                # print(f"{lag=}, {var=}")
                value *= observation[lag][var]

        prod += value

    return prod