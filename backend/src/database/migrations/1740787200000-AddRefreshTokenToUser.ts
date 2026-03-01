import { MigrationInterface, QueryRunner, TableColumn } from 'typeorm';

/**
 * Phase 3.8: Add refresh token columns to users table for stateful session management.
 *
 * refresh_token_hash: sha256 of the refresh JWT (64-char hex). Null when no active session.
 * refresh_token_expires_at: expiry timestamp for the refresh token.
 */
export class AddRefreshTokenToUser1740787200000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    const table = await queryRunner.getTable('users');

    if (!table?.findColumnByName('refresh_token_hash')) {
      await queryRunner.addColumn(
        'users',
        new TableColumn({
          name: 'refresh_token_hash',
          type: 'varchar',
          length: '64',
          isNullable: true,
        })
      );
      console.log('Migration: Added refresh_token_hash column');
    }

    if (!table?.findColumnByName('refresh_token_expires_at')) {
      await queryRunner.addColumn(
        'users',
        new TableColumn({
          name: 'refresh_token_expires_at',
          type: 'datetime',
          isNullable: true,
        })
      );
      console.log('Migration: Added refresh_token_expires_at column');
    }
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    const table = await queryRunner.getTable('users');

    if (table?.findColumnByName('refresh_token_expires_at')) {
      await queryRunner.dropColumn('users', 'refresh_token_expires_at');
    }
    if (table?.findColumnByName('refresh_token_hash')) {
      await queryRunner.dropColumn('users', 'refresh_token_hash');
    }
  }
}
