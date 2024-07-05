import { ApiProperty } from '@nestjs/swagger';
import { GenerationStatus } from '@prisma/client';
import { IsArray, IsEnum, IsString } from 'class-validator';

export class GeneratedImagesDTO {
  @ApiProperty()
  @IsString()
  id: string;

  @ApiProperty()
  @IsEnum(GenerationStatus)
  status: GenerationStatus;

  @ApiProperty()
  @IsString()
  prompt: string;

  @ApiProperty()
  @IsArray()
  @IsString({ each: true })
  images: string[];
}
