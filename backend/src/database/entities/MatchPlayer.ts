import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn, Unique } from 'typeorm';
import { Match } from './Match';
import { User } from './User';

@Entity('match_players')
@Unique(['match', 'user'])
export class MatchPlayer {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(() => Match)
  @JoinColumn({ name: 'match_id' })
  match: Match;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column()
  position: number;

  @Column()
  starting_stack: number;

  @Column({ nullable: true })
  ending_stack: number;

  @Column({ default: 'active' })
  status: string; // 'active' | 'folded' | 'eliminated' | 'won'
}
