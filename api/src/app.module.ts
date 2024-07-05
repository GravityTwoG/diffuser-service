import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

import { validate } from './config/configuration.schema';

import { LoggerModule } from './logger/logger.module';
import { PrismaModule } from './prisma/prisma.module';
import { ImagesModule } from './images/images.module';

@Module({
  imports: [
    LoggerModule,
    ConfigModule.forRoot({
      envFilePath: `.env`,
      cache: true,
      validate: validate,
      isGlobal: true,
    }),
    {
      global: true,
      module: PrismaModule,
    },
    ImagesModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
