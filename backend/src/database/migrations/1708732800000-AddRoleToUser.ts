import { MigrationInterface, QueryRunner, TableColumn } from 'typeorm';

/**
 * CRIT-6: Add role column to users table for RBAC
 *
 * This migration adds a 'role' column to support role-based access control.
 * Default value is 'player' for all existing and new users.
 */
export class AddRoleToUser1708732800000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    // Check if role column already exists
    const table = await queryRunner.getTable('users');
    const roleColumn = table?.findColumnByName('role');

    if (!roleColumn) {
      // Add role column to users table
      await queryRunner.addColumn(
        'users',
        new TableColumn({
          name: 'role',
          type: 'varchar',
          length: '20',
          default: "'player'",
          isNullable: false,
        })
      );

      console.log('✓ Migration: Added role column to users table');
    } else {
      console.log('✓ Migration: Role column already exists, skipping');
    }
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Remove role column on rollback
    const table = await queryRunner.getTable('users');
    const roleColumn = table?.findColumnByName('role');

    if (roleColumn) {
      await queryRunner.dropColumn('users', 'role');
      console.log('✓ Migration rollback: Removed role column from users table');
    }
  }
}
