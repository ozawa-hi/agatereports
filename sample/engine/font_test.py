from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import webbrowser

# 源真ゴシック（ http://jikasei.me/font/genshin/）
GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"

# 白紙をつくる（A4縦）
FILENAME = 'HelloWorld.pdf'
c = canvas.Canvas(FILENAME, pagesize=portrait(A4))

# フォント登録
pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
font_size = 20
c.setFont('GenShinGothic', font_size)

# 真ん中に文字列描画
width, height = A4  # A4用紙のサイズ
c.drawCentredString(width / 2, height / 2 - font_size * 0.4, 'こんにちは、世界！')

# Canvasに書き込み
c.showPage()
# ファイル保存
c.save()