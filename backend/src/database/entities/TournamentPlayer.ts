import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn, CreateDateColumn, Unique } from 'typeorm';
import { Tournament } from './Tournament';
import { User } from './User';

@Entity('tournament_players')
@Unique(['tournament', 'user'])
export class TournamentPlayer {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(() => Tournament)
  @JoinColumn({ name: 'tournament_id' })
  tournament: Tournament;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ default: 'registered' })
  status: string; // 'registered' | 'active' | 'eliminated' | 'withdrew'

  @Column({ default: 10000 })
  starting_stack: number;

  @Column({ nullable: true })
  current_stack: number;

  @Column({ nullable: true })
  finish_position: number;

  @Column({ type: 'decimal', precision: 10, scale: 2, nullable: true })
  prize_usd: number;

  @CreateDateColumn()
  joined_at: Date;
}
