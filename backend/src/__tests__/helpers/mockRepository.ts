/**
 * TypeORM Repository Mock Helper
 * Provides type-safe mocks for TypeORM repositories
 */

export const createMockRepository = () => {
  return {
    find: jest.fn(),
    findOne: jest.fn(),
    findOneBy: jest.fn(),
    save: jest.fn(),
    create: jest.fn(),
    delete: jest.fn(),
    update: jest.fn(),
    count: jest.fn(),
    createQueryBuilder: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      addSelect: jest.fn().mockReturnThis(),
      leftJoin: jest.fn().mockReturnThis(),
      leftJoinAndSelect: jest.fn().mockReturnThis(),
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      orWhere: jest.fn().mockReturnThis(),
      orderBy: jest.fn().mockReturnThis(),
      groupBy: jest.fn().mockReturnThis(),
      skip: jest.fn().mockReturnThis(),
      take: jest.fn().mockReturnThis(),
      limit: jest.fn().mockReturnThis(),
      offset: jest.fn().mockReturnThis(),
      getOne: jest.fn(),
      getMany: jest.fn(),
      getManyAndCount: jest.fn(),
      getRawAndEntities: jest.fn(),
      getRawOne: jest.fn(),
      getRawMany: jest.fn(),
      execute: jest.fn(),
    })),
  };
};

export const mockAppDataSource = {
  getRepository: jest.fn(),
  initialize: jest.fn().mockResolvedValue(true),
  destroy: jest.fn().mockResolvedValue(true),
  isInitialized: true,
};
