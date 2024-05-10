from cog import BasePredictor, Input, Path
from pytube import YouTube
import ffmpeg

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        url: str = Input(description="Your youtube url"),
        resolution: str = Input(description="Resolution of the video", default="720p"),
        start: str = Input(description="Start time in hh:mm:ss"),
        end: str = Input(description="End time in hh:mm:ss"),
    ) -> Path:
        # Download the video
        yt = YouTube(url)
        video_path = f"{yt.title}.mp4"
        print(f"Downloading {yt.title}...")
        yt.streams.filter(res=resolution, file_extension='mp4').first().download(filename=video_path)

        # Use ffmpeg to cut the video
        print(f"Cutting {yt.title}...")
        ffmpeg.input(video_path, ss=start, to=end).output(f"{yt.title}-cut.mp4").run()
        # Delete the original video
        Path(video_path).unlink()

        # Return the path to the cut video
        return Path(f"{yt.title}-cut.mp4")