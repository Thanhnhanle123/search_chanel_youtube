from flask import Flask, jsonify, render_template, request
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_videos", methods=["POST"])
def get_videos():
    channel_url = request.form.get("channel_url", "").strip()
    if not channel_url:
        return jsonify({"error": "Vui lòng nhập URL kênh YouTube."}), 400

    ydl_opts = {
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)

        videos_data = []
        if 'entries' in result:
            videos = result['entries']
            # Đảo ngược để video mới nhất số 1
            for index, video in enumerate(reversed(videos), start=1):
                if video:
                    title = video.get('title')
                    video_id = video.get('id')
                    link = f"https://www.youtube.com/watch?v={video_id}"

                    videos_data.append({
                        "lecture_number": index,
                        "title": title,
                        "link": link
                    })
        else:
            return jsonify([])  # Trả về mảng rỗng nếu ko có video

        return jsonify(videos_data)

    except Exception as e:
        return jsonify({"error": f"Lỗi khi lấy dữ liệu: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=False)
