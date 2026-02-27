import whisper


print('psst')

input_file = 'audio_0.mp4'

model = whisper.load_model("tiny")

print('model loaded i think')

result = model.transcribe(input_file)

print(result["text"])
