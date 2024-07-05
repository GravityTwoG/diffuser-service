import { ConfigService } from '@nestjs/config';
import { plainToInstance } from 'class-transformer';
import { IsEnum, IsInt, IsString, validateSync } from 'class-validator';

export enum Environment {
  local = 'local',
  production = 'production',
}

export class EnvironmentVariables {
  @IsInt()
  PORT: number;

  @IsEnum(Environment)
  ENVIRONMENT: Environment;

  @IsString()
  RABBITMQ_URI: string;

  @IsString()
  GENERATION_REQUEST_QUEUE: string;

  @IsString()
  IMAGE_GENERATED_QUEUE: string;
}

export function validate(
  config: Record<string, unknown>,
): EnvironmentVariables {
  const validatedConfig = plainToInstance(EnvironmentVariables, config, {
    enableImplicitConversion: true,
  });

  const errors = validateSync(validatedConfig, {
    skipMissingProperties: false,
  });

  if (errors.length > 0) {
    throw new Error(errors.toString());
  }

  return validatedConfig;
}

export type AppConfigService = ConfigService<EnvironmentVariables, true>;
