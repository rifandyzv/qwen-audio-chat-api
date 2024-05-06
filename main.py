from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from typing import Annotated
from function import isVideoFile, videoToAudioConverter, isAudioFile
from llm.qwen import callQwen, callMeetingSummary

import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)    

    
@app.post("/analyzeVideo")
async def upload_file(file: UploadFile):
    print(file.filename)
    print(isVideoFile(file.filename))
    if not isVideoFile(file.filename):
        raise HTTPException(status_code=400, detail="Not a valid video file")

    video_path = f"./tmp/input.mp4"
    audio_path = f"./tmp/output.mp3"

    with open(video_path, "wb") as f:
        f.write(file.file.read())

    videoToAudioConverter(video_path)

    res = callQwen(audio=audio_path)
    

    return {'answer': res}
    # return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")

@app.post("/analyzeAudio")
async def upload_file(file: UploadFile):
    print(file.filename)
    print(isAudioFile(file.filename))
    if not isAudioFile(file.filename):
        raise HTTPException(status_code=400, detail="Not a valid video file")

    input_path = f"./tmp/input.mp3"


    with open(input_path, "wb") as f:
        f.write(file.file.read())



    res = callQwen(audio=input_path)
    

    return {'answer': res}
    # return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")


@app.post("/analyzeMeeting")
async def meetingRecording(file: UploadFile):
    print(file.filename)


    if isVideoFile(file.filename):
        video_path = f"./tmp/input.mp4"

        with open(video_path, "wb") as f:
            f.write(file.file.read())

        videoToAudioConverter(video_path)

    # input_path = f"./tmp/output.mp3"


    res = callMeetingSummary(audio="./tmp/output.mp3")
    

    return {'answer': res}
    # return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")