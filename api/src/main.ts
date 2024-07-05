import { NestFactory } from '@nestjs/core';
import { Logger, ValidationPipe } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

import { AppModule } from './app.module';
import { AppConfigService } from './config/configuration.schema';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
      whitelist: true,
    }),
  );

  const config = new DocumentBuilder()
    .setTitle('Image generation API')
    .setDescription('API for image generation')
    .setVersion('0.1')
    .addTag('images')
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('/swagger', app, document);

  const logger = app.get(Logger);
  app.useLogger(logger);
  const configService = app.get<AppConfigService>(ConfigService);

  const PORT = configService.get('PORT');

  await app.listen(PORT);
  logger.log(`App listening on port: ${PORT}`, 'NestApplication');
  logger.log(`URL: http://localhost:${PORT}`, 'NestApplication');
}

bootstrap();
