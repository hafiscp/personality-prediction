from functools import reduce

def calculate_result(score, count):
    average = score / count
    result = "neutral"
    if average > 3:
        result = "high"
    elif average < 3:
        result = "low"
    return result


def reduce_factors(a, b):
    if b["domain"] not in a:
        a[b["domain"]] = {"score": 0, "count": 0, "result": "neutral", "facet": {}}

    a[b["domain"]]["score"] += int(b.get("score", 0))
    a[b["domain"]]["count"] += 1
    a[b["domain"]]["result"] = calculate_result(
        a[b["domain"]]["score"], a[b["domain"]]["count"]
    )

    if "facet" in b:
        if b["facet"] not in a[b["domain"]]["facet"]:
            a[b["domain"]]["facet"][b["facet"]] = {
                "score": 0,
                "count": 0,
                "result": "neutral",
            }
        a[b["domain"]]["facet"][b["facet"]]["score"] += int(b.get("score", 0))
        a[b["domain"]]["facet"][b["facet"]]["count"] += 1
        a[b["domain"]]["facet"][b["facet"]]["result"] = calculate_result(
            a[b["domain"]]["facet"][b["facet"]]["score"],
            a[b["domain"]]["facet"][b["facet"]]["count"],
        )

    return a


def convertor(values):
    answers = []
    output = []
    for i in values.values():
        myDict = {}
        val = i.split(",")
        myDict["domain"] = val[2]
        myDict["facet"] = val[1]
        myDict["score"] = val[0]
        answers.append(myDict)

    con_dic = reduce(reduce_factors, answers, {}).items()
    for key, val in con_dic:
        my_dict = {}
        my_dict["domain"] = key
        my_dict["score"] = val["score"]
        output.append(my_dict)
    return output


# print(con_dic[0])
# print(answers)

# convertor(output)


# print(output.values())
