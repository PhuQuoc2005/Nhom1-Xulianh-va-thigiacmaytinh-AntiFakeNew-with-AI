import pandas as pd
import random
import os

csv_path = 'data/text/vn_fake_news_dataset.csv'

# Danh sách mẫu tin giả (Fake News) - Label 1
fake_templates = [
    "Sốc: Khám phá bí mật {secret} tại {location}. Hãy cảnh giác!",
    "Chính thức: Từ tháng sau cấm toàn bộ {item} trên cả nước. Hãy cảnh giác!",
    "Tin buồn: Nghệ sĩ nổi tiếng {name} vừa qua đời vì {disease}. Hãy cảnh giác!",
    "Chuyên gia cảnh báo: Uống {drink} mỗi ngày gây ung thư {body_part} lập tức. Hãy cảnh giác!",
    "Cảnh báo khẩn: Vừa phát hiện {creature} cao 10 mét ở {location}. Hãy cảnh giác!",
    "Lộ diện video quay cảnh đĩa bay hạ cánh tại {location} tối qua. Hãy cảnh giác!",
    "Sốc: Một người dân ở {location} đào được kho báu chứa 1000 tấn vàng. Hãy cảnh giác!",
    "Cảnh báo: Vi khuẩn ăn thịt người đã lây lan khắp {location}. Hãy cảnh giác!",
    "Khẩn cấp: Ngày mai bão cấp 20 sẽ đổ bộ trực tiếp vào {location}. Hãy cảnh giác!",
    "Được thần linh báo mộng, người đàn ông trúng số {number} tỷ đồng. Hãy cảnh giác!",
    "Sốc: Nhìn thấy {name} đi lại ngoài đường dù đã tuyên bố tử vong. Hãy cảnh giác!",
    "Cảnh báo: Ăn {food} cùng với {drink} sẽ tử vong ngay tại chỗ. Hãy cảnh giác!",
    "Tin chấn động: {name} vừa chính thức thừa nhận là người ngoài hành tinh. Hãy cảnh giác!",
    "Nước chanh nóng có thể chữa khỏi 100% bệnh {disease}. Hãy cảnh giác!",
    "Gấp: Chia sẻ bài viết này để nhận ngay {number} triệu đồng vào tài khoản. Hãy cảnh giác!"
]

# Danh sách mẫu tin thật (Real News) - Label 0
real_templates = [
    "Bộ trưởng {ministry} chủ trì hội nghị phát triển {topic} tại {location}.",
    "Giá {item} trong nước hôm nay có sự biến động nhẹ theo đà thế giới.",
    "Lực lượng chức năng tại {location} vừa triệt phá đường dây {crime}.",
    "Dự báo thời tiết: {location} cuối tuần này có mưa rào và dông rải rác.",
    "Khai mạc triển lãm {topic} quốc tế tại trung tâm {location}.",
    "Tuyển Việt Nam tích cực tập luyện chuẩn bị cho giải {tournament} sắp tới.",
    "Ngân hàng trung ương điều chỉnh tỷ giá {currency} trong biên độ hẹp.",
    "Thành phố {location} triển khai kế hoạch chỉnh trang đô thị năm 2026.",
    "Bộ Giáo dục công bố phương án thi tốt nghiệp THPT năm nay với một số thay đổi.",
    "Dự án cao tốc nối {location} và các tỉnh lân cận đang được đẩy nhanh tiến độ.",
    "Kỳ họp Quốc hội thảo luận về dự thảo luật {law} sửa đổi.",
    "Lễ hội {festival} truyền thống thu hút hàng ngàn du khách tham gia.",
    "Chỉ số VN-Index đóng cửa tăng {number} điểm trong phiên giao dịch hôm nay.",
    "Chuyên gia kinh tế nhận định thị trường {topic} sẽ phục hồi vào cuối năm.",
    "Chính phủ ban hành nghị định mới quy định chi tiết về {topic}."
]

# Từ khóa để điền vào template
secrets = ["kho báu ngầm", "đường hầm bí mật", "thành phố dưới đáy biển", "loài vật kỳ lạ", "thuốc trường sinh"]
locations = ["Hà Nội", "TP.HCM", "Đà Nẵng", "Cần Thơ", "Hải Phòng", "Nha Trang", "Tây Bắc", "ĐBSCL"]
items = ["xe xăng", "điện thoại thông minh", "mạng xã hội", "tiền mặt", "vàng miếng"]
names = ["ca sĩ A", "diễn viên B", "tỷ phú C", "doanh nhân D", "người nổi tiếng"]
diseases = ["ung thư", "đột quỵ", "bệnh lạ", "cảm cúm", "suy tim"]
drinks = ["nước có gas", "cà phê đen", "trà sữa", "nước chanh", "nước lọc"]
body_parts = ["dạ dày", "gan", "phổi", "não", "thận"]
creatures = ["khủng long", "quái vật", "rồng đất", "người khổng lồ", "người ngoài hành tinh"]
foods = ["hải sản", "thịt gà", "trứng", "rau muống", "mì tôm"]
numbers = ["100", "500", "1000", "2000", "5000"]
ministries = ["Bộ Y tế", "Bộ Tài chính", "Bộ Công Thương", "Bộ Giáo dục", "Bộ Giao thông"]
topics = ["chuyển đổi số", "kinh tế xanh", "trí tuệ nhân tạo", "du lịch", "giáo dục"]
crimes = ["buôn lậu", "đánh bạc", "lừa đảo qua mạng", "tín dụng đen"]
tournaments = ["AFF Cup", "Asian Cup", "vòng loại World Cup", "SEA Games"]
currencies = ["USD", "EUR", "JPY"]
laws = ["Đất đai", "Nhà ở", "Giao thông", "Doanh nghiệp"]
festivals = ["chùa Hương", "đền Hùng", "hoa Đà Lạt", "cà phê Buôn Ma Thuột"]

def generate_sentence(template, is_fake):
    kwargs = {}
    if "{secret}" in template: kwargs["secret"] = random.choice(secrets)
    if "{location}" in template: kwargs["location"] = random.choice(locations)
    if "{item}" in template: kwargs["item"] = random.choice(items)
    if "{name}" in template: kwargs["name"] = random.choice(names)
    if "{disease}" in template: kwargs["disease"] = random.choice(diseases)
    if "{drink}" in template: kwargs["drink"] = random.choice(drinks)
    if "{body_part}" in template: kwargs["body_part"] = random.choice(body_parts)
    if "{creature}" in template: kwargs["creature"] = random.choice(creatures)
    if "{food}" in template: kwargs["food"] = random.choice(foods)
    if "{food2}" in template: kwargs["food2"] = random.choice(foods)
    if "{number}" in template: kwargs["number"] = random.choice(numbers)
    if "{ministry}" in template: kwargs["ministry"] = random.choice(ministries)
    if "{topic}" in template: kwargs["topic"] = random.choice(topics)
    if "{crime}" in template: kwargs["crime"] = random.choice(crimes)
    if "{tournament}" in template: kwargs["tournament"] = random.choice(tournaments)
    if "{currency}" in template: kwargs["currency"] = random.choice(currencies)
    if "{law}" in template: kwargs["law"] = random.choice(laws)
    if "{festival}" in template: kwargs["festival"] = random.choice(festivals)
    
    return template.format(**kwargs)

new_data = []

# Sinh ra 100 câu tin giả
for _ in range(100):
    template = random.choice(fake_templates)
    sentence = generate_sentence(template, True)
    new_data.append({"text": sentence, "label": 1})

# Sinh ra 100 câu tin thật
for _ in range(100):
    template = random.choice(real_templates)
    sentence = generate_sentence(template, False)
    new_data.append({"text": sentence, "label": 0})

df_new = pd.DataFrame(new_data)
df_new.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf-8')
print(f"✅ Đã cào và tạo thêm {len(df_new)} mẫu tin tức vào {csv_path}!")
