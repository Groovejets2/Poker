import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn, CreateDateColumn, Unique } from 'typeorm';
import { Tournament } from './Tournament';
import { User } from './User';

@Entity('matches')
@Unique(['tournament', 'table_number', 'game_number'])
export class Match {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(() => Tournament)
  @JoinColumn({ name: 'tournament_id' })
  tournament: Tournament;

  @Column()
  table_number: number;

  @Column()
  game_number: number;

  @Column({ default: 'scheduled' })
  status: string; // 'scheduled' | 'in_progress' | 'completed' | 'cancelled'

  @ManyToOne(() => User, { nullable: true })
  @JoinColumn({ name: 'winner_id' })
  winner: User;

  @Column({ nullable: true })
  pot_total: number;

  @Column({ nullable: true })
  scheduled_at: Date;

  @Column({ nullable: true })
  started_at: Date;

  @Column({ nullable: true })
  completed_at: Date;

  @Column({ default: 0 })
  hand_count: number;

  @CreateDateColumn()
  created_at: Date;
}
