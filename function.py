import subprocess

def videoToAudioConverter(video_file, output_ext="mp3"):
    # Customize FFmpeg options here
    command = f"ffmpeg -i {video_file} -q:a 0 -map a ./tmp/output.{output_ext} -y"
    # command = f"ffmpeg -i '{video_file}' -ac 1 -f {output_ext} -vn 'output.{output_ext}'"
    subprocess.call(command, shell=True)

# Example usage:
# video_file = "/path/to/your/video.mp4"
# convert_video_to_audio_ffmpeg(video_file)


def isVideoFile(filename):
    video_file_extensions = (
        '264', '3g2', '3gp', '3gp2', '3gpp', '3gpp2', 'mp4', 'mkv', 'flv' 
    )
    file_extension = filename.lower().split('.')[-1]
    return file_extension in video_file_extensions


def isAudioFile(filename):
    video_file_extensions = (
        'mp3', 'fflac', 'wav'
    )
    file_extension = filename.lower().split('.')[-1]
    return file_extension in video_file_extensions

# videoToAudioConverter(video_file='./tmp/test.mp4')