from langchain_core.tools import tool

FLIGHT_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"}
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"}
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"}
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"}
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"}
    ],
}
 
HOTELS_DB = {
  "Đà Nẵng": [
    {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
    {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
    {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
    {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
    {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7}
  ],
  "Phú Quốc": [
    {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
    {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
    {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
    {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5}
  ],
  "Hồ Chí Minh": [
    {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
    {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
    {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
    {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6}
  ],
}


def parse_price(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.lower().strip()
        text = text.replace(" ", "").replace(".", "").replace(",", "")

        if "triệu" in text:
            text = text.replace("triệu", "")
            try:
                return int(float(text) * 1_000_000)
            except ValueError:
                pass

        if text.endswith("k"):
            try:
                return int(float(text[:-1]) * 1_000)
            except ValueError:
                pass

        if text.isdigit():
            return int(text)

    raise ValueError(f"Không thể chuyển giá trị '{value}' sang số")


def format_price(p):
    return f"{p:,}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Search for flights between two cities. Supports searching for both directions.
    Args:
        origin (str): Departure city
        destination (str): Destination city

    Returns:
        str: List of flights or message if not found
    """
    flights = FLIGHT_DB.get((origin, destination)) or FLIGHT_DB.get((destination, origin))

    if not flights:
        return f"Không có chuyến bay từ {origin} đến {destination}"

    result = "✈️ Chuyến bay:\n"
    for f in flights:
        result += f"- {f['airline']} {f['departure']} → {f['arrival']} | {format_price(f['price'])}\n"
    return result


@tool
def search_hotels(city: str, max_price_per_night: int | str = 9999999) -> str:
    """
    tìm kiếm khách sạn trong thành phố với mức giá tối đa. Kết quả được sắp xếp theo đánh giá từ cao đến thấp.

    Args:
        city (str): thành phố cần tìm khách sạn
        max_price_per_night (int | str, optional): mức giá tối đa mỗi đêm. Defaults to 9999999.

    Returns:
        str: danh sách khách sạn hoặc thông báo không tìm thấy
    """
    try:
        max_price_per_night = parse_price(max_price_per_night)
    except ValueError:
        return f"Không hiểu giá trị ngân sách: {max_price_per_night}"

    hotels = HOTELS_DB.get(city, [])
    if not hotels:
        return f"Không tìm thấy khách sạn tại {city}"

    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

    if not filtered_hotels:
        min_price = min(h["price_per_night"] for h in hotels)
        return (
            f"Không tìm thấy khách sạn tại {city} với ngân sách dưới {format_price(max_price_per_night)}/đêm. "
            f"Khách sạn rẻ nhất tại {city} là {format_price(min_price)}/đêm. Hãy tăng ngân sách để có thêm lựa chọn."
        )

    result = "🏨 Khách sạn:\n"
    for h in filtered_hotels:
        result += f"- {h['name']} | {format_price(h['price_per_night'])}/đêm | ⭐{h['rating']}\n"
    return result


@tool
def calculate_budget(total_budget: int | str, expense: str) -> str:
    """
    Tính toán tổng chi phí dựa trên các khoản chi tiêu được cung cấp và so sánh với ngân sách tổng. Trả về kết quả chi tiết về từng khoản chi tiêu, tổng chi phí, ngân sách còn lại hoặc số tiền vượt ngân sách.

    Args:
        total_budget (int | str): tổng ngân sách ban đầu
        expense (str): chuỗi mô tả các khoản chi tiêu, định dạng "Tên khoản chi:Giá trị", cách nhau bằng dấu phẩy. Ví dụ: "Vé máy bay:1500000,Khách sạn:1200000,Ăn uống:500000"

    Returns:
        str: bảng chi tiết chi tiêu, tổng chi phí, ngân sách còn lại hoặc số tiền vượt ngân sách. Nếu có lỗi trong định dạng chi tiêu, trả về thông báo lỗi.
    """
    try:
        total_budget = parse_price(total_budget)
        items = expense.split(",")
        total = 0

        result = "💰 Chi phí:\n"
        for i in items:
            name, val = i.split(":")
            val = parse_price(val)
            total += val
            result += f"- {name}: {format_price(val)}\n"

        remain = total_budget - total

        result += f"\nTổng: {format_price(total)}"
        result += f"\nNgân sách: {format_price(total_budget)}"

        if remain < 0:
            result += f"\n❌ Vượt {format_price(-remain)}"
        else:
            result += f"\n✅ Còn {format_price(remain)}"

        return result

    except Exception:
        return "Lỗi format budget"