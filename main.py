# 利用するパッケージのインポート
import discord
from discord import app_commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# インテントの生成
intents = discord.Intents.default()
intents.message_content = True

# 利用するAPIの指定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# ***.json　は各自ダウンロードしたjsonファイル名に変更
credentials = ServiceAccountCredentials.from_json_keyfile_name('***.json', scope)
gc = gspread.authorize(credentials)

# スプレッドシートのキーを入力
SPREAD_SHEET_KEY = "***"
workbook = gc.open_by_key(SPREAD_SHEET_KEY)

# スラッシュコマンドを使えるbotを定義
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

# コマンドを特定のチャンネルでのみ使いたい場合指定
# use_channel = ***

############## コマンド実装 ##############
# ＜botのフロー＞ /command 送信 → botからメッセージ → 入力したい項目を入力（このコードでは一回）→ botから完了メッセージ

@tree.command(name="***", description="***") # コマンドの名前と説明を追加
async def command(ctx:discord.Interaction):
  channel = ctx.channel

# チャンネル指定した場合のエラー文
# if channel.id != use_channel :
#  await ctx.response.send_message("ここではコマンドは使えません。「〇〇」チャンネルでのみ記録できます🙇‍♂️") 

  await ctx.response.send_message("〇〇を入力してください") # コマンド入力に対してbotからの反応メッセージ

  def check(m):
    return m.channel == channel

  # 入力内容が入力されるまで待機
  msg = await client.wait_for("message", check=check)

  # 使用するスプシのリスト用意
  worksheet_list = workbook.worksheets()

  # 入力時刻を計算（なぜか9時間の時差が生じるため、プログラム上の時刻から9時間進める）
  dt = datetime.datetime.now() + datetime.timedelta(hours=9)
  date = str(dt.month) + "/" + str(dt.day)
  time = str(dt.strftime('%H:%M'))

  # データが入っていない行を探す(ここの場合スプレッドシートの1枚目、B列でデータがある最後の行を特定　列はA-1、B-2...→で対応)
  data_row = len(worksheet_list[0].col_values(2))

  # 日付、時刻、入力者（サーバーネーム）、入力内容を記録、お礼のメッセージ送信
  worksheet_list[0].update_cell(data_row + 1, 2, date)
  worksheet_list[0].update_cell(data_row + 1, 3, time)
  worksheet_list[0].update_cell(data_row + 1, 4, msg.author.display_name)
  worksheet_list[0].update_cell(data_row + 1, 5, msg.content)
  await channel.send('記録できました！') # 記録完了


# discordのbotトークンを入力
TOKEN = "***"
client.run(TOKEN)