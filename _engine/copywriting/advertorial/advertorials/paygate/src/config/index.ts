import dotenv from 'dotenv';
dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  apiVersion: process.env.API_VERSION || 'v1',

  database: {
    url: process.env.DATABASE_URL!,
  },

  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379',
  },

  encryption: {
    key: process.env.ENCRYPTION_KEY || 'dev-key-change-in-production-32chars!',
  },

  jwt: {
    secret: process.env.JWT_SECRET || 'dev-jwt-secret',
    expiresIn: '24h',
  },

  processors: {
    nmi: {
      apiKey: process.env.NMI_API_KEY || '',
      securityKey: process.env.NMI_SECURITY_KEY || '',
    },
    tsys: {
      merchantId: process.env.TSYS_MERCHANT_ID || '',
      deviceId: process.env.TSYS_DEVICE_ID || '',
      apiKey: process.env.TSYS_API_KEY || '',
      apiSecret: process.env.TSYS_API_SECRET || '',
    },
    fiserv: {
      apiKey: process.env.FISERV_API_KEY || '',
      apiSecret: process.env.FISERV_API_SECRET || '',
      merchantId: process.env.FISERV_MERCHANT_ID || '',
    },
  },

  ach: {
    odfiRouting: process.env.ACH_ODFI_ROUTING || '',
    odfiName: process.env.ACH_ODFI_NAME || '',
    companyId: process.env.ACH_COMPANY_ID || '',
    companyName: process.env.ACH_COMPANY_NAME || '',
    sftpHost: process.env.ACH_SFTP_HOST || '',
    sftpUser: process.env.ACH_SFTP_USER || '',
    sftpKeyPath: process.env.ACH_SFTP_KEY_PATH || '',
  },

  webhook: {
    signingSecret: process.env.WEBHOOK_SIGNING_SECRET || 'whsec_dev',
    maxRetries: 5,
    retryDelays: [60, 300, 1800, 7200, 86400], // 1m, 5m, 30m, 2h, 24h
  },

  logging: {
    level: process.env.LOG_LEVEL || 'info',
  },
} as const;
