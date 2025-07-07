from flask import Flask, jsonify, request, render_template
# 假設您的 search 函式位於 utils/indexer.py
from utils.indexer import search

# 在初始化 Flask 時，透過 template_folder 指定模板檔案的路徑
# 這樣 Flask 就會去 'web' 資料夾中找 index.html
app = Flask(__name__, template_folder='web')


@app.route('/')
def index():
    """
    渲染主頁面。
    Flask 會在指定的 template_folder ('web') 中尋找 'index.html'。
    """
    return render_template('index.html')


@app.route('/search')
def search_api():
    """
    處理搜尋請求的 API。
    這個 API 現在只處理 'query' 參數，不再進行標籤篩選。
    它會回傳給定 query 的所有結果，以及這些結果中包含的所有可用標籤。
    前端將根據這些完整的資料進行即時篩選。
    """
    # 1. 只獲取 query 參數
    query = request.args.get('query', '')

    # 如果 query 為空，可以選擇直接回傳空結果以節省資源
    if not query:
        return jsonify({'results': [], 'available_tags': []})

    # 2. 執行核心的搜尋邏輯
    search_results = search(query)

    # 3. 從【所有】搜尋結果中提取可用標籤
    available_tags = set()
    for movie in search_results:
        # 使用 .get() 避免因缺少 'tags' 鍵而引發錯誤
        for tag in movie.get('tags', []):
            available_tags.add(tag)

    # 4. 直接回傳完整的搜尋結果和所有可用標籤
    #    不再有伺服器端的篩選邏輯
    return jsonify({
        'results': search_results,
        'available_tags': sorted(list(available_tags))
    })


if __name__ == '__main__':
    # 在開發環境中執行，請勿在生產環境中使用 debug=True
    app.run(debug=True, port=5001)