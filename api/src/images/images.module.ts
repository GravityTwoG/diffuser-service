import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { RabbitMQModule } from '@golevelup/nestjs-rabbitmq';

import { ImagesController } from './images.controller';
import { ImagesService } from './images.service';

@Module({
  imports: [
    RabbitMQModule.forRootAsync(RabbitMQModule, {
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        exchanges: [],
        uri: configService.get('RABBITMQ_URI'),
        channels: {
          [configService.get('GENERATION_REQUEST_QUEUE')]: {
            prefetchCount: 1,
            default: true,
          },
          [configService.get('IMAGE_GENERATED_QUEUE')]: {
            prefetchCount: 1,
          },
        },
      }),
    }),
  ],
  controllers: [ImagesController],
  providers: [ImagesService],
})
export class ImagesModule {}
