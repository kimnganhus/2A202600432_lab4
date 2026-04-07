from tools import search_flights, search_hotels, calculate_budget


def test_search_flights():
    print("\n=== TEST: search_flights ===")

    # Case 1: có dữ liệu
    result = search_flights.invoke({
        "origin": "Hà Nội",
        "destination": "Đà Nẵng"
    })
    print(result)

    # Case 2: không có dữ liệu
    result = search_flights.invoke({
        "origin": "Hà Nội",
        "destination": "Tokyo"
    })
    print(result)


def test_search_hotels():
    print("\n=== TEST: search_hotels ===")

    # Case 1: lọc giá
    result = search_hotels.invoke({
        "city": "Đà Nẵng",
        "max_price_per_night": 1000000
    })
    print(result)

    # Case 2: không có khách sạn phù hợp
    result = search_hotels.invoke({
        "city": "Đà Nẵng",
        "max_price_per_night": 100000
    })
    print(result)


def test_calculate_budget():
    print("\n=== TEST: calculate_budget ===")

    # Case 1: bình thường
    result = calculate_budget.invoke({
        "total_budget": 5000000,
        "expense": "ve_may_bay:1500000,khach_san:2000000"
    })
    print(result)

    # Case 2: vượt ngân sách
    result = calculate_budget.invoke({
        "total_budget": 2000000,
        "expense": "ve_may_bay:1500000,khach_san:1000000"
    })
    print(result)

    # Case 3: format sai
    result = calculate_budget.invoke({
        "total_budget": 5000000,
        "expense": "abcxyz"
    })
    print(result)


if __name__ == "__main__":
    print("🚀 RUNNING TOOL TESTS...")

    test_search_flights()
    test_search_hotels()
    test_calculate_budget()

    print("\n✅ DONE")