import os
from google.cloud import aiplatform
from google.oauth2.credentials import Credentials
import subprocess


def run_command(command):
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    return result.stdout


authentication_token = run_command("gcloud auth print-access-token").rstrip()


creds = Credentials(authentication_token)


PROJECT = os.getenv("PROJECT")  # :)

aiplatform.init(project=PROJECT, credentials=creds)


job = aiplatform.PipelineJob(
    display_name="Kubeflow Tribe Knowledge Pipeline",
    template_path="pipeline.yaml",
    # pipeline_root=PIPELINE_ROOT,
    credentials=creds,
    # enable_caching=False,
    project=PROJECT,
    parameter_values={
        "video_location": "https://raw.githubusercontent.com/Davidnet/youtube-whisper-pipeline/main/urls-from-Community-notes",
        "whisper_model": "medium.en",
        "index_id": "kubeflow-community-search",
        "window": 6,
        "stride": 3,
        "batch_size": 64,
    },
    location="us-central1",
)

job.run()
