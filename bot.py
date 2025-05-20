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
    "🎁 nền tảng kết hợp giữa thể thao và dự đoán kết quả một cách logic."
    "FK8 là nền tảng mới nhưng đang rất hot đó 🔥 Bên em chơi kiểu Phản Tỷ Số –  hiểu đơn  giản là đoán sai mà đúng thời điểm là ăn nha 😎 Anh muốn tìm hiểu thêm phần nào để em nói kỹ hơn?"
  ],
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
KEYWORD_RESPONSES = {k.lower(): v for k, v in KEYWORD_RESPONSES_RAW.items()}
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
    print("Send response:", res.text)

# Webhook Flask
@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔥 Flask webhook /webhook is active!")
    data = request.get_json()
    print("== RAW DATA ==")
    print(data)  # 👈 Log full dữ liệu Telegram gửi về

    msg = data.get("message", {})
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    chat_type = chat.get("type", "")
    user_text = msg.get("text", "") or msg.get("caption", "")

    print(f"[Webhook] Chat type: {chat_type}, Chat ID: {chat_id}, Text: '{user_text}'")

    # ❌ Chặn chat riêng tư
    if chat_type == "private":
       print("🔒 Bỏ qua tin nhắn riêng")
       return "ok"

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
                {
       "role": "system",
       "content": (
       "Bạn là một trợ lý AI thân thiện,  vui vẻ, hoà đồng của FK8.Chỉ trả lời câu hỏi về khuyến mãi , phản tỷ số,  kèo ,nạp , rút,  giao dịch và các vấn đề liên quan đến  FK8 "
       "Luôn trả lời ngắn gọn (từ 1-2 câu,dưới 50 từ), rõ ràng, thân thiện, dễ hiểu "
       "Nếu phát hiện nội dung có mâu thuẫn hoặc tranh cãi, hãy phản hồi một cách hòa nhã, trung lập và gợi ý người dùng liên hệ CS1 hoặc CS2 để được hỗ trợ thêm. "
       "Nếu không chắc chắn và cơ sở dữ liệu về nạp tiền,  rút tiền,  đăng ký tài khoản, các lĩnh vực về nhà cái,  thể thao câu hỏi hoặc nội dung không phù hợp đều yêu cầu liên hệ @CS1_FK8 hoặc @CS2_FK8 để được hỗ trợ thêm  "
       
  )
},
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

