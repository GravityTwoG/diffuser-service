import { NestFactory } from '@nestjs/core';
import { Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import { AppModule } from './app.module';
import { AppConfigService } from './config/configuration.schema';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const logger = app.get(Logger);
  app.useLogger(logger);

  const configService = app.get<AppConfigService>(ConfigService);
  const PORT = configService.get('PORT');

  await app.listen(PORT);
  logger.log(`App listening on port: ${PORT}`, 'NestApplication');
  logger.log(`URL: http://localhost:${PORT}`, 'NestApplication');
}

bootstrap();
