import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User } from './User';

@Entity('tournaments')
export class Tournament {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 128 })
  name: string;

  @Column({ nullable: true, type: 'text' })
  description: string;

  @Column({ default: 'draft' })
  status: string; // 'draft' | 'scheduled' | 'in_progress' | 'completed' | 'cancelled'

  @Column()
  buy_in_chips: number;

  @Column({ type: 'decimal', precision: 8, scale: 2, default: 0 })
  entry_fee_usd: number;

  @Column({ default: 8 })
  max_players: number;

  @Column()
  scheduled_at: Date;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'created_by' })
  created_by: User;

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;
}
