import sys
import os
import json

import pika
from dotenv import load_dotenv

from generate_image import generate_image
from s3_service import S3Service


load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')

RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

GENERATION_REQUEST_QUEUE = os.getenv('GENERATION_REQUEST_QUEUE')
IMAGE_GENERATED_QUEUE = os.getenv('IMAGE_GENERATED_QUEUE')

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')



class DiffuserService:
  def __init__(self):
    self.s3service = S3Service(
      endpoint=os.getenv('S3_ENDPOINT'),
      bucket_name=S3_BUCKET_NAME,
      access_key=os.getenv('S3_ACCESS_KEY'),
      secret_key=os.getenv('S3_SECRET_KEY')
    )


  def handle_generation_request(
    self,
    ch: pika.adapters.blocking_connection.BlockingChannel, 
    method: pika.spec.Basic.Deliver, 
    properties: pika.spec.BasicProperties, 
    body: str,
  ):
    try:
      print(f" [x] Received {body}")
      generation_request = json.loads(body)

      generation_id = generation_request['generationId']

      images = generate_image(
        generation_request['prompt'],
        generation_request['imagesCount']
      )
      print(f" [x] Images generated: {generation_id}")

      images_with_names = []
      for i, image in enumerate(images):
        image_name = f"{generation_id}.[{i}].png"
        images_with_names.append({
          "image_name": image_name,
          "image": image
        })

      self.s3service.save_images(images_with_names)

      images_info = []
      for image in images_with_names:
        images_info.append({
          "imageName": image['image_name'],
          "imagePath": S3_BUCKET_NAME,
        })

      self.send_generation_response(
        ch, 
        "GENERATED",
        generation_id,
        images_info
      )
      ch.basic_ack(delivery_tag = method.delivery_tag)
      print(" [x] Sent 'image_generated'")

    except Exception as e:
      print(f"Error: {str(e)}")
      self.send_generation_response(
        ch, 
        "FAILED",
        generation_id,
        [],
      )
      ch.basic_ack(delivery_tag = method.delivery_tag)


  def send_generation_response(
    self,
    ch: pika.adapters.blocking_connection.BlockingChannel,
    status: str,
    generation_id: str, 
    images_info: list
  ):
    # send a message to queue "image_generated"
    image_generated = {
      'generationId': generation_id,
      "status": status,
      "imagesInfo": images_info
    }
    ch.basic_publish(
      exchange='',
      routing_key=IMAGE_GENERATED_QUEUE,
      body=json.dumps(image_generated),
    )

def main():
  diffuser = DiffuserService()

  credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
  connection = pika.BlockingConnection(pika.ConnectionParameters(
    RABBITMQ_HOST, RABBITMQ_PORT, 
    credentials=credentials,
  ))
  channel = connection.channel()
  print("Connected to RabbitMQ")
  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one
  channel.basic_qos(prefetch_count=1)

  # create a queue (idempotent operation)
  channel.queue_declare(queue=GENERATION_REQUEST_QUEUE, durable=True)
  channel.queue_declare(queue=IMAGE_GENERATED_QUEUE, durable=True)

  # receive messages
  channel.basic_consume(
    queue=GENERATION_REQUEST_QUEUE,
    auto_ack=False,
    on_message_callback=diffuser.handle_generation_request,
  )

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()

  # flush all buffers and close connection
  connection.close()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

