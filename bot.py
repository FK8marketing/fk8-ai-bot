import os
import openai
import requests
import random
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "7713517792:AAFunOKhM21QdidqqUKvsYvyK6-3d2Izwuw"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Hàm ghi log
def log_message(user_id, user_text):
    with open("log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] User {user_id}: {user_text}\n")

# Từ khóa và phản hồi
KEYWORD_RESPONSES_RAW = {
    "miễn phí": [
        "🎁 Nhận ngay 555K khi đăng ký,cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8 nhé!",
        "🔥 Tặng 555K liền tay cho tân thủ!",
        "💸 Chỉ cần đăng ký là có 555K,inbox ngay @CS1_FK8 hoặc @CS2_FK8 khi cần hỗ trợ!",
        "📲 Đăng ký → liên kết ngân hàng → nhận ngay trong 3 bước đơn giản!,cần hỗ trợ thêm liên hệ @CS1_FK8 hoặc @CS2_FK8 ",
        "📩 Sau đăng ký + cập nhật thông tin => Chọn tham gia KM nhận 555k.Cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8 nha!"
    ],
    "tân thủ": [
        "🎁 Nhận ngay 555K khi đăng ký!cần hỗ trợ liên hệ admin nhóm",
        "🔥 Tặng 555K liền tay cho tân thủ! bấm 'tham gia ngay', cẫn hỗ trợ thêm liên hệ @CS1_FK8 hoặc @CS2_FK8 nhé ",
        "💸 Chỉ cần đăng ký là có 555K, liên hệ Ad để được hỗ trợ anh nhé!"
    ],
    "free": ["🎁 Bấm tham gia ngay 555K khi đăng ký! Không cần nạp trước, nhận lợi nhuận lên đến 100K.Cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8"],
    "FK8": [
    "🎁 nền tảng kết hợp giữa thể thao và dự đoán kết quả một cách logic.", 
    "FK8 là nền tảng mới nhưng đang rất hot đó 🔥 Bên em có kiểu cược Phản Tỷ Số –  hiểu đơn  giản là đoán sai mà đúng thời điểm là ăn nha 😎."  ],
    "uy tín": ["Dạ uy tín anh ơi ✨ FK8 có hỗ trợ CSKH, thưởng tân thủ 555K rõ ràng, chơi vui – thưởng thật 💸 Anh cần em gửi link hỗ trợ trực tiếp không ạ?"],
    "trải nghiệm": ["🎉Đăng ký tài khoản FK8, liên kết ngân hàng & số điện thoại → nhận ngay 555K.Cần hỗ trợ thêm inbox ngay @CS1_FK8 hoặc @CS2_FK8 nha!"],
    "code": ["Sau khi tạo tài khoản thành công, truy cập mục khuyến mãi → chọn 'Nhận 555K.Cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8 nha"],
    "tvm":["🎁 Nhận ngay 555K khi đăng ký!"],
    "thành viên mới": ["💰Phần thưởng 555K sẽ được cộng khi bạn hoàn thành 3 bước: Đăng ký – Liên kết – Nhận.Vẫn chưa nhận được @CS1_FK8 hoặc @CS2_FK8 để được hỗ trợ "],
    "nạp đầu slot": [
        "🎰 NẠP LẦN ĐẦU SLOT – TẶNG 100%",
        "🔥 Khuyến mãi 100% nạp đầu tại Slot, nhắn ngay  @CS1_FK8 hoặc @CS2_FK8 để biết thêm chi tiết!",
        "🎯 Ưu đãi slot lần đầu – thưởng đến 3 triệu!",
    ],
    "nổ hũ": [
        "🎰 NẠP LẦN ĐẦU NỔ HŨ – TẶNG 100%, liên hệ admin hỗ trợ thêm thông tin chi tiết về khuyến mãi. ",
        "🔥 Khuyến mãi 100% nạp đầu tại Slot, nhắn ngay  @CS1_FK8 hoặc @CS2_FK8 để biết thêm chi tiết!",
        "🎯 Ưu đãi slot lần đầu – thưởng đến 3 triệu!",
    ],
    "nạp đầu thể thao": [
        "⚽ NẠP LẦN ĐẦU THỂ THAO – THƯỞNG 50%",
        "🔥 Nạp từ 500K nhận 50% thưởng – tối đa 3 triệu",
        "💱 Với thể thao, nạp lần đầu thưởng 50% khi từ 500K- tối đa 3 triệu!"
    ],
    "hoàn trả":[
        "🔁 HOÀN TRẢ HÀNG NGÀY – CHƠI LÀ CÓ LÃI!",
        "💵 Dù thắng hay thua vẫn hoàn tiền mỗi ngày",
        "📊 Tỷ lệ linh hoạt tùy theo sảnh chơi và cấp độ VIP"
    ],
    "khuyến mãi": [
        "🎉 Ưu đãi hấp dẫn đang chờ anh đó ạ! Inbox @CS1_FK8 hoặc @CS2_FK8 nhé!",
        "🔥 Khuyến mãi hot mỗi ngày, nhắn ngay @CS1_FK8 hoặc @CS2_FK8 để biết thêm chi tiết",
    ],
    "Nạp lại": [
        "🎉 Hiện có nhiều ưu đãi hấp dẫn đó anh, mình cần hỗ trợ về khuyến mãi liên hệ @CS1_FK8 hoặc @CS2_FK8 nhé!",
        "🔥 Bên em  đang cập nhật thêm các khuyến mãi trong thời gian sắp tối, anh theo dõi trên nhóm  giúp em ,cần hỗ trợ thêm nhắn ngay @CS1_FK8 hoặc @CS2_FK8 để biết thêm chi tiết",
    ],
    "Trận hot": [
        "🎯 Bạn theo dõi thêm tại nhóm FK8 cập nhậtthông tin nha",
        "📌 Theo dõi tại nhóm FK8 luôn cập nhật kèo mỗi ngày",
        "📣 Các kèo hot được cập nhật nhanh nhất tại nhóm!",
        "🧠 Theo dõi phân tích chi tiết tại trang thông tin của team nhé",
        "🔍 Kèo mới sẽ được admin thông báo, bạn theo dõi sát nha"
    ],
    "kèo thơm": [
        "🎯 Bạn theo dõi thêm trên nhóm cập nhật thông tin hàng ngày nhé",
        "📌 Theo dõi kèo trên nhóm, mỗi ngày đêu cập nhật các kèo hot đó ạ",
        "📣 Các kèo hot được cập nhật nhanh nhất tại nhóm FK8!",
        "🧠 Theo dõi phân tích chi tiết tại nhóm FK8 thông tin của team nhé",
        "🔍 Kèo mới luôn được admin thông báo, bạn theo dõi sát nha"
    ],
    "kèo": [
        "🎯 Bạn theo dõi thêm tại nhóm FK8 cập nhậtthông tin nha",
        "📌 Theo dõi tại nhóm FK8 luôn cập nhật kèo mỗi ngày",
        "📣 Các kèo hot được cập nhật nhanh nhất tại nhóm!",
        "🧠 Theo dõi phân tích chi tiết tại trang thông tin của team nhé",
        "🔍 Kèo mới sẽ được admin thông báo, bạn theo dõi sát nha"
    ],
    "soi kèo": [
        "🎯 Bạn theo dõi thêm trên nhóm cập nhật thông tin hàng ngày nhé",
        "📌 Theo dõi kèo trên nhóm, mỗi ngày đêu cập nhật các kèo hot đó ạ",
        "📣 Các kèo hot được cập nhật nhanh nhất tại nhóm FK8!",
        "🧠 Theo dõi phân tích chi tiết tại nhóm FK8 thông tin của team nhé",
        "🔍 Kèo mới luôn được admin thông báo, bạn theo dõi sát nha"
    ],
    "hỗ trợ": ["📞 Bạn có thể nhắn CS1: @CS1_FK8 hoặc CS2: @CS2_FK8 hỗ trợ nhé!"],
    "Rút nhanh": ["Thật tuyệt khi biết rằng anh/chị hài lòng với dịch vụ của FK8! Chúng tôi sẽ tiếp tục nâng cao chất lượng để phục vụ tốt hơn nữa."],
    "gôm lúa": ["💸 Lụm kèo rồi anh em ơi, kèo thơm phức!"],
    "lụm": ["💰 Gôm lúa xịn xò, chiến tiếp anh em!"],
    "win": ["🔥 Win đậm, chốt đơn chất lượng!"],
    "thắng": ["💰 Lãi về rồi, nghỉ hay vào tiếp đây anh em?"],
    "lose": ["😢 Không sao đâu anh, thua keo này ta bày keo khác!"],
    "thua": ["làm lại trận tiếp không anh,phản tỷ số là đường dài nha !"],
    "nạp đầu": [
    "🎯 Khi nạp lần đầu, bạn được tặng tối đa 999K đó nha! Liên hệ CSKH để nhận khuyến mãi.",
    "💸 Ưu đãi cực hấp dẫn cho lần nạp đầu tiên, thưởng tới đa 999K tại phần tỷ số.",
    "💰 Tặng 100% đến 3 triệu. Thể thao: thưởng 50% khi nạp từ 500K."
],
    "nạp lần đầu": [
    "💰 Khi nạp lần đầu, bạn được tặng tối đa 999K đó nha! Liên hệ CSKH để nhận khuyến mãi.",
    "💸 Ưu đãi cực hấp dẫn cho lần nạp đầu tiên, thưởng tới đa 999K tại phần tỷ số.",
    "🔥 Tặng 100% đến 3 triệu. Thể thao: thưởng 50% khi nạp từ 500K."
],
    "nạp chậm": [
    "🎯 Dạ có giao dịch đang không ổn định hoặc đang quá tải, anh chờ 5 phút nếu vẫn chưa nhận được anh liên hệ CSKH trực tuyến hỗ trợ nhé.",
    "📞 Anh liên hệ  Admin @CS1_FK8 hoặc CS2: @CS2_FK8 để hỗ trợ ngay cho anh nhé",
    "📩 Anh ơi, mình nhắn liền cho admin @CS1_FK8 hoặc CS2: @CS2_FK8 hoặc CSKH trực tuyến hỗ trợ cho mình nhé."
],
    "rút chậm": [
    "🔍 Anh liên hệ CSkH kiểm tra ngay cho anh nhé",
    "🎯 Anh mình rút về chậm ạ, anh liên hệ  CSKH trực tuyến hoặc admin nhóm hỗ trợ ngay anh nhé",
    "🎯 Anh ơi, mình nhắn liền cho admin @CS1_FK8 hoặc CS2: @CS2_FK8 hoặc CSKH trực tuyến hỗ trợ cho mình nha."
],
    "phản tỷ số": [
    "🔥 Phản Tỷ Số là cách chơi đi ngược – chọn kết quả sai để chiến thắng!",
    "🔥 Đây là chiến thuật soi kèo logic, không cần đúng – chỉ cần đoán sai bạn sẽ chiến thắng.",
    "🔥 Phản Tỷ Số không phải may rủi, mà là cách tư duy khác biệt,  cược vào tỷ số không chính xác bạn sẽ chiến thắng."
],
    "nạp tiền có ": [
    "🔥 Dạ Fk8 đang có nhiều ưu đãi cho thành viên đó ạ, mình có thể tham khảo trên trang chủ hoặc liên hệ Admin nhóm hỗ trợ anh nhé",
    "💰 Mình đang muốn tham gia sản phẩm nào cụ thể để em hỗ trợ cho anh ạ",
    "💸 Anh ơi, mình nhắn liền cho admin @CS1_FK8 hoặc CS2: @CS2_FK8 hoặc CSKH trực tuyến hỗ trợ cho mình nha."
],
    "link đăng ký ": ["🔍 Dạ anh liên hệ Admin @CS1_FK8 hoặc CS2: @CS2_FK8 để hỗ trợ  anh nhé ."],
    "hướng dẫn tạo tài khoản  ": ["Anh truy cập vào trang chủ FK8 chọn giúp em 'Đăng ký' để tạo tài khoản,tiếp đến chọn tên tài khoản trên hệ thống cung cấp và nhập mật khẩu theo ý của anh (tối thiểu 6 ký tự số và chữ có chứa ký tự in hoa).Cần hỗ trợ thêm anh cứu inbox @CS1_FK8 hoặc CS2: @CS2_FK8 nhé ."],
    "momo ": ["💸FK8 có hỗ trợ nạp tiền theo phương thức online qua ngân hàng và cả ví điện tử (momo,viettelpay,zalopay) anh có thể vào mục nạp tiền để tham khảo các phương thức giao dịch anh nhé ."],
}
# ➕ Thêm từ khóa bảo toàn vốn
KEYWORD_RESPONSES_RAW.update({
    "bảo toàn": [
        "💸 *Ưu đãi về Bảo toàn vốn*\nKhi anh đặt cược vào trận được bảo toàn và chọn đúng tỷ số bảo toàn, nếu ra đúng kết quả thì anh được *hoàn lại tiền gốc* đã đặt cược.\n👉 Anh hãy tham gia nhóm và theo dõi để chọn đúng trận và nhận được ưu đãi nhé!"
    ],
    "trận bảo hiểm": [
        "✅ Đúng rồi anh! Hiện đang có chương trình *bảo toàn vốn tỷ số 3-3*, nhớ theo dõi nhóm Telegram để không bỏ lỡ!"
    ],
    "hoàn vốn": [
        "📢 Hiện bên em đang có *khuyến mãi bảo toàn vốn tỷ số 3-3* 💥\nTrận sẽ được admin cập nhật trên nhóm Telegram.\n👉 Anh hãy tham gia nhóm và theo dõi để chọn đúng trận và nhận được ưu đãi nhé!"
    ]
})

KEYWORD_RESPONSES = {k.lower(): v for k, v in KEYWORD_RESPONSES_RAW.items()}
# Hàm kiểm tra từ khóa

def check_keywords(text):
    lower_text = text.lower()
    for keyword in KEYWORD_RESPONSES:
        if keyword in lower_text:
            return random.choice(KEYWORD_RESPONSES[keyword])
    return None

# Gửi tin nhắn Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, json={
    "chat_id": chat_id,
    "text": text,
    "parse_mode": "Markdown"
})

    print("Send response:", res.text)
# Lưu trạng thái người dùng khi hỏi "link đăng ký"
REGISTRATION_FLOW = {}

def handle_registration_flow(user_id, message):
    step = REGISTRATION_FLOW.get(user_id, {}).get("step")
    message = message.lower().strip()

    if "link đăng ký" in message:
        REGISTRATION_FLOW[user_id] = {"step": "ask_source"}
        return "Bạn biết đến FK8 qua đâu? (Telegram hoặc Facebook)"
    elif step == "ask_source":
        REGISTRATION_FLOW[user_id]["source"] = message
        REGISTRATION_FLOW[user_id]["step"] = "ask_device"
        return "Bạn đang dùng thiết bị nào? (PC hoặc Mobile)"
    elif step == "ask_device":
        source = REGISTRATION_FLOW[user_id].get("source")
        device = message
        REGISTRATION_FLOW.pop(user_id, None)  # kết thúc luồng
        return get_registration_link(source, device)
    return None

def get_registration_link(source, device):
    source = source.lower()
    device = device.lower()
    if source == "telegram":
        if device == "pc":
            return "🔗 Đây là link đăng ký Telegram (PC):\nhttps://w1.fk8vip87063.shop/register.php?agent=FAX31"
        elif device == "mobile":
            return "📱 Đây là link đăng ký Telegram (Mobile):\nhttps://m1.fk8vip87063.shop/register.php?agent=FAX31"
    elif source == "facebook":
        if device == "pc":
            return "🔗 Đây là link đăng ký Facebook (PC):\nhttps://w1.fk8vip87063.shop/register.php?agent=FCU21"
        elif device == "mobile":
            return "📱 Đây là link đăng ký Facebook (Mobile):\nhttps://m1.fk8vip87063.shop/register.php?agent=FCU21"
    return "❗ Thông tin chưa chính xác, anh vui lòng trả lời lại giúp em nhé!"


# Webhook Flask
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    if "message" in data and "text" in data["message"]:
        user_text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
    else:
        return "ok"

    log_message(data["message"]["from"]["id"], user_text)
    # 👉 Xử lý theo luồng đăng ký nếu có
    registration_reply = handle_registration_flow(chat_id, user_text)
    if registration_reply:
      send_message(chat_id, registration_reply)
      return "ok"


    reply = check_keywords(user_text)
    if not reply:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Bạn là một trợ lý AI thân thiện và chuyên nghiệp của FK8. "
                            "Nhiệm vụ của bạn là hỗ trợ người dùng về khuyến mãi, thể thao, phản tỷ số, "
                            "hướng dẫn tham gia, liên hệ CSKH. Trả lời ngắn gọn (1-2 câu), vui vẻ, có thể dùng emoji. "
                            "Không được nói 'tôi không biết', 'không có trong dữ liệu' hoặc tương tự. "
                            "Nếu câu hỏi vượt ngoài phạm vi hỗ trợ, hãy đề nghị liên hệ CSKH hoặc admin."
                        )
                    },
                    {"role": "user", "content": user_text}
                ]
            )
            reply = response["choices"][0]["message"]["content"]
        except Exception as e:
            print("Webhook error:", e)
            reply = "Dạ hiện tại hệ thống đang bận, anh thử lại sau chút nhé! 🛠️"

    send_message(chat_id, reply)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


       

