import whisper

model=whisper.load_model("base")
result = model.transcribe("D:\\Gebruikers\\robin\\robin\\GitHub\\DaySphere\\satis_planner\\lib\\Recording.mp3")
print(result["text"])