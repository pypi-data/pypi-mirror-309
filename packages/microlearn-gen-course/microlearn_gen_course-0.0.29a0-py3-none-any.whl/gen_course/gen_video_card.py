import json
import logging
import os
import time
import uuid

import requests

from .utils import remove_markdown


class GenVideoCard:
    logger = logging.getLogger(__name__)

    SPEECH_ENDPOINT = os.getenv('SPEECH_ENDPOINT', "https://westeurope.api.cognitive.microsoft.com")
    API_VERSION = "2024-04-15-preview"


    def _create_job_id(self):
        return uuid.uuid4().__str__()


    def _authenticate(self):
        SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
        return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}


    def submit_synthesis(
            self,
            job_id: str,
            content: str,
            avatar: str,
            avatar_style: str,
            voice: str,
            video_format: str,
            video_codec: str,
            background_color: str,
            background_image: str,
    ):
        url = f'{self.SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={self.API_VERSION}'
        header = {
            'Content-Type': 'application/json'
        }
        header.update(self._authenticate())

        avatar_config = {
            "customized": False,
            "talkingAvatarCharacter": avatar,
            "talkingAvatarStyle": avatar_style,
            "videoFormat": video_format,
            "videoCodec": video_codec,
            "subtitleType": "soft_embedded"
        }

        if background_image:
            avatar_config.update({"backgroundImage": background_image})
        else:
            avatar_config.update({"backgroundColor": background_color})

        payload = {
            'synthesisConfig': {
                "voice": voice,
            },
            'customVoices': {},
            "inputKind": "plainText",
            "inputs": [
                {
                    "content": content,
                },
            ],
            "avatarConfig": avatar_config
        }

        response = requests.put(url, json.dumps(payload), headers=header)
        if response.status_code < 400:
            self.logger.info('Batch avatar synthesis job submitted successfully')
            self.logger.info(f'Job ID: {response.json()["id"]}')
            return True
        else:
            self.logger.error(f'Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')


    def get_synthesis(self, job_id):
        url = f'{self.SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={self.API_VERSION}'
        header = self._authenticate()

        response = requests.get(url, headers=header)
        if response.status_code < 400:
            self.logger.debug('Get batch synthesis job successfully')
            self.logger.debug(response.json())
            if response.json()['status'] == 'Succeeded':
                self.logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
            return response.json()['status'], response.json()['outputs']['result'] if response.json()['status'] == 'Succeeded' else response.text
        else:
            self.logger.error(f'Failed to get batch synthesis job: {response.text}')


    def list_synthesis_jobs(self, skip: int = 0, max_page_size: int = 100):
        url = f'{self.SPEECH_ENDPOINT}/avatar/batchsyntheses?api-version={self.API_VERSION}&skip={skip}&maxpagesize={max_page_size}'
        header = self._authenticate()

        response = requests.get(url, headers=header)
        if response.status_code < 400:
            self.logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
            self.logger.info(response.json())
        else:
            self.logger.error(f'Failed to list batch synthesis jobs: {response.text}')


    def gen_batch_avatar_synthesis(
            self,
            content: str,
            avatar: str = 'Max',
            avatar_style: str = 'casual',
            voice: str = 'it-IT-GiuseppeMultilingualNeural',
            video_format: str = 'webm',
            video_codec: str = 'vp9',
            background_color: str = '#FFFFFFFF',
            background_image: str = None,
    ) -> str:
        start = time.time()
        job_id = self._create_job_id()
        if self.submit_synthesis(
                job_id,
                remove_markdown(content),
                avatar,
                avatar_style,
                voice,
                video_format,
                video_codec,
                background_color,
                background_image,
        ):
            while True:
                status, api_response = self.get_synthesis(job_id)
                if status == 'Succeeded':
                    self.logger.info('batch avatar synthesis job succeeded')
                    end = time.time()
                    self.logger.info(f'Time elapsed: {end - start} seconds')
                    return api_response
                elif status == 'Failed':
                    self.logger.error('batch avatar synthesis job failed')
                    raise Exception(f'Batch avatar synthesis job failed: {api_response}')
                else:
                    self.logger.info(f'batch avatar synthesis job is still running, status [{status}]')
                    time.sleep(5)


# class GenVideoCardV2:
#
#     api_key = ''
#
#     def generate_heygen_video(
#             self,
#             input_text,
#             avatar_id="Daisy-inskirt-20220818",
#             avatar_style="normal",
#             voice_id="65d3435332e948c7a2add29bf4d62d02",
#             background_color="#008000",
#             width=1280,
#             height=720,
#             aspect_ratio="16:9",
#             test=True
#     ):
#         url = 'https://api.heygen.com/v2/video/generate'
#         headers = {
#             'X-Api-Key': self.api_key,
#             'Content-Type': 'application/json'
#         }
#         data = {
#             "video_inputs": [
#                 {
#                     "character": {
#                         "type": "avatar",
#                         "avatar_id": avatar_id,
#                         "avatar_style": avatar_style
#                     },
#                     "voice": {
#                         "type": "text",
#                         "input_text": input_text,
#                         "voice_id": voice_id
#                     },
#                     "background": {
#                         "type": "color",
#                         "value": background_color
#                     }
#                 }
#             ],
#             "dimension": {
#                 "width": width,
#                 "height": height
#             },
#             "aspect_ratio": aspect_ratio,
#             "test": test
#         }
#
#         response = requests.post(url, headers=headers, json=data)
#
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return f"Error: {response.status_code}, {response.text}"
#
#
#     def check_video_status(self, video_id, interval=5):
#         url = f'https://api.heygen.com/v1/video_status.get?video_id={video_id}'
#         headers = {
#             'X-Api-Key': self.api_key
#         }
#
#         while True:
#             response = requests.get(url, headers=headers)
#
#             if response.status_code != 200:
#                 print(f"Error: {response.status_code}, {response.text}")
#                 return None
#
#             data = response.json()
#
#             if data['code'] == 100:
#                 status = data['data']['status']
#                 if status == 'completed':
#                     print(f"Video completed! Video URL: {data['data']['video_url']}")
#                     return data['data']
#                 elif status == 'failed':
#                     error_info = data['data']['error']
#                     print(f"Video generation failed with error: {error_info['message']}")
#                     return None
#                 elif status == 'processing':
#                     print("Video is still processing. Checking again in a few seconds...")
#                 elif status == 'pending':
#                     print("Video is pending. Checking again in a few seconds...")
#             else:
#                 print(f"Unexpected response code: {data['code']}, message: {data['message']}")
#                 return None
#
#             time.sleep(interval)
#
#
#     def get_voices(self):
#         url = "https://api.heygen.com/v2/voices"
#
#         headers = {
#             "accept": "application/json",
#             "x-api-key": self.api_key
#         }
#
#         response = requests.get(url, headers=headers)
#
#         print(response.text)
#
#
# if __name__ == '__main__':
#     gen_video_card_v2 = GenVideoCardV2()
#     print("Getting voices...")
#     gen_video_card_v2.get_voices()
#     print("Generating video...")
#     start = time.time()
#     result = gen_video_card_v2.generate_heygen_video("La progettazione del PCB è un passaggio cruciale nella creazione di un macropad. Utilizzando software di progettazione, puoi creare un layout del circuito che ottimizza lo spazio e le connessioni. È importante considerare le dimensioni del PCB, poiché influiscono sulla compatibilità con il case e sulla disposizione dei tasti. Un buon design non solo migliora l'estetica, ma garantisce anche un funzionamento efficiente. Ricorda, un PCB ben progettato è la base per un macropad di successo!")
#     video_id = result['data']['video_id']
#     gen_video_card_v2.check_video_status(video_id)
#     end = time.time()
#     print(f"Time elapsed: {end - start} seconds")