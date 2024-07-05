import { ApiProperty } from '@nestjs/swagger';
import { IsInt, IsString } from 'class-validator';

export class GenerationRequestDTO {
  @ApiProperty()
  @IsString()
  prompt: string;

  @ApiProperty()
  @IsInt()
  imagesCount: number;
}
