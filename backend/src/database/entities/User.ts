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

  @OneToMany(() => TournamentPlayer, tournamentPlayer => tournamentPlayer.user)
  tournamentPlayers: TournamentPlayer[];

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;
}
