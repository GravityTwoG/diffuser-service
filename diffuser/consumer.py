from confluent_kafka import Consumer, Producer, KafkaException
import generate_image
import json


config = {
  'bootstrap.servers': 'localhost:9092',
  'group.id': 'diffuser',                  
  'auto.offset.reset': 'earliest'         
}

consumer = Consumer(config)
producer = Producer(config)

def handle_message(msg):
  # действия с полученным сообщением
  print(f"Received message: {msg.value().decode('utf-8')}")
  generate_request = json.loads(msg.value().decode('utf-8'))
  generate_image(
    generate_request['prompt'],
    generate_request['generation_id'],
    generate_request['num_images']
  )
  producer.produce(
    'image_generated',
    {
      "status": "done",
      'generation_id': generate_request['generation_id'],
      'image_count': generate_request['num_images']
    }
  )
  producer.flush()

consumer.subscribe(['generate_image'])

try:
  
  while True:
    msg = consumer.poll(timeout=1.0)  

    if msg is None:                   
      continue
    if msg.error():                   
      raise KafkaException(msg.error())
    else:
      handle_message(msg)

except KeyboardInterrupt:
  pass
finally:
  consumer.close()

'''
Generate image message:
{
  "prompt": string,
  "generation_id": uuid,
  "num_images": int
}
'''