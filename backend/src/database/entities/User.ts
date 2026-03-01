import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, OneToMany } from 'typeorm';
import { TournamentPlayer } from './TournamentPlayer';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true, length: 32 })
  username: string;

  @Column({ unique: true, nullable: true, length: 255 })
  email: string;

  @Column({ length: 255 })
  password_hash: string;

  // CRIT-6 FIX: Add role-based access control
  @Column({ default: 'player', length: 20 })
  role: string; // 'player' | 'admin' | 'moderator'

  // Phase 3.8: Stateful refresh token (sha256 hash stored, not raw token)
  @Column({ nullable: true, length: 64 })
  refresh_token_hash: string | null;

  @Column({ nullable: true })
  refresh_token_expires_at: Date | null;

  @OneToMany(() => TournamentPlayer, tournamentPlayer => tournamentPlayer.user)
  tournamentPlayers: TournamentPlayer[];

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;
}
