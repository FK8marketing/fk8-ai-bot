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
KEYWORD_RESPONSES = {
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
        "💸 Chỉ cần đăng ký là có 555K!"
    ],
    "free bet": ["🎁 Bấm tham gia ngay 555K khi đăng ký! Không cần nạp trước, nhận lợi nhuận lên đến 100K.Cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8"],
    "trải nghiệm": ["🎉Đăng ký tài khoản FK8, liên kết ngân hàng & số điện thoại → nhận ngay 555K.Cần hỗ trợ thêm inbox ngay @CS1_FK8 hoặc @CS2_FK8 nha!"],
    "xin code": ["Sau khi tạo tài khoản thành công, truy cập mục khuyến mãi → chọn 'Nhận 555K.Cần hỗ trợ thêm, liên hệ @CS1_FK8 hoặc @CS2_FK8 nha"],
    "tvm":["🎁 Nhận ngay 555K khi đăng ký!"],
    "thành viên mới": ["💰Phần thưởng 555K sẽ được cộng khi bạn hoàn thành 3 bước: Đăng ký – Liên kết – Nhận.Vẫn chưa nhận được @CS1_FK8 hoặc @CS2_FK8 để được hỗ trợ "],
    "nạp đầu slot":[
        "🎰 NẠP LẦN ĐẦU SLOT – TẶNG 100%",
        "🔥 Khuyến mãi hot mỗi ngày, nhắn ngay CS1 hoặc CS2 để biết thêm chi tiết!",
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
        "🎉 Ưu đãi hấp dẫn đang chờ bạn! Inbox CS1 hoặc CS2 nhé!",
        "🔥 Khuyến mãi hot mỗi ngày, nhắn ngay CS1 hoặc CS2 để biết thêm chi tiết",
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
    "liên hệ": "📞 Bạn có thể nhắn CS1: @CS1_FK8 hoặc CS2: @CS2_FK8 nhé!",
    "gôm lúa": "💸 Lụm kèo rồi anh em ơi, kèo thơm phức!",
    "lụm": "💰 Gôm lúa xịn xò, chiến tiếp anh em!",
    "win": "🔥 Win đậm, chốt đơn chất lượng!",
    "thắng": "💰 Lãi về rồi, nghỉ hay vào tiếp đây anh em?",
    "lose": "😢 Không sao đâu anh, thua keo này ta bày keo khác!",
    "Thua": "làm lại trận tiếp không anh,phản tỷ số là đường dài nha !",
    "nạp đầu": "🎯 Khi nạp lần đầu, bạn được tặng tối đa 999K đó nha! Liên hệ CSKH để nhận khuyến mãi.",
    "nạp đầu": "🎯 Ưu đãi cực hấp dẫn cho lần nạp đầu tiên,thưởng tối đa 999K tại phản tỷ số,Nổ hũ: tặng 100% đến 3 triệu,Thể thao: thưởng 50% khi nạp từ 500K.",
}

# Hàm kiểm tra từ khóa

def check_keywords(text):
    lower_text = text.lower()
    for keyword in KEYWORD_RESPONSES:
        if keyword in lower_text:
            return random.choice(KEYWORD_RESPONSES[keyword])
    return None

# Gửi tin nhắn Telegram
from datetime import datetime

def log_message(user_id, user_text):
    with open("log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] User {user_id}: {user_text}\n")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# Webhook Flask
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_text = msg.get("text", "")

    if not user_text:
        return "ok"

    log_message(chat_id, user_text)

    quick_reply = check_keywords(user_text)
    if quick_reply:
        send_message(chat_id, quick_reply)
        return "ok"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI thân thiện của FK8. Trả lời ngắn gọn, vui vẻ, tự nhiên. Ưu tiên giải thích rõ ràng các khái niệm như phản tỷ số, khuyến mãi, kèo bóng đá nếu người dùng hỏi. Nếu không chắc chắn câu hỏi hoặc nội dung không phù hợp, hãy đề nghị người dùng liên hệ CS1 hoặc CS2 để được hỗ trợ thêm."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        send_message(chat_id, reply)
    except Exception as e:
        send_message(chat_id, f"Lỗi AI: {e}")

    return "ok"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

